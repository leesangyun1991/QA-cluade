"""
pages/web/press_ethics_code_page.py
[STEP 2 — POM v1]  언론윤리강령(Press Ethics Code) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_termsContent-module-scss-module__7BiZnG__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │  언론윤리강령은 이전 페이지들과 동일한 CSS 모듈(7BiZnG) 공유                 │
    │                                                                              │
    │  ✅ 안정 셀렉터 (HTML에서 직접 확인됨):                                      │
    │  · 페이지 타이틀:      h1 = "언론윤리강령"                                   │
    │  · 공통 래퍼:          div[class*='termsContentWrapper']                     │
    │  · 날짜 라벨:          span.dateLabel  ← plain class!                       │
    │  · 드롭다운 컨테이너:  div.dropdown    ← plain class!                       │
    │  · 선택 날짜 표시:     div.dropdown > div > span = "2022.10.07"             │
    │  · 드롭다운 토글 버튼: div.dropdown button[type='button']                    │
    │  · 강령 본문 영역:     div#termsContent  ← ID! 최강!                        │
    │  · 조항 헤딩:          div#termsContent p strong                             │
    │    ← <strong> 사용! (청소년보호정책의 <b>와 달리 <strong> 복귀!)            │
    │    11개: 윤리강령(intro) + 제1조~제10조                                      │
    │  · 전체 단락:          div#termsContent p (11개)                            │
    │                                                                              │
    │  ⚠️  청소년보호정책(youth_protection)과의 핵심 차이점:                        │
    │  · 볼드 태그: <strong> (청소년보호정책은 <b>였음!)                           │
    │    → div#termsContent p strong 셀렉터 정상 동작 (11개 반환)                 │
    │  · 각 조항이 <p><strong>제목</strong><br>내용</p> 1개 태그 구조              │
    │    (제목과 본문 내용이 같은 <p> 태그 안에 존재)                              │
    │  · 조항 간 <br> 태그가 단독으로 존재 (p 태그 밖)                            │
    │  · 본문 구조: div#termsContent > div > p (span 래퍼 없음)                  │
    │  · 관리자 정보 없음 (청소년보호정책과 다름)                                  │
    │  · mailto 링크 없음                                                          │
    │                                                                              │
    │  ⚠️  TODO_ 셀렉터 (실제 DOM 확인 후 교체 필요):                              │
    │  · 드롭다운 옵션 목록: DROPDOWN_LIST, DROPDOWN_OPTION                        │
    │  · LNB 메뉴:           LNB_WRAPPER, LNB_ETHICS_MENU, LNB_ACTIVE_MENU       │
    │                                                                              │
    │  확인된 조항 (11개):                                                          │
    │    윤리강령(intro) / 제1조(언론의 자유) / 제2조(언론의 책임) /               │
    │    제3조(인격권 보호) / 제4조(약자 보호) / 제5조(저작권 보호) /              │
    │    제6조(이해 상충) / 제7조(부당 게재 금지) / 제8조(기사·광고 분리) /        │
    │    제9조(광고 신뢰성) / 제10조(이용자 참여)                                  │
    │                                                                              │
    │  드롭다운 날짜 (HTML): "2022.10.07"                                          │
    │  페이지 URL 추정: /mypage/press-ethics  (F12 주소창 확인 후 수정 필요)       │
    └──────────────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - ID 최우선: div#termsContent
    - plain class 활용: div.dropdown, span.dateLabel
    - 조항 헤딩: p strong  (<strong> 태그 — 청소년보호정책의 <b>와 다름!)
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
"""

import re

from playwright.sync_api import Page


class PressEthicsCodePage:
    """블루밍비트 언론윤리강령 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    ETHICS_CODE_PATH = "/terms/ethics"
    MYPAGE_PATH      = "/mypage"
    SIGNIN_PATH      = "/user/signin"

    # ── 상수 (HTML에서 직접 확인) ─────────────────────────────────────
    EXPECTED_TITLE      = "언론윤리강령"
    EXPECTED_DATE_LABEL = "시행/변경 일자"
    # HTML 기준 드롭다운에 표시된 날짜 (가장 오래된 날짜)
    KNOWN_LATEST_DATE   = "2022.10.07"
    # 조항 수: 윤리강령(intro) + 제1조~제10조 = 11개
    EXPECTED_ARTICLE_COUNT = 11
    MIN_ARTICLE_COUNT      = 5  # 최소 검증 헤딩 수 (여유값)

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반 + TODO_)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 (✅ 안정 — 이전 페이지들과 동일) ─────────────────
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    PAGE_HEADER  = "header[class*='contentHeader']"
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 강령 상단 영역 (✅ 안정 — 동일 CSS 모듈) ─────────────────────
    CONTENT_WRAPPER   = "div[class*='termsContentWrapper']"
    CONTENT_TOP       = "div[class*='termsTopWrapper']"
    # HTML: <span class="dateLabel">시행/변경 일자</span>  ← plain class!
    DATE_LABEL        = "span.dateLabel"

    # ── 드롭다운 (✅ 안정 — plain class "dropdown") ──────────────────
    DROPDOWN              = "div.dropdown"
    DROPDOWN_TRIGGER      = "div.dropdown > div"
    # 현재 선택 날짜: "2022.10.07"
    DROPDOWN_CURRENT_DATE = "div.dropdown > div > span"
    DROPDOWN_TOGGLE_BTN   = "div.dropdown button[type='button']"

    # ── 드롭다운 옵션 목록 (⚠️ TODO — 드롭다운 미펼쳐진 상태) ─────────
    DROPDOWN_LIST   = (
        "[data-testid='TODO_dropdownList'], "
        "div.dropdown ul, "
        "div.dropdown [role='listbox'], "
        "div.dropdown > div:nth-child(2)"
    )
    DROPDOWN_OPTION = (
        "[data-testid='TODO_dropdownOption'], "
        "div.dropdown li, "
        "div.dropdown [role='option'], "
        "div.dropdown > div:nth-child(2) > div"
    )

    # ── 강령 본문 (✅ 최강 안정 — ID 기반, 동일 ID) ──────────────────
    # HTML: <div id="termsContent" class="...__termsContent">
    ETHICS_CONTENT   = "div#termsContent"
    # 조항 헤딩: <p><strong>조항명</strong><br>내용</p> 구조
    # ✅ <strong> 태그 사용 (청소년보호정책의 <b>와 다름! 이용약관 등과 동일)
    ARTICLE_HEADINGS = "div#termsContent p strong"
    ALL_PARAGRAPHS   = "div#termsContent p"

    # ── 특정 조항 셀렉터 (✅ 안정 — 텍스트 기반) ─────────────────────
    # HTML에서 각 조항 <strong> 텍스트 직접 확인됨
    INTRO_HEADING   = "div#termsContent p strong:has-text('윤리강령')"
    ARTICLE_1       = "div#termsContent p strong:has-text('제1조')"
    ARTICLE_5       = "div#termsContent p strong:has-text('제5조')"
    ARTICLE_10      = "div#termsContent p strong:has-text('제10조')"

    # ── LNB(좌측 네비게이션 바) (⚠️ TODO — HTML 미노출) ─────────────
    LNB_WRAPPER     = (
        "[data-testid='TODO_lnbWrapper'], "
        "[class*='lnb'], "
        "[class*='sideNav'], "
        "aside nav"
    )
    LNB_ETHICS_MENU = (
        "[data-testid='TODO_lnbEthicsMenu'], "
        "nav a[href*='ethics'], "
        "nav button:has-text('언론윤리'), "
        "aside a:has-text('언론윤리강령')"
    )
    LNB_ACTIVE_MENU = (
        "[data-testid='TODO_lnbActiveMenu'], "
        "nav a[class*='active'], "
        "aside a[class*='active']"
    )

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def _safe_goto(self, url: str) -> None:
        """about:blank 충돌 및 ERR_ABORTED 방지하는 안전한 goto (최대 3회 재시도)"""
        for attempt in range(3):
            try:
                self.page.wait_for_timeout(300)
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Exception as e:
                err = str(e)
                if attempt < 2 and (
                    "about:blank" in err
                    or "interrupted" in err
                    or "ERR_ABORTED" in err
                ):
                    self.page.wait_for_timeout(1_000)
                    continue
                raise

    def go_to_ethics_code(self) -> None:
        """언론윤리강령 페이지로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.ETHICS_CODE_PATH}")
        self.page.wait_for_timeout(600)

    def go_to_mypage(self) -> None:
        """마이페이지(/mypage)로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.MYPAGE_PATH}")
        self.page.wait_for_timeout(500)

    def go_back(self) -> None:
        """브라우저 뒤로가기"""
        try:
            self.page.go_back(wait_until="domcontentloaded")
        except Exception:
            pass
        self.page.wait_for_timeout(600)

    def refresh_page(self) -> None:
        """현재 페이지 새로고침"""
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(600)

    def get_current_url(self) -> str:
        return self.page.url

    def is_on_ethics_code_page(self) -> bool:
        return self.ETHICS_CODE_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """페이지 로드 완료 여부 (강령 본문 영역 기준)"""
        try:
            self.page.wait_for_selector(self.ETHICS_CONTENT, timeout=timeout)
            return True
        except Exception:
            return (
                self.page.locator(self.PAGE_WRAPPER).count() > 0
                or self.page.locator(self.CONTENT_WRAPPER).count() > 0
            )

    def is_page_title_correct(self) -> bool:
        """페이지 타이틀이 '언론윤리강령'인지 확인"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            return "언론윤리강령" in el.first.inner_text()
        except Exception:
            return False

    def get_page_title_text(self) -> str:
        """페이지 h1 타이틀 텍스트 반환"""
        try:
            return self.page.locator(self.PAGE_TITLE).first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  드롭다운 메서드 (✅ div.dropdown plain class — 안정)
    # ══════════════════════════════════════════════════════════════════

    def is_dropdown_visible(self) -> bool:
        """드롭다운 컨테이너 노출 여부"""
        return self.page.locator(self.DROPDOWN).count() > 0

    def get_dropdown_current_date(self) -> str:
        """드롭다운에 현재 표시된 날짜 텍스트 반환 (예: '2022.10.07')"""
        try:
            return self.page.locator(self.DROPDOWN_CURRENT_DATE).first.inner_text().strip()
        except Exception:
            return ""

    def is_date_format_valid(self, date_text: str) -> bool:
        """날짜 텍스트가 'YYYY.MM.DD' 형식인지 확인"""
        if not date_text.strip():
            return False
        return bool(re.match(r"\d{4}\.\d{2}\.\d{2}", date_text.strip()))

    def is_date_label_visible(self) -> bool:
        """'시행/변경 일자' 라벨 노출 여부 (span.dateLabel — plain class)"""
        return self.page.locator(self.DATE_LABEL).count() > 0

    def get_date_label_text(self) -> str:
        """날짜 라벨 텍스트 반환"""
        try:
            return self.page.locator(self.DATE_LABEL).first.inner_text().strip()
        except Exception:
            return ""

    def click_dropdown_toggle(self) -> None:
        """드롭다운 토글 버튼 클릭
        ① 버튼(button) 우선 클릭, ② 드롭다운 트리거(div) 폴백
        """
        btn = self.page.locator(self.DROPDOWN_TOGGLE_BTN).first
        try:
            btn.wait_for(state="visible", timeout=3_000)
            btn.click(timeout=3_000)
            self.page.wait_for_timeout(500)
            return
        except Exception:
            pass
        try:
            trigger = self.page.locator(self.DROPDOWN_TRIGGER).first
            trigger.wait_for(state="attached", timeout=3_000)
            trigger.click(force=True)
            self.page.wait_for_timeout(500)
        except Exception:
            pass

    def is_dropdown_open(self) -> bool:
        """드롭다운이 열린 상태인지 확인
        ① 옵션 목록 DOM 존재 ② SVG transform 180도 여부
        """
        if self.page.locator(self.DROPDOWN_LIST).count() > 0:
            return True
        try:
            svg_style = self.page.locator(
                "div.dropdown button[type='button']"
            ).first.evaluate("e => e.style.transform")
            return "180" in str(svg_style)
        except Exception:
            return False

    def get_dropdown_option_count(self) -> int:
        """드롭다운 옵션 항목 수 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.DROPDOWN_OPTION).count()

    def get_dropdown_option_texts(self) -> list:
        """드롭다운 옵션 텍스트 목록 반환 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        texts = []
        try:
            options = self.page.locator(self.DROPDOWN_OPTION).all()
            for opt in options:
                txt = opt.inner_text().strip()
                if txt:
                    texts.append(txt)
        except Exception:
            pass
        return texts

    def select_dropdown_option_by_index(self, index: int = 0) -> str:
        """드롭다운에서 index 번째 옵션 선택 후 선택된 날짜 반환
        ⚠️ TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요
        """
        try:
            opt = self.page.locator(self.DROPDOWN_OPTION).nth(index)
            opt.wait_for(state="visible", timeout=3_000)
            selected_text = opt.inner_text().strip()
            opt.click(force=True)
            self.page.wait_for_timeout(800)
            return selected_text
        except Exception:
            return ""

    def select_different_version(self) -> str:
        """현재 선택된 날짜와 다른 과거 버전 선택. 선택된 날짜 반환 (없으면 빈 문자열)"""
        current_date = self.get_dropdown_current_date()
        self.click_dropdown_toggle()
        self.page.wait_for_timeout(600)

        options = self.page.locator(self.DROPDOWN_OPTION).all()
        for opt in options:
            try:
                txt = opt.inner_text().strip()
                if txt and txt != current_date and self.is_date_format_valid(txt):
                    opt.click(force=True)
                    self.page.wait_for_timeout(800)
                    return txt
            except Exception:
                continue
        return ""

    # ══════════════════════════════════════════════════════════════════
    #  강령 본문 메서드 (✅ div#termsContent — ID 기반 최강 안정)
    # ══════════════════════════════════════════════════════════════════

    def is_ethics_content_visible(self) -> bool:
        """강령 본문 영역(div#termsContent) 노출 여부"""
        return self.page.locator(self.ETHICS_CONTENT).count() > 0

    def get_all_ethics_text(self) -> str:
        """전체 강령 본문 텍스트 반환"""
        try:
            return self.page.locator(self.ETHICS_CONTENT).first.inner_text().strip()
        except Exception:
            return ""

    def is_ethics_content_not_empty(self) -> bool:
        """강령 본문에 충분한 텍스트가 있는지 확인 (최소 200자 기준)"""
        return len(self.get_all_ethics_text()) >= 200

    def get_article_heading_count(self) -> int:
        """조항 헤딩(<strong>) 수 반환
        ✅ <strong> 태그 사용 (이전 이용약관·개인정보처리방침·커뮤니티와 동일)
        """
        return self.page.locator(self.ARTICLE_HEADINGS).count()

    def get_article_heading_texts(self) -> list:
        """모든 조항 헤딩 텍스트 목록 반환"""
        headings = []
        try:
            els = self.page.locator(self.ARTICLE_HEADINGS).all()
            for el in els:
                txt = el.inner_text().strip()
                if txt:
                    headings.append(txt)
        except Exception:
            pass
        return headings

    def get_paragraph_count(self) -> int:
        """전체 단락(<p>) 수 반환"""
        return self.page.locator(self.ALL_PARAGRAPHS).count()

    # ── 개별 조항 검증 메서드 (✅ 안정 — has-text 기반) ──────────────

    def is_intro_heading_present(self) -> bool:
        """윤리강령 인트로 헤딩 노출 여부"""
        return self.page.locator(self.INTRO_HEADING).count() > 0

    def is_article_1_present(self) -> bool:
        """제1조(언론의 자유) 헤딩 노출 여부"""
        return self.page.locator(self.ARTICLE_1).count() > 0

    def is_article_5_present(self) -> bool:
        """제5조(저작권 보호) 헤딩 노출 여부"""
        return self.page.locator(self.ARTICLE_5).count() > 0

    def is_article_10_present(self) -> bool:
        """제10조(이용자 참여) 헤딩 노출 여부 — 마지막 조항"""
        return self.page.locator(self.ARTICLE_10).count() > 0

    def are_key_articles_present(self) -> bool:
        """핵심 조항(intro, 제1조, 제10조)이 모두 노출되는지 확인"""
        return (
            self.is_intro_heading_present()
            and self.is_article_1_present()
            and self.is_article_10_present()
        )

    def get_missing_key_articles(self) -> list:
        """미노출 핵심 조항 이름 목록 반환"""
        missing = []
        checks = {
            "윤리강령(intro)": self.is_intro_heading_present(),
            "제1조(언론의 자유)": self.is_article_1_present(),
            "제5조(저작권 보호)": self.is_article_5_present(),
            "제10조(이용자 참여)": self.is_article_10_present(),
        }
        return [name for name, present in checks.items() if not present]

    def get_article_1_text(self) -> str:
        """제1조 전체 단락 텍스트 (헤딩 + 본문 포함)
        ※ 언론윤리강령은 제목과 본문이 같은 <p> 태그 안에 있음
        """
        try:
            # <p><strong>제1조...</strong><br>본문...</p> 구조
            loc = self.page.locator(self.ARTICLE_1).first
            # strong의 부모 p 요소 텍스트
            return loc.evaluate("e => e.closest('p')?.innerText || ''").strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  LNB 메서드 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_lnb_visible(self) -> bool:
        """LNB 영역 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.LNB_WRAPPER).count() > 0

    def click_lnb_ethics_menu(self) -> None:
        """LNB에서 '언론윤리강령' 메뉴 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(self.LNB_ETHICS_MENU).first
        try:
            loc.wait_for(state="visible", timeout=3_000)
            loc.click(timeout=3_000)
            self.page.wait_for_timeout(800)
            return
        except Exception:
            pass
        try:
            loc.wait_for(state="attached", timeout=5_000)
            loc.click(force=True)
            self.page.wait_for_timeout(800)
        except Exception:
            pass

    def is_lnb_ethics_menu_active(self) -> bool:
        """LNB에서 '언론윤리강령' 메뉴가 활성(하이라이트) 상태인지 확인
        (⚠️ TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요)
        """
        try:
            active_text = self.page.locator(self.LNB_ACTIVE_MENU).first.inner_text().strip()
            return "윤리" in active_text or "언론" in active_text
        except Exception:
            return False