# 📱 WEB 자동화 테스트 — 완전 가이드

## 📂 파일 구조

```
/Users/bloomingbit/Documents/LEESANGYUN/automation/appium/WEB/
├── run_web_tests.sh       ← 자동 실행 스크립트 ⭐
├── config.py              ← 설정 파일
├── conftest.py            ← pytest fixture
├── test_full_web.py       ← 43개 TC (생성 필요)
├── requirements.txt       ← 의존성
├── QUICK_START.md        ← 빠른 시작
└── screenshots/          ← 결과 (생성됨)
```

---

## 🚀 즉시 실행 (3줄)

```bash
cd /Users/bloomingbit/Documents/LEESANGYUN/automation/appium/WEB
bash run_web_tests.sh
```

---

## ⚙️ 첫 실행 준비 (한 번만)

```bash
cd /Users/bloomingbit/Documents/LEESANGYUN/automation/appium/WEB

# 1️⃣ 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 2️⃣ 의존성 설치
pip install -r requirements.txt

# 3️⃣ Playwright 설치
playwright install chromium

# 이제 준비 완료! 아래 명령어 실행:
bash run_web_tests.sh
```

---

## 🎯 테스트 옵션

```bash
# 전체 43개 TC
bash run_web_tests.sh

# 뉴스 탭만 (14개)
bash run_web_tests.sh News

# 커뮤니티만 (6개)
bash run_web_tests.sh Community

# 특정 TC만
bash run_web_tests.sh test_01
```

---

## 📊 테스트 내용 (43개 TC)

### 1️⃣ 뉴스 탭 (14개)
- 탭 진입 → 목록 스크롤 → 기사 상세 → 좋아요/북마크 → 공유 → 댓글 → 검색 → 필터 → 정렬

### 2️⃣ 커뮤니티 탭 (6개)
- 진입 → 목록 → 게시글 상세 → 좋아요 → 댓글 → 뒤로

### 3️⃣ 핫 피플 탭 (5개)
- 진입 → 목록 → 프로필 → 스크롤 → 뒤로

### 4️⃣ 리워드 탭 (3개)
- 진입 → 스크롤 → 항목 탭

### 5️⃣ 내 정보 탭 (5개)
- 진입 → 스크롤 → 설정 → 알림 → 프로필 편집

### 6️⃣ 크로스 플로우 (5개)
- 탭 순차 → 뉴스→커뮤니티 → 새로고침 → 빠른 전환 → 브라우저 뒤로

### 7️⃣ 엣지 케이스 (5개)
- 빈 댓글 → 특수문자 → 이중 클릭 → 스크롤 극단값 → 반응형

---

## 🔧 고급 설정

### 브라우저 보이기

```python
# config.py 수정
HEADLESS = False  # 브라우저 UI 표시
```

### 느린 실행

```python
# config.py 수정
SLOW_MO = 1000  # 1초 간격
```

---

## ✅ 완료 후 확인

```bash
# 스크린샷 확인
open ./screenshots/

# pytest 결과
# → ✓ 43 passed
```

---

## 📞 문제 해결

| 문제 | 해결 |
|------|------|
| Chromium not found | `playwright install chromium` |
| Timeout 에러 | `config.py`에서 `TIMEOUT` 값 증가 |
| Element not found | 브라우저 개발자 도구에서 actual 셀렉터 확인 후 `config.py` 업데이트 |
| 로그인 실패 | Google 계정 2단계 인증 비활성화 후 재시도 |

---

**준비 완료! 이제 실행하세요:** 👇

```bash
bash run_web_tests.sh
```
