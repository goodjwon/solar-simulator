

# 🌞 Solar Monitor Pro - 가상 시뮬레이터 (Virtual Simulator)

이 프로젝트는 Solar Monitor Pro의 백엔드 및 프론트엔드 개발을 위해 실제 하드웨어 없이도 사실적인 태양광 발전 데이터를 생성하고 API 서버로 전송하는 Python 기반의 가상 시뮬레이터입니다.

## ✨ 주요 기능

  - **실시간 데이터 생성**: 1초 단위로 태양광 발전 관련 데이터를 생성합니다.
  - **동적 제어**: 실행 중 `config.json` 파일 수정만으로 시뮬레이션 환경(패널 수, 날씨 등)을 실시간 변경할 수 있습니다.
  - **현실적인 환경 반영**:
      - **시간 및 계절**: 태양 위치 계산 라이브러리(`suncalc`)를 사용하여 일출/일몰 및 계절에 따른 발전량 변화를 자동으로 시뮬레이션합니다.
      - **실시간 날씨**: OpenWeatherMap API와 연동하여 실제 날씨(맑음, 구름, 비 등)를 발전량 계산에 반영합니다.
  - **상세 로깅**: 데이터 생성, 전송 성공/실패 등 모든 과정을 추적할 수 있는 상세한 로그를 제공합니다.
  - **테스트 서버 포함**: 전송된 데이터가 올바른 형식으로 수신되는지 즉시 확인할 수 있는 간단한 Flask 테스트 서버(`test_server.py`)가 포함되어 있습니다.

## ⚙️ 시스템 요구사항

  - Windows 10/11 또는 macOS
  - Python 3.8 이상
  - Homebrew (macOS 사용자)

## 🚀 설치 및 설정 가이드

### 1단계: Python 설치

  - **Windows:**

    1.  [python.org](https://python.org/)에서 최신 버전의 Python을 다운로드합니다.
    2.  설치 프로그램 실행 시, **반드시 "Add Python.exe to PATH" 옵션을 체크**합니다.
    3.  설치 후 터미널(PowerShell)에서 `python --version` 명령어로 설치를 확인합니다.

  - **macOS:**

    1.  터미널을 열고, [Homebrew](https://www.google.com/search?q=https://brew.sh/index_ko)가 설치되어 있지 않다면 아래 명령어로 설치합니다.
        ```bash
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
    2.  Homebrew를 통해 Python 최신 버전을 설치합니다.
        ```bash
        brew install python
        ```
    3.  설치 후 터미널에서 `python3 --version` 명령어로 설치를 확인합니다.

### 2단계: `uv` 설치

`uv`는 매우 빠른 파이썬 패키지 관리 도구입니다.

  - **Windows:**
    PowerShell을 **관리자 권한으로 실행**하고 아래 명령어를 입력합니다.

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

  - **macOS:**
    터미널에 아래 명령어를 입력합니다.

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

설치 후 새 터미널에서 `uv --version` 명령어로 설치를 확인합니다.

### 3단계: 프로젝트 파일 준비

1.  `solar-simulator`와 같은 프로젝트 폴더를 생성합니다.
2.  이전 안내에서 제공된 `config.json`, `simulator.py`, `test_server.py` 파일을 이 폴더 안에 저장합니다.

### 4단계: 가상 환경 및 라이브러리 설치

프로젝트 폴더에서 터미널을 열고 아래 명령어를 순서대로 실행합니다.

1.  **가상 환경 생성 (Windows & macOS 동일)**

    ```bash
    uv venv
    ```

2.  **가상 환경 활성화**

      - **Windows (PowerShell):**
        ```bash
        .\.venv\Scripts\activate
        ```
      - **macOS (zsh/bash):**
        ```bash
        source .venv/bin/activate
        ```

    터미널 프롬프트 앞에 `(.venv)`가 표시되면 가상 환경이 활성화된 것입니다.

3.  **필요한 라이브러리 설치 (Windows & macOS 동일)**

    ```bash
    uv pip install requests suncalc pytz Flask
    ```

### 5단계: API 키 설정

1.  [OpenWeatherMap](https://openweathermap.org/)에 가입하고 무료 API 키를 발급받습니다.
2.  `config.json` 파일을 열어 `YOUR_OPENWEATHERMAP_API_KEY` 부분을 자신의 API 키로 교체합니다.

## ▶️ 사용 방법

두 개의 터미널 창을 사용합니다. 각 터미널에서 **반드시 먼저 가상 환경을 활성화**해야 합니다.

**터미널 1: 테스트 서버 실행**

> 이 터미널에는 시뮬레이터로부터 수신된 데이터가 JSON 형식으로 출력됩니다.

  - **Windows:**
    ```bash
    .\.venv\Scripts\activate
    python test_server.py
    ```
  - **macOS:**
    ```bash
    source .venv/bin/activate
    python3 test_server.py
    ```

**터미널 2: 시뮬레이터 실행**

> 이 터미널에는 데이터 생성 및 전송 상태에 대한 로그가 출력됩니다.

  - **Windows:**
    ```bash
    .\.venv\Scripts\activate
    python simulator.py
    ```
  - **macOS:**
    ```bash
    source .venv/bin/activate
    python3 simulator.py
    ```

## 데이터 포멧
```json
{
  "장치ID": "태양광_패널_01",
  "데이터_수신_시각": "2025-10-08T16:10:14.840374+09:00",
  "전력_계측": {
    "전압_V": 221.44,
    "전류_A": 2.34,
    "유효_전력_W": 509.73,
    "피상_전력_VA": 517.5,
    "역률": 0.985
  },
  "누적_에너지_kWh": 4.2233,
  "배터리_정보": {
    "사용_여부": true,
    "상태": "방전 중",
    "충전_상태_%": 44.54,
    "전력_흐름_W": -468.43,
    "배터리_용량_kWh": 10,
    "배터리_온도_℃": 27.53
  },
  "환경_정보": {
    "조도_Lux": 55992.84,
    "패널_온도_℃": 39.99,
    "외부_온도_℃": 26.9,
    "습도_%": 51.4
  }
}

```

```json
{
  "deviceId": "SOLAR_PANEL_01",
  "timestamp": "2025-10-08T16:13:03.326859+09:00",
  "power_metrics": {
    "voltage_v": 221.4,
    "current_a": 2.3,
    "active_power_w": 497.64,
    "apparent_power_va": 508.84,
    "power_factor": 0.978
  },
  "energy_kwh": 4.2427,
  "battery_metrics": {
    "enabled": true,
    "status": "Discharging",
    "soc_percent": 44.35,
    "power_flow_w": -475.43,
    "capacity_kwh": 10,
    "temperature_c": 27.63
  },
  "environment": {
    "illuminance_lux": 54715.35,
    "panel_temp_c": 38.22,
    "ambient_temp_c": 26.72,
    "humidity_percent": 50.21
  }
}
```

## 🔧 문제 해결

  - **`ModuleNotFoundError` 발생 시**: 터미널에 `(.venv)` 표시가 있는지 확인하세요. 없다면 각 운영체제에 맞는 가상 환경 활성화 명령어를 먼저 실행하세요.
  - **데이터가 수신되지 않을 경우**:
    1.  `simulator.py`의 `requests.post` 부분이 주석 처리되어 있지 않은지 확인하세요.
    2.  `test_server.py` 실행 시 운영체제(Windows 또는 macOS)의 **방화벽 허용** 창이 뜨면 반드시 \*\*'허용'\*\*을 클릭했는지 확인하세요.