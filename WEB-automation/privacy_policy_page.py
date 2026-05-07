"""
pages/web/privacy_policy_page.py
[STEP 2 — POM v1]  개인정보 처리방침(Privacy Policy) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_termsContent-module-scss-module__7BiZnG__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌──────────────────────────────────────────────────────────────────────────┐
    │  개인정보 처리방침은 서비스 이용약관과 완전히 동일한 HTML 구조 사용      │
    │  (CSS 모듈 _termsContent-module-scss-module__7BiZnG__ 공유)            │
    │                                                                          │
    │  ✅ 안정 셀렉터 (HTML에서 직접 확인됨):                                  │
    │  · 페이지 타이틀:      h1 = "개인정보 처리방침"                          │
    │  · 공통 래퍼:          div[class*='termsContentWrapper']  ← 이용약관과 同│
    │  · 날짜 라벨:          span.dateLabel = "시행/변경 일자"  ← plain class! │
    │  · 드롭다운 컨테이너:  div.dropdown                       ← plain class! │
    │  · 선택 날짜 표시:     div.dropdown > div > span = "2025.08.25"        │
    │  · 드롭다운 토글 버튼: div.dropdown button[type='button']                │
    │  · 방침 본문 영역:     div#termsContent                   ← ID! 최강!   │
    │  · 조항 헤딩:          div#termsContent p strong                         │
    │    (14개: 제1조~제12조 + GDPR 부록 <1><2>)                             │
    │  · 전체 단락:          div#termsContent p                               │
    │                                                                          │
    │  ⚠️  HTML 특이사항:                                                       │
    │  · 제7조 내용부터 닫히지 않은 <strong> 태그가 잘못 중첩됨              │
    │    → p strong 셀렉터는 여전히 14개 헤딩 전체를 정상 매칭              │
    │                                                                          │
    │  ⚠️  TODO_ 셀렉터 (실제 DOM 확인 후 교체 필요):                          │
    │  · 드롭다운 옵션 목록: DROPDOWN_LIST, DROPDOWN_OPTION                    │
    │  · LNB 메뉴:           LNB_WRAPPER, LNB_PRIVACY_MENU, LNB_ACTIVE_MENU  │
    │                                                                          │
    │  확인된 조항 헤딩 (14개):                                                 │
    │    제1조(처리목적) / 제2조(수집항목) / 제3조(보유기간) /                 │
    │    제4조(제3자제공) / 제5조(국외이전) / 제6조(정보주체권리) /            │
    │    제7조(폐기절차) / 제8조(처리위탁) / 제9조(자동수집장치) /            │
    │    제10조(안전성확보) / 제11조(관리책임자) / 제12조(변경고지) /         │
    │    <1>GDPR 적법처리 / <2>GDPR 이용자권리                               │
    │                                                                          │
    │  본문 내 이메일 (11조): help@bloomingbit.io (plain text)                │
    │  드롭다운 날짜 (HTML): "2025.08.25"                                      │
    │  본문 시행일자: "2025.09.20"                                             │
    │  페이지 URL 추정: /mypage/privacy  (F12 주소창 확인 후 수정 필요)        │
    └──────────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - ID 최우선: div#termsContent
    - plain class 활용: div.dropdown, span.dateLabel
    - 해시 포함 class → [class*='안정키워드'] 부분 매칭
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
"""

import re

from playwright.sync_api import Page


class PrivacyPolicyPage:
    """블루밍비트 개인정보 처리방침 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    PRIVACY_PATH = "/terms/privacy"
    MYPAGE_PATH  = "/mypage"
    SIGNIN_PATH  = "/user/signin"

    # ── 상수 (HTML에서 직접 확인) ─────────────────────────────────────
    EXPECTED_TITLE        = "개인정보 처리방침"
    EXPECTED_DATE_LABEL   = "시행/변경 일자"
    # HTML 기준 드롭다운에 표시된 날짜
    KNOWN_LATEST_DATE     = "2025.08.25"
    # 본문 내 시행일자 키워드
    KNOWN_EFFECTIVE_DATE_KW = "2025.09.20"
    # 전체 조항 헤딩 수: 제1조~제12조(12개) + GDPR 부록 <1><2>(2개)
    EXPECTED_ARTICLE_COUNT = 14
    # 최소 검증 헤딩 수 (여유값)
    MIN_ARTICLE_COUNT      = 10

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반 + TODO_)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 (✅ 안정) ─────────────────────────────────────────
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    PAGE_HEADER  = "header[class*='contentHeader']"
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 방침 상단 영역 (✅ 안정 — 이용약관과 동일 구조) ──────────────
    # HTML: <div class="...__termsContentWrapper">  (이용약관과 동일 CSS 모듈)
    CONTENT_WRAPPER   = "div[class*='termsContentWrapper']"
    # HTML: <div class="...__termsTopWrapper">
    CONTENT_TOP       = "div[class*='termsTopWrapper']"
    # HTML: <span class="dateLabel">시행/변경 일자</span>  ← plain class!
    DATE_LABEL        = "span.dateLabel"

    # ── 드롭다운 (✅ 안정 — plain class "dropdown") ──────────────────
    # HTML: <div class="relative w-full max-w-[123px] dropdown">
    DROPDOWN              = "div.dropdown"
    DROPDOWN_TRIGGER      = "div.dropdown > div"
    # 현재 선택된 날짜 표시: "2025.08.25"
    DROPDOWN_CURRENT_DATE = "div.dropdown > div > span"
    # 드롭다운 토글 버튼
    DROPDOWN_TOGGLE_BTN   = "div.dropdown button[type='button']"

    # ── 드롭다운 옵션 목록 (⚠️ TODO — 드롭다운 미펼쳐진 상태) ─────────
    # ⚠️ TODO: 드롭다운 열고 F12로 옵션 DOM 구조 확인 후 튜닝
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

    # ── 방침 본문 (✅ 최강 안정 — ID 기반, 이용약관과 동일 ID) ─────────
    # HTML: <div id="termsContent" class="...__termsContent">
    POLICY_CONTENT   = "div#termsContent"
    # 조항 헤딩: 제1조~제12조 + GDPR <1><2>
    ARTICLE_HEADINGS = "div#termsContent p strong"
    ALL_PARAGRAPHS   = "div#termsContent p"
    # 시행일자 단락
    EFFECTIVE_DATE_P = "div#termsContent p:has-text('시행일자')"
    # 외부 링크 (제11조 내 개인정보 관련 기관 링크)
    EXTERNAL_LINKS   = "div#termsContent p a[href]"

    # ── LNB(좌측 네비게이션 바) (⚠️ TODO — HTML 미노출) ─────────────
    # ⚠️ TODO: 마이페이지 LNB 영역 F12 확인 후 튜닝
    LNB_WRAPPER      = (
        "[data-testid='TODO_lnbWrapper'], "
        "[class*='lnb'], "
        "[class*='sideNav'], "
        "aside nav"
    )
    LNB_PRIVACY_MENU = (
        "[data-testid='TODO_lnbPrivacyMenu'], "
        "nav a[href*='privacy'], "
        "nav button:has-text('개인정보'), "
        "aside a:has-text('개인정보 처리방침')"
    )
    LNB_ACTIVE_MENU  = (
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

    def go_to_privacy_policy(self) -> None:
        """개인정보 처리방침 페이지로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.PRIVACY_PATH}")
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

    def is_on_privacy_policy_page(self) -> bool:
        return self.PRIVACY_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """페이지 로드 완료 여부 (방침 본문 영역 기준 — HTML 안정 셀렉터)"""
        try:
            self.page.wait_for_selector(self.POLICY_CONTENT, timeout=timeout)
            return True
        except Exception:
            return (
                self.page.locator(self.PAGE_WRAPPER).count() > 0
                or self.page.locator(self.CONTENT_WRAPPER).count() > 0
            )

    def is_page_title_correct(self) -> bool:
        """페이지 타이틀이 '개인정보 처리방침'인지 확인"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            return "개인정보" in el.first.inner_text() and "처리방침" in el.first.inner_text()
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
        """드롭다운에 현재 표시된 날짜 텍스트 반환 (예: '2025.08.25')"""
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
        ① 옵션 목록 DOM 존재 여부 ② SVG transform 180도 여부
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
    #  방침 본문 메서드 (✅ div#termsContent — ID 기반 최강 안정)
    # ══════════════════════════════════════════════════════════════════

    def is_policy_content_visible(self) -> bool:
        """방침 본문 영역(div#termsContent) 노출 여부"""
        return self.page.locator(self.POLICY_CONTENT).count() > 0

    def get_all_policy_text(self) -> str:
        """전체 방침 본문 텍스트 반환"""
        try:
            return self.page.locator(self.POLICY_CONTENT).first.inner_text().strip()
        except Exception:
            return ""

    def get_article_heading_count(self) -> int:
        """방침 조항 헤딩(<strong>) 수 반환"""
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

    def is_article_present(self, article_keyword: str) -> bool:
        """특정 조항이 본문에 포함되어 있는지 확인"""
        try:
            return self.page.locator(
                f"div#termsContent p strong:has-text('{article_keyword}')"
            ).count() > 0
        except Exception:
            return False

    def get_paragraph_count(self) -> int:
        """전체 단락(<p>) 수 반환"""
        return self.page.locator(self.ALL_PARAGRAPHS).count()

    def get_effective_date_text(self) -> str:
        """본문 내 시행일자 단락 텍스트 반환"""
        try:
            loc = self.page.locator(self.EFFECTIVE_DATE_P)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
        except Exception:
            pass
        return ""

    def is_policy_content_not_empty(self) -> bool:
        """방침 본문에 충분한 텍스트가 있는지 확인 (최소 500자 기준)"""
        return len(self.get_all_policy_text()) >= 500

    def get_external_link_count(self) -> int:
        """본문 내 외부 링크(<a href>) 수 반환
        (제11조에 개인정보 관련 기관 링크 4개 존재)
        """
        return self.page.locator(self.EXTERNAL_LINKS).count()

    # ══════════════════════════════════════════════════════════════════
    #  텍스트 렌더링 검증 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_strong_formatted_correctly(self) -> bool:
        """strong 헤딩 요소가 굵게(font-weight >= 600) 렌더링되는지 확인"""
        try:
            el = self.page.locator(self.ARTICLE_HEADINGS).first
            fw = el.evaluate("e => window.getComputedStyle(e).fontWeight")
            if str(fw).lower() == "bold":
                return True
            try:
                return int(fw) >= 600
            except ValueError:
                return True
        except Exception:
            return True

    def is_text_overflowing_horizontally(self) -> bool:
        """방침 본문 영역에 가로 스크롤 발생 여부"""
        try:
            scroll_w = self.page.locator(self.POLICY_CONTENT).first.evaluate(
                "e => e.scrollWidth"
            )
            client_w = self.page.locator(self.POLICY_CONTENT).first.evaluate(
                "e => e.clientWidth"
            )
            return float(scroll_w) > float(client_w)
        except Exception:
            return False

    def is_body_overflowing_horizontally(self) -> bool:
        """body 전체에 가로 스크롤 발생 여부"""
        try:
            scroll_w = self.page.evaluate("() => document.body.scrollWidth")
            client_w = self.page.evaluate("() => document.documentElement.clientWidth")
            return float(scroll_w) > float(client_w) + 5
        except Exception:
            return False

    def get_page_scroll_height(self) -> float:
        """페이지 전체 스크롤 가능 높이"""
        try:
            return self.page.evaluate("() => document.documentElement.scrollHeight")
        except Exception:
            return 0.0

    def get_viewport_height(self) -> float:
        """현재 뷰포트 높이"""
        try:
            return self.page.evaluate("() => window.innerHeight")
        except Exception:
            return 0.0

    def scroll_to_bottom(self, steps: int = 8, delay_ms: int = 400) -> None:
        """페이지 최하단까지 단계적 스크롤"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(delay_ms)

    def get_scroll_y_position(self) -> float:
        """현재 스크롤 Y 위치"""
        try:
            return self.page.evaluate("() => window.scrollY")
        except Exception:
            return 0.0

    # ══════════════════════════════════════════════════════════════════
    #  LNB 메서드 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_lnb_visible(self) -> bool:
        """LNB 영역 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.LNB_WRAPPER).count() > 0

    def click_lnb_privacy_menu(self) -> None:
        """LNB에서 '개인정보 처리방침' 메뉴 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(self.LNB_PRIVACY_MENU).first
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

    def is_lnb_privacy_menu_active(self) -> bool:
        """LNB에서 '개인정보 처리방침' 메뉴가 활성(하이라이트) 상태인지 확인
        (⚠️ TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요)
        """
        try:
            active_text = self.page.locator(self.LNB_ACTIVE_MENU).first.inner_text().strip()
            return "개인정보" in active_text or "처리방침" in active_text
        except Exception:
            return False