# Epic 3: 백엔드 API 개발

*센서 데이터를 받아 저장하고 처리하는 백엔드 시스템*

## Story 3.1: 백엔드 프로젝트 초기 설정

**목표**: Spring Boot 기반 프로젝트 구조 및 개발 환경 구축

### Task 3.1.1: 프로젝트 생성 및 의존성 설정

- **SubTask 3.1.1.1**: Spring Initializr로 프로젝트 생성
    - Spring Boot 3.x, Java 17+
    - Dependencies: Web, JPA, PostgreSQL, WebSocket, Validation
- **SubTask 3.1.1.2**: Gradle 또는 Maven 설정 파일 구성
- **SubTask 3.1.1.3**: application.yml 환경 설정 (dev, prod)
- **SubTask 3.1.1.4**: Git 저장소 초기화 및 .gitignore 설정

### Task 3.1.2: 프로젝트 구조 설계

- **SubTask 3.1.2.1**: 패키지 구조 설계 (도메인 기반)
    - /domain/sensor, /domain/power, /domain/alert 등
- **SubTask 3.1.2.2**: 레이어 분리 (controller, service, repository)
- **SubTask 3.1.2.3**: 공통 설정 클래스 작성 (Config)
- **SubTask 3.1.2.4**: 예외 처리 전략 수립

### Task 3.1.3: 데이터베이스 설정

- **SubTask 3.1.3.1**: PostgreSQL Docker 컨테이너 설정
- **SubTask 3.1.3.2**: 데이터베이스 스키마 초기화 스크립트
- **SubTask 3.1.3.3**: JPA/Hibernate 설정
- **SubTask 3.1.3.4**: 마이그레이션 도구 설정 (Flyway 또는 Liquibase)

---

## Story 3.2: 도메인 모델 설계 및 구현

**목표**: 핵심 엔티티 및 비즈니스 로직 모델링

### Task 3.2.1: SensorReading 엔티티 설계

- **SubTask 3.2.1.1**: 엔티티 클래스 작성
    
    ```java
    @Entityclass SensorReading {  Long id;  LocalDateTime timestamp;  Double voltage;  Double current;  Double power;  Double temperature;  Double humidity;  Double illuminance;}
    
    ```
    
- **SubTask 3.2.1.2**: 인덱스 전략 (timestamp, 복합 인덱스)
- **SubTask 3.2.1.3**: 파티셔닝 전략 (월별 또는 일별)
- **SubTask 3.2.1.4**: Repository 인터페이스 작성

### Task 3.2.2: PowerGeneration 집계 모델

- **SubTask 3.2.2.1**: 시간별/일별/월별 집계 엔티티
- **SubTask 3.2.2.2**: 피크/평균/최소 전력 필드
- **SubTask 3.2.2.3**: 총 발전량 (kWh) 계산 필드
- **SubTask 3.2.2.4**: 집계 Repository 및 쿼리 메서드

### Task 3.2.3: BatteryStatus 모델

- **SubTask 3.2.3.1**: 배터리 상태 엔티티 설계
    - 전압, 전류, SOC(%), 온도, 건강도
- **SubTask 3.2.3.2**: 충전/방전 상태 enum
- **SubTask 3.2.3.3**: 이력 관리 (상태 변경 로그)
- **SubTask 3.2.3.4**: Repository 구현

### Task 3.2.4: SystemStatus 모델

- **SubTask 3.2.4.1**: 시스템 상태 엔티티
    - 온라인/오프라인, 마지막 통신 시간
- **SubTask 3.2.4.2**: 센서 상태 체크 필드
- **SubTask 3.2.4.3**: 에러 카운터 및 경고 플래그
- **SubTask 3.2.4.4**: 단일 레코드 관리 (싱글톤 패턴)

### Task 3.2.5: Alert 알림 모델

- **SubTask 3.2.5.1**: 알림 엔티티 설계
    - 타입, 심각도, 메시지, 발생 시간
- **SubTask 3.2.5.2**: 알림 상태 (New, Read, Acknowledged)
- **SubTask 3.2.5.3**: 알림 규칙 엔티티 (AlertRule)
- **SubTask 3.2.5.4**: Repository 및 쿼리 메서드

---

## Story 3.3: 데이터 수신 API 구현

**목표**: 아두이노에서 전송한 센서 데이터 수신

### Task 3.3.1: REST API 엔드포인트 개발

- **SubTask 3.3.1.1**: POST /api/v1/sensors/data 구현
    - Request DTO 정의 (SensorDataRequest)
    - 검증 로직 (@Valid, 범위 체크)
- **SubTask 3.3.1.2**: POST /api/v1/sensors/batch 배치 수신
- **SubTask 3.3.1.3**: 에러 응답 표준화 (RFC 7807 Problem Details)
- **SubTask 3.3.1.4**: API 문서화 (Swagger/OpenAPI)

### Task 3.3.2: 데이터 검증 및 변환

- **SubTask 3.3.2.1**: DTO to Entity 매핑 (ModelMapper 또는 MapStruct)
- **SubTask 3.3.2.2**: 데이터 범위 검증 (min/max)
- **SubTask 3.3.2.3**: 타임스탬프 처리 (UTC vs 로컬 시간)
- **SubTask 3.3.2.4**: 중복 데이터 감지 및 필터링

### Task 3.3.3: 데이터 저장 서비스

- **SubTask 3.3.3.1**: SensorDataService 구현
    - save(), saveBatch() 메서드
- **SubTask 3.3.3.2**: 트랜잭션 관리 (@Transactional)
- **SubTask 3.3.3.3**: 배치 저장 최적화 (JDBC Batch Insert)
- **SubTask 3.3.3.4**: 저장 실패 시 재시도 로직

### Task 3.3.4: API 인증 및 보안

- **SubTask 3.3.4.1**: API Key 기반 인증 구현
- **SubTask 3.3.4.2**: Rate Limiting (API 호출 제한)
- **SubTask 3.3.3**: CORS 설정
- **SubTask 3.3.4.4**: HTTPS 설정 (프로덕션 환경)

---

## Story 3.4: 실시간 데이터 처리 파이프라인

**목표**: 원시 데이터를 의미있는 정보로 변환

### Task 3.4.1: 데이터 집계 서비스 구현

- **SubTask 3.4.1.1**: AggregationService 클래스 작성
- **SubTask 3.4.1.2**: 1분 단위 평균 계산 (스케줄러)
    
    ```java
    @Scheduled(fixedRate = 60000)void aggregateMinuteData()
    
    ```
    
- **SubTask 3.4.1.3**: 시간별 집계 (매 시 정각)
- **SubTask 3.4.1.4**: 일별 집계 (자정 실행)

### Task 3.4.2: 실시간 계산 로직

- **SubTask 3.4.2.1**: 전력(W) → 에너지(Wh) 변환
    - 적분 계산 (사다리꼴 규칙)
- **SubTask 3.4.2.2**: 발전 효율 계산
    - 실제 출력 / 이론 출력 (일사량 기반)
- **SubTask 3.4.2.3**: 자가소비율 계산
    - (생산량 - 수출량) / 생산량
- **SubTask 3.4.2.4**: 예상 수익 계산
    - 발전량 × 전력 단가

### Task 3.4.3: 이벤트 기반 처리

- **SubTask 3.4.3.1**: Spring Events 설정
- **SubTask 3.4.3.2**: SensorDataReceivedEvent 발행
- **SubTask 3.4.3.3**: AggregationCompletedEvent 발행
- **SubTask 3.4.3.4**: AlertTriggeredEvent 발행

### Task 3.4.4: 비동기 처리

- **SubTask 3.4.4.1**: @Async 설정 및 ThreadPoolExecutor
- **SubTask 3.4.4.2**: 집계 작업 비동기 실행
- **SubTask 3.4.4.3**: CompletableFuture 활용
- **SubTask 3.4.4.4**: 에러 핸들링 및 로깅

---

## Story 3.5: 데이터 보관 정책 및 최적화

**목표**: 데이터베이스 성능 및 용량 관리

### Task 3.5.1: 데이터 라이프사이클 정책

- **SubTask 3.5.1.1**: 원시 데이터 30일 보관
- **SubTask 3.5.1.2**: 집계 데이터 영구 보관
- **SubTask 3.5.1.3**: 오래된 데이터 아카이빙 (S3 등)
- **SubTask 3.5.1.4**: 자동 삭제 스케줄러 구현

### Task 3.5.2: 쿼리 최적화

- **SubTask 3.5.2.1**: 인덱스 추가 (자주 조회되는 컬럼)
- **SubTask 3.5.2.2**: 복합 인덱스 설계
- **SubTask 3.5.2.3**: 쿼리 실행 계획 분석 (EXPLAIN)
- **SubTask 3.5.2.4**: N+1 문제 해결 (fetch join)

### Task 3.5.3: 파티셔닝 전략

- **SubTask 3.5.3.1**: timestamp 기준 파티셔닝
- **SubTask 3.5.3.2**: 월별 파티션 자동 생성
- **SubTask 3.5.3.3**: 파티션 프루닝 확인
- **SubTask 3.5.3.4**: 파티션 유지보수 스크립트

### Task 3.5.4: 캐싱 전략

- **SubTask 3.5.4.1**: Spring Cache 추상화 설정
- **SubTask 3.5.4.2**: 최신 데이터 캐싱 (Redis)
- **SubTask 3.5.4.3**: 집계 데이터 캐싱
- **SubTask 3.5.4.4**: 캐시 무효화 전략

---

## 산출물

- [ ]  Spring Boot 프로젝트 (GitHub)
- [ ]  ERD (Entity Relationship Diagram)
- [ ]  API 명세서 (Swagger UI)
- [ ]  데이터베이스 마이그레이션 스크립트
- [ ]  단위 테스트 (JUnit 5)
- [ ]  통합 테스트 (TestContainers)
- [ ]  성능 테스트 결과 보고서
- [ ]  데이터 보관 정책 문서

---

## 다음 에픽으로 이동 조건

- [ ]  센서 데이터 수신 API 정상 작동
- [ ]  데이터베이스 저장 성공률 99% 이상
- [ ]  실시간 집계 정확도 검증 완료
- [ ]  API 문서화 완료
- [ ]  단위 테스트 커버리지 80% 이상
- [ ]  부하 테스트 통과 (초당 100 요청)