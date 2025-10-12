# Epic 5: 데이터 조회 API 및 실시간 통신

*프론트엔드에서 필요한 데이터를 제공하는 API*

## Story 5.1: 실시간 데이터 조회 API

**목표**: 현재 상태 및 최신 데이터 제공

### Task 5.1.1: 현재 발전량 API

- **SubTask 5.1.1.1**: GET /api/v1/power/current 엔드포인트
- **SubTask 5.1.1.2**: PowerCurrentResponse DTO 정의
    
    ```java
    class PowerCurrentResponse {  Double currentPower;  Double peakPower;  Double avgPower;  Double minPower;  LocalDateTime timestamp;}
    
    ```
    
- **SubTask 5.1.1.3**: Service 레이어 구현
- **SubTask 5.1.1.4**: 캐싱 적용 (1초 TTL)

### Task 5.1.2: 배터리 상태 API

- **SubTask 5.1.2.1**: GET /api/v1/battery/status 엔드포인트
- **SubTask 5.1.2.2**: BatteryStatusResponse DTO
    - voltage, current, soc, temperature, health
- **SubTask 5.1.2.3**: 충전/방전 상태 계산 로직
- **SubTask 5.1.2.4**: 예상 잔여 시간 계산

### Task 5.1.3: 현재 소비량 API

- **SubTask 5.1.3.1**: GET /api/v1/consumption/current
- **SubTask 5.1.3.2**: ConsumptionResponse DTO
    - totalConsumption, byArea (Map)
- **SubTask 5.1.3.3**: 영역별 소비량 계산
- **SubTask 5.1.3.4**: 실시간 업데이트 주기 설정

### Task 5.1.4: 환경 정보 API

- **SubTask 5.1.4.1**: GET /api/v1/environment/current
- **SubTask 5.1.4.2**: EnvironmentResponse DTO
    - temperature, humidity, illuminance
- **SubTask 5.1.4.3**: 외부 날씨 API 통합 (선택사항)
- **SubTask 5.1.4.4**: 데이터 집계 및 평균 계산

---

## Story 5.2: WebSocket 실시간 스트리밍

**목표**: 실시간 데이터 푸시

### Task 5.2.1: Spring WebSocket 설정

- **SubTask 5.2.1.1**: WebSocket Configuration 클래스
    
    ```java
    @Configuration@EnableWebSocketMessageBrokerclass WebSocketConfig implements WebSocketMessageBrokerConfigurer
    
    ```
    
- **SubTask 5.2.1.2**: STOMP 엔드포인트 설정
- **SubTask 5.2.1.3**: 메시지 브로커 설정
- **SubTask 5.2.1.4**: CORS 설정

### Task 5.2.2: 구독 채널 구현

- **SubTask 5.2.2.1**: /topic/power 채널 (전력 데이터)
- **SubTask 5.2.2.2**: /topic/battery 채널 (배터리 상태)
- **SubTask 5.2.2.3**: /topic/alerts 채널 (알림)
- **SubTask 5.2.2.4**: /topic/system 채널 (시스템 상태)

### Task 5.2.3: 메시지 발행 서비스

- **SubTask 5.2.3.1**: WebSocketPublisher 서비스 클래스
- **SubTask 5.2.3.2**: SimpMessagingTemplate 주입
- **SubTask 5.2.3.3**: 데이터 수신 시 자동 발행
- **SubTask 5.2.3.4**: 메시지 포맷 표준화 (JSON)

### Task 5.2.4: 연결 관리

- **SubTask 5.2.4.1**: 세션 연결/해제 이벤트 처리
- **SubTask 5.2.4.2**: 하트비트 메커니즘
- **SubTask 5.2.4.3**: 재연결 로직
- **SubTask 5.2.4.4**: 연결 수 모니터링

---

## Story 5.3: 히스토리 데이터 조회 API

**목표**: 과거 데이터 및 통계 제공

### Task 5.3.1: 시계열 데이터 조회

- **SubTask 5.3.1.1**: GET /api/v1/power/history
    - Query Params: from, to, resolution
- **SubTask 5.3.1.2**: 날짜 범위 검증
- **SubTask 5.3.1.3**: 해상도별 데이터 집계 (1분/1시간/1일)
- **SubTask 5.3.1.4**: 페이지네이션 구현

### Task 5.3.2: 일별 통계 API

- **SubTask 5.3.2.1**: GET /api/v1/statistics/daily
- **SubTask 5.3.2.2**: DailyStatisticsResponse DTO
    - date, totalEnergy, peakPower, avgEfficiency
- **SubTask 5.3.2.3**: 날짜 범위 필터링
- **SubTask 5.3.2.4**: 정렬 옵션 (날짜 오름차순/내림차순)

### Task 5.3.3: 월별 통계 API

- **SubTask 5.3.3.1**: GET /api/v1/statistics/monthly
- **SubTask 5.3.3.2**: MonthlyStatisticsResponse DTO
- **SubTask 5.3.3.3**: 12개월 데이터 조회
- **SubTask 5.3.3.4**: 전년 대비 증감률 계산

### Task 5.3.4: 연별 통계 API

- **SubTask 5.3.4.1**: GET /api/v1/statistics/yearly
- **SubTask 5.3.4.2**: YearlyStatisticsResponse DTO
- **SubTask 5.3.4.3**: 누적 발전량 계산
- **SubTask 5.3.4.4**: 목표 달성률 계산

---

## Story 5.4: 분석 및 리포트 API

**목표**: 고급 분석 및 예측 데이터 제공

### Task 5.4.1: 효율 분석 API

- **SubTask 5.4.1.1**: GET /api/v1/analytics/efficiency
- **SubTask 5.4.1.2**: 일사량 대비 실제 발전량 분석
- **SubTask 5.4.1.3**: 시간대별 효율 패턴 분석
- **SubTask 5.4.1.4**: 비효율 원인 추정 (온도, 먼지 등)

### Task 5.4.2: 기간 비교 API

- **SubTask 5.4.2.1**: GET /api/v1/analytics/comparison
    - Query Params: period1, period2
- **SubTask 5.4.2.2**: 두 기간 통계 비교
- **SubTask 5.4.2.3**: 증감률 및 차이 계산
- **SubTask 5.4.2.4**: 시각화 데이터 포맷

### Task 5.4.3: 발전량 예측 API (선택사항)

- **SubTask 5.4.3.1**: GET /api/v1/analytics/forecast
- **SubTask 5.4.3.2**: 날씨 예보 API 통합
- **SubTask 5.4.3.3**: 과거 데이터 기반 예측 모델
    - 이동 평균 또는 선형 회귀
- **SubTask 5.4.3.4**: 예측 신뢰도 표시

### Task 5.4.4: 데이터 내보내기 API

- **SubTask 5.4.4.1**: GET /api/v1/export/csv
- **SubTask 5.4.4.2**: GET /api/v1/export/json
- **SubTask 5.4.4.3**: 날짜 범위 및 필드 선택
- **SubTask 5.4.4.4**: 파일 다운로드 응답 (Content-Disposition)

---

## Story 5.5: 시스템 상태 API

**목표**: 시스템 및 센서 상태 조회

### Task 5.5.1: 전체 시스템 상태 API

- **SubTask 5.5.1.1**: GET /api/v1/system/status
- **SubTask 5.5.1.2**: SystemStatusResponse DTO
    - online, lastCommunication, sensorStatus[]
- **SubTask 5.5.1.3**: 센서별 상태 체크
- **SubTask 5.5.1.4**: 전반적인 시스템 건강도 점수

### Task 5.5.2: 알림 목록 API

- **SubTask 5.5.2.1**: GET /api/v1/alerts
    - Query Params: page, size, severity
- **SubTask 5.5.2.2**: AlertResponse DTO
    - id, type, severity, message, timestamp, isRead
- **SubTask 5.5.2.3**: 페이지네이션
- **SubTask 5.5.2.4**: 필터링 (읽음/안읽음, 심각도)

### Task 5.5.3: 알림 상태 업데이트 API

- **SubTask 5.5.3.1**: PATCH /api/v1/alerts/{id}/read
- **SubTask 5.5.3.2**: DELETE /api/v1/alerts/{id}
- **SubTask 5.5.3.3**: POST /api/v1/alerts/mark-all-read
- **SubTask 5.5.3.4**: 권한 체크 (사용자별)

### Task 5.5.4: 헬스체크 API

- **SubTask 5.5.4.1**: GET /api/v1/system/health
- **SubTask 5.5.4.2**: Spring Boot Actuator 통합
- **SubTask 5.5.4.3**: 데이터베이스 연결 상태
- **SubTask 5.5.4.4**: 디스크 사용량, 메모리 상태

---

## Story 5.6: API 문서화 및 테스트

**목표**: API 사용성 향상

### Task 5.6.1: Swagger/OpenAPI 문서화

- **SubTask 5.6.1.1**: Springdoc OpenAPI 의존성 추가
- **SubTask 5.6.1.2**: API 설명 어노테이션 추가
    
    ```java
    @Operation(summary = "현재 발전량 조회")@ApiResponses({...})
    
    ```
    
- **SubTask 5.6.1.3**: DTO 스키마 문서화
- **SubTask 5.6.1.4**: Swagger UI 설정 및 커스터마이징

### Task 5.6.2: Postman Collection

- **SubTask 5.6.2.1**: API 테스트용 Postman Collection 작성
- **SubTask 5.6.2.2**: 환경 변수 설정 (dev, prod)
- **SubTask 5.6.2.3**: 샘플 요청/응답 추가
- **SubTask 5.6.2.4**: Collection 공유 (팀원)

### Task 5.6.3: API 통합 테스트

- **SubTask 5.6.3.1**: MockMvc 테스트 작성
- **SubTask 5.6.3.2**: 각 엔드포인트별 성공/실패 케이스
- **SubTask 5.6.3.3**: 데이터 검증 테스트
- **SubTask 5.6.3.4**: 성능 테스트 (응답 시간)

---

## 산출물

- [ ]  API 명세서 (Swagger UI)
- [ ]  Postman Collection
- [ ]  API 통합 테스트 코드
- [ ]  API 사용 가이드 문서
- [ ]  응답 시간 성능 리포트
- [ ]  WebSocket 연결 가이드

---

## 다음 에픽으로 이동 조건

- [ ]  모든 주요 API 엔드포인트 구현 완료
- [ ]  Swagger 문서화 100% 완료
- [ ]  API 테스트 커버리지 80% 이상
- [ ]  WebSocket 실시간 통신 정상 작동
- [ ]  응답 시간 평균 100ms 이하
- [ ]  프론트엔드 연동 테스트 완료