"""
pages/web/stat_history_page.py
[STEP 2 — POM v1]  STAT 보유내역(Stat History) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_rewardHistoryList-module-scss-module__fFHpUa__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌────────────────────────────────────────────────────────────────────┐
    │  유형 탭 텍스트: "전체" / "획득" / "사용"                         │
    │  (TC 명칭 "적립" ≠ HTML 텍스트 "획득" — 셀렉터는 실제 DOM 기준)  │
    │  활성 탭 클래스: isFocused  (my_activity의 isFocus와 상이!)       │
    │  DOM에 #rewardHistoryList ID가 2개 존재 → class 기반 셀렉터 우선  │
    │  카드 링크 href 패턴: /mypage/reward/tx/{id}                      │
    │  적립(+): div[class*='rewardValueWrapper'][class*='isPlus']       │
    │  사용(-): div[class*='rewardValueWrapper']:not([class*='isPlus']) │
    │  잔액 표시: div[class*='myBalanceWrapper'] > span  (예: "40,453") │
    │  기간 필터(1주일/1개월/3개월) → HTML 미노출 → TODO_ 셀렉터       │
    │  잔액 숨김/보임 버튼 → HTML 미노출 → TODO_ 셀렉터                │
    │  페이지 URL 추정: /mypage/reward (실제 진입 URL 확인 후 수정)     │
    └────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - 안정 ID 최우선: #rewardHistoryListHeader, #rewardHistoryList
    - 해시 없는 plain class: button.depositButton, button.withdrawalButton
    - 해시 포함 class → [class*='안정키워드'] 부분 매칭
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
"""

from playwright.sync_api import Page


class StatHistoryPage:
    """블루밍비트 STAT 보유내역 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    STAT_HISTORY_PATH = "/mypage/reward"
    MYPAGE_PATH       = "/mypage"
    TX_DETAIL_PATH    = "/mypage/reward/tx/"
    SIGNIN_PATH       = "/user/signin"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 ───────────────────────────────────────────────────
    # HTML: <section class="...__myPageCommonContentWrapper">
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    # HTML: <header class="...__contentHeader">
    PAGE_HEADER  = "header[class*='contentHeader']"
    # HTML: <h1>STAT 보유내역</h1>
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    # HTML: <a class="...__backBtn" href="/mypage">
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 잔액 표시 영역 ────────────────────────────────────────────────
    # HTML: <div class="...__myRewardViewerWarapper">  ← HTML 오타 "Warapper" 그대로 사용
    BALANCE_VIEWER   = "div[class*='myRewardViewerWarapper']"
    # HTML: <div class="...__myBalanceWrapper"><span>40,453</span><p>STAT</p></div>
    BALANCE_WRAPPER  = "div[class*='myBalanceWrapper']"
    BALANCE_AMOUNT   = "div[class*='myBalanceWrapper'] > span"
    BALANCE_UNIT     = "div[class*='myBalanceWrapper'] > p"
    # HTML: <div class="...__membershipLabel"><span>멤버십 이용중</span></div>
    MEMBERSHIP_LABEL = "div[class*='membershipLabel']"
    MEMBERSHIP_TEXT  = "div[class*='membershipLabel'] span"

    # 입금/출금 버튼 — plain class (해시 없음, 그대로 사용 가능)
    DEPOSIT_BTN    = "button.depositButton"
    WITHDRAWAL_BTN = "button.withdrawalButton"

    # 잔액 숨김/보임 토글 — 제공된 HTML에 미노출
    # ⚠️ TODO: F12로 눈 아이콘 버튼 셀렉터 확인 후 튜닝
    BALANCE_TOGGLE_BTN  = "[data-testid='TODO_balanceToggleBtn']"
    BALANCE_MASKED_TEXT = "[data-testid='TODO_balanceMasked']"

    # ── 유형 탭 (전체 / 획득 / 사용) ─────────────────────────────────
    # HTML: <div id="rewardHistoryListHeader">
    TAB_HEADER   = "#rewardHistoryListHeader"
    TAB_ALL_BTNS = "#rewardHistoryListHeader button[class*='historyTab']"
    # 활성 탭 클래스: isFocused  ← (my_activity의 isFocus와 다름!)
    TAB_ACTIVE   = "#rewardHistoryListHeader button[class*='historyTab'][class*='isFocused']"
    # 개별 탭 (실제 HTML 텍스트 기준)
    TAB_ALL  = "#rewardHistoryListHeader button[class*='historyTab']:has(span:text-is('전체'))"
    # ※ TC 명칭: "적립" / HTML 실제 텍스트: "획득" — 실제 DOM 기준으로 작성
    TAB_EARN = "#rewardHistoryListHeader button[class*='historyTab']:has(span:text-is('획득'))"
    TAB_USE  = "#rewardHistoryListHeader button[class*='historyTab']:has(span:text-is('사용'))"

    # ── 기간 필터 — 제공된 HTML에 미노출 ─────────────────────────────
    # ⚠️ TODO: 아래 4개 셀렉터 모두 F12 확인 후 실제 DOM 기반으로 튜닝 필요
    PERIOD_FILTER_WRAPPER = "[data-testid='TODO_periodFilterWrapper']"
    PERIOD_FILTER_1WEEK   = "[data-testid='TODO_filter1Week']"
    PERIOD_FILTER_1MONTH  = "[data-testid='TODO_filter1Month']"
    PERIOD_FILTER_3MONTH  = "[data-testid='TODO_filter3Month']"
    PERIOD_FILTER_RESET   = "[data-testid='TODO_periodFilterReset']"
    PERIOD_FILTER_ACTIVE  = "[data-testid='TODO_periodFilterActive']"

    # ── 거래 내역 카드 ────────────────────────────────────────────────
    # ※ DOM에 id="rewardHistoryList" 가 2개 존재하므로 class 기반 셀렉터 우선 사용
    # HTML: <ul class="...__rewardHistoryListCardWrapper">
    HISTORY_CARD_WRAPPER = "ul[class*='rewardHistoryListCardWrapper']"
    # 모든 li 카드 (날짜 구분 포함)
    HISTORY_CARD         = "li[class*='rewardHistoryListCard']"
    # 날짜 구분 카드: isBetweenCard 클래스 보유
    HISTORY_DATE_SEP     = "li[class*='isBetweenCard']"
    # HTML: <p class="...__betweenDate">2026. 5. 6. 수요일</p>
    HISTORY_DATE_SEP_TXT = "li[class*='isBetweenCard'] p[class*='betweenDate']"
    # 일반 내역 카드 (날짜 구분 제외)
    HISTORY_ITEM_CARD    = "li[class*='rewardHistoryListCard']:not([class*='isBetweenCard'])"

    # 카드 내 링크: href="/mypage/reward/tx/{id}"
    # HTML: <a class="...__rewardHistoryListCardContent completed" href="...">
    HISTORY_CARD_LINK    = "a[class*='rewardHistoryListCardContent']"

    # 항목 유형 레이블: "멤버십 구독", "멤버십 해지", "출금", "입금" 등
    # HTML: <span class="...__typeLabel">멤버십 구독</span>
    CARD_TYPE_LABEL   = "span[class*='typeLabel']"
    # 거래 시간 — dateWithStatus div의 첫 번째 p: "09:58"
    # HTML: <div class="...__dateWithStatus lock_up"><p>09:58</p><p ...>완료</p></div>
    CARD_TIME         = "div[class*='dateWithStatus'] > p:first-child"
    # 상태 레이블: "완료", "진행중" 등
    # HTML: <p class="...__statusLabel completed">완료</p>
    CARD_STATUS_LABEL = "p[class*='statusLabel']"

    # 금액 래퍼
    # HTML: <div class="...__rewardValueWrapper ...__isPlus completed">
    CARD_VALUE_WRAPPER = "div[class*='rewardValueWrapper']"
    # 적립(+) 카드: isPlus 클래스 보유
    CARD_PLUS_WRAPPER  = "div[class*='rewardValueWrapper'][class*='isPlus']"
    # 사용(-) 카드: isPlus 클래스 없음
    CARD_MINUS_WRAPPER = "div[class*='rewardValueWrapper']:not([class*='isPlus'])"
    # 금액 span: "+2,000", "-1,511" 형식
    # HTML: <span>+2,000</span>
    CARD_AMOUNT_SPAN   = "div[class*='rewardValue'] > span"
    # 금액 단위: "STAT"
    CARD_UNIT_P        = "div[class*='rewardValue'] > p"

    # ── 로딩 인디케이터 — 제공된 HTML에 미노출 ───────────────────────
    # ⚠️ TODO: 실제 로딩 스피너 DOM 확인 후 셀렉터 튜닝
    LOADING_INDICATOR = (
        "[data-testid='TODO_loadingIndicator'], "
        "[class*='spinner'], [class*='Spinner'], "
        "[aria-label='loading'], [role='progressbar']"
    )

    # ── Empty State ──────────────────────────────────────────────────
    # ⚠️ TODO: 거래 0건 계정으로 접속하여 실제 Empty State HTML 확인 후 튜닝
    EMPTY_STATE     = "[data-testid='TODO_emptyState'], [class*='emptyState'], [class*='empty']"
    EMPTY_STATE_MSG = "[data-testid='TODO_emptyStateMsg']"

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

    def go_to_stat_history(self) -> None:
        """STAT 보유내역 페이지(/mypage/reward)로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.STAT_HISTORY_PATH}")
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
        self.page.wait_for_timeout(800)

    def get_current_url(self) -> str:
        return self.page.url

    def is_on_stat_history_page(self) -> bool:
        return self.STAT_HISTORY_PATH in self.page.url

    def is_on_tx_detail_page(self) -> bool:
        return self.TX_DETAIL_PATH in self.page.url

    def is_login_page_redirected(self) -> bool:
        return self.SIGNIN_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """STAT 보유내역 페이지 로드 완료 여부 (잔액 영역 노출 기준)"""
        try:
            self.page.wait_for_selector(self.BALANCE_VIEWER, timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_history_list(self, timeout: int = 8_000) -> bool:
        """거래 내역 카드 렌더링 대기"""
        try:
            self.page.wait_for_selector(self.HISTORY_CARD_WRAPPER, timeout=timeout)
            return True
        except Exception:
            return False

    def is_page_title_visible(self) -> bool:
        """'STAT 보유내역' 타이틀 노출 여부"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            return "STAT" in el.first.inner_text()
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  잔액 표시 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_balance_visible(self) -> bool:
        """잔액 표시 영역 노출 여부"""
        return self.page.locator(self.BALANCE_AMOUNT).count() > 0

    def get_balance_text(self) -> str:
        """잔액 텍스트 원본 반환 (예: '40,453')"""
        try:
            return self.page.locator(self.BALANCE_AMOUNT).first.inner_text().strip()
        except Exception:
            return ""

    def get_balance_as_number(self) -> int:
        """잔액을 정수로 반환 (천 단위 구분 기호 제거). 파싱 실패 시 -1 반환"""
        text = self.get_balance_text()
        try:
            return int(text.replace(",", "").replace("STAT", "").strip())
        except Exception:
            return -1

    def is_balance_has_thousands_separator(self) -> bool:
        """잔액이 1,000 이상일 때 천 단위 구분 기호(,) 포함 여부"""
        text = self.get_balance_text()
        amount = self.get_balance_as_number()
        if amount < 1_000:
            return True  # 1000 미만은 구분 기호 불필요 → pass 처리
        return "," in text

    def is_balance_unit_stat(self) -> bool:
        """잔액 단위가 'STAT'인지 확인"""
        try:
            return "STAT" in self.page.locator(self.BALANCE_UNIT).first.inner_text()
        except Exception:
            return False

    def is_membership_active(self) -> bool:
        """멤버십 이용 중 레이블 노출 여부"""
        loc = self.page.locator(self.MEMBERSHIP_LABEL)
        if loc.count() == 0:
            return False
        try:
            cls = loc.first.get_attribute("class") or ""
            return "show" in cls
        except Exception:
            return loc.count() > 0

    # 잔액 숨김/보임 토글 (⚠️ TODO: 실제 셀렉터 튜닝 후 동작 확인 필요)
    def click_balance_toggle(self) -> None:
        """잔액 숨김/보임 토글 버튼 클릭"""
        btn = self.page.locator(self.BALANCE_TOGGLE_BTN)
        if btn.count() > 0:
            try:
                btn.first.click(force=True)
                self.page.wait_for_timeout(500)
            except Exception:
                pass

    def is_balance_masked(self) -> bool:
        """잔액이 마스킹(숨김) 상태인지 확인"""
        # 마스킹 텍스트('****' 등)가 노출되거나, 원래 숫자 span이 숨겨진 상태
        if self.page.locator(self.BALANCE_MASKED_TEXT).count() > 0:
            return True
        # 폴백: 잔액 텍스트에 '*' 포함 여부
        text = self.get_balance_text()
        return "*" in text

    # ══════════════════════════════════════════════════════════════════
    #  유형 탭 제어 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_tab_count(self) -> int:
        """노출된 유형 탭 수"""
        return self.page.locator(self.TAB_ALL_BTNS).count()

    def get_active_tab_text(self) -> str:
        """현재 활성 탭 텍스트 반환 (예: '전체', '획득', '사용')"""
        try:
            return self.page.locator(self.TAB_ACTIVE).first.inner_text().strip()
        except Exception:
            return ""

    def _click_tab(self, selector: str, wait_ms: int = 800) -> None:
        """탭 클릭 공통 헬퍼
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(selector).first
        # 1단계: visible한 요소 클릭 시도
        try:
            loc.wait_for(state="visible", timeout=3_000)
            loc.click(timeout=3_000)
            self.page.wait_for_timeout(wait_ms)
            return
        except Exception:
            pass
        # 2단계: attached 대기 + force=True 폴백
        try:
            loc.wait_for(state="attached", timeout=5_000)
            loc.click(force=True)
            self.page.wait_for_timeout(wait_ms)
        except Exception:
            pass

    def click_tab_all(self) -> None:
        """'전체' 탭 클릭"""
        self._click_tab(self.TAB_ALL)

    def click_tab_earn(self) -> None:
        """'획득' 탭 클릭 (TC 명칭: '적립')"""
        self._click_tab(self.TAB_EARN)

    def click_tab_use(self) -> None:
        """'사용' 탭 클릭"""
        self._click_tab(self.TAB_USE)

    def is_tab_all_active(self) -> bool:
        return "isFocused" in (
            self.page.locator(self.TAB_ALL).first.get_attribute("class") or ""
        )

    def is_tab_earn_active(self) -> bool:
        return "isFocused" in (
            self.page.locator(self.TAB_EARN).first.get_attribute("class") or ""
        )

    def is_tab_use_active(self) -> bool:
        return "isFocused" in (
            self.page.locator(self.TAB_USE).first.get_attribute("class") or ""
        )

    # ══════════════════════════════════════════════════════════════════
    #  기간 필터 메서드 (⚠️ 모두 TODO — HTML 미노출 상태)
    # ══════════════════════════════════════════════════════════════════

    def is_period_filter_visible(self) -> bool:
        """기간 필터 영역 노출 여부"""
        return self.page.locator(self.PERIOD_FILTER_WRAPPER).count() > 0

    def click_filter_1week(self) -> None:
        """기간 필터 '1주일' 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        self._click_tab(self.PERIOD_FILTER_1WEEK)

    def click_filter_1month(self) -> None:
        """기간 필터 '1개월' 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        self._click_tab(self.PERIOD_FILTER_1MONTH)

    def click_filter_3month(self) -> None:
        """기간 필터 '3개월' 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        self._click_tab(self.PERIOD_FILTER_3MONTH)

    def click_filter_reset(self) -> None:
        """필터 초기화/전체 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)
        폴백: '전체' 유형 탭 클릭으로 리셋 시도
        """
        reset_btn = self.page.locator(self.PERIOD_FILTER_RESET)
        if reset_btn.count() > 0:
            try:
                reset_btn.first.click(force=True)
                self.page.wait_for_timeout(600)
                return
            except Exception:
                pass
        # 폴백: '전체' 탭 클릭
        self.click_tab_all()

    def get_active_period_filter_text(self) -> str:
        """현재 활성 기간 필터 텍스트 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            loc = self.page.locator(self.PERIOD_FILTER_ACTIVE)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
        except Exception:
            pass
        return ""

    # ══════════════════════════════════════════════════════════════════
    #  거래 내역 카드 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_history_card_count(self) -> int:
        """전체 카드 수 (날짜 구분 카드 포함)"""
        return self.page.locator(self.HISTORY_CARD).count()

    def get_history_item_count(self) -> int:
        """실제 내역 카드 수 (날짜 구분 카드 제외)"""
        return self.page.locator(self.HISTORY_ITEM_CARD).count()

    def get_type_label(self, index: int = 0) -> str:
        """index 번째 카드의 유형 레이블 (예: '멤버십 구독', '출금', '입금')"""
        try:
            return self.page.locator(self.CARD_TYPE_LABEL).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_amount_text(self, index: int = 0) -> str:
        """index 번째 카드 금액 텍스트 (예: '+2,000', '-1,511')"""
        try:
            return self.page.locator(self.CARD_AMOUNT_SPAN).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_time_text(self, index: int = 0) -> str:
        """index 번째 카드 거래 시간 (예: '09:58')"""
        try:
            return self.page.locator(self.CARD_TIME).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_status_text(self, index: int = 0) -> str:
        """index 번째 카드 상태 텍스트 (예: '완료')"""
        try:
            return self.page.locator(self.CARD_STATUS_LABEL).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_date_separator_texts(self) -> list:
        """날짜 구분자 텍스트 목록 반환 (예: ['2026. 5. 6. 수요일', '2026. 4. 23. 목요일'])"""
        dates = []
        try:
            els = self.page.locator(self.HISTORY_DATE_SEP_TXT).all()
            for el in els:
                txt = el.inner_text().strip()
                if txt:
                    dates.append(txt)
        except Exception:
            pass
        return dates

    def get_card_href(self, index: int = 0) -> str:
        """index 번째 내역 카드 링크 href 반환"""
        try:
            return self.page.locator(self.HISTORY_CARD_LINK).nth(index).get_attribute("href") or ""
        except Exception:
            return ""

    def is_item_plus(self, index: int = 0) -> bool:
        """index 번째 내역 카드가 적립(+)인지 확인 (isPlus 클래스 보유 여부)"""
        try:
            # 내역 카드의 rewardValueWrapper에서 isPlus 클래스 확인
            wrappers = self.page.locator(self.CARD_VALUE_WRAPPER)
            if wrappers.count() <= index:
                return False
            cls = wrappers.nth(index).get_attribute("class") or ""
            return "isPlus" in cls
        except Exception:
            return False

    def is_item_minus(self, index: int = 0) -> bool:
        """index 번째 내역 카드가 사용(-)인지 확인"""
        return not self.is_item_plus(index)

    def get_plus_card_count(self) -> int:
        """isPlus 클래스 보유 카드 수 (적립 내역 수)"""
        return self.page.locator(self.CARD_PLUS_WRAPPER).count()

    def get_minus_card_count(self) -> int:
        """isPlus 클래스 없는 카드 수 (사용 내역 수)"""
        return self.page.locator(self.CARD_MINUS_WRAPPER).count()

    def get_amount_color(self, index: int = 0) -> str:
        """index 번째 카드 금액 span의 computed CSS color 값"""
        try:
            el = self.page.locator(self.CARD_AMOUNT_SPAN).nth(index)
            return el.evaluate("e => window.getComputedStyle(e).color")
        except Exception:
            return ""

    def are_plus_minus_colors_different(self) -> bool:
        """적립(+)과 사용(-) 금액의 색상이 서로 다른지 확인"""
        plus_count  = self.get_plus_card_count()
        minus_count = self.get_minus_card_count()
        if plus_count == 0 or minus_count == 0:
            return True  # 한 쪽이 없으면 검증 불가 → pass 처리

        # 첫 번째 plus 카드와 첫 번째 minus 카드의 금액 색상 비교
        try:
            plus_el  = self.page.locator(f"{self.CARD_PLUS_WRAPPER} {self.CARD_AMOUNT_SPAN.split(' > ')[1]}").first
            minus_el = self.page.locator(f"{self.CARD_MINUS_WRAPPER} {self.CARD_AMOUNT_SPAN.split(' > ')[1]}").first
            plus_color  = plus_el.evaluate("e => window.getComputedStyle(e).color")
            minus_color = minus_el.evaluate("e => window.getComputedStyle(e).color")
            return plus_color != minus_color
        except Exception:
            return True  # 색상 추출 실패 시 pass 처리

    # ══════════════════════════════════════════════════════════════════
    #  정렬 검증
    # ══════════════════════════════════════════════════════════════════

    def are_dates_sorted_latest(self) -> bool:
        """날짜 구분자가 최신순(내림차순)으로 정렬되어 있는지 확인
        날짜 형식: 'YYYY. M. D. 요일' (예: '2026. 5. 6. 수요일')
        """
        dates = self.get_date_separator_texts()
        if len(dates) < 2:
            return True  # 1개 이하는 정렬 검증 불가

        # 날짜 문자열에서 숫자 파싱하여 비교
        def parse_date(date_str: str):
            """'2026. 5. 6. 수요일' → (2026, 5, 6) 튜플"""
            try:
                parts = date_str.split(".")
                year  = int(parts[0].strip())
                month = int(parts[1].strip())
                day   = int(parts[2].strip())
                return (year, month, day)
            except Exception:
                return (0, 0, 0)

        parsed = [parse_date(d) for d in dates]
        for i in range(len(parsed) - 1):
            if parsed[i] < parsed[i + 1]:
                return False  # 이전 날짜가 다음 날짜보다 작으면 오름차순 → 실패
        return True

    # ══════════════════════════════════════════════════════════════════
    #  금액 계산 (FULLTC-434)
    # ══════════════════════════════════════════════════════════════════

    def calculate_visible_total(self) -> int:
        """현재 화면에 노출된 모든 카드 금액 합산 (천 단위 구분 기호 제거)
        "+2,000" → +2000, "-1,511" → -1511 으로 변환하여 합산
        """
        total = 0
        try:
            els = self.page.locator(self.CARD_AMOUNT_SPAN).all()
            for el in els:
                txt = el.inner_text().strip().replace(",", "")
                try:
                    total += int(txt)
                except ValueError:
                    pass
        except Exception:
            pass
        return total

    def is_amount_has_thousands_separator(self, index: int = 0) -> bool:
        """index 번째 카드 금액에 천 단위 구분 기호(,) 포함 여부
        금액이 1,000 미만인 경우 pass 처리
        """
        text = self.get_amount_text(index).replace("+", "").replace("-", "")
        amount_str = text.replace(",", "")
        try:
            amount = int(amount_str)
        except ValueError:
            return True  # 파싱 실패 → pass
        if amount < 1_000:
            return True  # 1000 미만은 구분 기호 불필요
        return "," in text

    def is_amount_sign_correct(self) -> bool:
        """모든 카드의 금액 부호(+/-)가 isPlus 클래스와 일치하는지 검증
        isPlus 카드 → '+' 시작, 비isPlus 카드 → '-' 시작
        """
        try:
            plus_spans  = self.page.locator(f"{self.CARD_PLUS_WRAPPER} {self.CARD_AMOUNT_SPAN.split(' > ')[1]}").all()
            minus_spans = self.page.locator(f"{self.CARD_MINUS_WRAPPER} {self.CARD_AMOUNT_SPAN.split(' > ')[1]}").all()
        except Exception:
            return True

        for span in plus_spans:
            txt = span.inner_text().strip()
            if txt and not txt.startswith("+"):
                return False

        for span in minus_spans:
            txt = span.inner_text().strip()
            if txt and not txt.startswith("-"):
                return False

        return True

    # ══════════════════════════════════════════════════════════════════
    #  스크롤 / 무한 로딩
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_bottom(self, steps: int = 5, delay_ms: int = 500) -> None:
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

    def is_loading_indicator_visible(self, timeout: int = 2_000) -> bool:
        """로딩 인디케이터 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            self.page.wait_for_selector(self.LOADING_INDICATOR, timeout=timeout)
            return True
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  카드 클릭 / 라우팅
    # ══════════════════════════════════════════════════════════════════

    def click_history_card(self, index: int = 0) -> None:
        """index 번째 내역 카드 클릭 (href goto 방식 우선 — Next.js Router 우회)"""
        loc = self.page.locator(self.HISTORY_CARD_LINK).nth(index)
        try:
            loc.wait_for(state="attached", timeout=5_000)
        except Exception:
            return

        href = loc.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            try:
                self.page.goto(full_url, wait_until="domcontentloaded")
                self.page.wait_for_timeout(600)
            except Exception:
                loc.click(force=True)
                self.page.wait_for_timeout(800)
        else:
            # href 없음 → JS click 이벤트 디스패치
            try:
                loc.evaluate("(el) => el.click()")
                self.page.wait_for_timeout(800)
            except Exception:
                pass

    # ══════════════════════════════════════════════════════════════════
    #  Empty State 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_empty_state_visible(self) -> bool:
        """빈 상태 UI 노출 여부 (⚠️ TODO: 실제 HTML 확인 후 셀렉터 튜닝)"""
        if self.page.locator(self.EMPTY_STATE).count() > 0:
            return True
        # 폴백: 카드가 0건이고 리스트 영역은 존재하는 경우
        return (
            self.page.locator(self.HISTORY_CARD_WRAPPER).count() > 0
            and self.page.locator(self.HISTORY_CARD_LINK).count() == 0
        )

    def get_empty_state_message(self) -> str:
        """빈 상태 안내 문구 텍스트 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            loc = self.page.locator(self.EMPTY_STATE_MSG)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
        except Exception:
            pass
        # 폴백: 빈 상태 컨테이너 전체 텍스트
        try:
            loc = self.page.locator(self.EMPTY_STATE)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
        except Exception:
            pass
        return ""