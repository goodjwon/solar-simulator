# Epic 9: 테스트 및 품질 보증

*안정성 확보 및 버그 방지*

## Story 9.1: 백엔드 단위 테스트

**목표**: 비즈니스 로직 검증

### Task 9.1.1: 테스트 환경 설정

- **SubTask 9.1.1.1**: JUnit 5 설정 및 의존성
- **SubTask 9.1.1.2**: Mockito 설정
- **SubTask 9.1.1.3**: AssertJ 또는 Hamcrest 추가
- **SubTask 9.1.1.4**: 테스트 프로파일 설정 (application-test.yml)

### Task 9.1.2: Service 레이어 테스트

- **SubTask 9.1.2.1**: SensorDataService 테스트
    
    ```java
    @ExtendWith(MockitoExtension.class)class SensorDataServiceTest {  @Mock  SensorDataRepository repository;    @InjectMocks  SensorDataService service;    @Test  void shouldSaveSensorData() {    // given    SensorData data = createTestData();    when(repository.save(any())).thenReturn(data);        // when    SensorData result = service.save(data);        // then    assertThat(result).isNotNull();    verify(repository, times(1)).save(any());  }}
    
    ```
    
- **SubTask 9.1.2.2**: PowerGenerationService 테스트
- **SubTask 9.1.2.3**: AlertService 테스트
- **SubTask 9.1.2.4**: 예외 상황 테스트

### Task 9.1.3: Repository 테스트

- **SubTask 9.1.3.1**: @DataJpaTest 활용
- **SubTask 9.1.3.2**: 커스텀 쿼리 메서드 테스트
- **SubTask 9.1.3.3**: 페이지네이션 테스트
- **SubTask 9.1.3.4**: 인메모리 DB (H2) 사용

### Task 9.1.4: 테스트 커버리지

- **SubTask 9.1.4.1**: JaCoCo 플러그인 설정
- **SubTask 9.1.4.2**: 커버리지 80% 목표 설정
- **SubTask 9.1.4.3**: 커버리지 리포트 생성
- **SubTask 9.1.4.4**: 커버리지 부족 부분 파악 및 개선

---

## Story 9.2: 백엔드 통합 테스트

**목표**: API 엔드포인트 및 전체 플로우 검증

### Task 9.2.1: API 통합 테스트

- **SubTask 9.2.1.1**: @SpringBootTest 및 MockMvc 설정
- **SubTask 9.2.1.2**: 센서 데이터 수신 API 테스트
    
    ```java
    @SpringBootTest@AutoConfigureMockMvcclass SensorApiTest {  @Autowired  MockMvc mockMvc;    @Test  void shouldReceiveSensorData() throws Exception {    mockMvc.perform(post("/api/v1/sensors/data")        .contentType(MediaType.APPLICATION_JSON)        .content("{\"voltage\": 12.5, \"current\": 2.0}"))      .andExpect(status().isOk())      .andExpect(jsonPath("$.success").value(true));  }}
    
    ```
    
- **SubTask 9.2.1.3**: 통계 조회 API 테스트
- **SubTask 9.2.1.4**: 인증 API 테스트

### Task 9.2.2: 데이터베이스 통합 테스트

- **SubTask 9.2.2.1**: TestContainers 설정 (PostgreSQL)
    
    ```java
    @Containerstatic PostgreSQLContainer<?> postgres =   new PostgreSQLContainer<>("postgres:15");
    
    ```
    
- **SubTask 9.2.2.2**: 트랜잭션 롤백 테스트
- **SubTask 9.2.2.3**: 집계 쿼리 성능 테스트
- **SubTask 9.2.2.4**: 동시성 테스트

### Task 9.2.3: WebSocket 연결 테스트

- **SubTask 9.2.3.1**: STOMP 클라이언트 테스트
- **SubTask 9.2.3.2**: 메시지 수신 검증
- **SubTask 9.2.3.3**: 연결/해제 시나리오 테스트
- **SubTask 9.2.3.4**: 재연결 로직 테스트

### Task 9.2.4: E2E 시나리오 테스트

- **SubTask 9.2.4.1**: 데이터 수신 → 저장 → 조회 플로우
- **SubTask 9.2.4.2**: 알림 규칙 평가 → 알림 발송 플로우
- **SubTask 9.2.4.3**: 사용자 회원가입 → 로그인 → 설정 변경 플로우
- **SubTask 9.2.4.4**: 엣지 케이스 및 오류 상황 테스트

---

## Story 9.3: 프론트엔드 컴포넌트 테스트

**목표**: UI 컴포넌트 동작 검증

### Task 9.3.1: React Testing Library 설정

- **SubTask 9.3.1.1**: Jest 및 RTL 설정
    
    ```json
    "scripts": {  "test": "jest --watch",  "test:coverage": "jest --coverage"}
    
    ```
    
- **SubTask 9.3.1.2**: 테스트 유틸리티 함수 작성
- **SubTask 9.3.1.3**: Mock 데이터 생성 함수
- **SubTask 9.3.1.4**: 커스텀 렌더 함수 (Provider 포함)

### Task 9.3.2: 공통 컴포넌트 테스트

- **SubTask 9.3.2.1**: Card 컴포넌트 테스트
    
    ```tsx
    describe('Card', () => {  it('renders title and content', () => {    render(<Card title="Test">Content</Card>);    expect(screen.getByText('Test')).toBeInTheDocument();    expect(screen.getByText('Content')).toBeInTheDocument();  });});
    
    ```
    
- **SubTask 9.3.2.2**: Button 컴포넌트 클릭 이벤트 테스트
- **SubTask 9.3.2.3**: Input 컴포넌트 값 변경 테스트
- **SubTask 9.3.2.4**: Chart 컴포넌트 렌더링 테스트

### Task 9.3.3: 페이지 컴포넌트 테스트

- **SubTask 9.3.3.1**: Dashboard 페이지 테스트
- **SubTask 9.3.3.2**: Statistics 페이지 테스트
- **SubTask 9.3.3.3**: Settings 페이지 폼 제출 테스트
- **SubTask 9.3.3.4**: 로딩/에러 상태 테스트

### Task 9.3.4: API 모킹

- **SubTask 9.3.4.1**: MSW (Mock Service Worker) 설정
    
    ```tsx
    const handlers = [  rest.get('/api/v1/power/current', (req, res, ctx) => {    return res(ctx.json({ currentPower: 1500 }));  }),];
    
    ```
    
- **SubTask 9.3.4.2**: 성공/실패 응답 모킹
- **SubTask 9.3.4.3**: 네트워크 지연 시뮬레이션
- **SubTask 9.3.4.4**: 에러 상황 모킹

---

## Story 9.4: E2E 테스트 (선택사항)

**목표**: 사용자 관점의 전체 플로우 테스트

### Task 9.4.1: Playwright 설정

- **SubTask 9.4.1.1**: Playwright 설치 및 설정
    
    ```bash
    npm init playwright@latest
    
    ```
    
- **SubTask 9.4.1.2**: 브라우저 설정 (Chromium, Firefox, WebKit)
- **SubTask 9.4.1.3**: 테스트 환경 URL 설정
- **SubTask 9.4.1.4**: 스크린샷 및 비디오 녹화 설정

### Task 9.4.2: 주요 사용자 플로우 테스트

- **SubTask 9.4.2.1**: 로그인 플로우
    
    ```tsx
    test('user can login', async ({ page }) => {  await page.goto('/login');  await page.fill('[name="email"]', 'user@example.com');  await page.fill('[name="password"]', 'password');  await page.click('button[type="submit"]');  await expect(page).toHaveURL('/dashboard');});
    
    ```
    
- **SubTask 9.4.2.2**: 대시보드 데이터 조회 플로우
- **SubTask 9.4.2.3**: 설정 변경 플로우
- **SubTask 9.4.2.4**: 알림 규칙 생성 플로우

### Task 9.4.3: 시각적 회귀 테스트

- **SubTask 9.4.3.1**: 스크린샷 비교 설정
    
    ```tsx
    test('dashboard visual regression', async ({ page }) => {  await page.goto('/dashboard');  await expect(page).toHaveScreenshot('dashboard.png');});
    
    ```
    
- **SubTask 9.4.3.2**: 반응형 화면 테스트 (모바일, 태블릿, 데스크톱)
- **SubTask 9.4.3.3**: 다크/라이트 모드 스크린샷
- **SubTask 9.4.3.4**: 차이 발견 시 알림

### Task 9.4.4: 크로스 브라우저 테스트

- **SubTask 9.4.4.1**: Chrome, Firefox, Safari 테스트
- **SubTask 9.4.4.2**: 브라우저별 호환성 이슈 파악
- **SubTask 9.4.4.3**: 모바일 브라우저 테스트
- **SubTask 9.4.4.4**: 브라우저 테스트 매트릭스 문서화

---

## Story 9.5: 성능 테스트

**목표**: 부하 및 스트레스 테스트

### Task 9.5.1: API 부하 테스트

- **SubTask 9.5.1.1**: JMeter 또는 k6 설정
    
    ```jsx
    import http from 'k6/http';import { check } from 'k6';export let options = {  vus: 100,  duration: '30s',};export default function() {  let res = http.get('http://localhost:8080/api/v1/power/current');  check(res, { 'status is 200': (r) => r.status === 200 });}
    
    ```
    
- **SubTask 9.5.1.2**: 센서 데이터 수신 API 부하 테스트 (초당 100 요청)
- **SubTask 9.5.1.3**: 조회 API 부하 테스트
- **SubTask 9.5.1.4**: 응답 시간 및 처리량 측정

### Task 9.5.2: 데이터베이스 성능 테스트

- **SubTask 9.5.2.1**: 대용량 데이터 삽입 테스트 (100만 건)
- **SubTask 9.5.2.2**: 복잡한 집계 쿼리 성능 측정
- **SubTask 9.5.2.3**: 인덱스 효과 검증
- **SubTask 9.5.2.4**: 쿼리 실행 계획 분석 및 최적화

### Task 9.5.3: 프론트엔드 성능 측정

- **SubTask 9.5.3.1**: Lighthouse 성능 점수 측정
    - Performance, Accessibility, Best Practices, SEO
- **SubTask 9.5.3.2**: Core Web Vitals 측정
    - LCP (Largest Contentful Paint)
    - FID (First Input Delay)
    - CLS (Cumulative Layout Shift)
- **SubTask 9.5.3.3**: 번들 크기 분석 (webpack-bundle-analyzer)
- **SubTask 9.5.3.4**: 성능 개선 및 재측정

### Task 9.5.4: WebSocket 스트레스 테스트

- **SubTask 9.5.4.1**: 동시 WebSocket 연결 테스트 (1000개)
- **SubTask 9.5.4.2**: 메시지 처리량 테스트
- **SubTask 9.5.4.3**: 연결 안정성 장시간 테스트
- **SubTask 9.5.4.4**: 메모리 누수 확인

---

## Story 9.6: 보안 테스트

**목표**: 취약점 발견 및 수정

### Task 9.6.1: OWASP Top 10 점검

- **SubTask 9.6.1.1**: SQL Injection 테스트
    - Prepared Statement 사용 확인
- **SubTask 9.6.1.2**: XSS (Cross-Site Scripting) 테스트
    - 입력값 이스케이프 확인
- **SubTask 9.6.1.3**: CSRF (Cross-Site Request Forgery) 방어 확인
- **SubTask 9.6.1.4**: 인증/인가 우회 시도

### Task 9.6.2: 의존성 취약점 스캔

- **SubTask 9.6.2.1**: npm audit (프론트엔드)
- **SubTask 9.6.2.2**: OWASP Dependency Check (백엔드)
- **SubTask 9.6.2.3**: 취약한 라이브러리 업데이트
- **SubTask 9.6.2.4**: Dependabot 알림 설정

### Task 9.6.3: 컨테이너 이미지 스캔

- **SubTask 9.6.3.1**: Trivy로 Docker 이미지 스캔
    
    ```bash
    trivy image solar-monitor-backend:latest
    
    ```
    
- **SubTask 9.6.3.2**: 고위험 취약점 수정
- **SubTask 9.6.3.3**: 베이스 이미지 최신화
- **SubTask 9.6.3.4**: 스캔 결과 리포트

### Task 9.6.4: 침투 테스트 (선택사항)

- **SubTask 9.6.4.1**: OWASP ZAP 자동 스캔
- **SubTask 9.6.4.2**: 수동 침투 테스트 시나리오
- **SubTask 9.6.4.3**: 발견된 취약점 문서화
- **SubTask 9.6.4.4**: 보안 패치 적용

---

## Story 9.7: 코드 품질 관리

**목표**: 코드 리뷰 및 정적 분석

### Task 9.7.1: 정적 분석 도구

- **SubTask 9.7.1.1**: SonarQube 설정 (백엔드)
    - 코드 스멜, 버그, 취약점 검출
- **SubTask 9.7.1.2**: ESLint 규칙 강화 (프론트엔드)
- **SubTask 9.7.1.3**: Prettier 자동 포맷팅
- **SubTask 9.7.1.4**: Pre-commit Hook 설정 (Husky)

### Task 9.7.2: 코드 리뷰 프로세스

- **SubTask 9.7.2.1**: Pull Request 템플릿 작성
    - 변경 사항 요약
    - 테스트 체크리스트
    - 스크린샷 (UI 변경 시)
- **SubTask 9.7.2.2**: 리뷰 가이드라인 문서화
- **SubTask 9.7.2.3**: 최소 1명 승인 필수 규칙
- **SubTask 9.7.2.4**: 자동 머지 조건 설정 (CI 통과 + 승인)

### Task 9.7.3: 기술 부채 관리

- **SubTask 9.7.3.1**: TODO/FIXME 주석 추적
- **SubTask 9.7.3.2**: 리팩토링 우선순위 목록 작성
- **SubTask 9.7.3.3**: 정기적인 코드 정리 스프린트
- **SubTask 9.7.3.4**: 기술 부채 대시보드 (SonarQube)

### Task 9.7.4: 문서화 품질

- **SubTask 9.7.4.1**: API 문서 최신 상태 유지
- **SubTask 9.7.4.2**: 주석 및 JavaDoc/JSDoc 작성
- **SubTask 9.7.4.3**: README 업데이트 (설치, 실행 가이드)
- **SubTask 9.7.4.4**: 아키텍처 다이어그램 문서화

---

## Story 9.8: 사용자 수락 테스트 (UAT)

**목표**: 실제 사용자 환경에서 검증

### Task 9.8.1: UAT 환경 구축

- **SubTask 9.8.1.1**: 스테이징 환경 설정 (프로덕션 복제)
- **SubTask 9.8.1.2**: 테스트 데이터 준비
- **SubTask 9.8.1.3**: 테스트 계정 생성
- **SubTask 9.8.1.4**: 모니터링 및 로그 설정

### Task 9.8.2: UAT 시나리오 작성

- **SubTask 9.8.2.1**: 주요 기능 테스트 시나리오
    - 센서 데이터 실시간 확인
    - 통계 조회 및 내보내기
    - 알림 수신 확인
- **SubTask 9.8.2.2**: 엣지 케이스 시나리오
- **SubTask 9.8.2.3**: 사용성 테스트 시나리오
- **SubTask 9.8.2.4**: 테스트 체크리스트 작성

### Task 9.8.3: 피드백 수집 및 개선

- **SubTask 9.8.3.1**: 버그 리포트 양식 작성
- **SubTask 9.8.3.2**: 사용자 피드백 수집
- **SubTask 9.8.3.3**: 우선순위별 이슈 분류
- **SubTask 9.8.3.4**: 개선 사항 반영 및 재테스트

### Task 9.8.4: UAT 승인 및 배포

- **SubTask 9.8.4.1**: UAT 통과 기준 정의
    - 크리티컬 버그 0건
    - 주요 기능 100% 작동
- **SubTask 9.8.4.2**: 최종 승인 받기
- **SubTask 9.8.4.3**: 프로덕션 배포 계획 수립
- **SubTask 9.8.4.4**: 롤아웃 모니터링

---

## 산출물

- [ ]  단위 테스트 코드 (80% 커버리지)
- [ ]  통합 테스트 코드
- [ ]  E2E 테스트 코드 (선택사항)
- [ ]  성능 테스트 리포트
- [ ]  보안 테스트 리포트
- [ ]  Lighthouse 성능 점수 (90+)
- [ ]  UAT 시나리오 및 체크리스트
- [ ]  테스트 자동화 스크립트
- [ ]  품질 메트릭 대시보드

---

## 다음 에픽으로 이동 조건

- [ ]  단위 테스트 커버리지 80% 이상
- [ ]  모든 통합 테스트 통과
- [ ]  API 부하 테스트 통과 (초당 100 요청)
- [ ]  Lighthouse 성능 점수 90 이상
- [ ]  보안 취약점 크리티컬 0건
- [ ]  UAT 승인 완료
- [ ]  크로스 브라우저 테스트 통과