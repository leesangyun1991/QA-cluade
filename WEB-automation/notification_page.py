"""
pages/web/notification_page.py
[STEP 3 — POM v3]  알림(Notification) 도메인 Page Object (최종 튜닝판)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
셀렉터 전략:
    - CSS Modules 해시 클래스 직접 사용 금지 → [class*='...'] 부분 매칭
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > 시맨틱 태그+구조 > 안정 CSS 클래스
    - domcontentloaded 사용 — networkidle 30초 타임아웃 방지
    - 실제 HTML 기반: 읽음/안읽음은 ft-muted vs ft-secondary 클래스로 구분
    - ⚠️ GNB 알림 아이콘은 데스크톱/모바일 UI 중복으로 인한 :visible 필터 + force click 적용
"""

from playwright.sync_api import Page

class NotificationPage:
    """블루밍비트 알림(Notification) 도메인 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS (v3: 실제 HTML 반영 완료)
    # ══════════════════════════════════════════════════════════════════

    # ── GNB ──────────────────────────────────────────────────────────
    GNB_HEADER = "header#headerContainer"
    GNB_PROFILE_ICON = "div.myInfo button:has(div.userProfileImage)"

    # GNB 알림 아이콘 (모바일 hidden 중복을 피하기 위한 visible 필터와 폴백용)
    GNB_NOTIFICATION_ICON         = "header#headerContainer button[aria-label='open alarm center']"
    GNB_NOTIFICATION_ICON_VISIBLE = "header#headerContainer button[aria-label='open alarm center']:visible"

    # ── 알림 배지 ────────────────────────────────────────────────────
    # 힌트: GNB HTML에서 <path fill="#FF4A69">가 빨간 배지(붉은 점)
    GNB_NOTIFICATION_BADGE = (
        "header#headerContainer button[aria-label='open alarm center'] path[fill='#FF4A69'], "
        "header#headerContainer button[aria-label='open alarm center'] [class*='badge'], "
        "header#headerContainer button[aria-label='open alarm center'] ~ [class*='badge']"
    )

    BADGE_COUNT_TEXT = (
        "header#headerContainer button[aria-label='open alarm center'] span[class*='TODO_count'], "
        "header#headerContainer button[aria-label='open alarm center'] div[class*='TODO_badgeNum']"
    )

    # ── 알림 모달 ────────────────────────────────────────────────────
    NOTIFICATION_MODAL       = "section.alarmContentContainer"
    NOTIFICATION_MODAL_CLOSE = "section:has(> span:text-is('알림')) > svg"
    NOTIFICATION_MODAL_DIM   = None  # 별도 딤 오버레이 엘리먼트 없음, 뷰포트 여백 클릭으로 대체

    # ── 알림 리스트 ──────────────────────────────────────────────────
    NOTIFICATION_LIST = "ul.alarmList"
    NOTIFICATION_ITEM = "ul.alarmList > section"

    # ── 읽음/안 읽음 상태 ─────────────────────────────────────────────
    # 실제 HTML 기반: 안읽음은 --ft-muted, 읽음은 --ft-secondary를 포함
    UNREAD_NOTIFICATION_ITEM = "ul.alarmList > section:has(> div[class*='--ft-muted'])"
    READ_NOTIFICATION_ITEM   = "ul.alarmList > section:has(> div[class*='--ft-secondary'])"

    # ── 알림 타입(라우팅용) ───────────────────────────────────────────
    # SVG 클래스 기반으로 알림 종류 구분
    NOTIFICATION_ITEM_COMMENT    = "ul.alarmList > section:has(svg.alarmCommentSVG)"
    NOTIFICATION_ITEM_NEWS       = "ul.alarmList > section:has(svg.alarmNewsSVG)"
    NOTIFICATION_ITEM_NOTICE     = "ul.alarmList > section:has(svg.alarmNotificationSVG)"
    NOTIFICATION_ITEM_REWARD     = "ul.alarmList > section:has(svg.alarmRewardSVG)"
    NOTIFICATION_ITEM_PRICE_UP   = "ul.alarmList > section:has(svg.alarmPriceIncreaseSVG)"
    NOTIFICATION_ITEM_PRICE_DOWN = "ul.alarmList > section:has(svg.alarmPriceDecreaseSVG)"

    # ── 액션 버튼 및 기타 ─────────────────────────────────────────────
    READ_ALL_BTN              = "section.alarmContentContainer button:has-text('전체 읽음')"
    NOTIFICATION_SCROLL_AREA  = "section.alarmContentContainer div[class*='overflow-auto']"
    NOTIFICATION_FOOTER_TEXT  = "section.alarmContentContainer p:has-text('최근 7일간')"

    # ── 탭 ────────────────────────────────────────────────────────────
    _TAB_ROOT = "[role='tablist'][aria-label='tab list in alarm center']"
    TAB_ALL          = f"{_TAB_ROOT} button:has-text('전체')"
    TAB_NEWS         = f"{_TAB_ROOT} button:has-text('뉴스')"
    TAB_REPLY        = f"{_TAB_ROOT} button:has-text('댓글')"
    TAB_ANNOUNCEMENT = f"{_TAB_ROOT} button:has-text('소식')"
    TAB_REWARD       = f"{_TAB_ROOT} button:has-text('리워드')"
    TAB_SELECTED     = f"{_TAB_ROOT} button[class*='_selected']"
    TAB_NEW_DOT      = f"{_TAB_ROOT} div[class*='_newAlarmCircle']"

    # ── Empty State ──────────────────────────────────────────────────
    NOTIFICATION_EMPTY_STATE = (
        "section.alarmContentContainer p:has-text('아직 받은 알림이 없습니다'), "
        "section.alarmContentContainer p:has-text('알림이 없습니다')"
    )

    # ── 에러/로그인 감지 ─────────────────────────────────────────────
    ERROR_PAGE           = "p:has-text('이용에 불편을 드려 죄송합니다'), h1:has-text('이용에 불편을 드려 죄송합니다')"
    LOGIN_PAGE_CONTAINER = "main#signInContainer"
    SIGNIN_PATH          = "/user/signin"
    MAIN_PATH            = "/"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def _safe_goto(self, url: str) -> None:
        """about:blank 충돌 방지"""
        for attempt in range(2):
            try:
                self.page.wait_for_timeout(300)
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Exception as e:
                if attempt == 0 and ("about:blank" in str(e) or "interrupted" in str(e)):
                    self.page.wait_for_timeout(800)
                    continue
                raise

    def go_to_main(self) -> None:
        self._safe_goto(self.BASE_URL)
        self.page.wait_for_timeout(500)

    def refresh_page(self) -> None:
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  GNB 상태 확인
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_visible(self) -> bool:
        return self.page.is_visible(self.GNB_HEADER)

    def is_gnb_logged_in_state(self) -> bool:
        return self.page.locator(self.GNB_PROFILE_ICON).count() > 0

    def is_login_page_visible(self) -> bool:
        return (
            self.SIGNIN_PATH in self.page.url
            or self.page.locator(self.LOGIN_PAGE_CONTAINER).count() > 0
        )

    # ══════════════════════════════════════════════════════════════════
    #  GNB 알림 아이콘 (Hidden 우회 핵심 로직)
    # ══════════════════════════════════════════════════════════════════

    def is_notification_icon_visible(self) -> bool:
        """GNB 알림 아이콘 노출 여부 (DOM 존재 여부로 판단)"""
        return self.page.locator(self.GNB_NOTIFICATION_ICON).count() > 0

    def click_notification_icon(self) -> None:
        """
        GNB 알림 아이콘 클릭 → 알림 모달 오픈
        ※ 모바일/데스크톱 중복 버튼의 hidden 속성 때문에 3단계 폴백 적용
        """
        # 1) :visible 필터로 진짜 눈에 보이는 버튼만 찾아서 클릭 시도
        visible_btn = self.page.locator(self.GNB_NOTIFICATION_ICON_VISIBLE)
        if visible_btn.count() > 0:
            try:
                visible_btn.first.click()
                self.page.wait_for_timeout(500)
                return
            except Exception:
                pass  # 실패하면 다음으로

        # 2) attached 상태만 확인하고 강제(force=True) 클릭
        icon = self.page.locator(self.GNB_NOTIFICATION_ICON).first
        icon.wait_for(state="attached", timeout=8_000)
        try:
            icon.click(force=True)
            self.page.wait_for_timeout(500)
            return
        except Exception:
            pass

        # 3) 최후의 수단: JavaScript로 직접 클릭 이벤트 발생
        icon.evaluate("(el) => el.click()")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  알림 배지
    # ══════════════════════════════════════════════════════════════════

    def is_notification_badge_visible(self) -> bool:
        if self.page.locator(self.GNB_NOTIFICATION_BADGE).count() > 0:
            return True
        try:
            btn_html = self.page.locator(self.GNB_NOTIFICATION_ICON).first.inner_html()
            return "FF4A69" in btn_html or "badge" in btn_html.lower()
        except Exception:
            return False

    def get_badge_count_text(self) -> str:
        try:
            return self.page.locator(self.BADGE_COUNT_TEXT).first.inner_text().strip()
        except Exception:
            return ""

    def get_badge_count_as_number(self) -> int:
        text = self.get_badge_count_text()
        try:
            return int(text.replace("+", "").strip())
        except Exception:
            return -1

    # ══════════════════════════════════════════════════════════════════
    #  알림 모달 컨트롤
    # ══════════════════════════════════════════════════════════════════

    def is_notification_modal_visible(self) -> bool:
        """알림 모달의 실제 노출 여부 확인"""
        locator = self.page.locator(self.NOTIFICATION_MODAL).first
        if locator.count() == 0:
            return False
        try:
            return locator.is_visible()
        except Exception:
            return True  # is_visible 측정 실패 시 DOM에 있으면 True

    def open_notification_modal(self) -> None:
        """모달을 연다. (최대 5초 대기)"""
        if self.is_notification_modal_visible():
            return
        self.click_notification_icon()
        try:
            self.page.locator(self.NOTIFICATION_MODAL).first.wait_for(
                state="visible", timeout=5_000
            )
        except Exception:
            self.page.locator(self.NOTIFICATION_MODAL).first.wait_for(
                state="attached", timeout=2_000
            )

    def close_notification_modal_by_close_btn(self) -> None:
        """모달 내 X 아이콘(SVG) 클릭으로 닫기"""
        close_svg = self.page.locator(self.NOTIFICATION_MODAL_CLOSE)
        if close_svg.count() > 0:
            try:
                close_svg.first.click(force=True)
            except Exception:
                close_svg.first.evaluate("(el) => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
        else:
            self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(400)

    def close_notification_modal_by_dim(self) -> None:
        """화면 좌측 상단 빈 공간을 클릭하여 딤 클릭 효과 시뮬레이션"""
        self.page.mouse.click(10, 10)
        self.page.wait_for_timeout(400)

    def wait_for_modal_dismiss(self, timeout: int = 3_000) -> bool:
        try:
            self.page.locator(self.NOTIFICATION_MODAL).first.wait_for(
                state="hidden", timeout=timeout
            )
            return True
        except Exception:
            return self.page.locator(self.NOTIFICATION_MODAL).count() == 0

    # ══════════════════════════════════════════════════════════════════
    #  알림 리스트 & 스크롤
    # ══════════════════════════════════════════════════════════════════

    def is_notification_list_visible(self) -> bool:
        return self.page.locator(self.NOTIFICATION_LIST).count() > 0

    def get_notification_item_count(self) -> int:
        return self.page.locator(self.NOTIFICATION_ITEM).count()

    def get_notification_item_text(self, index: int = 0) -> str:
        try:
            return self.page.locator(self.NOTIFICATION_ITEM).nth(index).inner_text().strip()
        except Exception:
            return ""

    def scroll_notification_list_to_bottom(self, steps: int = 5) -> None:
        """무한 스크롤 트리거를 위해 리스트 끝까지 스크롤"""
        scroll_area = self.page.locator(self.NOTIFICATION_SCROLL_AREA).first
        if scroll_area.count() == 0:
            return
        for _ in range(steps):
            try:
                scroll_area.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")
            except Exception:
                break
            self.page.wait_for_timeout(700)

    # ══════════════════════════════════════════════════════════════════
    #  읽음/안 읽음 액션
    # ══════════════════════════════════════════════════════════════════

    def get_unread_item_count(self) -> int:
        return self.page.locator(self.UNREAD_NOTIFICATION_ITEM).count()

    def get_read_item_count(self) -> int:
        return self.page.locator(self.READ_NOTIFICATION_ITEM).count()

    def is_unread_item_visible(self) -> bool:
        return self.get_unread_item_count() > 0

    def click_unread_notification_item(self, index: int = 0) -> None:
        """안 읽은 알림을 클릭하여 읽음 처리 및 이동"""
        locator = self.page.locator(self.UNREAD_NOTIFICATION_ITEM).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        try:
            locator.scroll_into_view_if_needed(timeout=2_000)
        except Exception:
            pass
        locator.click(force=True)
        self.page.wait_for_timeout(700)

    def is_read_all_btn_visible(self) -> bool:
        return self.page.locator(self.READ_ALL_BTN).count() > 0

    def click_read_all_btn(self) -> None:
        self.page.locator(self.READ_ALL_BTN).first.click(force=True)
        self.page.wait_for_timeout(800)

    # ══════════════════════════════════════════════════════════════════
    #  특정 타입별 라우팅 클릭 (FULLTC-338~341)
    # ══════════════════════════════════════════════════════════════════

    def click_first_notice_notification(self) -> bool:
        """공지사항 알림 첫 번째 클릭"""
        loc = self.page.locator(self.NOTIFICATION_ITEM_NOTICE).first
        if loc.count() == 0:
            return False
        loc.click(force=True)
        self.page.wait_for_timeout(700)
        return True

    def click_first_news_notification(self) -> bool:
        """뉴스 알림 첫 번째 클릭"""
        loc = self.page.locator(self.NOTIFICATION_ITEM_NEWS).first
        if loc.count() == 0:
            return False
        loc.click(force=True)
        self.page.wait_for_timeout(700)
        return True

    def click_first_reply_notification(self) -> bool:
        """댓글 알림 첫 번째 클릭"""
        loc = self.page.locator(self.NOTIFICATION_ITEM_COMMENT).first
        if loc.count() == 0:
            return False
        loc.click(force=True)
        self.page.wait_for_timeout(700)
        return True

    def click_first_reward_notification(self) -> bool:
        """리워드 알림 첫 번째 클릭"""
        loc = self.page.locator(self.NOTIFICATION_ITEM_REWARD).first
        if loc.count() == 0:
            return False
        loc.click(force=True)
        self.page.wait_for_timeout(700)
        return True

    # ══════════════════════════════════════════════════════════════════
    #  알림 탭 이동
    # ══════════════════════════════════════════════════════════════════

    def click_tab_all(self) -> None:
        btn = self.page.locator(self.TAB_ALL)
        if btn.count() > 0: btn.first.click()

    def click_tab_news(self) -> None:
        btn = self.page.locator(self.TAB_NEWS)
        if btn.count() > 0: btn.first.click()

    def click_tab_reply(self) -> None:
        btn = self.page.locator(self.TAB_REPLY)
        if btn.count() > 0: btn.first.click()

    def click_tab_announcement(self) -> None:
        btn = self.page.locator(self.TAB_ANNOUNCEMENT)
        if btn.count() > 0: btn.first.click()

    def click_tab_reward(self) -> None:
        btn = self.page.locator(self.TAB_REWARD)
        if btn.count() > 0: btn.first.click()

    # ══════════════════════════════════════════════════════════════════
    #  Empty State
    # ══════════════════════════════════════════════════════════════════

    def is_notification_empty_state_visible(self) -> bool:
        if self.page.locator(self.NOTIFICATION_EMPTY_STATE).count() > 0:
            return True
        return (
            "아직 받은 알림이 없습니다" in self.page.content()
            or "알림이 없습니다" in self.page.content()
        )

    def get_notification_empty_text(self) -> str:
        try:
            return self.page.locator(self.NOTIFICATION_EMPTY_STATE).first.inner_text().strip()
        except Exception:
            return ""