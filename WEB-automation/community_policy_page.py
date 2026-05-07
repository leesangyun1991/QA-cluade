"""
pages/web/community_policy_page.py
[STEP 2 — POM v1]  커뮤니티 운영정책(Community Operation Policy) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_termsContent-module-scss-module__7BiZnG__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │  커뮤니티 운영정책은 이용약관·개인정보처리방침과 동일한 CSS 모듈(7BiZnG) 공유 │
    │                                                                              │
    │  ✅ 안정 셀렉터 (HTML에서 직접 확인됨):                                      │
    │  · 페이지 타이틀:      h1 = "커뮤니티 운영정책"                              │
    │  · 공통 래퍼:          div[class*='termsContentWrapper']                     │
    │  · 날짜 라벨:          span.dateLabel = "시행/변경 일자"  ← plain class!     │
    │  · 드롭다운 컨테이너:  div.dropdown                       ← plain class!     │
    │  · 선택 날짜 표시:     div.dropdown > div > span = "2025.09.02"             │
    │  · 드롭다운 토글 버튼: div.dropdown button[type='button']                    │
    │  · 정책 본문 영역:     div#termsContent                   ← ID! 최강!       │
    │  · 섹션 헤딩:          div#termsContent p strong                             │
    │    (17개: 1. ~ 1.4, 2. ~ 2.9, 3., 4.)                                      │
    │  · 전체 단락:          div#termsContent p                                   │
    │  · mailto 링크(실제!): div#termsContent a[href^='mailto:']                  │
    │    ← 이용자불만처리(plain text)와 달리 실제 <a href="mailto:"> 링크 존재!   │
    │                                                                              │
    │  ⚠️  이전 페이지(이용약관·개인정보처리방침)와의 차이점:                       │
    │  · 본문 구조: div#termsContent > div > p  (span 래퍼 없음)                 │
    │  · 섹션 번호 형식: 조항 번호(1., 2.) + 소항목(1.1, 2.9) 방식               │
    │  · 시행일자 형식: "2025년 9월 9일" (한글, YYYY.MM.DD 아님)                 │
    │                                                                              │
    │  ⚠️  TODO_ 셀렉터 (실제 DOM 확인 후 교체 필요):                              │
    │  · 드롭다운 옵션 목록: DROPDOWN_LIST, DROPDOWN_OPTION                        │
    │  · LNB 메뉴:           LNB_WRAPPER, LNB_COMMUNITY_MENU, LNB_ACTIVE_MENU    │
    │                                                                              │
    │  확인된 섹션 헤딩 (17개):                                                     │
    │    1. 회원 정책 및 커뮤니티 이용 / 1.1 회원가입 / 1.2 회원정보 변경 /       │
    │    1.3 커뮤니티 소개 / 1.4 댓글·답글 정책 /                                 │
    │    2. 커뮤니티 제재 항목 / 2.1 욕설, 인신공격 / ... / 2.9 기본적인 윤리 /   │
    │    3. 제재 기준과 종류 / 4. 커뮤니티 이용 제재 유의 사항                     │
    │                                                                              │
    │  본문 mailto 링크: <a href="mailto:help@bloomingbit.io">                    │
    │  드롭다운 날짜 (HTML): "2025.09.02"                                          │
    │  시행일자 (본문): "2025년 9월 9일" (한글 형식)                              │
    │  페이지 URL 추정: /mypage/community-policy  (F12 주소창 확인 후 수정 필요)   │
    └──────────────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - ID 최우선: div#termsContent
    - plain class 활용: div.dropdown, span.dateLabel
    - 해시 포함 class → [class*='안정키워드'] 부분 매칭
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
"""

import re

from playwright.sync_api import Page


class CommunityPolicyPage:
    """블루밍비트 커뮤니티 운영정책 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    COMMUNITY_POLICY_PATH = "/terms/community"
    MYPAGE_PATH           = "/mypage"
    SIGNIN_PATH           = "/user/signin"

    # ── 상수 (HTML에서 직접 확인) ─────────────────────────────────────
    EXPECTED_TITLE        = "커뮤니티 운영정책"
    EXPECTED_DATE_LABEL   = "시행/변경 일자"
    # HTML 기준 드롭다운에 표시된 날짜 (최신 버전)
    KNOWN_LATEST_DATE     = "2025.09.02"
    # 본문 내 시행일자 (한글 형식 — YYYY.MM.DD 아님)
    KNOWN_EFFECTIVE_DATE_KW = "2025년 9월 9일"
    # 전체 섹션 헤딩 수: 1. + 1.1~1.4 + 2. + 2.1~2.9 + 3. + 4. = 17개
    EXPECTED_SECTION_COUNT = 17
    # 최소 검증 헤딩 수 (여유값)
    MIN_SECTION_COUNT      = 10
    # 본문 내 이메일 주소 (실제 mailto 링크로 존재)
    EXPECTED_EMAIL         = "help@bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반 + TODO_)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 (✅ 안정 — 이용약관·개인정보처리방침과 동일) ──────
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    PAGE_HEADER  = "header[class*='contentHeader']"
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 정책 상단 영역 (✅ 안정 — 동일 CSS 모듈) ─────────────────────
    # HTML: <div class="...__termsContentWrapper">
    CONTENT_WRAPPER   = "div[class*='termsContentWrapper']"
    # HTML: <div class="...__termsTopWrapper">
    CONTENT_TOP       = "div[class*='termsTopWrapper']"
    # HTML: <span class="dateLabel">시행/변경 일자</span>  ← plain class!
    DATE_LABEL        = "span.dateLabel"

    # ── 드롭다운 (✅ 안정 — plain class "dropdown") ──────────────────
    DROPDOWN              = "div.dropdown"
    DROPDOWN_TRIGGER      = "div.dropdown > div"
    # 현재 선택된 날짜 표시: "2025.09.02"
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

    # ── 정책 본문 (✅ 최강 안정 — ID 기반, 이용약관·개인정보처리방침과 동일 ID) ─
    # HTML: <div id="termsContent" class="...__termsContent">
    POLICY_CONTENT    = "div#termsContent"
    # 본문 구조: div#termsContent > div > p (span 래퍼 없음 — 이용약관과 상이)
    CONTENT_TEXT_DIV  = "div#termsContent > div"
    # 섹션 헤딩: 1. ~ 4. 및 하위 항목 (17개)
    SECTION_HEADINGS  = "div#termsContent p strong"
    ALL_PARAGRAPHS    = "div#termsContent p"
    # 시행일자 단락 (한글 형식: "2025년 9월 9일")
    EFFECTIVE_DATE_P  = "div#termsContent p:has-text('시행일자')"

    # ── mailto 링크 (✅ 안정 — 실제 <a href="mailto:"> 태그로 존재!) ──
    # HTML: <a href="mailto:help@bloomingbit.io">help@bloomingbit.io</a>
    MAILTO_LINK = "div#termsContent a[href^='mailto:']"
    # 이메일 포함 단락
    EMAIL_PARA  = "div#termsContent p:has-text('help@bloomingbit.io')"

    # ── LNB(좌측 네비게이션 바) (⚠️ TODO — HTML 미노출) ─────────────
    # ⚠️ TODO: 마이페이지 LNB 영역 F12 확인 후 튜닝
    LNB_WRAPPER          = (
        "[data-testid='TODO_lnbWrapper'], "
        "[class*='lnb'], "
        "[class*='sideNav'], "
        "aside nav"
    )
    LNB_COMMUNITY_MENU   = (
        "[data-testid='TODO_lnbCommunityMenu'], "
        "nav a[href*='community'], "
        "nav button:has-text('커뮤니티 운영정책'), "
        "aside a:has-text('커뮤니티 운영정책')"
    )
    LNB_ACTIVE_MENU      = (
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

    def go_to_community_policy(self) -> None:
        """커뮤니티 운영정책 페이지로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.COMMUNITY_POLICY_PATH}")
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

    def is_on_community_policy_page(self) -> bool:
        return self.COMMUNITY_POLICY_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """페이지 로드 완료 여부 (정책 본문 영역 기준 — HTML 안정 셀렉터)"""
        try:
            self.page.wait_for_selector(self.POLICY_CONTENT, timeout=timeout)
            return True
        except Exception:
            return (
                self.page.locator(self.PAGE_WRAPPER).count() > 0
                or self.page.locator(self.CONTENT_WRAPPER).count() > 0
            )

    def is_page_title_correct(self) -> bool:
        """페이지 타이틀이 '커뮤니티 운영정책'인지 확인"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            text = el.first.inner_text()
            return "커뮤니티" in text and "운영정책" in text
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
        """드롭다운에 현재 표시된 날짜 텍스트 반환 (예: '2025.09.02')"""
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
    #  정책 본문 메서드 (✅ div#termsContent — ID 기반 최강 안정)
    # ══════════════════════════════════════════════════════════════════

    def is_policy_content_visible(self) -> bool:
        """정책 본문 영역(div#termsContent) 노출 여부"""
        return self.page.locator(self.POLICY_CONTENT).count() > 0

    def get_all_policy_text(self) -> str:
        """전체 정책 본문 텍스트 반환"""
        try:
            return self.page.locator(self.POLICY_CONTENT).first.inner_text().strip()
        except Exception:
            return ""

    def get_section_heading_count(self) -> int:
        """정책 섹션 헤딩(<strong>) 수 반환"""
        return self.page.locator(self.SECTION_HEADINGS).count()

    def get_section_heading_texts(self) -> list:
        """모든 섹션 헤딩 텍스트 목록 반환"""
        headings = []
        try:
            els = self.page.locator(self.SECTION_HEADINGS).all()
            for el in els:
                txt = el.inner_text().strip()
                if txt:
                    headings.append(txt)
        except Exception:
            pass
        return headings

    def is_section_present(self, section_keyword: str) -> bool:
        """특정 섹션 키워드가 본문에 포함되어 있는지 확인"""
        try:
            return self.page.locator(
                f"div#termsContent p strong:has-text('{section_keyword}')"
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
        """정책 본문에 충분한 텍스트가 있는지 확인 (최소 500자 기준)"""
        return len(self.get_all_policy_text()) >= 500

    # ══════════════════════════════════════════════════════════════════
    #  mailto 링크 메서드 (✅ 실제 <a href="mailto:"> 태그로 존재!)
    # ══════════════════════════════════════════════════════════════════

    def is_mailto_link_present(self) -> bool:
        """실제 mailto 링크 요소 존재 여부
        ✅ HTML에서 <a href="mailto:help@bloomingbit.io"> 태그로 직접 확인됨
        """
        return self.page.locator(self.MAILTO_LINK).count() > 0

    def get_mailto_href(self) -> str:
        """mailto 링크의 href 속성값 반환 (예: 'mailto:help@bloomingbit.io')"""
        try:
            return self.page.locator(self.MAILTO_LINK).first.get_attribute("href") or ""
        except Exception:
            return ""

    def get_mailto_display_text(self) -> str:
        """mailto 링크의 표시 텍스트 반환 (예: 'help@bloomingbit.io')"""
        try:
            return self.page.locator(self.MAILTO_LINK).first.inner_text().strip()
        except Exception:
            return ""

    def is_mailto_email_correct(self) -> bool:
        """mailto 링크의 이메일 주소가 정확한지 확인"""
        href = self.get_mailto_href()
        display = self.get_mailto_display_text()
        expected = self.EXPECTED_EMAIL
        return (
            f"mailto:{expected}" == href
            and expected in display
        )

    # ══════════════════════════════════════════════════════════════════
    #  LNB 메서드 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_lnb_visible(self) -> bool:
        """LNB 영역 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.LNB_WRAPPER).count() > 0

    def click_lnb_community_menu(self) -> None:
        """LNB에서 '커뮤니티 운영정책' 메뉴 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(self.LNB_COMMUNITY_MENU).first
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

    def is_lnb_community_menu_active(self) -> bool:
        """LNB에서 '커뮤니티 운영정책' 메뉴가 활성(하이라이트) 상태인지 확인
        (⚠️ TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요)
        """
        try:
            active_text = self.page.locator(self.LNB_ACTIVE_MENU).first.inner_text().strip()
            return "커뮤니티" in active_text and ("운영정책" in active_text or "정책" in active_text)
        except Exception:
            return False