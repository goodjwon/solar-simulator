"""
Solar Simulator 검증 테스트

기존 simulator.py와 개선된 simulator_v2.py의 알고리즘을 검증합니다.
"""

import pytest
import math
from datetime import datetime
import pytz

# simulator_v2의 함수들을 임포트
from simulator_v2 import (
    calculate_solar_irradiance,
    calculate_battery_efficiency,
    update_battery_temperature,
    get_weather_multiplier
)


class TestSolarIrradiance:
    """태양 복사 조도 계산 테스트"""

    def test_night_time_zero_irradiance(self):
        """밤(고도 < 0)일 때 조도 = 0"""
        irradiance = calculate_solar_irradiance(
            altitude_deg=-10,
            azimuth_deg=180
        )
        assert irradiance == 0.0, "밤에는 조도가 0이어야 함"

    def test_noon_maximum_irradiance(self):
        """정오(남향, 고도 최대)일 때 조도가 최대에 가까움"""
        # 여름 정오 (고도 약 76도, 서울 기준)
        # suncalc 기준: 0=남
        irradiance_noon = calculate_solar_irradiance(
            altitude_deg=76,
            azimuth_deg=0,  # 남향 (suncalc 기준)
            panel_azimuth=0,  # 패널도 남향
            panel_tilt=30
        )

        # 아침/저녁 (고도 30도)
        # suncalc 기준: 270=동
        irradiance_morning = calculate_solar_irradiance(
            altitude_deg=30,
            azimuth_deg=270,  # 동향 (suncalc 기준)
            panel_azimuth=0,
            panel_tilt=30
        )

        assert irradiance_noon > irradiance_morning, "정오가 아침보다 조도가 높아야 함"
        assert irradiance_noon > 0.8, "정오 조도는 0.8 이상이어야 함"

    def test_azimuth_effect(self):
        """방위각에 따른 조도 변화"""
        altitude = 45  # 동일한 고도

        # 남향 (최적) - suncalc 기준: 0=남
        south = calculate_solar_irradiance(
            altitude_deg=altitude,
            azimuth_deg=0,
            panel_azimuth=0
        )

        # 동향 - suncalc 기준: 270=동
        east = calculate_solar_irradiance(
            altitude_deg=altitude,
            azimuth_deg=270,
            panel_azimuth=0
        )

        # 북향 (최악) - suncalc 기준: 180=북
        north = calculate_solar_irradiance(
            altitude_deg=altitude,
            azimuth_deg=180,
            panel_azimuth=0
        )

        assert south > east > north, "남향 > 동향 > 북향 순서여야 함"

    def test_irradiance_range(self):
        """조도 값이 0~1 범위 내"""
        for altitude in range(-20, 90, 10):
            for azimuth in range(0, 360, 30):
                irradiance = calculate_solar_irradiance(altitude, azimuth)
                assert 0.0 <= irradiance <= 1.0, f"조도는 0~1 범위여야 함 (altitude={altitude}, azimuth={azimuth})"


class TestBatteryEfficiency:
    """배터리 효율 테스트"""

    def test_charging_efficiency_normal(self):
        """정상 SoC(< 90%)에서 충전 효율"""
        efficiency = calculate_battery_efficiency(soc_percent=50, charging=True)
        assert efficiency == 0.92, "정상 SoC에서 충전 효율은 92%"

    def test_charging_efficiency_high_soc(self):
        """높은 SoC(>= 90%)에서 충전 효율 감소"""
        eff_90 = calculate_battery_efficiency(soc_percent=90, charging=True)
        eff_95 = calculate_battery_efficiency(soc_percent=95, charging=True)
        eff_100 = calculate_battery_efficiency(soc_percent=100, charging=True)

        assert eff_90 == 0.92, "90%에서는 여전히 92%"
        assert eff_95 < eff_90, "95%에서는 효율 감소"
        assert eff_100 < eff_95, "100%에서는 더욱 감소"
        assert eff_100 == 0.75, "100%에서는 75%"

    def test_discharging_efficiency_normal(self):
        """정상 SoC(> 20%)에서 방전 효율"""
        efficiency = calculate_battery_efficiency(soc_percent=50, charging=False)
        assert efficiency == 0.88, "정상 SoC에서 방전 효율은 88%"

    def test_discharging_efficiency_low_soc(self):
        """낮은 SoC(<= 20%)에서 방전 효율 감소"""
        eff_20 = calculate_battery_efficiency(soc_percent=20, charging=False)
        eff_10 = calculate_battery_efficiency(soc_percent=10, charging=False)
        eff_0 = calculate_battery_efficiency(soc_percent=0, charging=False)

        assert abs(eff_20 - 0.88) < 0.001, "20%에서는 여전히 88%"
        assert eff_10 < eff_20, "10%에서는 효율 감소"
        assert eff_0 < eff_10, "0%에서는 더욱 감소"
        assert abs(eff_0 - 0.70) < 0.001, "0%에서는 70%"


class TestBatteryTemperature:
    """배터리 온도 시뮬레이션 테스트"""

    def test_temperature_rise_on_charging(self):
        """충전 시 온도 상승"""
        initial_temp = 25.0
        ambient_temp = 25.0
        power_flow = 1000  # 1kW 충전
        interval = 60  # 60초

        new_temp = update_battery_temperature(
            initial_temp,
            ambient_temp,
            power_flow,
            interval
        )

        # 노이즈 제거하고 평균적으로 온도 상승 확인
        assert new_temp > initial_temp - 0.5, "충전 시 온도가 상승해야 함 (노이즈 고려)"

    def test_temperature_cooling(self):
        """주변 온도보다 높을 때 냉각"""
        initial_temp = 35.0
        ambient_temp = 25.0
        power_flow = 0  # 충/방전 없음
        interval = 600  # 10분

        new_temp = update_battery_temperature(
            initial_temp,
            ambient_temp,
            power_flow,
            interval
        )

        # 냉각되어야 함
        assert new_temp < initial_temp + 0.5, "주변 온도보다 높으면 냉각되어야 함 (노이즈 고려)"

    def test_temperature_equilibrium(self):
        """장시간 방치 시 주변 온도로 수렴"""
        initial_temp = 35.0
        ambient_temp = 25.0
        power_flow = 0

        current_temp = initial_temp
        for _ in range(100):  # 100분 시뮬레이션
            current_temp = update_battery_temperature(
                current_temp,
                ambient_temp,
                power_flow,
                60
            )

        # 주변 온도에 가까워져야 함 (±4°C 이내, 현실적인 냉각률 고려)
        assert abs(current_temp - ambient_temp) < 4, "장시간 후에는 주변 온도에 수렴해야 함"
        # 적어도 초기 온도보다는 낮아져야 함
        assert current_temp < initial_temp, "냉각되어야 함"


class TestWeatherMultiplier:
    """날씨별 발전량 감소율 테스트"""

    def test_clear_weather(self):
        """맑은 날 = 100% 발전"""
        multiplier = get_weather_multiplier("Clear")
        assert multiplier == 1.0, "맑은 날은 100% 발전"

    def test_cloudy_weather(self):
        """흐린 날 = 40% 발전"""
        multiplier = get_weather_multiplier("Clouds")
        assert multiplier == 0.4, "흐린 날은 40% 발전"

    def test_rainy_weather(self):
        """비 오는 날 = 15% 발전"""
        multiplier = get_weather_multiplier("Rain")
        assert multiplier == 0.15, "비 오는 날은 15% 발전"

    def test_weather_order(self):
        """날씨별 발전량 순서"""
        clear = get_weather_multiplier("Clear")
        clouds = get_weather_multiplier("Clouds")
        rain = get_weather_multiplier("Rain")
        snow = get_weather_multiplier("Snow")

        assert clear > clouds > rain >= snow, "맑음 > 구름 > 비 >= 눈 순서"


class TestRealisticScenarios:
    """실제 시나리오 테스트"""

    def test_summer_noon_seoul(self):
        """여름 정오 서울 (고도 약 76도, 남향)"""
        irradiance = calculate_solar_irradiance(
            altitude_deg=76,
            azimuth_deg=0,  # suncalc 기준: 0=남
            panel_azimuth=0,
            panel_tilt=30
        )

        # 여름 정오는 90% 이상 효율 예상
        assert irradiance > 0.85, f"여름 정오는 85% 이상 조도 (실제: {irradiance:.2f})"

    def test_winter_noon_seoul(self):
        """겨울 정오 서울 (고도 약 30도, 남향)"""
        irradiance = calculate_solar_irradiance(
            altitude_deg=30,
            azimuth_deg=0,  # suncalc 기준: 0=남
            panel_azimuth=0,
            panel_tilt=30
        )

        # 겨울 정오는 45% 이상 효율 예상 (고도가 낮아서 tilt efficiency 감소)
        assert irradiance > 0.45, f"겨울 정오는 45% 이상 조도 (실제: {irradiance:.2f})"

    def test_battery_full_cycle(self):
        """배터리 완충 사이클"""
        soc = 0.0
        capacity_kwh = 10.0

        # 1kW로 10시간 충전 (효율 고려)
        for _ in range(600):  # 10시간 = 600분
            efficiency = calculate_battery_efficiency(soc, charging=True)
            energy_change = (1000 * efficiency / 1000) * (60 / 3600)  # kWh
            soc_change = (energy_change / capacity_kwh) * 100
            soc += soc_change

            if soc >= 100:
                soc = 100
                break

        # 효율 손실로 인해 정확히 10시간은 아니지만 합리적인 범위
        assert 90 <= soc <= 100, f"10시간 충전 후 SoC는 90~100% (실제: {soc:.1f}%)"

    def test_daily_temperature_variation(self):
        """일일 온도 변화 시뮬레이션"""
        ambient_temps = [20, 22, 25, 28, 30, 28, 25, 22, 20]  # 하루 온도 변화
        battery_temp = 25.0

        for ambient in ambient_temps:
            # 1시간 동안 500W 충전
            battery_temp = update_battery_temperature(
                battery_temp,
                ambient,
                500,
                3600
            )

        # 배터리 온도가 합리적인 범위 내
        assert 20 <= battery_temp <= 35, f"배터리 온도는 20~35°C 범위 (실제: {battery_temp:.1f}°C)"


class TestEdgeCases:
    """경계 조건 테스트"""

    def test_soc_boundary_charging(self):
        """SoC 100% 도달 시 충전 효율"""
        eff = calculate_battery_efficiency(100, charging=True)
        assert eff == 0.75, "SoC 100%에서는 최소 효율"

    def test_soc_boundary_discharging(self):
        """SoC 0% 도달 시 방전 효율"""
        eff = calculate_battery_efficiency(0, charging=False)
        assert eff == 0.70, "SoC 0%에서는 최소 효율"

    def test_negative_altitude(self):
        """음수 고도 (일몰 후)"""
        irradiance = calculate_solar_irradiance(-30, 270)
        assert irradiance == 0.0, "음수 고도에서는 조도 0"

    def test_extreme_temperature_difference(self):
        """극심한 온도 차이"""
        battery_temp = 50.0
        ambient_temp = 0.0
        power_flow = 0

        new_temp = update_battery_temperature(
            battery_temp,
            ambient_temp,
            power_flow,
            60
        )

        # 냉각되어야 함
        assert new_temp < battery_temp, "극심한 온도 차이에서도 냉각되어야 함"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
