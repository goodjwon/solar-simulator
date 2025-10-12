# Epic 8: 배포 및 인프라 구축

*안정적인 서비스 운영 기반*

## Story 8.1: Docker 컨테이너화

**목표**: 애플리케이션 컨테이너 배포

### Task 8.1.1: Spring Boot Dockerfile

- **SubTask 8.1.1.1**: 멀티 스테이지 Dockerfile 작성
    
    ```docker
    # Build stageFROM gradle:7-jdk17 AS buildWORKDIR /appCOPY . .RUN gradle build -x test# Run stageFROM openjdk:17-jdk-slimWORKDIR /appCOPY --from=build /app/build/libs/*.jar app.jarENTRYPOINT ["java", "-jar", "app.jar"]
    
    ```
    
- **SubTask 8.1.1.2**: 환경 변수 설정 (ENV)
- **SubTask 8.1.1.3**: 헬스체크 설정 (HEALTHCHECK)
- **SubTask 8.1.1.4**: 이미지 크기 최적화

### Task 8.1.2: Next.js Dockerfile

- **SubTask 8.1.2.1**: Next.js Dockerfile 작성
    
    ```docker
    FROM node:18-alpine AS baseFROM base AS depsWORKDIR /appCOPY package*.json ./RUN npm ciFROM base AS builderWORKDIR /appCOPY --from=deps /app/node_modules ./node_modulesCOPY . .RUN npm run buildFROM base AS runnerWORKDIR /appENV NODE_ENV productionCOPY --from=builder /app/public ./publicCOPY --from=builder /app/.next/standalone ./COPY --from=builder /app/.next/static ./.next/staticEXPOSE 3000CMD ["node", "server.js"]
    
    ```
    
- **SubTask 8.1.2.2**: 빌드 최적화 (캐시 레이어)
- **SubTask 8.1.2.3**: 프로덕션 빌드 설정
- **SubTask 8.1.2.4**: 정적 파일 최적화

### Task 8.1.3: PostgreSQL 컨테이너

- **SubTask 8.1.3.1**: 공식 PostgreSQL 이미지 사용
- **SubTask 8.1.3.2**: 초기화 스크립트 마운트
- **SubTask 8.1.3.3**: 데이터 볼륨 설정 (영구 저장)
- **SubTask 8.1.3.4**: 환경 변수로 계정 정보 주입

### Task 8.1.4: Docker 이미지 빌드 및 푸시

- **SubTask 8.1.4.1**: 이미지 태깅 전략 (latest, version)
- **SubTask 8.1.4.2**: Docker Hub 또는 ECR에 푸시
- **SubTask 8.1.4.3**: 이미지 스캔 (보안 취약점)
- **SubTask 8.1.4.4**: 이미지 크기 모니터링

---

## Story 8.2: Docker Compose 구성

**목표**: 로컬 개발 및 테스트 환경

### Task 8.2.1: docker-compose.yml 작성

- **SubTask 8.2.1.1**: 서비스 정의
    
    ```yaml
    version: '3.8'services:  postgres:    image: postgres:15    environment:      POSTGRES_DB: solar_monitor      POSTGRES_USER: admin      POSTGRES_PASSWORD: ${DB_PASSWORD}    volumes:      - postgres_data:/var/lib/postgresql/data    ports:      - "5432:5432"    backend:    build: ./backend    environment:      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/solar_monitor    depends_on:      - postgres    ports:      - "8080:8080"    frontend:    build: ./frontend    environment:      NEXT_PUBLIC_API_URL: http://backend:8080    depends_on:      - backend    ports:      - "3000:3000"volumes:  postgres_data:
    
    ```
    
- **SubTask 8.2.1.2**: 네트워크 설정 (bridge)
- **SubTask 8.2.1.3**: 헬스체크 설정
- **SubTask 8.2.1.4**: 재시작 정책 (restart: unless-stopped)

### Task 8.2.2: 환경 변수 관리

- **SubTask 8.2.2.1**: .env 파일 생성 (템플릿)
    
    ```
    DB_PASSWORD=secretJWT_SECRET=your-secret-keyEMAIL_USERNAME=your-emailEMAIL_PASSWORD=your-password
    
    ```
    
- **SubTask 8.2.2.2**: .env.example 제공
- **SubTask 8.2.2.3**: docker-compose.override.yml (로컬용)
- **SubTask 8.2.2.4**: 민감 정보 Git 제외 (.gitignore)

### Task 8.2.3: 볼륨 및 퍼시스턴스

- **SubTask 8.2.3.1**: 데이터베이스 볼륨 설정
- **SubTask 8.2.3.2**: 로그 파일 볼륨 마운트
- **SubTask 8.2.3.3**: 업로드 파일 저장소 볼륨
- **SubTask 8.2.3.4**: 볼륨 백업 스크립트

### Task 8.2.4: 개발 환경 구성

- **SubTask 8.2.4.1**: 핫 리로드 설정 (Next.js)
- **SubTask 8.2.4.2**: 디버그 포트 노출
- **SubTask 8.2.4.3**: docker-compose up 원클릭 실행
- **SubTask 8.2.4.4**: 개발 환경 문서화

---

## Story 8.3: CI/CD 파이프라인

**목표**: 자동화된 빌드 및 배포

### Task 8.3.1: GitHub Actions 워크플로우

- **SubTask 8.3.1.1**: .github/workflows/ci.yml 작성
    
    ```yaml
    name: CIon:  push:    branches: [main, develop]  pull_request:    branches: [main]jobs:  test:    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3      - name: Set up JDK 17        uses: actions/setup-java@v3        with:          java-version: '17'      - name: Run tests        run: ./gradlew test
    
    ```
    
- **SubTask 8.3.1.2**: 백엔드 테스트 자동화
- **SubTask 8.3.1.3**: 프론트엔드 린트 및 테스트
- **SubTask 8.3.1.4**: 테스트 커버리지 리포트

### Task 8.3.2: Docker 이미지 빌드 자동화

- **SubTask 8.3.2.1**: .github/workflows/build.yml
- **SubTask 8.3.2.2**: Docker Buildx 설정 (멀티 플랫폼)
- **SubTask 8.3.2.3**: 이미지 푸시 (Docker Hub/ECR)
- **SubTask 8.3.2.4**: 이미지 태그 자동화 (Git SHA, version)

### Task 8.3.3: 배포 자동화

- **SubTask 8.3.3.1**: .github/workflows/deploy.yml
- **SubTask 8.3.3.2**: SSH로 서버 접속 및 배포
    
    ```yaml
    - name: Deploy to server  uses: appleboy/ssh-action@master  with:    host: ${{ secrets.SERVER_HOST }}    username: ${{ secrets.SERVER_USER }}    key: ${{ secrets.SSH_PRIVATE_KEY }}    script: |      cd /app      docker-compose pull      docker-compose up -d
    
    ```
    
- **SubTask 8.3.3.3**: 배포 전 헬스체크
- **SubTask 8.3.3.4**: 배포 알림 (Slack, Email)

### Task 8.3.4: 롤백 전략

- **SubTask 8.3.4.1**: 이전 버전 이미지 보관
- **SubTask 8.3.4.2**: 수동 롤백 스크립트
- **SubTask 8.3.4.3**: 자동 롤백 조건 (헬스체크 실패)
- **SubTask 8.3.4.4**: Blue-Green 배포 (선택사항)

---

## Story 8.4: 모니터링 및 로깅

**목표**: 운영 중 시스템 상태 추적

### Task 8.4.1: 애플리케이션 로그 수집

- **SubTask 8.4.1.1**: Logback 설정 (JSON 포맷)
- **SubTask 8.4.1.2**: 로그 레벨 관리 (INFO, WARN, ERROR)
- **SubTask 8.4.1.3**: 로그 파일 로테이션
    - 일별 파일, 최대 30일 보관
- **SubTask 8.4.1.4**: 에러 로그 별도 파일 저장

### Task 8.4.2: 에러 추적 시스템 (선택사항)

- **SubTask 8.4.2.1**: Sentry 통합
    
    ```java
    Sentry.init(options -> {  options.setDsn("https://...");  options.setEnvironment("production");});
    
    ```
    
- **SubTask 8.4.2.2**: 프론트엔드 에러 추적
- **SubTask 8.4.2.3**: 에러 알림 설정
- **SubTask 8.4.2.4**: 에러 대시보드 모니터링

### Task 8.4.3: 성능 모니터링

- **SubTask 8.4.3.1**: Spring Boot Actuator 활성화
- **SubTask 8.4.3.2**: /actuator/health 엔드포인트
- **SubTask 8.4.3.3**: /actuator/metrics 엔드포인트
- **SubTask 8.4.3.4**: Prometheus 메트릭 노출 (선택사항)

### Task 8.4.4: 시스템 리소스 모니터링

- **SubTask 8.4.4.1**: CPU, 메모리 사용률 모니터링
- **SubTask 8.4.4.2**: 디스크 사용률 체크
- **SubTask 8.4.4.3**: 데이터베이스 커넥션 풀 모니터링
- **SubTask 8.4.4.4**: 알림 임계값 설정 (CPU > 80%)

---

## Story 8.5: 백업 및 복구

**목표**: 데이터 손실 방지

### Task 8.5.1: 데이터베이스 백업

- **SubTask 8.5.1.1**: pg_dump 백업 스크립트
    
    ```bash
    #!/bin/bashDATE=$(date +%Y%m%d_%H%M%S)pg_dump -U admin solar_monitor > backup_$DATE.sql
    
    ```
    
- **SubTask 8.5.1.2**: 일별 자동 백업 (cron)
- **SubTask 8.5.1.3**: 백업 파일 압축 및 암호화
- **SubTask 8.5.1.4**: 원격 저장소 업로드 (S3 등)

### Task 8.5.2: 백업 보관 정책

- **SubTask 8.5.2.1**: 일별 백업 7일 보관
- **SubTask 8.5.2.2**: 주별 백업 4주 보관
- **SubTask 8.5.2.3**: 월별 백업 12개월 보관
- **SubTask 8.5.2.4**: 오래된 백업 자동 삭제

### Task 8.5.3: 복구 절차 문서화

- **SubTask 8.5.3.1**: 복구 스크립트 작성
    
    ```bash
    psql -U admin solar_monitor < backup_20250101.sql
    
    ```
    
- **SubTask 8.5.3.2**: 복구 테스트 (정기적)
- **SubTask 8.5.3.3**: 복구 시나리오별 가이드
- **SubTask 8.5.3.4**: 재해 복구 계획 (DR Plan)

### Task 8.5.4: 설정 파일 백업

- **SubTask 8.5.4.1**: 환경 변수 백업
- **SubTask 8.5.4.2**: Docker Compose 파일 버전 관리
- **SubTask 8.5.4.3**: 인증서 백업 (SSL)
- **SubTask 8.5.4.4**: 백업 체크리스트

---

## Story 8.6: 보안 및 인프라 강화

**목표**: 프로덕션 환경 보안

### Task 8.6.1: HTTPS 설정

- **SubTask 8.6.1.1**: SSL/TLS 인증서 발급 (Let's Encrypt)
- **SubTask 8.6.1.2**: Nginx 리버스 프록시 설정
    
    ```
    server {  listen 443 ssl;  server_name solar-monitor.example.com;    ssl_certificate /etc/letsencrypt/live/.../fullchain.pem;  ssl_certificate_key /etc/letsencrypt/live/.../privkey.pem;    location /api {    proxy_pass http://backend:8080;  }    location / {    proxy_pass http://frontend:3000;  }}
    
    ```
    
- **SubTask 8.6.1.3**: HTTP → HTTPS 리다이렉트
- **SubTask 8.6.1.4**: 인증서 자동 갱신

### Task 8.6.2: 방화벽 설정

- **SubTask 8.6.2.1**: UFW 또는 iptables 설정
- **SubTask 8.6.2.2**: 필요한 포트만 오픈 (22, 80, 443)
- **SubTask 8.6.2.3**: SSH 포트 변경 (기본 22 → 커스텀)
- **SubTask 8.6.2.4**: Fail2Ban 설정 (무차별 대입 공격 방어)

### Task 8.6.3: 환경 변수 암호화

- **SubTask 8.6.3.1**: Secrets 관리 (AWS Secrets Manager 또는 Vault)
- **SubTask 8.6.3.2**: 민감 정보 하드코딩 제거
- **SubTask 8.6.3.3**: 환경별 설정 분리 (dev, prod)
- **SubTask 8.6.3.4**: 접근 권한 최소화 (Principle of Least Privilege)

### Task 8.6.4: 정기 보안 점검

- **SubTask 8.6.4.1**: 의존성 취약점 스캔 (Dependabot)
- **SubTask 8.6.4.2**: 컨테이너 이미지 스캔 (Trivy)
- **SubTask 8.6.4.3**: 침투 테스트 (선택사항)
- **SubTask 8.6.4.4**: 보안 업데이트 적용

---

## 산출물

- [ ]  Dockerfile (Backend, Frontend)
- [ ]  docker-compose.yml
- [ ]  GitHub Actions 워크플로우
- [ ]  배포 스크립트
- [ ]  백업 스크립트
- [ ]  Nginx 설정 파일
- [ ]  운영 매뉴얼 문서
- [ ]  재해 복구 계획서

---

## 다음 에픽으로 이동 조건

- [ ]  Docker 컨테이너 정상 작동
- [ ]  CI/CD 파이프라인 구축 완료
- [ ]  프로덕션 환경 배포 성공
- [ ]  HTTPS 적용 완료
- [ ]  백업 자동화 테스트 통과
- [ ]  모니터링 시스템 작동 확인