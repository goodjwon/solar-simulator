# Epic 6: 알림 시스템 및 모니터링

*이상 징후 감지 및 알림*

## Story 6.1: 알림 규칙 엔진 구축

**목표**: 설정 가능한 알림 조건 및 자동 감지

### Task 6.1.1: 알림 규칙 도메인 모델

- **SubTask 6.1.1.1**: AlertRule 엔티티 설계
    
    ```java
    @Entityclass AlertRule {  Long id;  String name;  RuleType type; // THRESHOLD, RATE_CHANGE, STATE_CHANGE  String targetMetric; // "battery.temperature", "power.output"  String condition; // ">", "<", "==", "!=", "DELTA"  Double threshold;  Severity severity; // INFO, WARNING, ERROR, CRITICAL  Boolean enabled;  List<NotificationChannel> channels;}
    
    ```
    
- **SubTask 6.1.1.2**: RuleType enum 정의
- **SubTask 6.1.1.3**: Severity enum 정의
- **SubTask 6.1.1.4**: NotificationChannel enum 정의

### Task 6.1.2: 규칙 평가 엔진

- **SubTask 6.1.2.1**: RuleEvaluationService 클래스 작성
- **SubTask 6.1.2.2**: 실시간 데이터 모니터링
    
    ```java
    @EventListenervoid onSensorDataReceived(SensorDataReceivedEvent event)
    
    ```
    
- **SubTask 6.1.2.3**: 규칙 조건 평가 로직
    - 임계값 비교 (threshold)
    - 변화율 계산 (rate of change)
    - 상태 변경 감지 (state transition)
- **SubTask 6.1.2.4**: 규칙 매칭 알고리즘 최적화

### Task 6.1.3: 중복 알림 방지

- **SubTask 6.1.3.1**: 쿨다운 기간 설정 (5분/10분/30분)
- **SubTask 6.1.3.2**: 알림 이력 추적 (AlertHistory 엔티티)
- **SubTask 6.1.3.3**: 동일 조건 중복 체크
- **SubTask 6.1.3.4**: 알림 그룹핑 (같은 타입 묶기)

### Task 6.1.4: 기본 알림 규칙 구현

- **SubTask 6.1.4.1**: 배터리 고온 경고 (> 50℃)
- **SubTask 6.1.4.2**: 저발전량 알림 (일사량 대비 < 70%)
- **SubTask 6.1.4.3**: 시스템 오프라인 감지 (5분 무응답)
- **SubTask 6.1.4.4**: 배터리 과충전/과방전 경고
    - 과충전: SOC > 95%, 전류 > 0
    - 과방전: SOC < 10%

---

## Story 6.2: 알림 전달 시스템

**목표**: 다양한 채널로 알림 전송

### Task 6.2.1: 이메일 알림

- **SubTask 6.2.1.1**: Spring Mail 의존성 추가 및 설정
    
    ```yaml
    spring:  mail:    host: smtp.gmail.com    port: 587    username: ${EMAIL_USERNAME}    password: ${EMAIL_PASSWORD}
    
    ```
    
- **SubTask 6.2.1.2**: EmailNotificationService 구현
- **SubTask 6.2.1.3**: HTML 이메일 템플릿 작성 (Thymeleaf)
    - 알림 타입별 템플릿
    - 로고, 헤더, 본문, 액션 버튼
- **SubTask 6.2.1.4**: 수신자 목록 관리

### Task 6.2.2: 비동기 전송 큐

- **SubTask 6.2.2.1**: @Async 설정 및 ThreadPoolTaskExecutor
- **SubTask 6.2.2.2**: 알림 전송 큐 구현
- **SubTask 6.2.2.3**: 전송 실패 재시도 로직 (최대 3회)
- **SubTask 6.2.2.4**: 전송 상태 추적 (Pending, Sent, Failed)

### Task 6.2.3: 푸시 알림 (선택사항)

- **SubTask 6.2.3.1**: Firebase Cloud Messaging 프로젝트 설정
- **SubTask 6.2.3.2**: FCM Admin SDK 통합
- **SubTask 6.2.3.3**: 디바이스 토큰 관리 (UserDevice 엔티티)
- **SubTask 6.2.3.4**: 푸시 알림 페이로드 구성
    
    ```java
    Message.builder()  .setNotification(Notification.builder()    .setTitle("배터리 고온 경고")    .setBody("현재 온도: 52℃")    .build())  .setToken(deviceToken)  .build()
    
    ```
    

### Task 6.2.4: 대시보드 알림

- **SubTask 6.2.4.1**: WebSocket을 통한 실시간 푸시
    - /topic/alerts 채널로 발행
- **SubTask 6.2.4.2**: 브라우저 Notification API 연동
- **SubTask 6.2.4.3**: 알림 배지 카운터 업데이트
- **SubTask 6.2.4.4**: 알림 음향 효과 (선택사항)

---

## Story 6.3: 알림 관리 기능

**목표**: 사용자가 알림을 관리할 수 있는 기능

### Task 6.3.1: 알림 규칙 CRUD API

- **SubTask 6.3.1.1**: POST /api/v1/alert-rules - 규칙 생성
- **SubTask 6.3.1.2**: GET /api/v1/alert-rules - 규칙 목록 조회
- **SubTask 6.3.1.3**: PUT /api/v1/alert-rules/{id} - 규칙 수정
- **SubTask 6.3.1.4**: DELETE /api/v1/alert-rules/{id} - 규칙 삭제

### Task 6.3.2: 규칙 활성화/비활성화

- **SubTask 6.3.2.1**: PATCH /api/v1/alert-rules/{id}/toggle
- **SubTask 6.3.2.2**: 비활성화된 규칙 평가 스킵
- **SubTask 6.3.2.3**: 일괄 활성화/비활성화 기능
- **SubTask 6.3.2.4**: 스케줄 기반 자동 토글 (야간 음소거)

### Task 6.3.3: 알림 우선순위 및 그룹핑

- **SubTask 6.3.3.1**: 알림 우선순위 설정 (High, Medium, Low)
- **SubTask 6.3.3.2**: 관련 알림 그룹핑 (배터리 관련, 전력 관련)
- **SubTask 6.3.3.3**: 우선순위 기반 정렬
- **SubTask 6.3.3.4**: 중요 알림 강조 표시

### Task 6.3.4: 알림 통계 및 리포트

- **SubTask 6.3.4.1**: GET /api/v1/alerts/statistics
    - 기간별 알림 발생 횟수
    - 타입별 분포
    - 해결 시간 평균
- **SubTask 6.3.4.2**: 알림 트렌드 분석
- **SubTask 6.3.4.3**: 주간/월간 알림 리포트 생성
- **SubTask 6.3.4.4**: 이메일 리포트 자동 발송

---

## Story 6.4: 시스템 모니터링 및 진단

**목표**: 시스템 건강도 모니터링

### Task 6.4.1: 헬스 체크 서비스

- **SubTask 6.4.1.1**: HealthCheckService 구현
- **SubTask 6.4.1.2**: 센서 응답 시간 모니터링
- **SubTask 6.4.1.3**: 데이터베이스 연결 상태 체크
- **SubTask 6.4.1.4**: 외부 API 연결 상태 체크

### Task 6.4.2: 자동 진단 기능

- **SubTask 6.4.2.1**: 센서 데이터 이상 패턴 감지
    - 급격한 변화
    - 지속적인 0값
    - 범위 초과
- **SubTask 6.4.2.2**: 네트워크 지연 감지
- **SubTask 6.4.2.3**: 메모리 및 CPU 사용률 모니터링
- **SubTask 6.4.2.4**: 진단 결과 로그 및 알림

### Task 6.4.3: 성능 메트릭 수집

- **SubTask 6.4.3.1**: Micrometer 메트릭 설정
- **SubTask 6.4.3.2**: 커스텀 메트릭 정의
    - 센서 데이터 수신률
    - API 응답 시간
    - WebSocket 연결 수
- **SubTask 6.4.3.3**: Prometheus 통합 (선택사항)
- **SubTask 6.4.3.4**: Grafana 대시보드 구성 (선택사항)

### Task 6.4.4: 로그 집계 및 분석

- **SubTask 6.4.4.1**: Logback 설정 및 로그 레벨 관리
- **SubTask 6.4.4.2**: 구조화된 로그 포맷 (JSON)
- **SubTask 6.4.4.3**: 에러 로그 자동 알림
- **SubTask 6.4.4.4**: 로그 파일 로테이션 및 보관 정책

---

## Story 6.5: 알림 프론트엔드 연동

**목표**: 대시보드에서 알림 관리

### Task 6.5.1: 알림 규칙 설정 UI

- **SubTask 6.5.1.1**: AlertRuleForm 컴포넌트
    - 규칙 이름, 조건, 임계값 입력
- **SubTask 6.5.1.2**: 조건 빌더 UI (드롭다운, 숫자 입력)
- **SubTask 6.5.1.3**: 알림 채널 선택 (체크박스)
- **SubTask 6.5.1.4**: 규칙 테스트 기능 (미리보기)

### Task 6.5.2: 알림 목록 및 상세

- **SubTask 6.5.2.1**: AlertList 컴포넌트
- **SubTask 6.5.2.2**: 알림 타입별 필터링
- **SubTask 6.5.2.3**: 읽음/안읽음 토글
- **SubTask 6.5.2.4**: 알림 상세 모달

### Task 6.5.3: 실시간 알림 토스트

- **SubTask 6.5.3.1**: react-toastify 통합
- **SubTask 6.5.3.2**: WebSocket 알림 수신 시 토스트 표시
- **SubTask 6.5.3.3**: 심각도별 색상 및 아이콘
- **SubTask 6.5.3.4**: 토스트 클릭 시 상세 페이지 이동

### Task 6.5.4: 알림 설정 페이지

- **SubTask 6.5.4.1**: NotificationSettings 컴포넌트
- **SubTask 6.5.4.2**: 이메일 알림 ON/OFF 토글
- **SubTask 6.5.4.3**: 푸시 알림 권한 요청 버튼
- **SubTask 6.5.4.4**: 음소거 시간대 설정 (시작-종료 시간)

---

## 산출물

- [ ]  AlertRule 엔티티 및 Repository
- [ ]  알림 규칙 평가 엔진
- [ ]  이메일 템플릿 (HTML)
- [ ]  알림 관리 API 명세서
- [ ]  알림 프론트엔드 컴포넌트
- [ ]  알림 테스트 시나리오 문서
- [ ]  모니터링 대시보드 (Grafana, 선택사항)

---

## 다음 에픽으로 이동 조건

- [ ]  기본 알림 규칙 4개 이상 구현
- [ ]  이메일 알림 정상 발송
- [ ]  WebSocket 실시간 알림 작동
- [ ]  알림 규칙 CRUD API 완성
- [ ]  중복 알림 방지 로직 테스트 통과
- [ ]  프론트엔드 알림 UI 구현 완료