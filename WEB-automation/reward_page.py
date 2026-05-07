"""
pages/web/reward_page.py
[STEP 2 — POM v1]  리워드(Reward) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
셀렉터 전략:
    - CSS Modules 해시 클래스 직접 사용 금지 → [class*='...'] 부분 매칭
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > 시맨틱 태그+구조 > 안정 CSS 클래스
    - Next.js SPA 링크: locator.get_attribute("href") + page.goto() 방식
    - domcontentloaded 사용 — networkidle 30초 타임아웃 방지
    - ⚠️  TODO_ 접두사 셀렉터는 F12 → 실제 DOM 확인 후 반드시 교체 필요

    리워드 URL 패턴:
        리워드 메인    : /reward/ste
        STAT 내역      : /mypage/reward (또는 /mypage/reward/STAT 등)
        커뮤니티       : /community  (댓글 작성 트리거)

    TC 도메인 구성:
        접근 권한    : FULLTC-243~246  (비로그인/로그인 접근)
        메인 페이지  : FULLTC-247~248  (STAT 잔액, 내역 이동)
        출석 체크    : FULLTC-249~250  (획득, 중복 방지)
        미션         : FULLTC-251~252  (획득, 중복 방지)
        댓글 지급    : FULLTC-253~255  (지급, 잔액, 내역)
        일일 한도    : FULLTC-256~258  (한도 초과, 미지급, 익일 초기화)
        댓글 회수    : FULLTC-259~263  (삭제 회수, 잔액, 알림, 내역, 사용 처리)
        금칙어       : FULLTC-264~266  (차단, 보상 미지급, UI)
        내역 페이징  : FULLTC-267~270  (적립/사용 페이징, Empty State)
        네트워크 오류: FULLTC-271~273  (연결 끊김, 중복 방지, Throttle)
"""

from playwright.sync_api import Page


class RewardPage:
    """블루밍비트 리워드(Reward) 도메인 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS
    # ══════════════════════════════════════════════════════════════════

    # ── GNB ──────────────────────────────────────────────────────────
    GNB_HEADER = "header#headerContainer"

    # GNB '리워드' 탭
    # ⚠️ TODO: data-label 또는 href 확인 후 교체
    GNB_REWARD_TAB = (
        "#menuWithMySettingContainer nav a[data-label='리워드'], "
        "#menuWithMySettingContainer nav a[href*='/reward']"
    )

    # 로그인 상태 GNB 프로필 버튼 (로그인 시에만 존재)
    GNB_PROFILE_ICON = "div.myInfo button:has(div.userProfileImage)"

    # GNB STAT 잔액 링크 (로그인 시에만 존재)
    # HTML: <a class="...rewardValueCompWrapper..." href="/mypage/reward">
    GNB_STAT_BALANCE = (
        "a[class*='rewardValueCompWrapper'], "
        "a[href='/mypage/reward']"
    )

    # ── 리워드 메인 페이지 컨테이너 ─────────────────────────────────
    # HTML: <main id="steMainPageContainer" class="...steMainPageContainer...">
    REWARD_MAIN = "main#steMainPageContainer"

    # 내 활동 섹션 컨테이너
    # HTML: <div class="...mySteActivityContainer...">
    MY_ACTIVITY_SECTION = "div[class*='mySteActivityContainer']"

    # ── STAT 잔액 영역 (로그인 시) ───────────────────────────────────
    # HTML: <button class="...myBalanceBox...">
    #         <div class="...myBalanceLabel...">보유중 →</div>
    #         <div class="...myBalanceAmountBox...">
    #           <div class="...myBalanceAmount...">
    #             <span class="...value...">32,964</span>
    #             <span class="...unit...">STAT</span>
    #           </div>
    #         </div>
    #       </button>
    STAT_BALANCE_SECTION = (
        "button[class*='myBalanceBox'], "
        "div[class*='myBalanceWrapper']"
    )

    # 잔액 숫자 텍스트
    # HTML: <span class="...value...">32,964</span>
    STAT_BALANCE_VALUE = (
        "button[class*='myBalanceBox'] span[class*='value'], "
        "div[class*='myBalanceAmount'] span[class*='value']"
    )

    # STAT 단위 텍스트 ('STAT' 문자)
    STAT_UNIT_TEXT = "button[class*='myBalanceBox'] span[class*='unit']"

    # '보유중' 버튼 클릭 → STAT 내역 페이지 이동 (버튼 자체가 내역 링크)
    # HTML: <button class="...myBalanceBox..."> (클릭 시 /mypage/reward 이동)
    STAT_HISTORY_BTN = (
        "button[class*='myBalanceBox'], "
        "a[href*='/mypage/reward']"
    )

    # ── 비로그인 전용 안내 UI ─────────────────────────────────────────
    # 비로그인 시 /reward/ste URL 그대로 유지하면서 아래 UI 노출
    # HTML: <div class="...loginGuideBox...">
    #         <p class="...loginGuideText...">로그인 후 확인할 수 있어요!</p>
    #         <button class="...loginBtn...">로그인 하기</button>
    #       </div>
    GUEST_LOGIN_GUIDE    = "div[class*='loginGuideBox']"
    GUEST_LOGIN_GUIDE_TEXT = "p[class*='loginGuideText']"
    GUEST_LOGIN_BTN_REWARD = "button[class*='loginBtn']"  # 리워드 페이지 내 로그인 버튼

    # ── 출석 체크 섹션 ───────────────────────────────────────────────
    # ⚠️ TODO: 출석 체크 섹션 class 확인 후 교체
    ATTENDANCE_SECTION = (
        "[data-testid='TODO_attendanceSection'], "
        "section[class*='TODO_attendance'], "
        "div[class*='TODO_attendanceCheck'], "
        "div[class*='TODO_dailyCheck']"
    )

    # 출석 체크 버튼 (미완료 상태)
    # ⚠️ TODO: 출석 버튼 class/text 확인 후 교체
    ATTENDANCE_BTN = (
        "[data-testid='TODO_attendanceBtn'], "
        "button[class*='TODO_attendanceBtn'], "
        "button:has-text('출석 체크'), "
        "button:has-text('출석하기')"
    )

    # 출석 체크 완료 상태 요소
    # ⚠️ TODO: 완료 상태 class/text 확인 후 교체
    ATTENDANCE_COMPLETE = (
        "[data-testid='TODO_attendanceComplete'], "
        "button[class*='TODO_attendanceDone'], "
        "div[class*='TODO_checked'], "
        "span:has-text('출석 완료'), "
        "span:has-text('이미 출석'), "
        "button[disabled]:has-text('출석')"
    )

    # ── 미션 섹션 ───────────────────────────────────────────────────
    # ⚠️ TODO: 미션 섹션 class 확인 후 교체
    MISSION_SECTION = (
        "[data-testid='TODO_missionSection'], "
        "section[class*='TODO_mission'], "
        "div[class*='TODO_missionList']"
    )

    # 개별 미션 아이템
    MISSION_ITEM = (
        "[data-testid='TODO_missionItem'], "
        "div[class*='TODO_missionItem'], "
        "li[class*='TODO_missionCard']"
    )

    # 미션 완료 버튼 (미완료 미션)
    MISSION_COMPLETE_BTN = (
        "[data-testid='TODO_missionCompleteBtn'], "
        "button[class*='TODO_missionBtn'], "
        "button:has-text('받기'), "
        "button:has-text('완료하기')"
    )

    # 미션 완료 상태
    MISSION_COMPLETE_STATE = (
        "[data-testid='TODO_missionDone'], "
        "span[class*='TODO_missionDone'], "
        "button[disabled][class*='TODO_missionBtn'], "
        "span:has-text('완료'), "
        "div[class*='TODO_completed']"
    )

    # ── STE 캠페인 / 댓글 리워드 영역 ─────────────────────────────
    # ⚠️ TODO: STE 캠페인 섹션 class 확인 후 교체
    STE_CAMPAIGN_SECTION = (
        "[data-testid='TODO_steCampaign'], "
        "section[class*='TODO_ste'], "
        "div[class*='TODO_steSection'], "
        "div[class*='TODO_campaignList']"
    )

    # ── 리워드 알림/토스트 ───────────────────────────────────────────
    # 리워드 지급 완료 토스트 메시지
    # ⚠️ TODO: 토스트 class 확인 후 교체
    REWARD_TOAST = (
        "[data-testid='TODO_rewardToast'], "
        "div[class*='TODO_rewardToast'], "
        ".Toastify__toast, "
        "div[class*='toast']:has-text('적립'), "
        "div[class*='toast']:has-text('STAT')"
    )

    # 리워드 회수 알림 토스트
    REWARD_DEDUCT_TOAST = (
        "[data-testid='TODO_rewardDeductToast'], "
        "div[class*='toast']:has-text('회수'), "
        "div[class*='toast']:has-text('차감'), "
        ".Toastify__toast:has-text('회수')"
    )

    # ── 댓글 관련 (커뮤니티 페이지 / 게시물 상세 페이지) ──────────────
    # 커뮤니티 페이지: div.ql-editor
    # 게시물 상세 페이지 이동 후: 동일한 Quill 에디터 또는 contenteditable div
    # ⚠️ 금칙어 차단 후 게시물 상세(/community/post/...)로 이동 가능 → 범용 셀렉터 사용
    COMMENT_INPUT = (
        "div.ql-editor[contenteditable='true'], "
        "div[contenteditable='true'], "
        "textarea[placeholder*='댓글'], "
        "textarea[placeholder*='내용']"
    )

    # 댓글 등록 버튼
    COMMENT_SUBMIT_BTN = (
        "#customToolbar button:has(span:text-is('등록')), "
        "#portal-modal button:has(span:text-is('등록')), "
        "button[class*='TODO_commentSubmit']:has-text('등록'), "
        "button:has-text('등록')"
    )

    # 금칙어 차단 안내 메시지
    PROFANITY_BLOCK_MSG = (
        "[data-testid='TODO_profanityMsg'], "
        "p[class*='TODO_profanityError'], "
        "span:has-text('부적절한 표현'), "
        "p:has-text('금칙어'), "
        "div:has-text('부적절한 표현이 포함')"
    )

    # 일일 한도 초과 안내 메시지
    DAILY_LIMIT_MSG = (
        "[data-testid='TODO_dailyLimitMsg'], "
        "p[class*='TODO_limitMessage'], "
        "span:has-text('한도'), "
        "div:has-text('오늘의 댓글 리워드 한도'), "
        "p:has-text('리워드 한도')"
    )

    # ── 리워드 내역 페이지 ───────────────────────────────────────────
    # ⚠️ TODO: 내역 페이지 main/section ID 확인 후 교체
    REWARD_HISTORY_MAIN = (
        "[data-testid='TODO_rewardHistoryMain'], "
        "main[id*='TODO_rewardHistory'], "
        "main[class*='TODO_historyPage'], "
        "section[class*='TODO_rewardHistory']"
    )

    # '적립' 탭
    HISTORY_EARN_TAB = (
        "[data-testid='TODO_earnTab'], "
        "button[class*='TODO_earnTab']:has-text('적립'), "
        "button:has-text('적립')"
    )

    # '사용' 탭
    HISTORY_USE_TAB = (
        "[data-testid='TODO_useTab'], "
        "button[class*='TODO_useTab']:has-text('사용'), "
        "button:has-text('사용')"
    )

    # 내역 아이템 목록
    HISTORY_ITEM = (
        "[data-testid='TODO_historyItem'], "
        "li[class*='TODO_historyItem'], "
        "div[class*='TODO_rewardHistoryItem']"
    )

    # 내역 더보기 버튼 (페이징)
    HISTORY_LOAD_MORE = (
        "[data-testid='TODO_loadMore'], "
        "button[class*='TODO_loadMore']:has-text('더보기'), "
        "button:has-text('더보기')"
    )

    # 빈 상태(Empty State) UI
    HISTORY_EMPTY_STATE = (
        "[data-testid='TODO_emptyState'], "
        "div[class*='TODO_emptyState'], "
        "p:has-text('내역이 없습니다'), "
        "p:has-text('아직 내역이 없어요'), "
        "div[class*='TODO_empty']"
    )

    # ── 로그인 화면 감지 ──────────────────────────────────────────────
    LOGIN_PAGE_CONTAINER = "main#signInContainer"
    SIGNIN_PATH          = "/user/signin"

    # ── 에러 페이지 ──────────────────────────────────────────────────
    ERROR_PAGE = (
        "p:has-text('이용에 불편을 드려 죄송합니다'), "
        "h1:has-text('이용에 불편을 드려 죄송합니다')"
    )

    # ── 네트워크/로딩 ───────────────────────────────────────────────
    # 로딩 인디케이터 (API 요청 중)
    LOADING_INDICATOR = (
        "[data-testid='TODO_loading'], "
        "div[class*='TODO_loadingSpinner'], "
        "div[class*='TODO_skeleton'], "
        "svg[class*='TODO_spinner']"
    )

    # 네트워크 오류 안내 메시지
    NETWORK_ERROR_MSG = (
        "[data-testid='TODO_networkError'], "
        "p:has-text('네트워크 오류'), "
        "p:has-text('잠시 후 다시 시도'), "
        "div:has-text('연결이 끊어졌습니다')"
    )

    # ── URL 패턴 ────────────────────────────────────────────────────
    REWARD_MAIN_PATH     = "/reward/ste"
    REWARD_HISTORY_PATH  = "/mypage/reward"
    COMMUNITY_PATH       = "/community"
    MAIN_PATH            = "/"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def go_to_reward_main(self) -> None:
        """리워드 메인(/reward/ste)으로 이동
        ※ wait_until='domcontentloaded' — networkidle 30초 타임아웃 방지
        """
        self.page.goto(
            f"{self.BASE_URL}{self.REWARD_MAIN_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_reward_history(self) -> None:
        """STAT 내역 페이지(/mypage/reward)로 이동"""
        self.page.goto(
            f"{self.BASE_URL}{self.REWARD_HISTORY_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_community(self) -> None:
        """커뮤니티 페이지로 이동"""
        self.page.goto(
            f"{self.BASE_URL}{self.COMMUNITY_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_main(self) -> None:
        """메인 페이지로 이동"""
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    def click_gnb_reward_tab(self) -> None:
        """GNB '리워드' 탭 클릭 → href goto 방식"""
        locator = self.page.locator(self.GNB_REWARD_TAB).first
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

    def scroll_to_bottom(self, steps: int = 3) -> None:
        """페이지 하단으로 스크롤 (무한 스크롤 트리거용)"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(600)

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_visible(self) -> bool:
        """GNB 헤더 노출 여부"""
        return self.page.is_visible(self.GNB_HEADER)

    def is_reward_main_loaded(self) -> bool:
        """리워드 메인 페이지 로드 완료 여부"""
        if self.REWARD_MAIN_PATH not in self.page.url:
            return False
        try:
            self.page.wait_for_selector(self.REWARD_MAIN, timeout=8_000)
            return True
        except Exception:
            return self.REWARD_MAIN_PATH in self.page.url

    def is_login_page_visible(self) -> bool:
        """로그인 페이지(/user/signin) 또는 로그인 유도 UI 노출 여부"""
        if self.SIGNIN_PATH in self.page.url:
            return True
        return self.page.locator(self.LOGIN_PAGE_CONTAINER).count() > 0

    def is_guest_login_guide_visible(self) -> bool:
        """비로그인 전용 안내 UI 노출 여부
        ※ 비로그인 시 /reward/ste URL 유지하며 loginGuideBox 노출됨
           HTML: <div class="...loginGuideBox...">
                   <p>로그인 후 확인할 수 있어요!</p>
                   <button>로그인 하기</button>
                 </div>
        """
        if self.page.locator(self.GUEST_LOGIN_GUIDE).count() > 0:
            return True
        if self.page.locator(self.GUEST_LOGIN_BTN_REWARD).count() > 0:
            return True
        return "로그인 후 확인할 수 있어요" in self.page.content()

    def is_error_page_visible(self) -> bool:
        """에러 페이지 노출 여부"""
        return self.page.locator(self.ERROR_PAGE).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  GNB 상태 확인
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_reward_tab_visible(self) -> bool:
        """GNB '리워드' 탭 노출 여부"""
        return self.page.locator(self.GNB_REWARD_TAB).count() > 0

    def is_gnb_logged_in_state(self) -> bool:
        """로그인 상태 여부 (div.userProfileImage 존재 기반)"""
        if self.page.locator("div.myInfo div.userProfileImage").count() > 0:
            return True
        return self.page.locator("a[class*='rewardValueCompWrapper']").count() > 0

    def get_gnb_stat_text(self) -> str:
        """GNB STAT 잔액 텍스트 반환"""
        try:
            return self.page.locator("div[class*='rewordValue']").first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  STAT 잔액 영역
    # ══════════════════════════════════════════════════════════════════

    def is_stat_balance_section_visible(self) -> bool:
        """보유 STAT 잔액 섹션 노출 여부"""
        return self.page.locator(self.STAT_BALANCE_SECTION).count() > 0

    def get_stat_balance_value(self) -> str:
        """보유 STAT 잔액 숫자 텍스트 반환"""
        try:
            return self.page.locator(self.STAT_BALANCE_VALUE).first.inner_text().strip()
        except Exception:
            return ""

    def get_stat_balance_as_number(self) -> int:
        """보유 STAT 잔액을 정수로 반환 (콤마 제거)"""
        text = self.get_stat_balance_value()
        try:
            return int(text.replace(",", "").replace(".", "").strip())
        except Exception:
            return -1

    def click_stat_history_btn(self) -> None:
        """'내역' 버튼 클릭 → STAT 내역 페이지 이동"""
        locator = self.page.locator(self.STAT_HISTORY_BTN).first
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

    def is_stat_history_page(self) -> bool:
        """현재 URL이 STAT 내역 페이지인지 확인"""
        return self.REWARD_HISTORY_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  출석 체크
    # ══════════════════════════════════════════════════════════════════

    def is_attendance_section_visible(self) -> bool:
        """출석 체크 섹션 노출 여부"""
        return self.page.locator(self.ATTENDANCE_SECTION).count() > 0

    def is_attendance_btn_visible(self) -> bool:
        """출석 체크 버튼 노출 여부 (미완료 상태)"""
        return self.page.locator(self.ATTENDANCE_BTN).count() > 0

    def is_attendance_completed(self) -> bool:
        """출석 체크 완료 상태 여부"""
        return self.page.locator(self.ATTENDANCE_COMPLETE).count() > 0

    def click_attendance_btn(self) -> None:
        """출석 체크 버튼 클릭"""
        self.page.locator(self.ATTENDANCE_BTN).first.click()
        self.page.wait_for_timeout(800)

    # ══════════════════════════════════════════════════════════════════
    #  미션
    # ══════════════════════════════════════════════════════════════════

    def is_mission_section_visible(self) -> bool:
        """미션 섹션 노출 여부"""
        return self.page.locator(self.MISSION_SECTION).count() > 0

    def get_mission_item_count(self) -> int:
        """미션 아이템 수 반환"""
        return self.page.locator(self.MISSION_ITEM).count()

    def is_mission_complete_btn_visible(self) -> bool:
        """완료 가능한 미션 버튼 노출 여부"""
        return self.page.locator(self.MISSION_COMPLETE_BTN).count() > 0

    def click_mission_complete_btn(self, index: int = 0) -> None:
        """미션 완료 버튼 클릭"""
        self.page.locator(self.MISSION_COMPLETE_BTN).nth(index).click()
        self.page.wait_for_timeout(800)

    def is_mission_completed(self, index: int = 0) -> bool:
        """특정 미션 완료 상태 여부"""
        return self.page.locator(self.MISSION_COMPLETE_STATE).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  리워드 알림/토스트
    # ══════════════════════════════════════════════════════════════════

    def is_reward_toast_visible(self) -> bool:
        """리워드 지급 토스트 메시지 노출 여부"""
        return self.page.locator(self.REWARD_TOAST).count() > 0

    def is_reward_deduct_toast_visible(self) -> bool:
        """리워드 회수 토스트 메시지 노출 여부"""
        if self.page.locator(self.REWARD_DEDUCT_TOAST).count() > 0:
            return True
        return "회수" in self.page.content() or "차감" in self.page.content()

    def wait_for_reward_toast(self, timeout: int = 5_000) -> bool:
        """리워드 토스트 메시지 출현 대기 (최대 timeout ms)"""
        try:
            self.page.locator(self.REWARD_TOAST).first.wait_for(
                state="visible", timeout=timeout
            )
            return True
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  댓글 작성 (커뮤니티)
    # ══════════════════════════════════════════════════════════════════

    def write_comment(self, text: str) -> None:
        """커뮤니티 댓글 입력창에 텍스트 입력"""
        input_el = self.page.locator(self.COMMENT_INPUT).first
        input_el.wait_for(state="visible", timeout=5_000)
        input_el.click()
        input_el.fill(text)
        self.page.wait_for_timeout(300)

    def submit_comment(self) -> None:
        """댓글 등록 버튼 클릭"""
        self.page.locator(self.COMMENT_SUBMIT_BTN).first.click()
        self.page.wait_for_timeout(800)

    def is_profanity_block_msg_visible(self) -> bool:
        """금칙어 차단 안내 메시지 노출 여부"""
        if self.page.locator(self.PROFANITY_BLOCK_MSG).count() > 0:
            return True
        return "부적절한 표현" in self.page.content() or "금칙어" in self.page.content()

    def is_daily_limit_msg_visible(self) -> bool:
        """일일 댓글 리워드 한도 초과 안내 메시지 노출 여부"""
        if self.page.locator(self.DAILY_LIMIT_MSG).count() > 0:
            return True
        return "한도" in self.page.content() or "오늘의 댓글 리워드" in self.page.content()

    # ══════════════════════════════════════════════════════════════════
    #  리워드 내역 페이지
    # ══════════════════════════════════════════════════════════════════

    def is_reward_history_loaded(self) -> bool:
        """리워드 내역 페이지 로드 완료 여부"""
        try:
            self.page.wait_for_selector(self.REWARD_HISTORY_MAIN, timeout=8_000)
            return True
        except Exception:
            return self.REWARD_HISTORY_PATH in self.page.url

    def click_earn_tab(self) -> None:
        """'적립' 탭 클릭"""
        self.page.locator(self.HISTORY_EARN_TAB).first.click()
        self.page.wait_for_timeout(500)

    def click_use_tab(self) -> None:
        """'사용' 탭 클릭"""
        self.page.locator(self.HISTORY_USE_TAB).first.click()
        self.page.wait_for_timeout(500)

    def get_history_item_count(self) -> int:
        """내역 아이템 수 반환"""
        return self.page.locator(self.HISTORY_ITEM).count()

    def click_load_more(self) -> None:
        """'더보기' 버튼 클릭 (페이징)"""
        self.page.locator(self.HISTORY_LOAD_MORE).first.click()
        self.page.wait_for_timeout(800)

    def is_load_more_visible(self) -> bool:
        """'더보기' 버튼 노출 여부"""
        return self.page.locator(self.HISTORY_LOAD_MORE).count() > 0

    def is_history_empty_state(self) -> bool:
        """내역 빈 상태(Empty State) 노출 여부"""
        if self.page.locator(self.HISTORY_EMPTY_STATE).count() > 0:
            return True
        return "내역이 없습니다" in self.page.content() or "내역이 없어요" in self.page.content()

    def get_first_history_item_text(self) -> str:
        """가장 최신 내역 아이템 텍스트 반환"""
        try:
            return self.page.locator(self.HISTORY_ITEM).first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  네트워크 / 로딩
    # ══════════════════════════════════════════════════════════════════

    def is_loading_visible(self) -> bool:
        """로딩 인디케이터 노출 여부"""
        return self.page.locator(self.LOADING_INDICATOR).count() > 0

    def is_network_error_msg_visible(self) -> bool:
        """네트워크 오류 안내 메시지 노출 여부"""
        if self.page.locator(self.NETWORK_ERROR_MSG).count() > 0:
            return True
        return "네트워크 오류" in self.page.content() or "잠시 후 다시 시도" in self.page.content()

    def set_network_offline(self) -> None:
        """네트워크 오프라인 모드 설정
        ※ Playwright CDP 기반 네트워크 에뮬레이션
        """
        try:
            self.page.context.set_offline(True)
        except Exception:
            pass

    def set_network_online(self) -> None:
        """네트워크 온라인 모드 복구"""
        try:
            self.page.context.set_offline(False)
        except Exception:
            pass

    def refresh_page(self) -> None:
        """현재 페이지 새로고침"""
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)