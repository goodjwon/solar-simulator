# Epic 7: 사용자 인증 및 설정 관리

*계정, 권한, 시스템 설정*

## Story 7.1: 사용자 인증 시스템

**목표**: 안전한 로그인 및 세션 관리

### Task 7.1.1: Spring Security 설정

- **SubTask 7.1.1.1**: Spring Security 의존성 추가
- **SubTask 7.1.1.2**: SecurityConfig 클래스 작성
    
    ```java
    @Configuration@EnableWebSecurityclass SecurityConfig extends WebSecurityConfigurerAdapter
    
    ```
    
- **SubTask 7.1.1.3**: 비밀번호 인코더 설정 (BCryptPasswordEncoder)
- **SubTask 7.1.1.4**: CORS 및 CSRF 설정

### Task 7.1.2: JWT 토큰 기반 인증

- **SubTask 7.1.2.1**: JWT 라이브러리 추가 (jjwt)
- **SubTask 7.1.2.2**: JwtTokenProvider 유틸리티 클래스
    - 토큰 생성, 검증, 파싱
- **SubTask 7.1.2.3**: JwtAuthenticationFilter 구현
- **SubTask 7.1.2.4**: 토큰 만료 및 갱신 로직
    - Access Token: 1시간
    - Refresh Token: 7일

### Task 7.1.3: 인증 API 구현

- **SubTask 7.1.3.1**: POST /api/v1/auth/login
    - 이메일, 비밀번호 검증
    - JWT 토큰 발급
- **SubTask 7.1.3.2**: POST /api/v1/auth/logout
    - 토큰 무효화 (블랙리스트)
- **SubTask 7.1.3.3**: POST /api/v1/auth/refresh
    - Refresh Token으로 Access Token 갱신
- **SubTask 7.1.3.4**: GET /api/v1/auth/me
    - 현재 로그인 사용자 정보

### Task 7.1.4: 비밀번호 보안

- **SubTask 7.1.4.1**: 비밀번호 강도 검증 (최소 8자, 특수문자 포함)
- **SubTask 7.1.4.2**: 비밀번호 재설정 기능
    - 이메일 인증 코드 발송
- **SubTask 7.1.4.3**: 비밀번호 변경 이력 관리
- **SubTask 7.1.4.4**: 로그인 실패 횟수 제한 (5회 이상 시 계정 잠금)

---

## Story 7.2: 사용자 관리

**목표**: 회원가입 및 프로필 관리

### Task 7.2.1: User 도메인 모델

- **SubTask 7.2.1.1**: User 엔티티 설계
    
    ```java
    @Entityclass User {  Long id;  String email;  String password;  String name;  Role role;  LocalDateTime createdAt;  LocalDateTime lastLoginAt;  Boolean enabled;}
    
    ```
    
- **SubTask 7.2.1.2**: Role enum 정의 (ADMIN, USER)
- **SubTask 7.2.1.3**: UserRepository 인터페이스
- **SubTask 7.2.1.4**: 유니크 제약 조건 (email)

### Task 7.2.2: 회원가입 API

- **SubTask 7.2.2.1**: POST /api/v1/auth/register
- **SubTask 7.2.2.2**: 이메일 중복 체크
- **SubTask 7.2.2.3**: 이메일 인증 (선택사항)
    - 인증 코드 발송
    - 인증 확인 엔드포인트
- **SubTask 7.2.2.4**: 회원가입 완료 알림 이메일

### Task 7.2.3: 프로필 관리 API

- **SubTask 7.2.3.1**: GET /api/v1/users/profile
- **SubTask 7.2.3.2**: PUT /api/v1/users/profile
    - 이름, 전화번호 등 수정
- **SubTask 7.2.3.3**: PUT /api/v1/users/password
    - 현재 비밀번호 확인 후 변경
- **SubTask 7.2.3.4**: DELETE /api/v1/users/account
    - 계정 삭제 (soft delete)

### Task 7.2.4: 프로필 이미지 (선택사항)

- **SubTask 7.2.4.1**: 이미지 업로드 API
- **SubTask 7.2.4.2**: 파일 저장 (로컬 또는 S3)
- **SubTask 7.2.4.3**: 이미지 리사이징 및 최적화
- **SubTask 7.2.4.4**: 이미지 URL 반환

---

## Story 7.3: 권한 관리 (선택사항)

**목표**: 역할 기반 접근 제어

### Task 7.3.1: RBAC 구현

- **SubTask 7.3.1.1**: Role 및 Permission 엔티티
- **SubTask 7.3.1.2**: @PreAuthorize 어노테이션 활용
    
    ```java
    @PreAuthorize("hasRole('ADMIN')")@DeleteMapping("/users/{id}")
    
    ```
    
- **SubTask 7.3.1.3**: 메서드 레벨 보안 설정
- **SubTask 7.3.1.4**: 권한 검증 실패 시 403 응답

### Task 7.3.2: Admin 전용 기능

- **SubTask 7.3.2.1**: GET /api/v1/admin/users - 전체 사용자 조회
- **SubTask 7.3.2.2**: PUT /api/v1/admin/users/{id}/role - 역할 변경
- **SubTask 7.3.2.3**: DELETE /api/v1/admin/users/{id} - 사용자 삭제
- **SubTask 7.3.2.4**: 시스템 설정 변경 권한

### Task 7.3.3: 권한별 UI 표시

- **SubTask 7.3.3.1**: 프론트엔드 권한 체크 유틸리티
- **SubTask 7.3.3.2**: Admin 전용 메뉴 표시/숨김
- **SubTask 7.3.3.3**: 권한 없을 시 리다이렉트
- **SubTask 7.3.3.4**: 권한 부족 안내 메시지

---

## Story 7.4: 시스템 설정 관리

**목표**: 사용자별 시스템 설정

### Task 7.4.1: SystemSettings 도메인 모델

- **SubTask 7.4.1.1**: SystemSettings 엔티티
    
    ```java
    @Entityclass SystemSettings {  Long id;  Long userId;  Double electricityRate; // kWh당 전력 단가  Double targetDailyEnergy; // 일 목표 발전량 (kWh)  String timezone;  String language;  Map<String, Object> preferences; // JSON}
    
    ```
    
- **SubTask 7.4.1.2**: 기본 설정값 정의
- **SubTask 7.4.1.3**: SettingsRepository 구현
- **SubTask 7.4.1.4**: 사용자당 1개 설정 제약 조건

### Task 7.4.2: 설정 API

- **SubTask 7.4.2.1**: GET /api/v1/settings
- **SubTask 7.4.2.2**: PUT /api/v1/settings
    - 전력 단가, 목표 발전량 수정
- **SubTask 7.4.2.3**: POST /api/v1/settings/reset
    - 기본값으로 초기화
- **SubTask 7.4.2.4**: 설정 검증 로직
    - 전력 단가 양수 체크
    - 목표 발전량 범위 체크

### Task 7.4.3: 알림 선호도 설정

- **SubTask 7.4.3.1**: NotificationPreferences 엔티티
    
    ```java
    class NotificationPreferences {  Boolean emailEnabled;  Boolean pushEnabled;  Boolean browserEnabled;  List<String> mutedHours; // ["22:00-07:00"]}
    
    ```
    
- **SubTask 7.4.3.2**: 알림 채널별 ON/OFF 설정
- **SubTask 7.4.3.3**: 음소거 시간대 설정
- **SubTask 7.4.3.4**: 알림 전송 시 선호도 체크

### Task 7.4.4: 디스플레이 설정

- **SubTask 7.4.4.1**: 단위 설정 (W/kW, Wh/kWh)
- **SubTask 7.4.4.2**: 소수점 자릿수 설정
- **SubTask 7.4.4.3**: 차트 색상 테마 선택
- **SubTask 7.4.4.4**: 다크 모드 ON/OFF

---

## Story 7.5: 설정 프론트엔드

**목표**: 사용자 친화적인 설정 페이지

### Task 7.5.1: 일반 설정 탭

- **SubTask 7.5.1.1**: GeneralSettings 컴포넌트
- **SubTask 7.5.1.2**: 전력 단가 입력 필드
    - 숫자 입력, 단위 표시 (원/kWh)
- **SubTask 7.5.1.3**: 목표 발전량 입력 필드
- **SubTask 7.5.1.4**: 타임존 선택 드롭다운

### Task 7.5.2: 알림 설정 탭

- **SubTask 7.5.2.1**: NotificationSettings 컴포넌트
- **SubTask 7.5.2.2**: 채널별 토글 스위치
    - 이메일, 푸시, 브라우저
- **SubTask 7.5.2.3**: 음소거 시간 설정 (시작/종료)
- **SubTask 7.5.2.4**: 테스트 알림 보내기 버튼

### Task 7.5.3: 계정 설정 탭

- **SubTask 7.5.3.1**: AccountSettings 컴포넌트
- **SubTask 7.5.3.2**: 이메일 표시 (변경 불가)
- **SubTask 7.5.3.3**: 이름 수정 폼
- **SubTask 7.5.3.4**: 비밀번호 변경 폼
    - 현재 비밀번호, 새 비밀번호, 확인

### Task 7.5.4: 디스플레이 설정 탭

- **SubTask 7.5.4.1**: DisplaySettings 컴포넌트
- **SubTask 7.5.4.2**: 단위 선택 라디오 버튼 (W/kW)
- **SubTask 7.5.4.3**: 다크 모드 토글
- **SubTask 7.5.4.4**: 설정 미리보기

---

## Story 7.6: 로그인 프론트엔드

**목표**: 사용자 인증 UI

### Task 7.6.1: 로그인 페이지

- **SubTask 7.6.1.1**: LoginPage 컴포넌트
- **SubTask 7.6.1.2**: 이메일/비밀번호 입력 폼
- **SubTask 7.6.1.3**: 로그인 버튼 및 로딩 상태
- **SubTask 7.6.1.4**: "비밀번호 찾기" 링크

### Task 7.6.2: 회원가입 페이지

- **SubTask 7.6.2.1**: RegisterPage 컴포넌트
- **SubTask 7.6.2.2**: 이메일, 비밀번호, 이름 입력
- **SubTask 7.6.2.3**: 비밀번호 강도 표시기
- **SubTask 7.6.2.4**: 약관 동의 체크박스

### Task 7.6.3: 인증 상태 관리

- **SubTask 7.6.3.1**: useAuth 커스텀 훅
    
    ```tsx
    const { user, login, logout, isAuthenticated } = useAuth();
    
    ```
    
- **SubTask 7.6.3.2**: JWT 토큰 저장 (쿠키 또는 메모리)
- **SubTask 7.6.3.3**: 자동 로그인 (Refresh Token)
- **SubTask 7.6.3.4**: 로그아웃 시 토큰 삭제

### Task 7.6.4: Protected Routes

- **SubTask 7.6.4.1**: PrivateRoute 컴포넌트
- **SubTask 7.6.4.2**: 미인증 시 로그인 페이지로 리다이렉트
- **SubTask 7.6.4.3**: 토큰 만료 시 자동 갱신 시도
- **SubTask 7.6.4.4**: 권한 부족 시 403 페이지 표시

---

## 산출물

- [ ]  User 엔티티 및 Repository
- [ ]  JWT 인증 시스템
- [ ]  회원가입/로그인 API
- [ ]  설정 관리 API
- [ ]  로그인/회원가입 UI
- [ ]  설정 페이지 UI
- [ ]  인증 테스트 코드
- [ ]  사용자 가이드 문서

---

## 다음 에픽으로 이동 조건

- [ ]  JWT 인증 정상 작동
- [ ]  회원가입/로그인 프로세스 완료
- [ ]  설정 CRUD API 구현 완료
- [ ]  프론트엔드 인증 상태 관리 완료
- [ ]  보안 테스트 통과 (SQL Injection, XSS 등)
- [ ]  비밀번호 암호화 검증 완료