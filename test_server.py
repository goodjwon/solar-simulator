from flask import Flask, request, jsonify
import json
import logging
import csv
import os

# 로깅 기본 설정 (Flask의 기본 로거 사용 안함)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# 저장할 CSV 파일 이름
CSV_FILE_NAME = 'sensor_data_log.csv'

@app.route('/api/sensors/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    # --- 터미널에 데이터 출력 (기존과 동일) ---
    print("\n" + "="*50)
    print(f"✅ {data.get('timestamp')} 데이터 수신 완료!")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("="*50)
    
    # --- [추가] CSV 파일 저장 로직 ---
    try:
        # 1. 데이터를 CSV에 쓸 한 줄(row)로 만듭니다. (중첩 구조 해제)
        row_data = {
            'timestamp': data.get('timestamp'),
            'voltage_v': data.get('power_metrics', {}).get('voltage_v'),
            'current_a': data.get('power_metrics', {}).get('current_a'),
            'active_power_w': data.get('power_metrics', {}).get('active_power_w'),
            'apparent_power_va': data.get('power_metrics', {}).get('apparent_power_va'),
            'power_factor': data.get('power_metrics', {}).get('power_factor'),
            'energy_kwh': data.get('energy_kwh'),
            'battery_status': data.get('battery_metrics', {}).get('status'),
            'battery_soc_percent': data.get('battery_metrics', {}).get('soc_percent'),
            'battery_power_flow_w': data.get('battery_metrics', {}).get('power_flow_w'),
            'battery_temperature_c': data.get('battery_metrics', {}).get('temperature_c'),
            'illuminance_lux': data.get('environment', {}).get('illuminance_lux'),
            'panel_temp_c': data.get('environment', {}).get('panel_temp_c'),
            'ambient_temp_c': data.get('environment', {}).get('ambient_temp_c'),
            'humidity_percent': data.get('environment', {}).get('humidity_percent')
        }

        # 2. 파일이 없으면 헤더(첫 줄)를 먼저 씁니다.
        file_exists = os.path.isfile(CSV_FILE_NAME)
        with open(CSV_FILE_NAME, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=row_data.keys())
            if not file_exists:
                writer.writeheader()
            
            # 3. 데이터 한 줄을 파일에 추가합니다.
            writer.writerow(row_data)
            
    except Exception as e:
        print(f"❌ CSV 파일 저장 중 오류 발생: {e}")

    return jsonify({"status": "success", "message": "Data received and saved"}), 201

if __name__ == '__main__':
    print("🚀 데이터를 수신하고 CSV 파일로 저장하는 테스트 서버를 시작합니다.")
    print(f"저장 파일: {CSV_FILE_NAME}")
    app.run(port=8080, debug=False)