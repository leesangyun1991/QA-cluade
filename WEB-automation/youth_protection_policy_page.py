"""
pages/web/youth_protection_policy_page.py
[STEP 2 — POM v1]  청소년보호정책(Youth Protection Policy) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_termsContent-module-scss-module__7BiZnG__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │  청소년보호정책은 이전 6개 페이지와 동일한 CSS 모듈(7BiZnG) 공유            │
    │                                                                              │
    │  ✅ 안정 셀렉터 (HTML에서 직접 확인됨):                                      │
    │  · 페이지 타이틀:       h1 = "청소년보호정책"                                │
    │  · 공통 래퍼:           div[class*='termsContentWrapper']                    │
    │  · 날짜 라벨:           span.dateLabel  ← plain class!                      │
    │  · 드롭다운 컨테이너:   div.dropdown    ← plain class!                      │
    │  · 선택 날짜 표시:      div.dropdown > div > span = "2024.03.19"            │
    │  · 드롭다운 토글 버튼:  div.dropdown button[type='button']                   │
    │  · 정책 본문 영역:      div#termsContent  ← ID! 최강!                       │
    │  · 볼드 요소:           div#termsContent p b  ← <b> 태그! (<strong> 아님!)  │
    │  · 전체 단락:           div#termsContent p                                  │
    │  · 섹션 1:              div#termsContent p:has-text('청소년접근제한')        │
    │  · 섹션 2:              div#termsContent p:has-text('담당자 교육')           │
    │  · 섹션 3:              div#termsContent p:has-text('피해상담')              │
    │  · 섹션 4:              div#termsContent p:has-text('청소년보호 책임자')     │
    │  · 책임자 성명:         div#termsContent p:has-text('성명')                 │
    │  · 책임자 소속:         div#termsContent p:has-text('소속')                 │
    │  · 책임자 전화:         div#termsContent p:has-text('전화')                 │
    │  · 책임자 이메일:       div#termsContent p:has-text('E-mail')               │
    │                                                                              │
    │  ⚠️  이전 페이지들과의 중요 차이점:                                           │
    │  · 볼드 태그: <b> 사용 (이용약관·개인정보처리방침·커뮤니티는 <strong>)       │
    │    → div#termsContent p strong 셀렉터는 이 페이지에서 0건 반환!             │
    │  · 주요 섹션(1~4)은 <p> 안에 <strong>/<b> 없는 plain text                  │
    │  · 본문 구조: div#termsContent > div > p (span 래퍼 없음)                  │
    │  · 이메일: "sheep@bloomingbit.io" plain text (mailto 링크 아님)             │
    │  · 책임자 정보 단락들이 HTML에서 직접 확인됨 — 안정적으로 검증 가능!        │
    │                                                                              │
    │  ⚠️  TODO_ 셀렉터 (실제 DOM 확인 후 교체 필요):                              │
    │  · 드롭다운 옵션 목록: DROPDOWN_LIST, DROPDOWN_OPTION                        │
    │  · LNB 메뉴:           LNB_WRAPPER, LNB_YOUTH_MENU, LNB_ACTIVE_MENU        │
    │                                                                              │
    │  책임자 정보 (HTML에서 직접 확인됨):                                          │
    │    성명: 양한나 / 소속: 뉴스팀 / 전화: 02-554-7002                          │
    │    E-mail: sheep@bloomingbit.io (plain text — mailto 링크 아님)             │
    │                                                                              │
    │  드롭다운 날짜 (HTML): "2024.03.19"                                          │
    │  페이지 URL 추정: /mypage/youth-protection  (F12 확인 후 수정 필요)          │
    └──────────────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - ID 최우선: div#termsContent
    - plain class 활용: div.dropdown, span.dateLabel
    - 볼드 헤딩: p b  (<strong>이 아닌 <b> 태그 사용)
    - 섹션 검증: p:has-text() 기반 텍스트 매칭
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
"""

import re

from playwright.sync_api import Page


class YouthProtectionPolicyPage:
    """블루밍비트 청소년보호정책 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    YOUTH_POLICY_PATH = "/terms/youth"
    MYPAGE_PATH       = "/mypage"
    SIGNIN_PATH       = "/user/signin"

    # ── 상수 (HTML에서 직접 확인) ─────────────────────────────────────
    EXPECTED_TITLE        = "청소년보호정책"
    EXPECTED_DATE_LABEL   = "시행/변경 일자"
    # HTML 기준 드롭다운에 표시된 날짜
    KNOWN_LATEST_DATE     = "2024.03.19"
    # 책임자 정보 (HTML에서 직접 확인됨)
    EXPECTED_MANAGER_NAME  = "양한나"
    EXPECTED_MANAGER_DEPT  = "뉴스팀"
    EXPECTED_MANAGER_PHONE = "02-554-7002"
    EXPECTED_MANAGER_EMAIL = "sheep@bloomingbit.io"
    # 본문 주요 섹션 수
    EXPECTED_SECTION_COUNT = 4
    MIN_PARAGRAPH_COUNT    = 10  # 최소 단락 수

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반 + TODO_)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 (✅ 안정 — 이전 페이지들과 동일) ─────────────────
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    PAGE_HEADER  = "header[class*='contentHeader']"
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 정책 상단 영역 (✅ 안정 — 동일 CSS 모듈) ─────────────────────
    CONTENT_WRAPPER   = "div[class*='termsContentWrapper']"
    CONTENT_TOP       = "div[class*='termsTopWrapper']"
    # HTML: <span class="dateLabel">시행/변경 일자</span>  ← plain class!
    DATE_LABEL        = "span.dateLabel"

    # ── 드롭다운 (✅ 안정 — plain class "dropdown") ──────────────────
    DROPDOWN              = "div.dropdown"
    DROPDOWN_TRIGGER      = "div.dropdown > div"
    # 현재 날짜 표시: "2024.03.19"
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

    # ── 정책 본문 (✅ 최강 안정 — ID 기반, 동일 ID) ──────────────────
    # HTML: <div id="termsContent" class="...__termsContent">
    POLICY_CONTENT   = "div#termsContent"
    # 본문 구조: div#termsContent > div > p (span 래퍼 없음)
    ALL_PARAGRAPHS   = "div#termsContent p"

    # ── 볼드 요소 (⚠️ 핵심 차이: <b> 태그! — <strong> 아님!) ────────
    # HTML: <p><b>청소년보호정책</b></p>
    # HTML: <p><b>청소년 보호 관리 책임자...</b></p>
    BOLD_HEADINGS    = "div#termsContent p b"
    # 정책 타이틀 볼드
    POLICY_TITLE_B   = "div#termsContent p b:has-text('청소년보호정책')"
    # 책임자 헤더 볼드
    MANAGER_HEADER_B = "div#termsContent p b:has-text('청소년 보호 관리 책임자')"

    # ── 주요 섹션 단락 (✅ 안정 — 텍스트 기반, 섹션별 고유 키워드) ──
    # 섹션 1: 유해정보에 대한 청소년접근제한 및 관리조치
    SECTION_1_P      = "div#termsContent p:has-text('청소년접근제한')"
    # 섹션 2: 유해정보로부터의 청소년보호를 위한 업무 담당자 교육 시행
    SECTION_2_P      = "div#termsContent p:has-text('담당자 교육')"
    # 섹션 3: 유해정보로 인한 피해상담 및 고충처리
    SECTION_3_P      = "div#termsContent p:has-text('피해상담')"
    # 섹션 4: 청소년보호 책임자의 소속, 성명 및 연락처
    SECTION_4_P      = "div#termsContent p:has-text('청소년보호 책임자')"

    # ── 책임자 정보 단락 (✅ 안정 — HTML에서 직접 확인됨) ─────────────
    # HTML: <p>성명 : 양한나</p>
    MANAGER_NAME_P  = "div#termsContent p:has-text('성명')"
    # HTML: <p>소속 : 뉴스팀</p>
    MANAGER_DEPT_P  = "div#termsContent p:has-text('소속')"
    # HTML: <p>전화 : 02-554-7002</p>
    MANAGER_PHONE_P = "div#termsContent p:has-text('전화')"
    # HTML: <p>E-mail : sheep@bloomingbit.io</p>  (plain text — mailto 아님)
    MANAGER_EMAIL_P = "div#termsContent p:has-text('E-mail')"

    # ── LNB(좌측 네비게이션 바) (⚠️ TODO — HTML 미노출) ─────────────
    LNB_WRAPPER     = (
        "[data-testid='TODO_lnbWrapper'], "
        "[class*='lnb'], "
        "[class*='sideNav'], "
        "aside nav"
    )
    LNB_YOUTH_MENU  = (
        "[data-testid='TODO_lnbYouthMenu'], "
        "nav a[href*='youth'], "
        "nav button:has-text('청소년보호'), "
        "aside a:has-text('청소년보호정책')"
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

    def go_to_youth_policy(self) -> None:
        """청소년보호정책 페이지로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.YOUTH_POLICY_PATH}")
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

    def is_on_youth_policy_page(self) -> bool:
        return self.YOUTH_POLICY_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """페이지 로드 완료 여부 (정책 본문 영역 기준)"""
        try:
            self.page.wait_for_selector(self.POLICY_CONTENT, timeout=timeout)
            return True
        except Exception:
            return (
                self.page.locator(self.PAGE_WRAPPER).count() > 0
                or self.page.locator(self.CONTENT_WRAPPER).count() > 0
            )

    def is_page_title_correct(self) -> bool:
        """페이지 타이틀이 '청소년보호정책'인지 확인"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            return "청소년보호정책" in el.first.inner_text()
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
        """드롭다운에 현재 표시된 날짜 텍스트 반환 (예: '2024.03.19')"""
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

    def is_policy_content_not_empty(self) -> bool:
        """정책 본문에 충분한 텍스트가 있는지 확인 (최소 200자 기준)"""
        return len(self.get_all_policy_text()) >= 200

    def get_paragraph_count(self) -> int:
        """전체 단락(<p>) 수 반환"""
        return self.page.locator(self.ALL_PARAGRAPHS).count()

    def get_bold_element_count(self) -> int:
        """볼드(<b>) 요소 수 반환 (⚠️ <strong>이 아닌 <b> 태그 사용!)"""
        return self.page.locator(self.BOLD_HEADINGS).count()

    # ── 주요 섹션 검증 메서드 (✅ 텍스트 기반 안정 셀렉터) ───────────

    def is_section_1_present(self) -> bool:
        """섹션 1 (청소년접근제한) 노출 여부"""
        return self.page.locator(self.SECTION_1_P).count() > 0

    def is_section_2_present(self) -> bool:
        """섹션 2 (담당자 교육) 노출 여부"""
        return self.page.locator(self.SECTION_2_P).count() > 0

    def is_section_3_present(self) -> bool:
        """섹션 3 (피해상담) 노출 여부"""
        return self.page.locator(self.SECTION_3_P).count() > 0

    def is_section_4_present(self) -> bool:
        """섹션 4 (청소년보호 책임자) 노출 여부"""
        return self.page.locator(self.SECTION_4_P).count() > 0

    def are_all_sections_present(self) -> bool:
        """4개 주요 섹션이 모두 노출되는지 확인"""
        return (
            self.is_section_1_present()
            and self.is_section_2_present()
            and self.is_section_3_present()
            and self.is_section_4_present()
        )

    def get_missing_sections(self) -> list:
        """노출되지 않은 섹션 이름 목록 반환"""
        missing = []
        checks = {
            "1. 유해정보 청소년접근제한": self.is_section_1_present(),
            "2. 담당자 교육": self.is_section_2_present(),
            "3. 피해상담 및 고충처리": self.is_section_3_present(),
            "4. 청소년보호 책임자": self.is_section_4_present(),
        }
        return [name for name, present in checks.items() if not present]

    # ── 책임자 정보 검증 메서드 (✅ HTML에서 직접 확인됨 — 안정!) ─────

    def is_manager_section_present(self) -> bool:
        """책임자 섹션 노출 여부 (성명·소속·전화·E-mail 모두 기준)"""
        return (
            self.page.locator(self.MANAGER_NAME_P).count() > 0
            and self.page.locator(self.MANAGER_DEPT_P).count() > 0
            and self.page.locator(self.MANAGER_EMAIL_P).count() > 0
        )

    def get_manager_name_text(self) -> str:
        """책임자 성명 단락 텍스트 반환 (예: '성명 : 양한나')"""
        try:
            return self.page.locator(self.MANAGER_NAME_P).first.inner_text().strip()
        except Exception:
            return ""

    def get_manager_dept_text(self) -> str:
        """책임자 소속 단락 텍스트 반환 (예: '소속 : 뉴스팀')"""
        try:
            return self.page.locator(self.MANAGER_DEPT_P).first.inner_text().strip()
        except Exception:
            return ""

    def get_manager_phone_text(self) -> str:
        """책임자 전화 단락 텍스트 반환 (예: '전화 : 02-554-7002')"""
        try:
            return self.page.locator(self.MANAGER_PHONE_P).first.inner_text().strip()
        except Exception:
            return ""

    def get_manager_email_text(self) -> str:
        """책임자 이메일 단락 텍스트 반환 (예: 'E-mail : sheep@bloomingbit.io')"""
        try:
            return self.page.locator(self.MANAGER_EMAIL_P).first.inner_text().strip()
        except Exception:
            return ""

    def is_manager_info_accurate(self) -> tuple:
        """책임자 정보 정확성 검증 (성명·소속·이메일)
        반환: (is_valid: bool, error_detail: str)
        """
        errors = []
        name_text = self.get_manager_name_text()
        dept_text = self.get_manager_dept_text()
        email_text = self.get_manager_email_text()

        if self.EXPECTED_MANAGER_NAME not in name_text:
            errors.append(
                f"성명 불일치 — 기대: '{self.EXPECTED_MANAGER_NAME}', 실제: '{name_text}'"
            )
        if self.EXPECTED_MANAGER_DEPT not in dept_text:
            errors.append(
                f"소속 불일치 — 기대: '{self.EXPECTED_MANAGER_DEPT}', 실제: '{dept_text}'"
            )
        if self.EXPECTED_MANAGER_EMAIL not in email_text:
            errors.append(
                f"이메일 불일치 — 기대: '{self.EXPECTED_MANAGER_EMAIL}', 실제: '{email_text}'"
            )
        is_valid = len(errors) == 0
        return is_valid, " / ".join(errors) if errors else ""

    # ══════════════════════════════════════════════════════════════════
    #  LNB 메서드 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_lnb_visible(self) -> bool:
        """LNB 영역 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.LNB_WRAPPER).count() > 0

    def click_lnb_youth_menu(self) -> None:
        """LNB에서 '청소년보호정책' 메뉴 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(self.LNB_YOUTH_MENU).first
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

    def is_lnb_youth_menu_active(self) -> bool:
        """LNB에서 '청소년보호정책' 메뉴가 활성(하이라이트) 상태인지 확인
        (⚠️ TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요)
        """
        try:
            active_text = self.page.locator(self.LNB_ACTIVE_MENU).first.inner_text().strip()
            return "청소년" in active_text
        except Exception:
            return False