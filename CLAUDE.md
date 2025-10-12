# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Solar Monitor Pro Virtual Simulator is a Python-based solar power generation data simulator. It generates realistic solar panel data in real-time and sends it to an API endpoint, designed for backend/frontend development without requiring actual hardware.

**Project Scope**: This repository contains only the virtual simulator component. The full Solar Monitor Pro project includes hardware design, backend API (Spring Boot), frontend dashboard (Next.js), and deployment infrastructure. See `todo-list/` folder for complete project roadmap (Epic 0-9) covering hardware design, parts procurement, Arduino firmware, backend/frontend development, testing, and deployment.

## Key Architecture

### Core Components

1. **simulator.py** - Main simulation engine
   - Generates solar power data every N seconds (configurable via `simulation_interval_seconds`)
   - Uses `suncalc` library to calculate sun position based on time/location for realistic power generation
   - Integrates with OpenWeatherMap API for real-time weather conditions
   - Simulates battery charge/discharge cycles based on power generation vs home consumption
   - Hot-reloads `config.json` without restart when file is modified

2. **test_server.py** - Flask-based test server
   - Receives POST requests at `/api/sensors/data` endpoint
   - Logs received data to console and saves to `sensor_data_log.csv`
   - Flattens nested JSON structure for CSV storage

3. **config.json** - Runtime configuration (hot-reloadable)
   - Device identification, API endpoint, simulation interval
   - Location (lat/lon/timezone) for solar calculations
   - Weather API settings (OpenWeatherMap integration)
   - Solar panel specs (max power per panel, panel count)
   - Battery configuration (capacity, initial state of charge)
   - Home consumption patterns (day/night)

### Data Flow

```
config.json → simulator.py → API endpoint (test_server.py or production)
                ↓
        OpenWeatherMap API (optional)
```

### Key Algorithms

**Power Generation (simulator.py:89-93)**:
- Calculates solar altitude angle using suncalc
- Base power = total_panel_wattage × sin(altitude)
- Applies weather multiplier (Clear=1.0, Clouds=0.4, Rain=0.15, etc.)
- Only generates power when sun altitude > 0 (daytime)

**Battery Simulation (simulator.py:104-127)**:
- Tracks state of charge (SoC) as percentage
- Net power = generation - consumption
- Charging when net > 10W and SoC < 100%
- Discharging when net < -10W and SoC > 0%
- Battery temperature increases with power flow

**Config Hot-Reload (simulator.py:27-40)**:
- Checks file modification time on each iteration
- Reloads if `config.json` has changed
- Allows runtime changes to panel count, weather, consumption patterns

## Common Commands

### Environment Setup

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.\.venv\Scripts\activate

# Install dependencies
uv pip install requests suncalc pytz Flask
```

### Running the System

**Terminal 1 - Start test server:**
```bash
# macOS:
source .venv/bin/activate && python3 test_server.py

# Windows:
.\.venv\Scripts\activate && python test_server.py
```

**Terminal 2 - Start simulator:**
```bash
# macOS:
source .venv/bin/activate && python3 simulator.py

# Windows:
.\.venv\Scripts\activate && python simulator.py
```

### Development

The project has no automated tests currently. Testing is done by:
1. Running test_server.py to verify data reception
2. Checking console logs for data generation
3. Reviewing `sensor_data_log.csv` for data integrity

## Data Format

The simulator outputs JSON with this structure:
- `deviceId`: Device identifier
- `timestamp`: ISO 8601 timestamp with timezone
- `power_metrics`: voltage, current, active/apparent power, power factor
- `energy_kwh`: Cumulative energy since simulation start
- `battery_metrics`: enabled flag, status, SoC%, power flow, capacity, temperature
- `environment`: illuminance (lux), panel temp, ambient temp, humidity

## Important Notes

- **API Key**: OpenWeatherMap API key is in `config.json`. Use `use_real_weather: false` to disable API calls
- **Time Zone**: All timestamps use timezone from `config.json` (default: Asia/Seoul)
- **State Persistence**: Battery SoC and cumulative energy are stored in memory only (reset on restart)
- **Hot Reload**: Only `config.json` is hot-reloaded; code changes require restart
- **CSV Output**: test_server.py appends to `sensor_data_log.csv` (not cleared on restart)

## Project Roadmap Context

The `todo-list/` folder contains detailed epic plans for the complete Solar Monitor Pro system:

- **Epic 0**: System requirements, parts research, circuit design, BOM creation
- **Epic 1**: Parts procurement and inspection
- **Epic 2**: Hardware assembly (Arduino/ESP32 sensor integration) - NOT IMPLEMENTED YET
- **Epic 3**: Backend API (Spring Boot, PostgreSQL, WebSocket, data aggregation)
- **Epic 4**: Frontend Dashboard (Next.js, real-time charts, responsive design)
- **Epic 5**: Alert system (threshold rules, notifications, email/SMS)
- **Epic 6**: Data analytics (ML predictions, efficiency analysis, anomaly detection)
- **Epic 7**: Mobile app (React Native)
- **Epic 8**: Deployment (Docker, Kubernetes, CI/CD, monitoring)
- **Epic 9**: Testing & QA (unit/integration/E2E tests, performance, security)

**Current Status**: Only the virtual simulator (this repo) is implemented. When working on backend/frontend integration, refer to Epic 3 (simulator.py:89-93 for data format expectations) and Epic 4 (API endpoint structure) in todo-list/.
