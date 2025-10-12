# Epic 2: 하드웨어 조립 및 펌웨어 개발

*센서와 마이크로컨트롤러를 연결하고 데이터 수집 펌웨어 개발*

## Story 2.1: 하드웨어 조립 및 회로 구성

**목표**: 센서와 컨트롤러를 연결하여 물리적 시스템 구축

### Task 2.1.1: 브레드보드 프로토타입 조립

- **SubTask 2.1.1.1**: 전원 공급 회로 구성 (12V → 5V 변환)
- **SubTask 2.1.1.2**: 메인 컨트롤러 배치 (ESP32 또는 Arduino Mega)
- **SubTask 2.1.1.3**: 전력 측정 센서 연결 (PZEM-004T)
    - TX/RX 핀 연결 (UART 통신)
- **SubTask 2.1.1.4**: 전압 센서 연결 (ZMPT101B)
    - 아날로그 핀 연결 및 분배기 설정

### Task 2.1.2: 환경 센서 연결

- **SubTask 2.1.2.1**: 온습도 센서 연결 (DHT22 또는 BME280)
    - I2C 또는 디지털 핀 연결
- **SubTask 2.1.2.2**: 조도 센서 연결 (BH1750)
    - I2C 통신 설정 (SDA, SCL)
- **SubTask 2.1.2.3**: 온도 센서 연결 (DS18B20)
    - OneWire 프로토콜 설정
- **SubTask 2.1.2.4**: 센서 전원 및 풀업 저항 설정

### Task 2.1.3: 통신 모듈 연결

- **SubTask 2.1.3.1**: WiFi 모듈 연결 (ESP8266 또는 ESP32 내장)
- **SubTask 2.1.3.2**: SD 카드 모듈 연결 (SPI 통신)
    - CS, MOSI, MISO, SCK 핀 설정
- **SubTask 2.1.3.3**: RTC 모듈 연결 (DS3231)
    - I2C 통신, 백업 배터리 설치
- **SubTask 2.1.3.4**: 디스플레이 연결 (LCD 또는 OLED, 선택사항)

### Task 2.1.4: 보호 회로 추가

- **SubTask 2.1.4.1**: 퓨즈 설치 (과전류 보호)
- **SubTask 2.1.4.2**: TVS 다이오드 설치 (서지 보호)
- **SubTask 2.1.4.3**: 다이오드 역전압 보호
- **SubTask 2.1.4.4**: 회로 점검 및 멀티미터 측정

---

## Story 2.2: Arduino/ESP32 개발 환경 설정

**목표**: 펌웨어 개발 및 업로드 환경 구축

### Task 2.2.1: Arduino IDE 설정

- **SubTask 2.2.1.1**: Arduino IDE 설치 (최신 버전)
- **SubTask 2.2.1.2**: 보드 매니저에서 ESP32 또는 Arduino Mega 추가
- **SubTask 2.2.1.3**: 필요한 라이브러리 설치
    - WiFi, HTTPClient
    - DHT, BME280, BH1750, OneWire
    - ArduinoJson, RTClib
- **SubTask 2.2.1.4**: 시리얼 포트 및 보드 설정 확인

### Task 2.2.2: 기본 동작 테스트

- **SubTask 2.2.2.1**: Blink 예제로 컨트롤러 동작 확인
- **SubTask 2.2.2.2**: Serial Monitor로 출력 확인
- **SubTask 2.2.2.3**: WiFi 연결 테스트 스케치 작성
- **SubTask 2.2.2.4**: HTTP GET/POST 테스트

### Task 2.2.3: 센서 라이브러리 테스트

- **SubTask 2.2.3.1**: 각 센서별 개별 테스트 스케치 작성
- **SubTask 2.2.3.2**: I2C 스캐너로 주소 확인
- **SubTask 2.2.3.3**: 센서 데이터 시리얼 출력 확인
- **SubTask 2.2.3.4**: 데이터 정확도 검증 (멀티미터 비교)

---

## Story 2.3: 센서 데이터 수집 펌웨어

**목표**: 실시간으로 센서 값을 읽어오는 코드 구현

### Task 2.3.1: 전력 측정 코드

- **SubTask 2.3.1.1**: PZEM-004T 라이브러리 초기화
    ```cpp
    #include <PZEM004Tv30.h>
    PZEM004Tv30 pzem(Serial2, RX_PIN, TX_PIN);
    ```
- **SubTask 2.3.1.2**: 전압(V), 전류(A), 전력(W) 읽기 함수
- **SubTask 2.3.1.3**: 에너지(kWh) 누적 계산
- **SubTask 2.3.1.4**: 역률(Power Factor) 읽기

### Task 2.3.2: 환경 센서 데이터 수집

- **SubTask 2.3.2.1**: DHT22/BME280 온습도 읽기 함수
    ```cpp
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    ```
- **SubTask 2.3.2.2**: BH1750 조도 읽기 함수 (lux)
- **SubTask 2.3.2.3**: DS18B20 온도 읽기 함수
- **SubTask 2.3.2.4**: 센서 에러 처리 (NaN, timeout)

### Task 2.3.3: 배터리 데이터 수집 (선택사항)

- **SubTask 2.3.3.1**: 배터리 전압 측정 (전압 분배기)
- **SubTask 2.3.3.2**: 배터리 전류 측정 (ACS712)
- **SubTask 2.3.3.3**: SOC(충전 상태) 계산 로직
- **SubTask 2.3.3.4**: 배터리 온도 모니터링

### Task 2.3.4: 데이터 집계 및 포맷팅

- **SubTask 2.3.4.1**: JSON 데이터 구조 정의
    ```cpp
    {
      "deviceId": "SOLAR_PANEL_01",
      "timestamp": "2025-01-12T10:30:00+09:00",
      "power_metrics": {...},
      "environment": {...}
    }
    ```
- **SubTask 2.3.4.2**: ArduinoJson 라이브러리로 직렬화
- **SubTask 2.3.4.3**: 타임스탬프 생성 (RTC 사용)
- **SubTask 2.3.4.4**: 데이터 샘플링 주기 설정 (1초/5초/10초)

---

## Story 2.4: 네트워크 통신 구현

**목표**: WiFi로 백엔드 서버에 데이터 전송

### Task 2.4.1: WiFi 연결 관리

- **SubTask 2.4.1.1**: WiFi 연결 함수 구현
    ```cpp
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
    }
    ```
- **SubTask 2.4.1.2**: 연결 실패 시 재시도 로직
- **SubTask 2.4.1.3**: 연결 상태 LED 표시
- **SubTask 2.4.1.4**: WiFi 절전 모드 설정 (배터리 사용 시)

### Task 2.4.2: HTTP POST 전송

- **SubTask 2.4.2.1**: HTTPClient 라이브러리 설정
- **SubTask 2.4.2.2**: POST 요청 함수 작성
    ```cpp
    http.begin(API_ENDPOINT);
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(jsonString);
    ```
- **SubTask 2.4.2.3**: 응답 코드 확인 (200, 201, 4xx, 5xx)
- **SubTask 2.4.2.4**: 전송 실패 시 재시도 로직 (최대 3회)

### Task 2.4.3: 데이터 버퍼링

- **SubTask 2.4.3.1**: 네트워크 단절 시 데이터 SD 카드 저장
- **SubTask 2.4.3.2**: 큐 또는 링 버퍼 구현
- **SubTask 2.4.3.3**: 재연결 시 버퍼 데이터 일괄 전송
- **SubTask 2.4.3.4**: 버퍼 오버플로우 처리

### Task 2.4.4: 시간 동기화

- **SubTask 2.4.4.1**: NTP 서버로 시간 동기화
    ```cpp
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    ```
- **SubTask 2.4.4.2**: RTC 모듈에 시간 설정
- **SubTask 2.4.4.3**: 부팅 시 자동 시간 동기화
- **SubTask 2.4.4.4**: 타임존 설정 (Asia/Seoul)

---

## Story 2.5: 로컬 데이터 저장

**목표**: SD 카드에 백업 데이터 저장

### Task 2.5.1: SD 카드 초기화

- **SubTask 2.5.1.1**: SD 라이브러리 설정 및 마운트
    ```cpp
    if(!SD.begin(CS_PIN)) {
      Serial.println("SD Card Mount Failed");
      return;
    }
    ```
- **SubTask 2.5.1.2**: 파일 시스템 확인 (FAT32)
- **SubTask 2.5.1.3**: SD 카드 용량 및 여유 공간 체크
- **SubTask 2.5.1.4**: 카드 제거 감지

### Task 2.5.2: CSV 파일 저장

- **SubTask 2.5.2.1**: 데이터 로그 파일 생성 (날짜별)
    - 예: `sensor_data_20250112.csv`
- **SubTask 2.5.2.2**: CSV 헤더 작성 (첫 줄)
- **SubTask 2.5.2.3**: 데이터 한 줄씩 추가 (append)
- **SubTask 2.5.2.4**: 파일 크기 제한 (10MB 초과 시 새 파일)

### Task 2.5.3: 로그 파일 관리

- **SubTask 2.5.3.1**: 오래된 파일 자동 삭제 (30일 이상)
- **SubTask 2.5.3.2**: 파일 목록 조회 및 정리
- **SubTask 2.5.3.3**: SD 카드 오류 로그 기록
- **SubTask 2.5.3.4**: 저장 실패 시 에러 처리

---

## Story 2.6: 디스플레이 및 상태 표시 (선택사항)

**목표**: 로컬에서 시스템 상태 확인

### Task 2.6.1: LCD/OLED 디스플레이

- **SubTask 2.6.1.1**: 디스플레이 초기화 (I2C 주소 설정)
- **SubTask 2.6.1.2**: 현재 발전량 표시 (W)
- **SubTask 2.6.1.3**: 누적 에너지 표시 (kWh)
- **SubTask 2.6.1.4**: WiFi 연결 상태 표시

### Task 2.6.2: LED 상태 인디케이터

- **SubTask 2.6.2.1**: 전원 LED (녹색)
- **SubTask 2.6.2.2**: WiFi 연결 LED (파란색)
- **SubTask 2.6.2.3**: 데이터 전송 LED (깜빡임)
- **SubTask 2.6.2.4**: 에러 LED (빨간색)

### Task 2.6.3: 버튼 인터페이스

- **SubTask 2.6.3.1**: 리셋 버튼 (재부팅)
- **SubTask 2.6.3.2**: 디스플레이 모드 전환 버튼
- **SubTask 2.6.3.3**: WiFi 재연결 버튼
- **SubTask 2.6.3.4**: 디바운싱 처리

---

## Story 2.7: 펌웨어 최적화 및 안정성

**목표**: 장시간 안정적인 동작 보장

### Task 2.7.1: 메모리 관리

- **SubTask 2.7.1.1**: 메모리 누수 확인 및 수정
    ```cpp
    Serial.printf("Free heap: %d\n", ESP.getFreeHeap());
    ```
- **SubTask 2.7.1.2**: 문자열 최적화 (String → char*)
- **SubTask 2.7.1.3**: 불필요한 전역 변수 제거
- **SubTask 2.7.1.4**: PROGMEM 활용 (상수를 Flash에 저장)

### Task 2.7.2: 전력 관리

- **SubTask 2.7.2.1**: Deep Sleep 모드 구현 (배터리 사용 시)
- **SubTask 2.7.2.2**: 센서 읽기 주기 최적화
- **SubTask 2.7.2.3**: WiFi 절전 모드 활성화
- **SubTask 2.7.2.4**: 소비 전류 측정 및 최적화

### Task 2.7.3: 에러 처리 및 복구

- **SubTask 2.7.3.1**: Watchdog Timer 설정 (자동 재부팅)
    ```cpp
    esp_task_wdt_init(WDT_TIMEOUT, true);
    ```
- **SubTask 2.7.3.2**: 센서 읽기 실패 시 기본값 사용
- **SubTask 2.7.3.3**: 네트워크 장애 시 재연결 로직
- **SubTask 2.7.3.4**: 예외 상황 로그 기록

### Task 2.7.4: OTA 업데이트 (선택사항)

- **SubTask 2.7.4.1**: ArduinoOTA 라이브러리 설정
- **SubTask 2.7.4.2**: WiFi로 펌웨어 업데이트 기능
- **SubTask 2.7.4.3**: 업데이트 중 안정성 보장
- **SubTask 2.7.4.4**: 버전 관리 및 롤백 기능

---

## Story 2.8: 테스트 및 검증

**목표**: 하드웨어 및 펌웨어 동작 확인

### Task 2.8.1: 단위 테스트

- **SubTask 2.8.1.1**: 센서별 개별 동작 테스트
- **SubTask 2.8.1.2**: 데이터 정확도 검증 (멀티미터 비교)
- **SubTask 2.8.1.3**: 네트워크 통신 테스트 (Mock 서버)
- **SubTask 2.8.1.4**: SD 카드 읽기/쓰기 테스트

### Task 2.8.2: 통합 테스트

- **SubTask 2.8.2.1**: 전체 시스템 동작 테스트 (1시간)
- **SubTask 2.8.2.2**: 네트워크 단절 시나리오 테스트
- **SubTask 2.8.2.3**: 전원 차단 및 재부팅 테스트
- **SubTask 2.8.2.4**: 고온/저온 환경 테스트 (선택사항)

### Task 2.8.3: 장시간 안정성 테스트

- **SubTask 2.8.3.1**: 24시간 연속 동작 테스트
- **SubTask 2.8.3.2**: 메모리 누수 확인
- **SubTask 2.8.3.3**: 데이터 무결성 확인
- **SubTask 2.8.3.4**: 센서 드리프트 체크

### Task 2.8.4: 문서화

- **SubTask 2.8.4.1**: 회로도 최종 업데이트
- **SubTask 2.8.4.2**: 핀맵 문서화
- **SubTask 2.8.4.3**: 펌웨어 설정 가이드
- **SubTask 2.8.4.4**: 트러블슈팅 가이드

---

## 산출물

- [ ]  조립된 프로토타입 하드웨어
- [ ]  최종 회로도 및 핀맵 문서
- [ ]  Arduino/ESP32 펌웨어 소스코드
- [ ]  센서 캘리브레이션 데이터
- [ ]  하드웨어 테스트 결과 보고서
- [ ]  펌웨어 설치 및 설정 가이드
- [ ]  트러블슈팅 매뉴얼

---

## 다음 에픽으로 이동 조건

- [ ]  모든 센서 정상 동작 확인
- [ ]  WiFi 통신 안정성 확보
- [ ]  데이터 전송 성공률 95% 이상
- [ ]  24시간 안정성 테스트 통과
- [ ]  SD 카드 백업 기능 정상 작동
- [ ]  펌웨어 문서화 완료
