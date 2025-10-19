import json
import os
import time
import requests
import math
from datetime import datetime, timedelta
import pytz
from suncalc import get_position
import random
import logging

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 전역 변수
CONFIG = {}
CONFIG_FILE_PATH = 'config.json'
LAST_MODIFIED_TIME = 0
CACHED_WEATHER = {"condition": "N/A", "last_fetch_time": None}
battery_soc_percent = 50.0
cumulative_energy_kwh = 0.0
battery_temp_c = 25.0  # 배터리 온도 상태 추가

def load_config():
    global CONFIG, LAST_MODIFIED_TIME, battery_soc_percent
    try:
        mtime = os.path.getmtime(CONFIG_FILE_PATH)
        if mtime != LAST_MODIFIED_TIME:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                CONFIG = json.load(f)
            battery_soc_percent = CONFIG.get('battery', {}).get('initial_soc_percent', 50.0)
            LAST_MODIFIED_TIME = mtime
            logging.info("✅ 설정 파일이 변경되어 새로 로드되었습니다.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"❌ 설정 파일 오류: {e}")
        time.sleep(5)
        load_config()

def get_real_weather(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        weather_condition = data['weather'][0]['main']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        logging.info(f"🌦️ 실시간 날씨 수신: {weather_condition}, 온도: {temp}°C, 습도: {humidity}%")
        CONFIG['environment']['ambient_temp_c'] = temp
        CONFIG['environment']['humidity_percent'] = humidity
        return weather_condition
    except requests.exceptions.RequestException as e:
        logging.warning(f"⚠️ 날씨 API 호출 실패: {e}")
        return None

def get_weather_multiplier(weather_str):
    """날씨별 발전량 감소율 (개선됨)"""
    weather_map = {
        "clear": 1.0,      # 맑음
        "clouds": 0.4,     # 구름
        "rain": 0.15,      # 비
        "snow": 0.1,       # 눈
        "drizzle": 0.25,   # 이슬비
        "mist": 0.3,       # 안개
        "fog": 0.2         # 짙은 안개
    }
    return weather_map.get(weather_str.lower(), 0.5)

def calculate_solar_irradiance(altitude_deg, azimuth_deg, panel_azimuth=0, panel_tilt=30):
    """
    개선된 태양 복사 조도 계산

    Args:
        altitude_deg: 태양 고도각 (도)
        azimuth_deg: 태양 방위각 (도, suncalc 기준: 0=남, 90=서, 180=북, 270=동)
        panel_azimuth: 패널 방위각 (도, suncalc 기준: 기본값 0=남향)
        panel_tilt: 패널 경사각 (도, 기본값 30도)

    Returns:
        상대 조도 (0.0 ~ 1.0)
    """
    if altitude_deg <= 0:
        return 0.0

    # 태양 고도에 따른 기본 조도
    altitude_rad = math.radians(altitude_deg)
    base_irradiance = math.sin(altitude_rad)

    # 방위각 차이 계산
    azimuth_diff = abs(azimuth_deg - panel_azimuth)
    if azimuth_diff > 180:
        azimuth_diff = 360 - azimuth_diff

    # 방위각 효율 (정남향일 때 1.0, 동/서향일 때 감소)
    azimuth_efficiency = math.cos(math.radians(azimuth_diff))

    # 패널 경사각 보정 (단순화된 모델)
    # 태양 고도가 패널 경사각과 유사할 때 최대 효율
    tilt_rad = math.radians(panel_tilt)
    optimal_altitude = 90 - panel_tilt
    altitude_from_optimal = abs(altitude_deg - optimal_altitude)
    tilt_efficiency = 1.0 - (altitude_from_optimal / 180) * 0.3  # 최대 30% 감소

    # 종합 조도
    total_irradiance = base_irradiance * azimuth_efficiency * tilt_efficiency

    return max(0.0, min(1.0, total_irradiance))

def calculate_battery_efficiency(soc_percent, charging=True):
    """
    SoC에 따른 배터리 충/방전 효율

    Args:
        soc_percent: 배터리 충전 상태 (%)
        charging: True=충전, False=방전

    Returns:
        효율 (0.0 ~ 1.0)
    """
    if charging:
        # 충전 효율: SoC 90% 이상에서 감소
        if soc_percent < 90:
            return 0.92  # 92% 효율
        else:
            # 90%~100%에서 선형 감소: 92% -> 75%
            return 0.92 - (soc_percent - 90) / 10 * 0.17
    else:
        # 방전 효율: SoC 20% 이하에서 감소
        if soc_percent > 20:
            return 0.88  # 88% 효율
        else:
            # 0%~20%에서 선형 감소: 88% -> 70%
            return 0.70 + (soc_percent / 20) * 0.18

def update_battery_temperature(current_temp, ambient_temp, power_flow_w, interval_seconds):
    """
    배터리 온도 업데이트 (열용량 고려)

    Args:
        current_temp: 현재 배터리 온도 (°C)
        ambient_temp: 주변 온도 (°C)
        power_flow_w: 충/방전 전력 (W, 양수=충전, 음수=방전)
        interval_seconds: 시간 간격 (초)

    Returns:
        새로운 배터리 온도 (°C)
    """
    # 배터리 열용량 (간단한 모델)
    # 10kWh LiFePO4 배터리: 약 150kg, 비열 약 1000 J/(kg·°C)
    # 열용량 = 150kg * 1000 J/(kg·°C) = 150,000 J/°C
    thermal_mass = 150000  # J/°C

    # 충/방전에 의한 발열 (비효율에 의한 손실 = 열)
    power_loss_w = abs(power_flow_w) * 0.08  # 약 8% 손실이 열로 전환
    heat_generated_j = power_loss_w * interval_seconds
    temp_rise_from_power = heat_generated_j / thermal_mass

    # 주변 온도로의 열 전달 (냉각)
    temp_diff = current_temp - ambient_temp
    cooling_rate = 0.01  # 냉각 계수 (실험적 값, 감소)
    temp_decrease_from_cooling = temp_diff * cooling_rate * (interval_seconds / 60)

    # 새 온도 계산
    new_temp = current_temp + temp_rise_from_power - temp_decrease_from_cooling

    # 노이즈 추가
    new_temp += random.uniform(-0.1, 0.1)

    return new_temp

def run_simulator():
    global CACHED_WEATHER, cumulative_energy_kwh, battery_soc_percent, battery_temp_c
    load_config()

    # 초기 배터리 온도 설정
    battery_temp_c = CONFIG.get('environment', {}).get('ambient_temp_c', 25.0)

    while True:
        load_config()

        loc_conf = CONFIG.get('location', {})
        panel_conf = CONFIG.get('solar_panel', {})
        weather_api_conf = CONFIG.get('weather_api', {})
        env_conf = CONFIG.get('environment', {})
        battery_conf = CONFIG.get('battery', {})
        consumption_conf = CONFIG.get('home_consumption', {})

        now = datetime.now(pytz.timezone(loc_conf.get('timezone', 'UTC')))

        # === 날씨 정보 가져오기 ===
        current_weather = env_conf.get('weather', 'Clear')
        if weather_api_conf.get('use_real_weather', False):
            if (CACHED_WEATHER['last_fetch_time'] is None or
                now > CACHED_WEATHER['last_fetch_time'] + timedelta(minutes=10)):
                new_weather = get_real_weather(
                    weather_api_conf.get('api_key'),
                    loc_conf.get('latitude'),
                    loc_conf.get('longitude')
                )
                if new_weather:
                    CACHED_WEATHER['condition'] = new_weather
                    CACHED_WEATHER['last_fetch_time'] = now
            current_weather = CACHED_WEATHER['condition']

        # === 태양 위치 계산 ===
        sun_pos = get_position(now, loc_conf.get('longitude', 0), loc_conf.get('latitude', 0))
        altitude_deg = math.degrees(sun_pos['altitude'])
        azimuth_deg = math.degrees(sun_pos['azimuth'])

        # === 개선된 발전량 계산 ===
        active_power_w = 0.0
        if altitude_deg > 0:
            weather_multiplier = get_weather_multiplier(current_weather)
            total_max_power = panel_conf.get('max_power_per_panel_watt', 0) * panel_conf.get('panel_count', 0)

            # 방위각과 경사각 고려한 조도 계산
            irradiance = calculate_solar_irradiance(altitude_deg, azimuth_deg)

            base_power = total_max_power * irradiance
            active_power_w = max(0, base_power * weather_multiplier + random.uniform(-5, 5))

        # === 소비 전력 ===
        interval_seconds = CONFIG.get('simulation_interval_seconds', 1)
        if 7 <= now.hour < 20:
            consumption_w = consumption_conf.get('day_peak_watt', 300) + random.uniform(-50, 50)
        else:
            consumption_w = consumption_conf.get('night_watt', 150) + random.uniform(-20, 20)

        net_power_w = active_power_w - consumption_w

        # === 배터리 시뮬레이션 (개선됨) ===
        battery_status = "Idle"
        battery_power_flow_w = 0.0
        actual_energy_change_kwh = 0.0

        if battery_conf.get('enabled', False):
            capacity_kwh = battery_conf.get('capacity_kwh', 10)

            # 충전 시도
            if net_power_w > 10 and battery_soc_percent < 100:
                battery_status = "Charging"
                efficiency = calculate_battery_efficiency(battery_soc_percent, charging=True)
                # 실제 배터리에 저장되는 에너지 (효율 적용)
                actual_energy_change_kwh = (net_power_w * efficiency / 1000) * (interval_seconds / 3600)
                battery_power_flow_w = net_power_w

            # 방전 시도
            elif net_power_w < -10 and battery_soc_percent > 0:
                battery_status = "Discharging"
                efficiency = calculate_battery_efficiency(battery_soc_percent, charging=False)
                # 실제 배터리에서 소모되는 에너지 (효율 적용)
                actual_energy_change_kwh = (net_power_w / efficiency / 1000) * (interval_seconds / 3600)
                battery_power_flow_w = net_power_w

            # SoC 업데이트
            soc_change_percent = (actual_energy_change_kwh / capacity_kwh) * 100
            new_soc = battery_soc_percent + soc_change_percent

            # SoC 범위 제한 (먼저 제한한 후 상태 업데이트)
            if new_soc >= 100:
                battery_soc_percent = 100
                battery_status = "Full"
            elif new_soc <= 0:
                battery_soc_percent = 0
                battery_status = "Empty"
            else:
                battery_soc_percent = new_soc

            # 배터리 온도 업데이트 (열용량 고려)
            battery_temp_c = update_battery_temperature(
                battery_temp_c,
                env_conf.get('ambient_temp_c', 25),
                battery_power_flow_w,
                interval_seconds
            )

        # === 누적 에너지 계산 (실제 사용 가능한 에너지만 누적) ===
        # 발전량에서 배터리 손실 고려
        if battery_conf.get('enabled', False) and actual_energy_change_kwh > 0:
            # 충전 시: 손실된 에너지 제외
            usable_energy_kwh = actual_energy_change_kwh
        else:
            # 배터리 미사용 또는 방전 시: 발전량 그대로
            usable_energy_kwh = (active_power_w / 1000) * (interval_seconds / 3600)

        cumulative_energy_kwh += usable_energy_kwh

        # === 전기적 특성 계산 ===
        voltage = 220 + random.uniform(-5, 5) if active_power_w > 0 else 220
        power_factor = round(random.uniform(0.95, 0.99), 3) if active_power_w > 0 else 1
        apparent_power_va = active_power_w / power_factor if power_factor > 0 else 0
        current = apparent_power_va / voltage if voltage > 0 else 0

        # === 개선된 조도 계산 ===
        # 표준 태양광: 1000 W/m² 조도 ≈ 100,000 lux
        # 패널 1400W (최대) ≈ 패널 면적 약 7-8m² ≈ 조도 7000-8000 W/m²
        # 실제 발전량에 비례하여 조도 계산
        if active_power_w > 0:
            total_max_power = panel_conf.get('max_power_per_panel_watt', 0) * panel_conf.get('panel_count', 0)
            power_ratio = active_power_w / total_max_power if total_max_power > 0 else 0
            # 최대 조도: 맑은 날 정오 100,000 lux
            max_lux = 100000
            illuminance_lux = max(0, max_lux * power_ratio + random.uniform(-1000, 1000))
        else:
            illuminance_lux = 0.0

        # === 개선된 패널 온도 계산 ===
        panel_temps_count = CONFIG.get('additional_sensors', {}).get('panel_temperature_sensors', 1)
        if panel_temps_count > 0 and active_power_w > 0:
            # 일반적인 공식: T_panel = T_ambient + k * Irradiance
            # k ≈ 0.03°C per W/m²
            total_max_power = panel_conf.get('max_power_per_panel_watt', 0) * panel_conf.get('panel_count', 0)
            irradiance_wm2 = (active_power_w / total_max_power) * 1000 if total_max_power > 0 else 0
            temp_rise = 0.03 * irradiance_wm2
            panel_temp = env_conf.get('ambient_temp_c', 25) + temp_rise + random.uniform(-2, 2)
        else:
            panel_temp = env_conf.get('ambient_temp_c', 25) + random.uniform(-1, 1)

        # === 출력 데이터 생성 ===
        output_data = {
            "deviceId": CONFIG.get("device_id", "UNKNOWN"),
            "timestamp": now.isoformat(),
            "power_metrics": {
                "voltage_v": round(voltage, 2),
                "current_a": round(current, 2),
                "active_power_w": round(active_power_w, 2),
                "apparent_power_va": round(apparent_power_va, 2),
                "power_factor": round(power_factor, 3)
            },
            "energy_kwh": round(cumulative_energy_kwh, 4),
            "battery_metrics": {
                "enabled": battery_conf.get('enabled', False),
                "status": battery_status,
                "soc_percent": round(battery_soc_percent, 2),
                "power_flow_w": round(battery_power_flow_w, 2),
                "capacity_kwh": battery_conf.get('capacity_kwh', 10),
                "temperature_c": round(battery_temp_c, 2)
            },
            "environment": {
                "illuminance_lux": round(illuminance_lux, 2),
                "panel_temp_c": round(panel_temp, 2),
                "ambient_temp_c": round(env_conf.get('ambient_temp_c', 25) + random.uniform(-0.5, 0.5), 2),
                "humidity_percent": round(env_conf.get('humidity_percent', 60) + random.uniform(-1, 1), 2)
            },
            # 디버그 정보 추가
            "debug_info": {
                "sun_altitude_deg": round(altitude_deg, 2),
                "sun_azimuth_deg": round(azimuth_deg, 2),
                "weather": current_weather
            }
        }

        log_message = (
            f"생성: {output_data['power_metrics']['active_power_w']:.0f}W, "
            f"소비: {consumption_w:.0f}W, "
            f"배터리: {output_data['battery_metrics']['soc_percent']}% "
            f"({output_data['battery_metrics']['status']}, {output_data['battery_metrics']['temperature_c']}°C), "
            f"태양: Alt={altitude_deg:.1f}° Az={azimuth_deg:.1f}°"
        )
        logging.info(log_message)

        # === API 전송 ===
        try:
            response = requests.post(
                CONFIG.get('api_endpoint'),
                json=output_data,
                timeout=5
            )
            response.raise_for_status()
            logging.info(f"✅ API 서버로 데이터 전송 성공")
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ API 전송 실패: {e}")

        time.sleep(interval_seconds)

if __name__ == "__main__":
    logging.info("🚀 Solar Monitor Pro 가상 시뮬레이터 v2.0 (개선판)을 시작합니다.")
    run_simulator()
