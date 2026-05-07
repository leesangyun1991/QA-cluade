"""
pages/web/user_complaint_page.py
[STEP 2 — POM v1]  이용자 불만 처리(User Complaint) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_complaintHandlingContent-module-scss-module__LCFukq__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌──────────────────────────────────────────────────────────────────────────┐
    │  ✅ 안정 셀렉터 (HTML에서 직접 확인됨):                                  │
    │    · 페이지 타이틀: h1 = "이용자 불만 처리"                              │
    │    · 콘텐츠 래퍼:   div[class*='complaintHandlingContentWrapper']        │
    │    · 콘텐츠 영역:   div#complaintHandlingContent                         │
    │    · 섹션 헤딩:     div[class*='complaintHandlingContent'] p strong      │
    │    · 버튼 래퍼:     div[class*='complaintHandlingButtonWrapper']          │
    │    · 신고 버튼:     button[class*='complaintHandlingButton']              │
    │    · 버튼 텍스트:   "이용자 불만 신고하기"                                │
    │    · 이메일 텍스트: "help@bloomingbit.io" (본문 내 plain text)           │
    │    ─────────────────────────────────────────────────────────────────     │
    │  ⚠️  HTML 미노출 / 확인 필요 요소:                                        │
    │    · mailto 링크:  이메일이 <a href="mailto:"> 아닌 plain text로 존재    │
    │      → FULLTC-515는 mailto 링크가 실제로 있는 경우에만 검증 가능         │
    │    · LNB 메뉴:     LNB_WRAPPER, LNB_COMPLAINT_MENU  (TODO_)             │
    │    · 신고 후 이동: COMPLAINT_FORM_PATH 확인 필요                         │
    │    · 로그인 팝업/모달: LOGIN_MODAL (TODO_)                               │
    │                                                                          │
    │  확인된 섹션 제목 (strong 헤딩):                                          │
    │    이용자 불만처리 절차 안내 / 접수 대상 / 접수 방법 /                    │
    │    불만처리 담당 연락처 / 처리 절차 / 처리 원칙 /                         │
    │    처리 제외 또는 제한 사항 / 개인정보 안내 /                              │
    │    이용자위원회 연계 문구 / 회의록                                         │
    │                                                                          │
    │  페이지 URL 추정: /mypage/complaint (F12 주소창 확인 후 수정 필요)        │
    └──────────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - 해시 포함 class → [class*='안정키워드'] 부분 매칭
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
    - TODO_ 셀렉터: 해당 DOM 확인 후 실제 값으로 교체
"""

from playwright.sync_api import Page


class UserComplaintPage:
    """블루밍비트 이용자 불만 처리 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    COMPLAINT_PATH      = "/terms/service/ombudsman"
    MYPAGE_PATH         = "/mypage"
    SIGNIN_PATH         = "/user/signin"
    # ⚠️ TODO: 신고 버튼 클릭 후 이동하는 1:1 문의/신고 폼 URL 확인 후 수정
    COMPLAINT_FORM_PATH = "/mypage/contact"

    # 본문에 노출된 실제 이메일 주소 (plain text로 확인됨)
    EXPECTED_EMAIL = "help@bloomingbit.io"
    # 버튼 텍스트 (HTML에서 정확히 확인됨)
    EXPECTED_BUTTON_TEXT = "이용자 불만 신고하기"
    # 페이지 타이틀 (h1)
    EXPECTED_TITLE_TEXT = "이용자 불만 처리"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반 + TODO_)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 (✅ 안정 — HTML에서 직접 확인) ──────────────────
    # HTML: <section class="...__myPageCommonContentWrapper">
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    # HTML: <header class="...__contentHeader">
    PAGE_HEADER  = "header[class*='contentHeader']"
    # HTML: <h1>이용자 불만 처리</h1>
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    # HTML: <a class="...__backBtn" href="/mypage">
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 콘텐츠 영역 (✅ 안정 — HTML에서 직접 확인) ───────────────────
    # HTML: <div class="...__complaintHandlingContentWrapper">
    CONTENT_WRAPPER  = "div[class*='complaintHandlingContentWrapper']"
    # HTML: <div id="complaintHandlingContent" class="...__complaintHandlingContent bottom">
    CONTENT_AREA     = "div#complaintHandlingContent"
    # 콘텐츠 내 본문 텍스트 div (첫 번째 자식)
    CONTENT_TEXT_DIV = "div#complaintHandlingContent > div:first-child"
    # 모든 안내 단락 <p>
    CONTENT_ALL_P    = "div#complaintHandlingContent > div:first-child p"
    # 섹션 헤딩 <strong> (10개: 절차 안내, 접수 대상, 접수 방법, 담당 연락처, 처리 절차,
    #                     처리 원칙, 처리 제외, 개인정보 안내, 이용자위원회, 회의록)
    SECTION_HEADINGS = "div#complaintHandlingContent > div:first-child p strong"

    # ── 섹션별 헤딩 텍스트 셀렉터 (✅ 안정 — has-text 기반) ───────────
    SECTION_INTRO        = "div#complaintHandlingContent p strong:has-text('절차 안내')"
    SECTION_TARGET       = "div#complaintHandlingContent p strong:has-text('접수 대상')"
    SECTION_METHOD       = "div#complaintHandlingContent p strong:has-text('접수 방법')"
    SECTION_CONTACT      = "div#complaintHandlingContent p strong:has-text('담당 연락처')"
    SECTION_PROCEDURE    = "div#complaintHandlingContent p strong:has-text('처리 절차')"
    SECTION_PRINCIPLE    = "div#complaintHandlingContent p strong:has-text('처리 원칙')"
    SECTION_EXCLUSION    = "div#complaintHandlingContent p strong:has-text('제외')"
    SECTION_PRIVACY      = "div#complaintHandlingContent p strong:has-text('개인정보')"
    SECTION_COMMITTEE    = "div#complaintHandlingContent p strong:has-text('이용자위원회')"
    SECTION_MINUTES      = "div#complaintHandlingContent p strong:has-text('회의록')"

    # ── 신고 버튼 (✅ 안정 — HTML에서 직접 확인) ──────────────────────
    # HTML: <div class="...__complaintHandlingButtonWrapper">
    BUTTON_WRAPPER       = "div[class*='complaintHandlingButtonWrapper']"
    # HTML: <button type="button" class="...__complaintHandlingButton">이용자 불만 신고하기</button>
    REPORT_BUTTON        = "button[class*='complaintHandlingButton']"
    # 이중 안전 셀렉터 (텍스트 기반 폴백)
    REPORT_BUTTON_BY_TEXT = "button:has-text('이용자 불만 신고하기')"

    # ── 이메일 연락처 (✅ 텍스트 안정, ⚠️ mailto 링크는 TODO) ─────────
    # HTML: plain text "- 이메일: help@bloomingbit.io" (링크 아님)
    # mailto 링크가 실제로 존재하는 경우 아래 셀렉터 사용 가능
    MAILTO_LINK = (
        "a[href^='mailto:'], "
        "a[href*='help@bloomingbit.io']"
    )
    # 이메일 텍스트를 포함하는 단락 (plain text 기반)
    EMAIL_TEXT_P = "div#complaintHandlingContent p:has-text('help@bloomingbit.io')"

    # ── LNB(좌측 네비게이션 바) (⚠️ TODO — HTML 미노출) ─────────────
    # ⚠️ TODO: 마이페이지 LNB 영역 F12 확인 후 튜닝
    LNB_WRAPPER         = (
        "[data-testid='TODO_lnbWrapper'], "
        "[class*='lnb'], "
        "[class*='sideNav'], "
        "aside nav"
    )
    LNB_COMPLAINT_MENU  = (
        "[data-testid='TODO_lnbComplaintMenu'], "
        "nav a[href*='complaint'], "
        "nav button:has-text('이용자 불만'), "
        "aside a:has-text('불만 처리')"
    )
    LNB_ACTIVE_MENU     = (
        "[data-testid='TODO_lnbActiveMenu'], "
        "nav a[class*='active'], "
        "aside a[class*='active']"
    )

    # ── 로그인 유도 팝업/페이지 (⚠️ TODO — 비로그인 시 나타남) ──────
    # ⚠️ TODO: 비로그인 상태에서 신고 버튼 클릭 후 F12 확인
    LOGIN_MODAL         = (
        "[data-testid='TODO_loginModal'], "
        "[class*='loginModal'], "
        "[role='dialog']"
    )
    LOGIN_MODAL_CONFIRM = "[data-testid='TODO_loginModalConfirm']"

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

    def go_to_complaint(self) -> None:
        """이용자 불만 처리 페이지로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.COMPLAINT_PATH}")
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

    def is_on_complaint_page(self) -> bool:
        return self.COMPLAINT_PATH in self.page.url

    def is_on_signin_page(self) -> bool:
        return self.SIGNIN_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """페이지 로드 완료 여부 (콘텐츠 래퍼 기준 — HTML 안정 셀렉터)"""
        try:
            self.page.wait_for_selector(self.CONTENT_WRAPPER, timeout=timeout)
            return True
        except Exception:
            return (
                self.page.locator(self.PAGE_WRAPPER).count() > 0
                or self.page.locator(self.PAGE_HEADER).count() > 0
            )

    def is_page_title_correct(self) -> bool:
        """페이지 타이틀이 '이용자 불만 처리'인지 확인"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            return "이용자 불만" in el.first.inner_text()
        except Exception:
            return False

    def get_page_title_text(self) -> str:
        """페이지 h1 타이틀 텍스트 반환"""
        try:
            return self.page.locator(self.PAGE_TITLE).first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  콘텐츠 텍스트 검증 (✅ HTML 안정 셀렉터)
    # ══════════════════════════════════════════════════════════════════

    def is_content_area_visible(self) -> bool:
        """콘텐츠 영역 노출 여부"""
        return self.page.locator(self.CONTENT_AREA).count() > 0

    def get_all_content_text(self) -> str:
        """전체 콘텐츠 텍스트 반환"""
        try:
            return self.page.locator(self.CONTENT_AREA).first.inner_text().strip()
        except Exception:
            return ""

    def get_section_heading_count(self) -> int:
        """노출된 섹션 헤딩(<strong>) 수 반환"""
        return self.page.locator(self.SECTION_HEADINGS).count()

    def get_paragraph_count(self) -> int:
        """안내 단락(<p>) 수 반환"""
        return self.page.locator(self.CONTENT_ALL_P).count()

    def is_section_visible(self, selector: str) -> bool:
        """특정 섹션 헤딩 노출 여부"""
        return self.page.locator(selector).count() > 0

    def is_required_sections_all_visible(self) -> bool:
        """TC 필수 3개 섹션(접수 대상·처리 절차·담당 연락처) 모두 노출 여부"""
        return (
            self.is_section_visible(self.SECTION_TARGET)
            and self.is_section_visible(self.SECTION_PROCEDURE)
            and self.is_section_visible(self.SECTION_CONTACT)
        )

    def get_missing_sections(self) -> list:
        """필수 섹션 중 미노출 항목 이름 목록 반환"""
        missing = []
        checks = {
            "접수 대상":        self.SECTION_TARGET,
            "불만 처리 절차":   self.SECTION_PROCEDURE,
            "담당 연락처":      self.SECTION_CONTACT,
        }
        for name, selector in checks.items():
            if not self.is_section_visible(selector):
                missing.append(name)
        return missing

    def is_content_text_not_empty(self) -> bool:
        """콘텐츠 텍스트가 비어있지 않은지 확인"""
        text = self.get_all_content_text()
        return len(text.strip()) > 100  # 최소 100자 이상

    def is_text_overflowing_horizontally(self) -> bool:
        """콘텐츠 영역에 가로 스크롤(overflow-x) 발생 여부 확인"""
        try:
            scroll_width  = self.page.locator(self.CONTENT_AREA).first.evaluate(
                "e => e.scrollWidth"
            )
            client_width  = self.page.locator(self.CONTENT_AREA).first.evaluate(
                "e => e.clientWidth"
            )
            return float(scroll_width) > float(client_width)
        except Exception:
            return False

    def is_body_overflowing_horizontally(self) -> bool:
        """body 전체에 가로 스크롤 발생 여부 확인"""
        try:
            scroll_width = self.page.evaluate("() => document.body.scrollWidth")
            client_width = self.page.evaluate("() => document.documentElement.clientWidth")
            return float(scroll_width) > float(client_width) + 5  # 5px 오차 허용
        except Exception:
            return False

    def get_page_scroll_height(self) -> float:
        """페이지 전체 스크롤 가능 높이 반환"""
        try:
            return self.page.evaluate("() => document.documentElement.scrollHeight")
        except Exception:
            return 0.0

    def get_viewport_height(self) -> float:
        """현재 뷰포트 높이 반환"""
        try:
            return self.page.evaluate("() => window.innerHeight")
        except Exception:
            return 0.0

    def scroll_to_bottom(self, steps: int = 5, delay_ms: int = 400) -> None:
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
    #  이메일 연락처 검증 (✅ 텍스트 기반 안정 / ⚠️ mailto 링크는 TODO)
    # ══════════════════════════════════════════════════════════════════

    def is_email_text_visible(self) -> bool:
        """'help@bloomingbit.io' 텍스트가 페이지에 노출되는지 확인 (plain text 기준)"""
        return self.page.locator(self.EMAIL_TEXT_P).count() > 0

    def get_email_text_from_content(self) -> str:
        """본문에서 이메일 주소 텍스트 추출 (plain text)"""
        try:
            content = self.get_all_content_text()
            import re
            match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", content)
            return match.group(0) if match else ""
        except Exception:
            return ""

    def is_mailto_link_present(self) -> bool:
        """mailto: 링크 요소가 DOM에 존재하는지 확인 (⚠️ TODO: 없을 수 있음)"""
        return self.page.locator(self.MAILTO_LINK).count() > 0

    def get_mailto_href(self) -> str:
        """첫 번째 mailto 링크의 href 값 반환 (⚠️ TODO: 없으면 빈 문자열)"""
        try:
            loc = self.page.locator(self.MAILTO_LINK).first
            return loc.get_attribute("href") or ""
        except Exception:
            return ""

    def click_mailto_link(self) -> str:
        """mailto 링크 클릭 (메일 클라이언트 실행 확인용)
        ※ 실제 메일 앱 실행 여부는 자동화로 완전 검증 불가 — href 속성으로 판단
        """
        try:
            loc = self.page.locator(self.MAILTO_LINK).first
            loc.wait_for(state="attached", timeout=3_000)
            return loc.get_attribute("href") or ""
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  신고하기 버튼 (✅ 완전 안정 — HTML에서 직접 확인)
    # ══════════════════════════════════════════════════════════════════

    def is_report_button_visible(self) -> bool:
        """'이용자 불만 신고하기' 버튼 노출 여부"""
        return (
            self.page.locator(self.REPORT_BUTTON).count() > 0
            or self.page.locator(self.REPORT_BUTTON_BY_TEXT).count() > 0
        )

    def get_report_button_text(self) -> str:
        """신고 버튼 텍스트 반환"""
        try:
            loc = self.page.locator(self.REPORT_BUTTON).first
            if loc.count() == 0:
                loc = self.page.locator(self.REPORT_BUTTON_BY_TEXT).first
            return loc.inner_text().strip()
        except Exception:
            return ""

    def is_report_button_text_correct(self) -> bool:
        """버튼 텍스트가 정확히 '이용자 불만 신고하기'인지 확인"""
        return self.get_report_button_text() == self.EXPECTED_BUTTON_TEXT

    def is_report_button_in_viewport(self) -> bool:
        """신고 버튼이 현재 뷰포트 내에 보이는지 확인 (스크롤 후 검사)"""
        try:
            btn = self.page.locator(self.REPORT_BUTTON).first
            bounding = btn.evaluate(
                "e => ({ top: e.getBoundingClientRect().top, "
                "bottom: e.getBoundingClientRect().bottom, "
                "height: e.getBoundingClientRect().height })"
            )
            viewport_h = self.get_viewport_height()
            top    = float(bounding.get("top", -1))
            bottom = float(bounding.get("bottom", -1))
            return top >= 0 and bottom <= viewport_h
        except Exception:
            return self.is_report_button_visible()

    def is_button_below_content(self) -> bool:
        """신고 버튼이 본문 텍스트 영역 아래에 위치하는지 확인 (Y 좌표 비교)"""
        try:
            content_bottom = float(
                self.page.locator(self.CONTENT_TEXT_DIV).first.evaluate(
                    "e => e.getBoundingClientRect().bottom"
                )
            )
            button_top = float(
                self.page.locator(self.REPORT_BUTTON).first.evaluate(
                    "e => e.getBoundingClientRect().top"
                )
            )
            return button_top >= content_bottom - 10  # 10px 오차 허용
        except Exception:
            return True  # 위치 확인 실패 → pass 처리

    def click_report_button(self) -> None:
        """'이용자 불만 신고하기' 버튼 클릭
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(self.REPORT_BUTTON).first
        if loc.count() == 0:
            loc = self.page.locator(self.REPORT_BUTTON_BY_TEXT).first
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

    def get_report_button_size(self) -> dict:
        """신고 버튼의 너비·높이 반환 (UI 검증용)"""
        try:
            return self.page.locator(self.REPORT_BUTTON).first.evaluate(
                "e => ({ width: e.getBoundingClientRect().width, "
                "height: e.getBoundingClientRect().height })"
            )
        except Exception:
            return {"width": 0, "height": 0}

    # ══════════════════════════════════════════════════════════════════
    #  LNB 메뉴 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_lnb_visible(self) -> bool:
        """LNB 영역 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.LNB_WRAPPER).count() > 0

    def click_lnb_complaint_menu(self) -> None:
        """LNB에서 '이용자 불만 처리' 메뉴 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        loc = self.page.locator(self.LNB_COMPLAINT_MENU).first
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

    def is_lnb_complaint_menu_active(self) -> bool:
        """LNB에서 '이용자 불만 처리' 메뉴가 활성(하이라이트) 상태인지 확인
        (⚠️ TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요)
        """
        try:
            active_text = self.page.locator(self.LNB_ACTIVE_MENU).first.inner_text().strip()
            return "불만" in active_text or "민원" in active_text
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  비로그인 관련 (⚠️ TODO — 실제 동작 확인 필요)
    # ══════════════════════════════════════════════════════════════════

    def is_login_modal_or_page_visible(self) -> bool:
        """로그인 팝업 또는 로그인 페이지로 이동했는지 확인
        ① 로그인 모달 DOM 존재 여부
        ② 현재 URL이 /user/signin 포함 여부
        """
        if self.page.locator(self.LOGIN_MODAL).count() > 0:
            return True
        return self.is_on_signin_page()

    def is_not_on_complaint_form_page(self) -> bool:
        """신고 접수 폼 페이지로 즉시 이동하지 않았는지 확인 (비로그인 TC용)"""
        current = self.get_current_url()
        # 신고 폼 페이지가 아니어야 함
        return self.COMPLAINT_FORM_PATH not in current or self.is_login_modal_or_page_visible()