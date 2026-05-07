# BloomingBit WEB STG 자동화 테스트 가이드

## 📋 개요

이 가이드는 bloomingbit WEB 플랫폼의 자동화 테스트 스크립트(`test_full_web.py`)를 설명합니다.

### 테스트 범위: 8개 기능 영역 + 43개 테스트 케이스

1. **내정보/로그인** (4 TC)
2. **뉴스 탭** (8 TC)
3. **커뮤니티 탭** (6 TC)
4. **핫 피플 탭** (5 TC)
5. **AI 리포트 탭** (5 TC)
6. **멤버십 탭** (5 TC)
7. **리워드 탭** (5 TC)
8. **마이페이지 탭** (6 TC)
9. **크로스 탭 통합** (3 TC)
10. **엣지 케이스/성능** (3 TC)

**총 50+ 테스트 케이스**

---

## 🚀 실행 방법

### 1. 환경 설정

```bash
cd /sessions/kind-loving-cray/mnt/WEB
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Firefox 브라우저 설치

```bash
python -m playwright install firefox
```

### 3. 전체 테스트 실행

```bash
pytest test_full_web.py -v -s
```

### 4. 특정 테스트 클래스만 실행

```bash
# 뉴스 탭 테스트만
pytest test_full_web.py::TestNewsTab -v -s

# 커뮤니티 탭 테스트만
pytest test_full_web.py::TestCommunityTab -v -s

# 마이페이지 테스트만
pytest test_full_web.py::TestMyPageTab -v -s
```

### 5. 특정 테스트 케이스만 실행

```bash
# 특정 TC만 실행
pytest test_full_web.py::TestNewsTab::test_101_news_tab_click -v -s
```

### 6. 상세 리포트와 함께 실행

```bash
pytest test_full_web.py -v -s --tb=short --html=report.html
```

---

## 📊 테스트 구조

### 각 기능 영역별 테스트 설계

#### 1️⃣ 내정보/로그인 (TestMyInfo)

```python
test_001_profile_display()      # 프로필 영역 표시
test_002_user_name_visible()    # 사용자명 표시
test_003_profile_image()        # 프로필 이미지 로드
test_004_logout_available()     # 로그아웃 기능
```

#### 2️⃣ 뉴스 탭 (TestNewsTab)

```python
test_101_news_tab_click()       # 탭 클릭
test_102_news_items_load()      # 아이템 로드
test_103_news_item_click()      # 아이템 클릭
test_104_news_scroll_load()     # 스크롤 추가 로드
test_105_news_like()            # 좋아요 기능
test_106_news_bookmark()        # 북마크 기능
test_107_news_share()           # 공유 기능
test_108_news_filter()          # 필터 기능
```

#### 3️⃣ 커뮤니티 탭 (TestCommunityTab)

```python
test_201_community_tab_click()  # 탭 클릭
test_202_posts_load()           # 포스트 로드
test_203_post_click()           # 포스트 클릭
test_204_write_post_button()    # 글쓰기 버튼
test_205_post_like()            # 좋아요 기능
test_206_post_comment()         # 댓글 기능
```

#### 4️⃣ 핫 피플 탭 (TestHotPeopleTab)

```python
test_301_hot_people_tab_click() # 탭 클릭
test_302_people_cards_load()    # 카드 로드
test_303_people_card_click()    # 카드 클릭
test_304_follow_button()        # 팔로우 기능
test_305_people_scroll()        # 스크롤
```

#### 5️⃣ AI 리포트 탭 (TestAIReportTab)

```python
test_401_ai_report_tab_click()  # 탭 클릭
test_402_reports_load()         # 리포트 로드
test_403_report_click()         # 리포트 클릭
test_404_report_like()          # 좋아요 기능
test_405_report_share()         # 공유 기능
```

#### 6️⃣ 멤버십 탭 (TestMembershipTab)

```python
test_501_membership_tab_click() # 탭 클릭
test_502_plans_load()           # 플랜 로드
test_503_plan_click()           # 플랜 클릭
test_504_subscribe_button()     # 구독 버튼
test_505_membership_info()      # 멤버십 정보
```

#### 7️⃣ 리워드 탭 (TestRewardTab)

```python
test_601_reward_tab_click()     # 탭 클릭
test_602_rewards_load()         # 리워드 로드
test_603_reward_claim()         # 리워드 적립
test_604_reward_point_display() # 포인트 표시
test_605_reward_scroll()        # 스크롤
```

#### 8️⃣ 마이페이지 탭 (TestMyPageTab)

```python
test_701_mypage_tab_click()     # 탭 클릭
test_702_profile_section()      # 프로필 섹션
test_703_edit_button()          # 수정 버튼
test_704_settings_menu()        # 설정 메뉴
test_705_activity_history()     # 활동 이력
test_706_account_menu()         # 계정 메뉴
```

#### 9️⃣ 크로스 탭 통합 (TestCrossTabFlow)

```python
test_801_all_tabs_navigation()  # 모든 탭 순차 이동
test_802_home_navigation()      # 홈 네비게이션
test_803_search_function()      # 검색 기능
```

#### 🔟 엣지 케이스 (TestEdgeCases)

```python
test_901_continuous_scroll()    # 연속 스크롤 성능
test_902_rapid_tab_switch()     # 빠른 탭 전환
test_903_network_stability()    # 네트워크 안정성
```

---

## 🔧 XPath 커스터마이징

스크립트의 XPath는 다음과 같이 구성되어 있습니다:

### 기본 패턴

```python
# 탭 선택
tab = login_page.query_selector("//button[contains(text(), '뉴스')]")

# 아이템 목록
items = login_page.query_selector_all("//div[contains(@class, 'news-item')]")

# 버튼
like_btn = login_page.query_selector("//button[contains(@class, 'like')]")
```

### STG 페이지 구조에 맞게 수정

`test_full_web.py`에서 XPath를 찾아 STG 페이지의 실제 구조에 맞게 업데이트하세요:

1. 브라우저에서 개발자 도구 (F12) 열기
2. 각 요소를 검사하여 class 또는 id 확인
3. 해당 XPath 수정

**예시:**

```python
# 변경 전
news_tab = login_page.query_selector("//button[contains(text(), '뉴스')]")

# 변경 후 (만약 class="nav-news"라면)
news_tab = login_page.query_selector("//button[@class='nav-news']")

# 또는 data-testid가 있다면
news_tab = login_page.query_selector("//*[@data-testid='news-tab']")
```

---

## 📸 스크린샷

모든 테스트가 실행될 때마다 스크린샷이 `screenshots/` 폴더에 저장됩니다.

```
screenshots/
├── 20260408_160000_001_profile_main.png
├── 20260408_160001_101_news_tab.png
├── 20260408_160002_102_news_items.png
└── ...
```

스크린샷을 통해:
- 각 테스트의 UI 상태 확인
- 결함 발생 시 증거 수집
- 리그레션 테스트 비교

---

## 🐛 문제 해결

### 1. 브라우저 실행 오류

```
Error: Executable doesn't exist at /...firefox/firefox
```

**해결:**
```bash
python -m playwright install firefox
```

### 2. 요소를 찾을 수 없음

**원인:** XPath가 잘못되었거나 요소 로드가 지연됨

**해결:**
```python
# 대기 시간 증가
time.sleep(3)  # 2초 → 3초

# 또는 명시적 대기
login_page.wait_for_selector("//button[contains(text(), '뉴스')]", timeout=10000)
```

### 3. Google 로그인 실패

**확인 사항:**
- `config.py`의 이메일/비밀번호 정확성
- STG 환경에 계정 생성 여부
- 2FA 설정 (자동화 테스트와 충돌)

---

## 📈 테스트 결과 분석

### 실행 결과 해석

```
test_full_web.py::TestNewsTab::test_101_news_tab_click PASSED
test_full_web.py::TestNewsTab::test_102_news_items_load PASSED
test_full_web.py::TestNewsTab::test_103_news_item_click FAILED
```

- **PASSED:** 테스트 성공
- **FAILED:** 요소 미발견 또는 동작 실패
- **SKIPPED:** 선택적으로 건너뜀
- **ERROR:** 예상치 못한 오류

### 결함 보고

실패한 테스트는:
1. 스크린샷 확인
2. 콘솔 로그 검토
3. XPath 수정
4. 재실행

---

## ✅ 체크리스트

테스트 실행 전 확인:

- [ ] venv 활성화됨
- [ ] requirements.txt 설치됨
- [ ] Firefox 브라우저 설치됨
- [ ] config.py 설정 확인
- [ ] STG_URL 접근 가능
- [ ] Google 계정 생성됨

---

## 📞 지원

문제 발생 시:
1. 최신 로그 확인
2. 스크린샷 검토
3. XPath 업데이트
4. 테스트 재실행

---

**마지막 업데이트:** 2026-04-08
**작성자:** AI Test Automation
**버전:** 2.0 (전체 기능 통합 테스트)
