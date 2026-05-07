"""
pages/web/ai_report_page.py
[STEP 2 — POM v1]  AI 리포트 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
셀렉터 전략:
    - CSS Modules 해시 클래스 직접 사용 금지 → [class*='...'] 부분 매칭
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > 시맨틱 태그+구조 > 안정 CSS 클래스
    - Next.js SPA 링크: locator.get_attribute("href") + page.goto() 방식
    - Portal 모달: 블루밍비트는 모달을 <div id="portal-modal"> 내부에 렌더링
    - domcontentloaded 사용 — Next.js SPA + 서드파티 스크립트로 networkidle 30초 타임아웃 발생
    - ⚠️  TODO_ 접두사가 붙은 셀렉터는 F12 → 실제 DOM 확인 후 반드시 교체 필요

    AI 리포트 URL 패턴:
        메인(서비스 중단) : /report
        서브 목록        : /report/list  → 에러 페이지 노출
        개별 리포트       : /report/{id}  → 에러 페이지 노출

현재 상태 (2025-04 기준):
    - /report 접속 시 '서비스 일시 중단' 안내 페이지 노출
    - 로그인/비로그인 무관하게 동일한 중단 페이지 노출 (로그인 유도 없음)
    - 다크 배경 전체 화면 레이아웃
    - 서브 경로(/report/list, /report/{id}) 접근 시 에러 페이지 노출

검증 대상 텍스트:
    - 필 배지   : '서비스 일시 중단 및 전면 개편 안내'
    - 브랜드 타이틀: 'Ai Report by. STAT'
    - 메인 제목  : 'AI 리포트, 더 강력한 모습으로 돌아옵니다'
    - 안내 본문  : '서비스 고도화를 위한 전면 개편을 잠시 준비 중이며...'
    - 에러 페이지: '이용에 불편을 드려 죄송합니다. 삭제되었거나 더이상 제공되지 않는 페이지입니다.'
"""

from playwright.sync_api import Page


class AiReportPage:
    """블루밍비트 AI 리포트 도메인 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS
    # ══════════════════════════════════════════════════════════════════

    # ── GNB ──────────────────────────────────────────────────────────
    GNB_HEADER       = "header#headerContainer"
    # ⚠️ TODO: GNB 내 'AI 리포트' 탭 — data-label / href 확인 후 교체
    GNB_AIREPORT_TAB = (
        "#menuWithMySettingContainer nav a[data-label='AI 리포트'], "
        "#menuWithMySettingContainer nav a[href*='/report'], "
        "#menuWithMySettingContainer nav a:has-text('AI 리포트')"
    )

    # ── AI 리포트 메인 페이지 컨테이너 ─────────────────────────────────
    # ⚠️ TODO: /report 페이지의 실제 main/section ID 확인 후 교체
    AIREPORT_MAIN    = (
        "[data-testid='TODO_aiReportMain'], "
        "main[id*='TODO_reportPage'], "
        "main[class*='TODO_reportMain'], "
        "main"
    )

    # ── 서비스 일시 중단 페이지 ─────────────────────────────────────
    # 다크 배경 전체 화면 래퍼
    # ⚠️ TODO: 다크 배경 컨테이너 class 확인 후 교체
    SUSPENSION_WRAPPER = (
        "[data-testid='TODO_suspensionWrapper'], "
        "div[class*='TODO_suspensionPage'], "
        "div[class*='TODO_darkBackground'], "
        "section[class*='TODO_serviceSuspension']"
    )

    # 필(pill) 배지 — '서비스 일시 중단 및 전면 개편 안내'
    # ⚠️ TODO: 배지 span/div class 확인 후 교체 (텍스트 기반 폴백 포함)
    SUSPENSION_BADGE = (
        "[data-testid='TODO_suspensionBadge'], "
        "span[class*='TODO_pillBadge']:has-text('서비스 일시 중단'), "
        "div[class*='TODO_badge']:has-text('서비스 일시 중단'), "
        "span:has-text('서비스 일시 중단 및 전면 개편 안내'), "
        "p:has-text('서비스 일시 중단 및 전면 개편 안내')"
    )

    # 브랜드 타이틀 — 'Ai Report by. STAT'
    # ⚠️ TODO: 브랜드 타이틀 h1/h2/p class 확인 후 교체
    BRAND_TITLE      = (
        "[data-testid='TODO_brandTitle'], "
        "h1[class*='TODO_brandTitle']:has-text('Ai Report'), "
        "h2[class*='TODO_brandTitle']:has-text('Ai Report'), "
        "p[class*='TODO_brandTitle']:has-text('Ai Report'), "
        "h1:has-text('Ai Report by. STAT'), "
        "h2:has-text('Ai Report by. STAT'), "
        "p:has-text('Ai Report by. STAT')"
    )

    # 메인 제목 — 'AI 리포트, 더 강력한 모습으로 돌아옵니다'
    # ⚠️ TODO: 메인 제목 태그/class 확인 후 교체
    MAIN_HEADING     = (
        "[data-testid='TODO_mainHeading'], "
        "h1[class*='TODO_mainTitle']:has-text('AI 리포트'), "
        "h2[class*='TODO_mainTitle']:has-text('AI 리포트'), "
        "h1:has-text('AI 리포트, 더 강력한 모습으로 돌아옵니다'), "
        "h2:has-text('AI 리포트, 더 강력한 모습으로 돌아옵니다'), "
        "p:has-text('AI 리포트, 더 강력한 모습으로 돌아옵니다')"
    )

    # 안내 본문 텍스트 — '서비스 고도화를 위한 전면 개편을 잠시 준비 중이며...'
    # ⚠️ TODO: 안내 본문 p/span class 확인 후 교체
    BODY_TEXT        = (
        "[data-testid='TODO_bodyText'], "
        "p[class*='TODO_description']:has-text('서비스 고도화'), "
        "p:has-text('서비스 고도화를 위한 전면 개편'), "
        "span:has-text('서비스 고도화를 위한 전면 개편')"
    )

    # ── 에러 페이지 ──────────────────────────────────────────────────
    # '이용에 불편을 드려 죄송합니다. 삭제되었거나 더이상 제공되지 않는 페이지입니다.'
    # ⚠️ TODO: 에러 페이지 컨테이너/텍스트 class 확인 후 교체
    ERROR_PAGE       = (
        "[data-testid='TODO_errorPage'], "
        "div[class*='TODO_errorPage'], "
        "section[class*='TODO_notFound'], "
        "p:has-text('이용에 불편을 드려 죄송합니다'), "
        "h1:has-text('이용에 불편을 드려 죄송합니다'), "
        "span:has-text('삭제되었거나 더이상 제공되지 않는 페이지')"
    )

    # 에러 페이지 검증용 텍스트 스니펫 (부분 일치)
    ERROR_TEXT_SNIPPET = "이용에 불편을 드려 죄송합니다"

    # ── 로그인 유도 모달 ──────────────────────────────────────────────
    LOGIN_MODAL      = (
        "#portal-modal div[class*='loginModal'], "
        "div[role='dialog'][class*='loginModal']"
    )

    # ── URL 패턴 ────────────────────────────────────────────────────
    AIREPORT_MAIN_PATH      = "/report"
    AIREPORT_LIST_PATH      = "/report/list"
    AIREPORT_INVALID_ID     = "/report/999999"

    # 검증용 텍스트 상수 (assert 메시지 및 텍스트 포함 여부 확인용)
    TEXT_BADGE        = "서비스 일시 중단 및 전면 개편 안내"
    TEXT_BRAND_TITLE  = "Ai Report by. STAT"
    TEXT_MAIN_HEADING = "AI 리포트, 더 강력한 모습으로 돌아옵니다"
    TEXT_BODY_SNIPPET = "서비스 고도화를 위한 전면 개편"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def go_to_aireport_main(self) -> None:
        """AI 리포트 메인(/report)으로 이동
        ※ wait_until='domcontentloaded' — Next.js SPA + 서드파티 스크립트로
          'networkidle' 30초 타임아웃 발생 방지
        """
        self.page.goto(
            f"{self.BASE_URL}{self.AIREPORT_MAIN_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_aireport_list(self) -> None:
        """AI 리포트 목록(/report/list)으로 이동 (에러 페이지 예상)"""
        self.page.goto(
            f"{self.BASE_URL}{self.AIREPORT_LIST_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_aireport_invalid_id(self, report_id: str = "999999") -> None:
        """존재하지 않는 리포트 ID 경로(/report/{id})로 이동 (에러 페이지 예상)"""
        self.page.goto(
            f"{self.BASE_URL}{self.AIREPORT_MAIN_PATH}/{report_id}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_main_loaded(self) -> bool:
        """AI 리포트 메인(/report) 로드 완료 여부"""
        return self.AIREPORT_MAIN_PATH in self.page.url

    def is_gnb_visible(self) -> bool:
        """GNB 헤더 노출 여부"""
        return self.page.is_visible(self.GNB_HEADER)

    # ══════════════════════════════════════════════════════════════════
    #  GNB 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_aireport_tab_visible(self) -> bool:
        """GNB 내 'AI 리포트' 탭 노출 여부"""
        return self.page.locator(self.GNB_AIREPORT_TAB).count() > 0

    def click_gnb_aireport_tab(self) -> None:
        """GNB 'AI 리포트' 탭 클릭 → href goto 방식"""
        locator = self.page.locator(self.GNB_AIREPORT_TAB).first
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  서비스 일시 중단 페이지 검증 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_suspension_page_visible(self) -> bool:
        """서비스 일시 중단 안내 페이지 노출 여부
        ※ 다크 배경 래퍼 OR 중단 배지 OR 메인 제목 중 하나라도 존재하면 True
        """
        if self.page.locator(self.SUSPENSION_WRAPPER).count() > 0:
            return True
        if self.page.locator(self.SUSPENSION_BADGE).count() > 0:
            return True
        if self.page.locator(self.MAIN_HEADING).count() > 0:
            return True
        # 최종 폴백: 페이지 텍스트 내 핵심 문구 포함 여부
        return self.TEXT_MAIN_HEADING in self.page.content()

    def is_dark_background_visible(self) -> bool:
        """다크 배경 전체 화면 레이아웃 노출 여부
        ※ 래퍼 div 존재 OR 페이지 body/main 배경색 어두움 여부로 판단
        """
        if self.page.locator(self.SUSPENSION_WRAPPER).count() > 0:
            return True
        # 폴백: 페이지 전체 콘텐츠에서 중단 페이지 특유 요소 존재 확인
        return self.page.locator(self.SUSPENSION_BADGE).count() > 0 or \
               self.page.locator(self.MAIN_HEADING).count() > 0

    def is_suspension_badge_visible(self) -> bool:
        """'서비스 일시 중단 및 전면 개편 안내' 필 배지 노출 여부"""
        if self.page.locator(self.SUSPENSION_BADGE).count() > 0:
            return True
        return self.TEXT_BADGE in self.page.content()

    def get_suspension_badge_text(self) -> str:
        """필 배지 텍스트 반환"""
        try:
            return self.page.locator(self.SUSPENSION_BADGE).first.inner_text().strip()
        except Exception:
            return ""

    def is_brand_title_visible(self) -> bool:
        """'Ai Report by. STAT' 브랜드 타이틀 노출 여부"""
        if self.page.locator(self.BRAND_TITLE).count() > 0:
            return True
        return self.TEXT_BRAND_TITLE in self.page.content()

    def get_brand_title_text(self) -> str:
        """브랜드 타이틀 텍스트 반환"""
        try:
            return self.page.locator(self.BRAND_TITLE).first.inner_text().strip()
        except Exception:
            return ""

    def is_main_heading_visible(self) -> bool:
        """'AI 리포트, 더 강력한 모습으로 돌아옵니다' 메인 제목 노출 여부"""
        if self.page.locator(self.MAIN_HEADING).count() > 0:
            return True
        return self.TEXT_MAIN_HEADING in self.page.content()

    def get_main_heading_text(self) -> str:
        """메인 제목 텍스트 반환"""
        try:
            return self.page.locator(self.MAIN_HEADING).first.inner_text().strip()
        except Exception:
            return ""

    def is_body_text_visible(self) -> bool:
        """안내 본문 텍스트 노출 여부 (부분 일치)"""
        if self.page.locator(self.BODY_TEXT).count() > 0:
            return True
        return self.TEXT_BODY_SNIPPET in self.page.content()

    def get_body_text(self) -> str:
        """안내 본문 텍스트 반환"""
        try:
            return self.page.locator(self.BODY_TEXT).first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  로그인 모달 검증
    # ══════════════════════════════════════════════════════════════════

    def is_login_modal_visible(self) -> bool:
        """로그인 유도 모달 노출 여부"""
        return self.page.locator(self.LOGIN_MODAL).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  에러 페이지 검증 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_error_page_visible(self) -> bool:
        """에러 페이지 노출 여부
        ※ '이용에 불편을 드려 죄송합니다. 삭제되었거나...' 텍스트 기준 검증
        """
        if self.page.locator(self.ERROR_PAGE).count() > 0:
            return True
        return self.ERROR_TEXT_SNIPPET in self.page.content()

    def get_error_page_text(self) -> str:
        """에러 페이지 주요 텍스트 반환"""
        try:
            return self.page.locator(self.ERROR_PAGE).first.inner_text().strip()
        except Exception:
            return ""

    def is_url_report_main(self) -> bool:
        """현재 URL이 /report (메인) 패턴인지 확인"""
        url = self.page.url
        # /report/xxx 형태가 아닌 순수 /report 경로 여부
        path = url.split("?")[0].rstrip("/")
        return path.endswith("/report")

    def is_url_redirected_away(self, original_path: str) -> bool:
        """original_path 에서 다른 페이지로 리디렉션 되었는지 확인
        ※ 에러 페이지는 URL 유지 or 404 페이지로 이동할 수 있음
        """
        return original_path not in self.page.url or self.is_error_page_visible()