# GitHub Issues 자동 등록 가이드

Claude Code와 GitHub CLI (`gh`)를 사용하여 todo-list의 Epic/Story/Task를 GitHub Issues로 등록합니다.

**저장소**: `goodjwon/solar-simulator`

---

## 🚀 빠른 시작

### 1. GitHub CLI 설치 및 인증

```bash
# macOS
brew install gh

# 인증
gh auth login
```

### 2. Claude Code에게 요청

```
epic-0.md를 읽고 GitHub Issues로 만들어줘.

중요:
1. 먼저 필요한 labels를 모두 생성해줘
2. Epic → Story → Task 순서로 생성
3. 각 Issue에 부모 Issue 번호를 포함시켜줘
```

---

## 📋 라벨링 전략

### 필수 Labels

Issues 생성 **전에** 다음 labels를 먼저 만들어야 합니다:

```bash
# Epic labels (파란색 계열)
gh label create "epic" --color "0052CC" --description "Epic 이슈"
gh label create "epic-0" --color "0052CC" --description "Epic 0: 시스템 설계 및 부품 조사"
gh label create "epic-1" --color "0052CC" --description "Epic 1: 부품 구매 및 검수"
gh label create "epic-2" --color "0052CC" --description "Epic 2: 하드웨어 조립 및 펌웨어 개발"
gh label create "epic-3" --color "0052CC" --description "Epic 3: 백엔드 API 개발"
gh label create "epic-4" --color "0052CC" --description "Epic 4: 프론트엔드 대시보드 개발"
gh label create "epic-5" --color "0052CC" --description "Epic 5: 데이터 조회 API 및 실시간 통신"
gh label create "epic-6" --color "0052CC" --description "Epic 6: 알림 시스템 및 모니터링"
gh label create "epic-7" --color "0052CC" --description "Epic 7: 사용자 인증 및 설정 관리"
gh label create "epic-8" --color "0052CC" --description "Epic 8: 배포 및 인프라 구축"
gh label create "epic-9" --color "0052CC" --description "Epic 9: 테스트 및 품질 보증"

# Story labels (초록색 계열)
gh label create "story" --color "5CB85C" --description "Story 이슈"

# Task labels (주황색 계열)
gh label create "task" --color "F0AD4E" --description "Task 이슈"
```

### Label 규칙

1. **Epic Issue**: `epic`, `epic-{번호}`
2. **Story Issue**: `story`, `epic-{번호}`
3. **Task Issue**: `task`, `epic-{번호}`

---

## 🔗 종속 관계 유지

### Issue Body 형식

각 Issue의 body에 부모 Issue 링크를 **반드시** 포함시켜야 합니다.

#### Epic Issue Body

```markdown
## 📋 Epic {번호}: {제목}

**설명**: {설명}

### Stories
- [ ] #2 Story 0.1: 시스템 요구사항 분석
- [ ] #3 Story 0.2: 센서 및 모듈 조사
- [ ] #4 Story 0.3: 회로 설계 및 시뮬레이션
- [ ] #5 Story 0.4: 부품 리스트 및 비용 산정
- [ ] #6 Story 0.5: 프로토타입 설계

---
📁 Source: `todo-list/epic-0.md`
```

#### Story Issue Body

```markdown
## 📖 Story {번호}: {제목}

**목표**: {목표}

**Epic**: #1 Epic 0: 시스템 설계 및 부품 조사

### Tasks
- [ ] #7 Task 0.1.1: 측정 데이터 항목 정의
- [ ] #8 Task 0.1.2: 시스템 아키텍처 설계
- [ ] #9 Task 0.1.3: 안전 요구사항 정의

---
📁 Source: `todo-list/epic-0.md`
```

#### Task Issue Body

```markdown
## ✅ Task {번호}: {제목}

**Story**: #2 Story 0.1: 시스템 요구사항 분석
**Epic**: #1 Epic 0: 시스템 설계 및 부품 조사

### SubTasks
- [ ] 필수 측정 항목 정의 (전압, 전류, 전력, 에너지)
- [ ] 환경 측정 항목 정의 (온도, 습도, 일사량)
- [ ] 측정 범위 및 정확도 요구사항 정의
- [ ] 데이터 샘플링 주기 결정

---
📁 Source: `todo-list/epic-0.md`
```

---

## 📝 Claude Code 사용 방법

### 방법 1: 직접 요청

```
epic-0.md를 읽고 GitHub Issues로 만들어줘.

레포지토리: goodjwon/solar-simulator

순서:
1. Labels가 없으면 먼저 생성 (epic, epic-0, story, task)
2. Epic Issue 생성 (#1)
3. Story Issues 생성 (#2-#6)
   - Body에 Epic #1 링크 포함
4. Task Issues 생성 (#7-#24)
   - Body에 Story 링크와 Epic 링크 포함

Issue 번호를 저장하면서 순차적으로 생성해줘.
```

### 방법 2: 단계별 생성

**Step 1: Labels 생성**
```
GitHub에 필요한 labels를 먼저 만들어줘.
epic-0.md에 필요한 labels:
- epic, epic-0, story, task
```

**Step 2: Epic Issue 생성**
```
Epic 0 Issue를 만들어줘.
body에 Story 목록 체크박스를 포함시켜줘.
```

**Step 3: Story Issues 생성**
```
Epic #1의 하위 Story Issues를 만들어줘.
각 Story body에 Epic #1 링크를 포함시켜줘.
```

**Step 4: Task Issues 생성**
```
Story #2의 하위 Task Issues를 만들어줘.
각 Task body에 Story #2와 Epic #1 링크를 포함시켜줘.
```

### 방법 3: Slash Command 사용

`.claude/commands/create-issues.md` 생성:

```markdown
Epic을 GitHub Issues로 등록합니다.

저장소: goodjwon/solar-simulator

사용자가 "Epic {번호}"를 입력하면:

1. 필요한 labels 확인 및 생성
2. epic-{번호}.md 파일 읽기
3. Issues 순차 생성:
   - Epic Issue (labels: epic, epic-{번호})
   - Story Issues (labels: story, epic-{번호})
   - Task Issues (labels: task, epic-{번호})
4. 각 Issue에 부모 링크 포함
5. 생성 결과 보고

Issue 번호를 변수에 저장하여 body에 정확한 링크 포함.
```

사용: `/create-issues Epic 0`

---

## 🎯 실전 예시

### Epic 0 전체 등록

```
Claude, epic-0.md를 GitHub Issues로 등록해줘.

레포지토리: goodjwon/solar-simulator

다음 순서로:
1. gh label create로 labels 생성 (없으면)
2. Epic Issue 생성하고 번호 저장 (EPIC_NUM)
3. 각 Story Issue 생성하고 번호 저장 (STORY_NUM)
   - body에 Epic #$EPIC_NUM 링크
4. 각 Task Issue 생성
   - body에 Story #$STORY_NUM, Epic #$EPIC_NUM 링크

진행 상황을 보여주면서 해줘.
```

예상 출력:
```
✅ Labels 생성 완료

✅ Epic #1: Epic 0: 시스템 설계 및 부품 조사

✅ Story #2: Story 0.1: 시스템 요구사항 분석 (Epic #1)
  ✅ Task #7: Task 0.1.1: 측정 데이터 항목 정의
  ✅ Task #8: Task 0.1.2: 시스템 아키텍처 설계
  ✅ Task #9: Task 0.1.3: 안전 요구사항 정의

✅ Story #3: Story 0.2: 센서 및 모듈 조사 (Epic #1)
  ✅ Task #10: Task 0.2.1: 전력 측정 센서 조사
  ...

총 26개 Issues 생성 완료!
GitHub: https://github.com/goodjwon/solar-simulator/issues?q=label:epic-0
```

---

## 🔧 유용한 gh 명령어

### Issue 조회

```bash
# Epic 0 관련 모든 Issues
gh issue list --label "epic-0" --repo goodjwon/solar-simulator

# Story만 보기
gh issue list --label "epic-0" --label "story" --repo goodjwon/solar-simulator

# Open 상태만
gh issue list --label "epic-0" --state open --repo goodjwon/solar-simulator
```

### Issue 수정

```bash
# Task 완료 처리
gh issue close 7 --comment "완료" --repo goodjwon/solar-simulator

# Label 추가
gh issue edit 7 --add-label "in-progress" --repo goodjwon/solar-simulator

# Assignee 할당
gh issue edit 7 --add-assignee "@me" --repo goodjwon/solar-simulator
```

### Issue 상세 보기

```bash
# 터미널에서 보기
gh issue view 1 --repo goodjwon/solar-simulator

# 브라우저에서 열기
gh issue view 1 --web --repo goodjwon/solar-simulator
```

---

## ⚠️ 주의사항

### 1. Issue 번호 저장 필수

Epic과 Story Issue를 생성할 때 **반드시 번호를 저장**해야 합니다:

```bash
EPIC_NUM=$(gh issue create --title "Epic 0" --body "..." --label "epic,epic-0" --repo goodjwon/solar-simulator --json number -q .number)

echo "Epic Issue: #$EPIC_NUM"
```

### 2. Body에 정확한 링크 포함

Story Issue body:
```markdown
**Epic**: #$EPIC_NUM Epic 0: 시스템 설계 및 부품 조사
```

Task Issue body:
```markdown
**Story**: #$STORY_NUM Story 0.1: 시스템 요구사항 분석
**Epic**: #$EPIC_NUM Epic 0: 시스템 설계 및 부품 조사
```

### 3. Labels 먼저 생성

Issues 생성 전에 labels가 없으면 에러 발생. 반드시 먼저 생성:

```bash
gh label create "epic-0" --color "0052CC" --repo goodjwon/solar-simulator
```

### 4. Rate Limit 주의

많은 Issues를 생성할 때는 지연 추가:

```bash
gh issue create ...
sleep 1  # 1초 대기
```

---

## 📊 진행 상황 추적

### Epic 진행률 확인

```bash
# Epic 0 전체 Issues
TOTAL=$(gh issue list --label "epic-0" --repo goodjwon/solar-simulator --json number -q '. | length')

# 완료된 Issues
CLOSED=$(gh issue list --label "epic-0" --state closed --repo goodjwon/solar-simulator --json number -q '. | length')

# 진행률 계산
echo "Epic 0 진행률: $((CLOSED * 100 / TOTAL))% ($CLOSED/$TOTAL)"
```

### Story별 진행률

```bash
# Story 0.1의 Tasks
gh issue list --label "epic-0" --search "Story 0.1 in:title" --repo goodjwon/solar-simulator
```

---

## 🎓 추가 팁

### 1. Milestone 사용

Epic별로 Milestone 생성:

```
Claude, "Epic 0 - Q1 2025" Milestone을 만들고,
Epic 0 관련 모든 Issues를 할당해줘.
```

### 2. Projects 연동

```
Claude, "Solar Monitor Pro" Project를 만들고,
Epic 0 Issues를 "To Do" 컬럼에 추가해줘.
```

### 3. Issue Template

`.github/ISSUE_TEMPLATE/` 에 템플릿 추가하면 일관성 유지 가능.

---

## 📚 참고

- **저장소**: https://github.com/goodjwon/solar-simulator
- **Epic 문서**: `todo-list/epic-{0-9}.md`
- **GitHub CLI 문서**: https://cli.github.com/manual/gh_issue
