# Epic 4: 프론트엔드 대시보드 개발

*사용자가 데이터를 직관적으로 볼 수 있는 UI*

## Story 4.1: React 기반 프로젝트 초기 설정

**목표**: Next.js 프로젝트 구조 및 개발 환경 구축

### Task 4.1.1: 프로젝트 생성 및 의존성 설정

- **SubTask 4.1.1.1**: Next.js 14+ 프로젝트 생성
    
    ```bash
    npx create-next-app@latest solar-monitor-dashboard
    
    ```
    
- **SubTask 4.1.1.2**: TypeScript 설정 (tsconfig.json)
- **SubTask 4.1.1.3**: ESLint 및 Prettier 설정
- **SubTask 4.1.1.4**: 필수 라이브러리 설치
    - Tailwind CSS 또는 Material-UI
    - Recharts (차트 라이브러리)
    - Axios (HTTP 클라이언트)
    - Socket.IO Client (WebSocket)

### Task 4.1.2: 프로젝트 구조 설계

- **SubTask 4.1.2.1**: App Router 구조 설계
    
    ```
    /app  /dashboard  /statistics  /settings/components  /common  /widgets  /charts/lib  /api  /utils/types
    
    ```
    
- **SubTask 4.1.2.2**: 환경 변수 설정 (.env.local)
- **SubTask 4.1.2.3**: 타입 정의 파일 생성 (types/index.ts)
- **SubTask 4.1.2.4**: API 클라이언트 설정 (axios instance)

### Task 4.1.3: 디자인 시스템 구축

- **SubTask 4.1.3.1**: 색상 팔레트 정의 (Primary, Secondary, etc.)
- **SubTask 4.1.3.2**: Typography 스타일 설정
- **SubTask 4.1.3.3**: Spacing 및 Layout 시스템
- **SubTask 4.1.3.4**: 다크 테마 설정 (태양광 모니터링에 적합)

---

## Story 4.2: 공통 컴포넌트 개발

**목표**: 재사용 가능한 UI 컴포넌트 라이브러리

### Task 4.2.1: Layout 컴포넌트

- **SubTask 4.2.1.1**: Header 컴포넌트
    - 로고, 네비게이션, 사용자 메뉴
- **SubTask 4.2.1.2**: Sidebar 컴포넌트 (선택사항)
    - 메뉴 항목, 접기/펼치기 기능
- **SubTask 4.2.1.3**: Footer 컴포넌트
- **SubTask 4.2.1.4**: MainLayout 컴포넌트 (Header + Content + Footer)

### Task 4.2.2: Card/Widget 컴포넌트

- **SubTask 4.2.2.1**: BaseCard 컴포넌트
    - 그림자, 라운드 코너, 패딩
- **SubTask 4.2.2.2**: WidgetCard 컴포넌트
    - 제목, 메뉴 버튼, 본문
- **SubTask 4.2.2.3**: StatCard 컴포넌트
    - 라벨, 값, 아이콘, 색상
- **SubTask 4.2.2.4**: 호버 애니메이션 효과

### Task 4.2.3: Chart 래퍼 컴포넌트

- **SubTask 4.2.3.1**: LineChart 컴포넌트
    - Recharts 기반, props 타입 정의
- **SubTask 4.2.3.2**: BarChart 컴포넌트
- **SubTask 4.2.3.3**: PieChart/DonutChart 컴포넌트
- **SubTask 4.2.3.4**: 공통 차트 옵션 (색상, 툴팁, 범례)

### Task 4.2.4: 상태 표시 컴포넌트

- **SubTask 4.2.4.1**: Loading 스피너 컴포넌트
- **SubTask 4.2.4.2**: Skeleton 로딩 컴포넌트
- **SubTask 4.2.4.3**: Error 경고 컴포넌트
- **SubTask 4.2.4.4**: Empty State 컴포넌트

---

## Story 4.3: 실시간 전력 생산 위젯

**목표**: 현재 발전량을 보여주는 핵심 위젯

### Task 4.3.1: 실시간 전력 표시

- **SubTask 4.3.1.1**: PowerDisplay 컴포넌트 생성
    - 원형 프로그레스 바 (현재 출력 / 최대 출력)
- **SubTask 4.3.1.2**: 실시간 데이터 fetch hook 구현
    
    ```tsx
    const { data, isLoading } = usePowerData();
    
    ```
    
- **SubTask 4.3.1.3**: 숫자 애니메이션 효과 (react-countup)
- **SubTask 4.3.1.4**: 피크/평균/최소 전력 표시

### Task 4.3.2: 24시간 발전 트렌드 차트

- **SubTask 4.3.2.1**: PowerTrendChart 컴포넌트
- **SubTask 4.3.2.2**: API 연동 (GET /api/v1/power/history?hours=24)
- **SubTask 4.3.2.3**: 시간대별 데이터 포인트 표시
- **SubTask 4.3.2.4**: 호버 시 툴팁 (시간, 전력값)

### Task 4.3.3: 배터리 상태 위젯

- **SubTask 4.3.3.1**: BatteryStatus 컴포넌트
- **SubTask 4.3.3.2**: 배터리 아이콘 SVG (충전 레벨 시각화)
- **SubTask 4.3.3.3**: 전압, 전류, SOC, 건강도 표시
- **SubTask 4.3.3.4**: 충전/방전 상태 인디케이터

### Task 4.3.4: 현재 소비량 위젯

- **SubTask 4.3.4.1**: ConsumptionDisplay 컴포넌트
- **SubTask 4.3.4.2**: 총 소비량 표시
- **SubTask 4.3.4.3**: 영역별 소비량 리스트 (거실, 주방 등)
- **SubTask 4.3.4.4**: 소비 비율 막대 그래프

---

## Story 4.4: WebSocket 실시간 업데이트

**목표**: 실시간으로 데이터 갱신

### Task 4.4.1: WebSocket 연결 설정

- **SubTask 4.4.1.1**: Socket.IO 클라이언트 설정
    
    ```tsx
    const socket = io(process.env.NEXT_PUBLIC_WS_URL);
    
    ```
    
- **SubTask 4.4.1.2**: useWebSocket 커스텀 훅 작성
- **SubTask 4.4.1.3**: 연결/재연결 로직
- **SubTask 4.4.1.4**: 연결 상태 표시 UI

### Task 4.4.2: 실시간 데이터 구독

- **SubTask 4.4.2.1**: 전력 데이터 채널 구독
    
    ```tsx
    socket.on('power:update', (data) => {...});
    
    ```
    
- **SubTask 4.4.2.2**: 배터리 상태 채널 구독
- **SubTask 4.4.2.3**: 알림 채널 구독
- **SubTask 4.4.2.4**: 시스템 상태 채널 구독

### Task 4.4.3: 상태 관리

- **SubTask 4.4.3.1**: Context API 또는 Zustand 설정
- **SubTask 4.4.3.2**: 실시간 데이터 전역 상태 관리
- **SubTask 4.4.3.3**: 상태 업데이트 최적화 (debounce)
- **SubTask 4.4.3.4**: 메모이제이션 (useMemo, useCallback)

---

## Story 4.5: 통계 및 히스토리 페이지

**목표**: 과거 데이터 분석 화면

### Task 4.5.1: 일별 에너지 차트

- **SubTask 4.5.1.1**: DailyEnergyChart 컴포넌트
- **SubTask 4.5.1.2**: 날짜 선택 필터 (DatePicker)
- **SubTask 4.5.1.3**: API 연동 (GET /api/v1/statistics/daily)
- **SubTask 4.5.1.4**: 차트 데이터 변환 및 포맷팅

### Task 4.5.2: 월별 에너지 차트

- **SubTask 4.5.2.1**: MonthlyEnergyChart 컴포넌트 (Bar Chart)
- **SubTask 4.5.2.2**: 12개월 데이터 표시
- **SubTask 4.5.2.3**: 년도 선택 필터
- **SubTask 4.5.2.4**: 전년 대비 증감률 표시

### Task 4.5.3: 연별 누적 차트

- **SubTask 4.5.3.1**: YearlyEnergyChart 컴포넌트 (Line Chart)
- **SubTask 4.5.3.2**: 누적 발전량 계산
- **SubTask 4.5.3.3**: 목표 대비 달성률 표시
- **SubTask 4.5.3.4**: 차트 인터랙션 (줌, 팬)

### Task 4.5.4: 데이터 테이블

- **SubTask 4.5.4.1**: DataTable 컴포넌트
    - 정렬, 필터링, 페이지네이션
- **SubTask 4.5.4.2**: 일별 상세 데이터 표시
- **SubTask 4.5.4.3**: CSV/Excel 내보내기 버튼
- **SubTask 4.5.4.4**: 날짜 범위 선택 필터

---

## Story 4.6: 알림 및 시스템 모니터링

**목표**: 시스템 상태 및 알림 표시

### Task 4.6.1: 알림 센터

- **SubTask 4.6.1.1**: NotificationCenter 컴포넌트
- **SubTask 4.6.1.2**: 알림 목록 표시 (최신순)
- **SubTask 4.6.1.3**: 알림 타입별 아이콘 및 색상
    - Error: 빨강, Warning: 주황, Info: 파랑
- **SubTask 4.6.1.4**: 알림 클릭 시 상세 정보 모달

### Task 4.6.2: 실시간 알림 푸시

- **SubTask 4.6.2.1**: WebSocket으로 알림 수신
- **SubTask 4.6.2.2**: 토스트 알림 표시 (react-toastify)
- **SubTask 4.6.2.3**: 브라우저 알림 권한 요청
- **SubTask 4.6.2.4**: 알림 배지 카운터 (헤더)

### Task 4.6.3: 시스템 상태 대시보드

- **SubTask 4.6.3.1**: SystemStatus 컴포넌트
- **SubTask 4.6.3.2**: 온라인/오프라인 상태 표시
- **SubTask 4.6.3.3**: 센서별 상태 체크리스트
- **SubTask 4.6.3.4**: 마지막 통신 시간 표시

### Task 4.6.4: 환경 정보 위젯

- **SubTask 4.6.4.1**: EnvironmentInfo 컴포넌트
- **SubTask 4.6.4.2**: 온도/습도 표시 카드
- **SubTask 4.6.4.3**: 조도(일사량) 게이지
- **SubTask 4.6.4.4**: 날씨 API 통합 (OpenWeatherMap)

---

## Story 4.7: 설정 페이지

**목표**: 사용자 설정 관리 화면

### Task 4.7.1: 시스템 설정 폼

- **SubTask 4.7.1.1**: SettingsForm 컴포넌트
- **SubTask 4.7.1.2**: 전력 단가 입력 필드
- **SubTask 4.7.1.3**: 목표 발전량 설정
- **SubTask 4.7.1.4**: 단위 설정 (W/kW, Wh/kWh)

### Task 4.7.2: 알림 설정

- **SubTask 4.7.2.1**: 알림 선호도 설정 (이메일, 푸시, 브라우저)
- **SubTask 4.7.2.2**: 알림 임계값 설정
    - 배터리 온도 임계값
    - 저발전량 기준
- **SubTask 4.7.2.3**: 알림 음소거 시간대 설정
- **SubTask 4.7.2.4**: 설정 저장 API 연동

### Task 4.7.3: 사용자 프로필

- **SubTask 4.7.3.1**: 프로필 정보 표시
- **SubTask 4.7.3.2**: 비밀번호 변경 폼
- **SubTask 4.7.3.3**: 2FA 설정 (선택사항)
- **SubTask 4.7.3.4**: 로그아웃 기능

---

## Story 4.8: 반응형 디자인 및 최적화

**목표**: 모바일 및 태블릿 대응

### Task 4.8.1: 반응형 레이아웃

- **SubTask 4.8.1.1**: 브레이크포인트 정의 (sm, md, lg, xl)
- **SubTask 4.8.1.2**: 모바일 네비게이션 (햄버거 메뉴)
- **SubTask 4.8.1.3**: 그리드 레이아웃 반응형 조정
- **SubTask 4.8.1.4**: 차트 반응형 크기 조정

### Task 4.8.2: 성능 최적화

- **SubTask 4.8.2.1**: 이미지 최적화 (Next.js Image)
- **SubTask 4.8.2.2**: 코드 스플리팅 (dynamic import)
- **SubTask 4.8.2.3**: 번들 크기 분석 및 최적화
- **SubTask 4.8.2.4**: 메모이제이션 및 lazy loading

### Task 4.8.3: PWA 설정 (선택사항)

- **SubTask 4.8.3.1**: manifest.json 작성
- **SubTask 4.8.3.2**: Service Worker 설정
- **SubTask 4.8.3.3**: 오프라인 지원
- **SubTask 4.8.3.4**: 설치 가능한 앱으로 만들기

---

## 산출물

- [ ]  Next.js 프로젝트 (GitHub)
- [ ]  컴포넌트 스토리북 (선택사항)
- [ ]  디자인 시스템 문서
- [ ]  API 연동 가이드
- [ ]  반응형 테스트 결과
- [ ]  Lighthouse 성능 점수 보고서
- [ ]  사용자 매뉴얼 (스크린샷 포함)

---

## 다음 에픽으로 이동 조건

- [ ]  모든 주요 페이지 구현 완료
- [ ]  WebSocket 실시간 업데이트 정상 작동
- [ ]  반응형 디자인 테스트 통과
- [ ]  Lighthouse 성능 점수 90 이상
- [ ]  크로스 브라우저 테스트 완료
- [ ]  컴포넌트 테스트 작성 완료