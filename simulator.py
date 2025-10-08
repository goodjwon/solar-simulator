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
    weather_map = {"clear": 1.0, "clouds": 0.4, "rain": 0.15, "snow": 0.1, "drizzle": 0.25, "mist": 0.3}
    return weather_map.get(weather_str.lower(), 0.5)

def run_simulator():
    global CACHED_WEATHER, cumulative_energy_kwh, battery_soc_percent
    load_config()
    
    while True:
        load_config()
        
        loc_conf = CONFIG.get('location', {})
        panel_conf = CONFIG.get('solar_panel', {})
        weather_api_conf = CONFIG.get('weather_api', {})
        env_conf = CONFIG.get('environment', {})
        battery_conf = CONFIG.get('battery', {})
        consumption_conf = CONFIG.get('home_consumption', {})
        
        now = datetime.now(pytz.timezone(loc_conf.get('timezone', 'UTC')))
        
        current_weather = env_conf.get('weather', 'Clear')
        if weather_api_conf.get('use_real_weather', False):
            if (CACHED_WEATHER['last_fetch_time'] is None or now > CACHED_WEATHER['last_fetch_time'] + timedelta(minutes=10)):
                new_weather = get_real_weather(weather_api_conf.get('api_key'), loc_conf.get('latitude'), loc_conf.get('longitude'))
                if new_weather: CACHED_WEATHER['condition'] = new_weather; CACHED_WEATHER['last_fetch_time'] = now
            current_weather = CACHED_WEATHER['condition']

        sun_pos = get_position(now, loc_conf.get('longitude', 0), loc_conf.get('latitude', 0))
        altitude_deg = math.degrees(sun_pos['altitude'])
        active_power_w = 0.0
        if altitude_deg > 0:
            weather_multiplier = get_weather_multiplier(current_weather)
            total_max_power = panel_conf.get('max_power_per_panel_watt', 0) * panel_conf.get('panel_count', 0)
            base_power = total_max_power * math.sin(math.radians(altitude_deg))
            active_power_w = max(0, base_power * weather_multiplier + random.uniform(-5, 5))

        interval_seconds = CONFIG.get('simulation_interval_seconds', 1)
        energy_this_interval_kwh = (active_power_w / 1000) * (interval_seconds / 3600)
        cumulative_energy_kwh += energy_this_interval_kwh

        if 7 <= now.hour < 20:
            consumption_w = consumption_conf.get('day_peak_watt', 300) + random.uniform(-50, 50)
        else:
            consumption_w = consumption_conf.get('night_watt', 150) + random.uniform(-20, 20)
        
        net_power_w = active_power_w - consumption_w
        battery_status = "Idle"
        battery_temp_c = env_conf.get('ambient_temp_c', 25) + random.uniform(-0.2, 0.2)
        
        if battery_conf.get('enabled', False):
            capacity_kwh = battery_conf.get('capacity_kwh', 10)
            energy_change_kwh = (net_power_w / 1000) * (interval_seconds / 3600)
            soc_change_percent = (energy_change_kwh / capacity_kwh) * 100
            
            battery_soc_percent += soc_change_percent
            
            if net_power_w > 10 and battery_soc_percent < 100:
                battery_status = "Charging"
            elif net_power_w < -10 and battery_soc_percent > 0:
                battery_status = "Discharging"
            
            if battery_soc_percent >= 100:
                battery_soc_percent = 100; battery_status = "Full"
            elif battery_soc_percent <= 0:
                battery_soc_percent = 0

            heat_factor = 1.5 
            temp_offset = (abs(net_power_w) / 1000) * heat_factor
            battery_temp_c = env_conf.get('ambient_temp_c', 25) + temp_offset + random.uniform(-0.2, 0.2)
        
        voltage = 220 + random.uniform(-5, 5) if active_power_w > 0 else 220
        power_factor = round(random.uniform(0.95, 0.99), 3) if active_power_w > 0 else 1
        apparent_power_va = active_power_w / power_factor
        current = apparent_power_va / voltage if voltage > 0 else 0

        illuminance_lux = max(0, active_power_w * 110 + random.uniform(-100, 100))
        panel_temps_count = CONFIG.get('additional_sensors', {}).get('panel_temperature_sensors', 1)
        panel_temp = 25 + (illuminance_lux / 4000) + random.uniform(-1, 1) if panel_temps_count > 0 else 0

        output_data = {
            "deviceId": CONFIG.get("device_id", "UNKNOWN"), "timestamp": now.isoformat(),
            "power_metrics": { "voltage_v": round(voltage, 2), "current_a": round(current, 2), "active_power_w": round(active_power_w, 2), "apparent_power_va": round(apparent_power_va, 2), "power_factor": round(power_factor, 3) },
            "energy_kwh": round(cumulative_energy_kwh, 4),
            "battery_metrics": { "enabled": battery_conf.get('enabled', False), "status": battery_status, "soc_percent": round(battery_soc_percent, 2), "power_flow_w": round(net_power_w, 2), "capacity_kwh": battery_conf.get('capacity_kwh', 10), "temperature_c": round(battery_temp_c, 2) },
            "environment": { "illuminance_lux": round(illuminance_lux, 2), "panel_temp_c": round(panel_temp, 2), "ambient_temp_c": round(env_conf.get('ambient_temp_c', 25) + random.uniform(-0.5, 0.5), 2), "humidity_percent": round(env_conf.get('humidity_percent', 60) + random.uniform(-1, 1), 2) }
        }

        log_message = (f"생성: Power={output_data['power_metrics']['active_power_w']:.0f}W, 소비: {consumption_w:.0f}W, 배터리: {output_data['battery_metrics']['soc_percent']}% ({output_data['battery_metrics']['status']}, {output_data['battery_metrics']['temperature_c']}°C)")
        logging.info(log_message)
        
        try:
            requests.post(CONFIG.get('api_endpoint'), json=output_data, timeout=5).raise_for_status()
            logging.info(f"✅ API 서버로 데이터 전송 성공")
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ API 전송 실패: {e}")
            
        time.sleep(interval_seconds)

if __name__ == "__main__":
    logging.info("🚀 Solar Monitor Pro 가상 시뮬레이터 (최종본)를 시작합니다.")
    run_simulator()