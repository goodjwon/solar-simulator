"""
Simulator 비교 분석 도구

simulator.py (v1)와 simulator_v2.py (v2)의 24시간 시뮬레이션 결과를 비교합니다.
"""

import json
import math
from datetime import datetime, timedelta
import pytz
from suncalc import get_position
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 한글 폰트 설정 (맥OS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


# === V1 알고리즘 (기존) ===
def simulate_v1(config, start_time, hours=24):
    """기존 simulator.py 알고리즘"""
    results = []
    battery_soc = config['battery']['initial_soc_percent']
    cumulative_energy = 0.0

    current_time = start_time
    interval_seconds = config['simulation_interval_seconds']

    for _ in range(int(hours * 3600 / interval_seconds)):
        # 태양 위치
        sun_pos = get_position(
            current_time,
            config['location']['longitude'],
            config['location']['latitude']
        )
        altitude_deg = math.degrees(sun_pos['altitude'])

        # 발전량 (V1: 방위각 미고려)
        active_power_w = 0.0
        if altitude_deg > 0:
            total_max_power = config['solar_panel']['max_power_per_panel_watt'] * \
                              config['solar_panel']['panel_count']
            base_power = total_max_power * math.sin(math.radians(altitude_deg))
            weather_multiplier = 1.0  # 맑음 가정
            active_power_w = max(0, base_power * weather_multiplier)

        # 소비 전력
        if 7 <= current_time.hour < 20:
            consumption_w = config['home_consumption']['day_peak_watt']
        else:
            consumption_w = config['home_consumption']['night_watt']

        net_power_w = active_power_w - consumption_w

        # 배터리 (V1: 효율 미적용)
        if config['battery']['enabled']:
            capacity_kwh = config['battery']['capacity_kwh']
            energy_change_kwh = (net_power_w / 1000) * (interval_seconds / 3600)
            soc_change = (energy_change_kwh / capacity_kwh) * 100

            battery_soc += soc_change

            if battery_soc >= 100:
                battery_soc = 100
            elif battery_soc <= 0:
                battery_soc = 0

        # 누적 에너지 (V1: 발전량만 누적)
        energy_this_interval = (active_power_w / 1000) * (interval_seconds / 3600)
        cumulative_energy += energy_this_interval

        results.append({
            'timestamp': current_time,
            'hour': current_time.hour + current_time.minute / 60,
            'altitude_deg': altitude_deg,
            'active_power_w': active_power_w,
            'consumption_w': consumption_w,
            'net_power_w': net_power_w,
            'battery_soc': battery_soc,
            'cumulative_energy_kwh': cumulative_energy
        })

        current_time += timedelta(seconds=interval_seconds)

    return pd.DataFrame(results)


# === V2 알고리즘 (개선) ===
def calculate_solar_irradiance_v2(altitude_deg, azimuth_deg, panel_azimuth=0, panel_tilt=30):
    """V2: 방위각 고려 (suncalc 기준: 0=남, 90=서, 180=북, 270=동)"""
    if altitude_deg <= 0:
        return 0.0

    altitude_rad = math.radians(altitude_deg)
    base_irradiance = math.sin(altitude_rad)

    azimuth_diff = abs(azimuth_deg - panel_azimuth)
    if azimuth_diff > 180:
        azimuth_diff = 360 - azimuth_diff

    azimuth_efficiency = math.cos(math.radians(azimuth_diff))

    tilt_rad = math.radians(panel_tilt)
    optimal_altitude = 90 - panel_tilt
    altitude_from_optimal = abs(altitude_deg - optimal_altitude)
    tilt_efficiency = 1.0 - (altitude_from_optimal / 180) * 0.3

    total_irradiance = base_irradiance * azimuth_efficiency * tilt_efficiency

    return max(0.0, min(1.0, total_irradiance))


def calculate_battery_efficiency_v2(soc_percent, charging=True):
    """V2: SoC에 따른 효율"""
    if charging:
        if soc_percent < 90:
            return 0.92
        else:
            return 0.92 - (soc_percent - 90) / 10 * 0.17
    else:
        if soc_percent > 20:
            return 0.88
        else:
            return 0.70 + (soc_percent / 20) * 0.18


def simulate_v2(config, start_time, hours=24):
    """개선된 simulator_v2.py 알고리즘"""
    results = []
    battery_soc = config['battery']['initial_soc_percent']
    cumulative_energy = 0.0

    current_time = start_time
    interval_seconds = config['simulation_interval_seconds']

    for _ in range(int(hours * 3600 / interval_seconds)):
        # 태양 위치
        sun_pos = get_position(
            current_time,
            config['location']['longitude'],
            config['location']['latitude']
        )
        altitude_deg = math.degrees(sun_pos['altitude'])
        azimuth_deg = math.degrees(sun_pos['azimuth'])

        # 발전량 (V2: 방위각 고려)
        active_power_w = 0.0
        if altitude_deg > 0:
            total_max_power = config['solar_panel']['max_power_per_panel_watt'] * \
                              config['solar_panel']['panel_count']
            irradiance = calculate_solar_irradiance_v2(altitude_deg, azimuth_deg)
            weather_multiplier = 1.0  # 맑음 가정
            active_power_w = max(0, total_max_power * irradiance * weather_multiplier)

        # 소비 전력
        if 7 <= current_time.hour < 20:
            consumption_w = config['home_consumption']['day_peak_watt']
        else:
            consumption_w = config['home_consumption']['night_watt']

        net_power_w = active_power_w - consumption_w

        # 배터리 (V2: 효율 적용)
        actual_energy_change_kwh = 0.0
        if config['battery']['enabled']:
            capacity_kwh = config['battery']['capacity_kwh']

            if net_power_w > 10 and battery_soc < 100:
                efficiency = calculate_battery_efficiency_v2(battery_soc, charging=True)
                actual_energy_change_kwh = (net_power_w * efficiency / 1000) * (interval_seconds / 3600)
            elif net_power_w < -10 and battery_soc > 0:
                efficiency = calculate_battery_efficiency_v2(battery_soc, charging=False)
                actual_energy_change_kwh = (net_power_w / efficiency / 1000) * (interval_seconds / 3600)

            soc_change = (actual_energy_change_kwh / capacity_kwh) * 100
            new_soc = battery_soc + soc_change

            if new_soc >= 100:
                battery_soc = 100
            elif new_soc <= 0:
                battery_soc = 0
            else:
                battery_soc = new_soc

        # 누적 에너지 (V2: 효율 고려)
        if config['battery']['enabled'] and actual_energy_change_kwh > 0:
            usable_energy_kwh = actual_energy_change_kwh
        else:
            usable_energy_kwh = (active_power_w / 1000) * (interval_seconds / 3600)

        cumulative_energy += usable_energy_kwh

        results.append({
            'timestamp': current_time,
            'hour': current_time.hour + current_time.minute / 60,
            'altitude_deg': altitude_deg,
            'azimuth_deg': azimuth_deg,
            'active_power_w': active_power_w,
            'consumption_w': consumption_w,
            'net_power_w': net_power_w,
            'battery_soc': battery_soc,
            'cumulative_energy_kwh': cumulative_energy
        })

        current_time += timedelta(seconds=interval_seconds)

    return pd.DataFrame(results)


def plot_comparison(df_v1, df_v2):
    """비교 그래프 생성"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. 발전량 비교
    ax1 = axes[0, 0]
    ax1.plot(df_v1['hour'], df_v1['active_power_w'], label='V1 (기존)', linewidth=2, alpha=0.7)
    ax1.plot(df_v2['hour'], df_v2['active_power_w'], label='V2 (개선)', linewidth=2, alpha=0.7)
    ax1.set_xlabel('시간 (시)')
    ax1.set_ylabel('발전량 (W)')
    ax1.set_title('24시간 발전량 비교')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 배터리 SoC 비교
    ax2 = axes[0, 1]
    ax2.plot(df_v1['hour'], df_v1['battery_soc'], label='V1 (기존)', linewidth=2, alpha=0.7)
    ax2.plot(df_v2['hour'], df_v2['battery_soc'], label='V2 (개선)', linewidth=2, alpha=0.7)
    ax2.set_xlabel('시간 (시)')
    ax2.set_ylabel('배터리 SoC (%)')
    ax2.set_title('24시간 배터리 충전 상태 비교')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)

    # 3. 누적 에너지 비교
    ax3 = axes[1, 0]
    ax3.plot(df_v1['hour'], df_v1['cumulative_energy_kwh'], label='V1 (기존)', linewidth=2, alpha=0.7)
    ax3.plot(df_v2['hour'], df_v2['cumulative_energy_kwh'], label='V2 (개선)', linewidth=2, alpha=0.7)
    ax3.set_xlabel('시간 (시)')
    ax3.set_ylabel('누적 에너지 (kWh)')
    ax3.set_title('24시간 누적 에너지 비교')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 발전량 차이
    ax4 = axes[1, 1]
    power_diff = df_v2['active_power_w'] - df_v1['active_power_w']
    ax4.plot(df_v1['hour'], power_diff, label='V2 - V1', linewidth=2, color='green', alpha=0.7)
    ax4.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax4.set_xlabel('시간 (시)')
    ax4.set_ylabel('발전량 차이 (W)')
    ax4.set_title('V2와 V1 발전량 차이 (양수=V2가 더 높음)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('simulator_comparison.png', dpi=150)
    print("📊 비교 그래프 저장: simulator_comparison.png")


def generate_report(df_v1, df_v2, config):
    """비교 리포트 생성"""
    days = len(df_v1) * config['simulation_interval_seconds'] / (24 * 3600)
    print("\n" + "=" * 80)
    print(f"📋 Simulator V1 vs V2 비교 리포트 ({days:.0f}일)")
    print("=" * 80)

    print(f"\n📍 시뮬레이션 설정:")
    print(f"   - 위치: {config['location']['latitude']}°N, {config['location']['longitude']}°E")
    print(f"   - 패널: {config['solar_panel']['panel_count']}개 x {config['solar_panel']['max_power_per_panel_watt']}W")
    print(f"   - 배터리: {config['battery']['capacity_kwh']} kWh")
    print(f"   - 소비: 주간 {config['home_consumption']['day_peak_watt']}W / 야간 {config['home_consumption']['night_watt']}W")

    print("\n" + "-" * 80)
    print("⚡ 발전량 비교")
    print("-" * 80)
    print(f"   V1 총 발전량:      {df_v1['cumulative_energy_kwh'].iloc[-1]:.3f} kWh")
    print(f"   V2 총 발전량:      {df_v2['cumulative_energy_kwh'].iloc[-1]:.3f} kWh")
    diff_energy = df_v2['cumulative_energy_kwh'].iloc[-1] - df_v1['cumulative_energy_kwh'].iloc[-1]
    diff_percent = (diff_energy / df_v1['cumulative_energy_kwh'].iloc[-1]) * 100
    print(f"   차이:              {diff_energy:+.3f} kWh ({diff_percent:+.1f}%)")

    print(f"\n   V1 최대 발전량:    {df_v1['active_power_w'].max():.1f} W")
    print(f"   V2 최대 발전량:    {df_v2['active_power_w'].max():.1f} W")
    print(f"   V1 평균 발전량:    {df_v1['active_power_w'].mean():.1f} W")
    print(f"   V2 평균 발전량:    {df_v2['active_power_w'].mean():.1f} W")

    print("\n" + "-" * 80)
    print("🔋 배터리 상태 비교")
    print("-" * 80)
    print(f"   V1 최종 SoC:       {df_v1['battery_soc'].iloc[-1]:.1f}%")
    print(f"   V2 최종 SoC:       {df_v2['battery_soc'].iloc[-1]:.1f}%")
    soc_diff = df_v2['battery_soc'].iloc[-1] - df_v1['battery_soc'].iloc[-1]
    print(f"   차이:              {soc_diff:+.1f}%")

    print(f"\n   V1 SoC 범위:       {df_v1['battery_soc'].min():.1f}% ~ {df_v1['battery_soc'].max():.1f}%")
    print(f"   V2 SoC 범위:       {df_v2['battery_soc'].min():.1f}% ~ {df_v2['battery_soc'].max():.1f}%")

    print("\n" + "-" * 80)
    print("🌞 태양 고도 정보")
    print("-" * 80)
    print(f"   최대 고도:         {df_v1['altitude_deg'].max():.1f}°")
    max_alt_idx = df_v1['altitude_deg'].idxmax()
    max_alt_time = df_v1.loc[max_alt_idx, 'timestamp']
    print(f"   최대 고도 시각:    {max_alt_time.strftime('%H:%M')}")

    print("\n" + "-" * 80)
    print("📊 주요 차이점 분석")
    print("-" * 80)

    # 정오 부근 발전량 차이
    noon_range = df_v1[(df_v1['hour'] >= 11) & (df_v1['hour'] <= 13)]
    v1_noon_avg = noon_range['active_power_w'].mean()
    v2_noon_avg = df_v2[(df_v2['hour'] >= 11) & (df_v2['hour'] <= 13)]['active_power_w'].mean()
    noon_diff_percent = ((v2_noon_avg - v1_noon_avg) / v1_noon_avg) * 100 if v1_noon_avg > 0 else 0

    print(f"   정오(11~13시) 평균 발전량:")
    print(f"      V1: {v1_noon_avg:.1f} W")
    print(f"      V2: {v2_noon_avg:.1f} W")
    print(f"      차이: {noon_diff_percent:+.1f}%")

    # 아침/저녁 발전량 차이
    morning_range = df_v1[(df_v1['hour'] >= 7) & (df_v1['hour'] <= 9)]
    v1_morning_avg = morning_range['active_power_w'].mean()
    v2_morning_avg = df_v2[(df_v2['hour'] >= 7) & (df_v2['hour'] <= 9)]['active_power_w'].mean()
    morning_diff_percent = ((v2_morning_avg - v1_morning_avg) / v1_morning_avg) * 100 if v1_morning_avg > 0 else 0

    print(f"\n   아침(07~09시) 평균 발전량:")
    print(f"      V1: {v1_morning_avg:.1f} W")
    print(f"      V2: {v2_morning_avg:.1f} W")
    print(f"      차이: {morning_diff_percent:+.1f}%")

    print("\n" + "-" * 80)
    print("✅ 개선 효과 요약")
    print("-" * 80)
    print(f"   1. 방위각 고려로 아침/저녁 발전량이 더 정확해짐 ({morning_diff_percent:+.1f}%)")
    print(f"   2. 배터리 효율 적용으로 실제 저장 에너지 감소 ({soc_diff:+.1f}% SoC)")
    print(f"   3. 전체 에너지 효율이 더 현실적으로 계산됨 ({diff_percent:+.1f}%)")

    print("\n" + "=" * 80 + "\n")


def main():
    """메인 실행 함수"""
    print("🚀 Simulator 비교 분석 시작...\n")

    # 설정 파일 로드
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 시뮬레이션 시작 시간 (한국 현재 - 1주일 전)
    # 2025년 10월 12일부터 7일간
    start_time = datetime(2025, 10, 12, 0, 0, 0, tzinfo=pytz.timezone(config['location']['timezone']))
    days = 7

    print(f"📅 시뮬레이션 기간: {start_time.strftime('%Y-%m-%d')} ~ {(start_time + timedelta(days=days)).strftime('%Y-%m-%d')} ({days}일)")
    print(f"⏱️  샘플링 간격: {config['simulation_interval_seconds']}초\n")

    # V1 시뮬레이션
    print("⚙️  V1 (기존) 시뮬레이션 실행 중...")
    df_v1 = simulate_v1(config, start_time, hours=days*24)
    print(f"✅ V1 완료: {len(df_v1)} 데이터 포인트")

    # V2 시뮬레이션
    print("⚙️  V2 (개선) 시뮬레이션 실행 중...")
    df_v2 = simulate_v2(config, start_time, hours=days*24)
    print(f"✅ V2 완료: {len(df_v2)} 데이터 포인트")

    # 리포트 생성
    generate_report(df_v1, df_v2, config)

    # 그래프 생성
    print("📊 비교 그래프 생성 중...")
    plot_comparison(df_v1, df_v2)

    # CSV 저장
    df_v1.to_csv('simulation_v1_results.csv', index=False)
    df_v2.to_csv('simulation_v2_results.csv', index=False)
    print("💾 CSV 결과 저장: simulation_v1_results.csv, simulation_v2_results.csv")

    print("\n✨ 분석 완료!")


if __name__ == "__main__":
    main()
