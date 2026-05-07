"""
pages/web/search_page.py
[STEP 2 — POM v1]  검색(Search) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
셀렉터 전략:
    - CSS Modules 해시 클래스 직접 사용 금지 → [class*='...'] 부분 매칭
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > 시맨틱 태그+구조 > 안정 CSS 클래스
    - Next.js SPA 링크: locator.get_attribute("href") + page.goto() 방식
    - domcontentloaded 사용 — networkidle 30초 타임아웃 방지
    - ⚠️  TODO_ 접두사 셀렉터는 F12 → 실제 DOM 확인 후 반드시 교체 필요

    검색 URL 패턴:
        검색 메인      : /search
        검색 결과      : /search?word={키워드}

    TC 도메인 구성:
        검색 진입    : FULLTC-274~277  (GNB 진입, 최근 검색어, PiCK 뉴스)
        검색 실행    : FULLTC-278~282  (키워드 검색, 결과 확인, 초기화)
        검색 필터    : FULLTC-283~288  (날짜, 정렬, 타입)
        검색 예외    : FULLTC-289~293  (공백, 특수문자, 영문, 장문, XSS)
        유효성 경계값: FULLTC-294~298  (공백/자음/모음/특수/최대글자)
        Empty State  : FULLTC-299~300  (UI 노출, 안내 문구)
        검색어 저장  : FULLTC-301~305  (저장, 정렬, 삭제, 전체삭제, 클릭)
        인기 검색어  : FULLTC-306~307  (노출, 클릭 라우팅)
        결과 리스트  : FULLTC-308~309, 315  (정확성, 페이징, 클릭)
        키보드/UI    : FULLTC-310~313  (Enter, 버튼, 초기화, 중복)
        접근 권한    : FULLTC-314  (비로그인 검색)
        기간 필터    : FULLTC-316~319  (1주/1개월/직접입력/역전예외)
        타입 필터    : FULLTC-320~322  (단일/다중/조합)
        필터 초기화  : FULLTC-323~324  (초기화, 빈 결과)
        알림 배지    : FULLTC-325  (배지 노출)
"""

from playwright.sync_api import Page


class SearchPage:
    """블루밍비트 검색(Search) 도메인 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS
    # ══════════════════════════════════════════════════════════════════

    # ── GNB ──────────────────────────────────────────────────────────
    GNB_HEADER = "header#headerContainer"

    # GNB 검색 아이콘/링크 → /search 이동
    # ⚠️ TODO: 검색 아이콘 a[href='/search'] 또는 class 확인 후 교체
    GNB_SEARCH_ICON = (
        "[data-testid='TODO_gnbSearchIcon'], "
        "a[href='/search'][class*='searchMoveButton'], "
        "a[href='/search'], "
        "button[aria-label*='검색']"
    )

    # 로그인 상태 프로필 버튼 (로그인 감지용)
    GNB_PROFILE_ICON = "div.myInfo button:has(div.userProfileImage)"

    # GNB 알림 아이콘 버튼
    # HTML: <button aria-haspopup="true" aria-label="open alarm center">
    GNB_NOTIFICATION_ICON = (
        "button[aria-label='open alarm center'], "
        "button[aria-haspopup='true'][aria-label*='alarm'], "
        "button[class*='TODO_notificationIcon']"
    )

    # 알림 배지 (읽지 않은 알림 있을 때 노출)
    # ⚠️ TODO: 알림 배지 class/path 확인 후 교체
    # 힌트: GNB HTML에서 <path fill="#FF4A69">가 빨간 점(배지)임을 확인
    GNB_NOTIFICATION_BADGE = (
        "[data-testid='TODO_notificationBadge'], "
        "button[aria-label='open alarm center'] path[fill='#FF4A69'], "
        "button[aria-label='open alarm center'] [class*='badge'], "
        "button[aria-label='open alarm center'] ~ div[class*='badge']"
    )

    # ── 검색 페이지 컨테이너 ─────────────────────────────────────────
    # ⚠️ TODO: /search 페이지의 실제 main ID 확인 후 교체
    SEARCH_MAIN = (
        "[data-testid='TODO_searchMain'], "
        "main[id*='TODO_searchContainer'], "
        "main[class*='TODO_searchPage'], "
        "div[class*='TODO_searchMain']"
    )

    # ── 검색 입력창 ──────────────────────────────────────────────────
    # ⚠️ TODO: 검색 input의 placeholder 문구 / type 확인 후 교체
    # placeholder: '"비트코인"을 검색해 보세요'
    SEARCH_INPUT = (
        "[data-testid='TODO_searchInput'], "
        "input[placeholder*='비트코인'], "
        "input[placeholder*='검색'], "
        "input[type='search'], "
        "input[class*='TODO_searchInput']"
    )

    # 검색 실행 버튼 (돋보기/검색 아이콘)
    # ⚠️ TODO: 검색 버튼 aria-label 또는 class 확인 후 교체
    SEARCH_SUBMIT_BTN = (
        "[data-testid='TODO_searchSubmitBtn'], "
        "button[type='submit'], "
        "button[aria-label*='검색 실행'], "
        "button[class*='TODO_searchBtn'], "
        "form button[type='submit']"
    )

    # 검색 입력값 초기화 버튼 (X 버튼)
    # ⚠️ TODO: 초기화 버튼 class/aria 확인 후 교체
    SEARCH_CLEAR_BTN = (
        "[data-testid='TODO_searchClearBtn'], "
        "button[class*='TODO_clearBtn'], "
        "button[aria-label*='초기화'], "
        "button[aria-label*='지우기'], "
        "button[class*='TODO_inputClear']"
    )

    # ── 최근 검색어 ──────────────────────────────────────────────────
    # 최근 검색어 섹션 전체 래퍼
    # ⚠️ TODO: 최근 검색어 섹션 class 확인 후 교체
    RECENT_KEYWORDS_SECTION = (
        "[data-testid='TODO_recentKeywordsSection'], "
        "div[class*='TODO_recentKeywords'], "
        "section[class*='TODO_recentSearch'], "
        "div[class*='TODO_searchHistory']"
    )

    # 개별 최근 검색어 태그
    # ⚠️ TODO: 검색어 태그 li/div/button class 확인 후 교체
    RECENT_KEYWORD_ITEM = (
        "[data-testid='TODO_recentKeywordItem'], "
        "div[class*='TODO_recentKeywordTag'], "
        "li[class*='TODO_recentItem'], "
        "button[class*='TODO_recentTag']"
    )

    # 최근 검색어 태그 내 삭제(X) 버튼
    # ⚠️ TODO: 태그 내 삭제 버튼 class 확인 후 교체
    RECENT_KEYWORD_DELETE_BTN = (
        "[data-testid='TODO_recentKeywordDeleteBtn'], "
        "div[class*='TODO_recentKeywordTag'] button, "
        "li[class*='TODO_recentItem'] button[class*='TODO_delete']"
    )

    # 최근 검색어 전체 삭제 버튼
    # ⚠️ TODO: 전체 삭제 버튼 class/text 확인 후 교체
    RECENT_KEYWORDS_CLEAR_ALL = (
        "[data-testid='TODO_recentKeywordsClearAll'], "
        "button[class*='TODO_clearAll'], "
        "button:has-text('전체 삭제'), "
        "button:has-text('검색어 전체 삭제')"
    )

    # ── 인기/추천 검색어 ─────────────────────────────────────────────
    # ⚠️ TODO: 인기 검색어 섹션 class 확인 후 교체
    POPULAR_KEYWORDS_SECTION = (
        "[data-testid='TODO_popularKeywordsSection'], "
        "div[class*='TODO_popularKeywords'], "
        "section[class*='TODO_trendingSearch'], "
        "div[class*='TODO_rankingSearch']"
    )

    # 개별 인기 검색어 아이템
    # ⚠️ TODO: 인기 검색어 항목 class 확인 후 교체
    POPULAR_KEYWORD_ITEM = (
        "[data-testid='TODO_popularKeywordItem'], "
        "li[class*='TODO_popularItem'], "
        "div[class*='TODO_rankingItem'], "
        "a[class*='TODO_trendingKeyword'], "
        "button[class*='TODO_popularTag']"
    )

    # ── 초기 화면 PiCK 뉴스 캐러셀 ──────────────────────────────────
    # 검색 결과 없는 초기 상태에서 노출되는 PiCK 뉴스 캐러셀 섹션
    # ⚠️ TODO: PiCK 뉴스 캐러셀 section/div class 확인 후 교체
    PICK_NEWS_CAROUSEL = (
        "[data-testid='TODO_pickNewsCarousel'], "
        "section[class*='TODO_pickNews'], "
        "div[class*='TODO_pickCarousel'], "
        "div[class*='TODO_recommendNews'], "
        "section:has-text('PiCK')"
    )

    # ── 검색 결과 영역 ───────────────────────────────────────────────
    # 검색 결과 리스트 컨테이너
    # ⚠️ TODO: 검색 결과 컨테이너 class 확인 후 교체
    SEARCH_RESULT_CONTAINER = (
        "[data-testid='TODO_searchResultContainer'], "
        "div[class*='TODO_searchResult'], "
        "ul[class*='TODO_resultList'], "
        "section[class*='TODO_searchResults']"
    )

    # 개별 검색 결과 아이템 (기사 카드)
    # ⚠️ TODO: 결과 아이템 li/a/div class 확인 후 교체
    SEARCH_RESULT_ITEM = (
        "[data-testid='TODO_searchResultItem'], "
        "li[class*='TODO_resultItem'], "
        "a[class*='TODO_newsCard'], "
        "div[class*='TODO_articleCard'], "
        "article[class*='TODO_searchItem']"
    )

    # 검색어 하이라이트 텍스트 (제목 내 키워드 강조)
    # ⚠️ TODO: <mark>, <em>, <strong> 등 하이라이트 태그 확인 후 교체
    SEARCH_HIGHLIGHT = (
        "mark, "
        "em[class*='TODO_highlight'], "
        "span[class*='TODO_keyword'], "
        "b[class*='TODO_highlight']"
    )

    # 검색 결과 없음 (Empty State)
    # ⚠️ TODO: 빈 상태 div/section class 확인 후 교체
    SEARCH_EMPTY_STATE = (
        "[data-testid='TODO_searchEmptyState'], "
        "div[class*='TODO_emptyState'], "
        "div[class*='TODO_noResult'], "
        "p:has-text('검색 결과가 없습니다'), "
        "span:has-text('검색 결과가 없습니다'), "
        "div:has-text('검색 결과가 없어요')"
    )

    # ── 검색 필터 — 정렬 ────────────────────────────────────────────
    # 정렬 '관련도순' 버튼
    # ⚠️ TODO: 관련도순 버튼 class/aria/radio 확인 후 교체
    SORT_RELEVANCE_BTN = (
        "[data-testid='TODO_sortRelevance'], "
        "button[class*='TODO_sortBtn']:has-text('관련도순'), "
        "input[type='radio'][value*='relevance'] + label, "
        "button:has-text('관련도순')"
    )

    # 정렬 '최신순' 버튼
    SORT_LATEST_BTN = (
        "[data-testid='TODO_sortLatest'], "
        "button[class*='TODO_sortBtn']:has-text('최신순'), "
        "input[type='radio'][value*='latest'] + label, "
        "button:has-text('최신순')"
    )

    # ── 검색 필터 — 날짜 범위 ────────────────────────────────────────
    # 날짜 범위 필터 컨테이너
    # ⚠️ TODO: 날짜 필터 div/section class 확인 후 교체
    DATE_FILTER_CONTAINER = (
        "[data-testid='TODO_dateFilter'], "
        "div[class*='TODO_dateFilter'], "
        "div[class*='TODO_dateRange'], "
        "div[class*='TODO_calendarFilter']"
    )

    # 날짜 필터 시작일 입력
    DATE_FILTER_START = (
        "[data-testid='TODO_dateStart'], "
        "input[class*='TODO_startDate'], "
        "input[placeholder*='시작'], "
        "input[name*='start'], "
        "input[aria-label*='시작일']"
    )

    # 날짜 필터 종료일 입력
    DATE_FILTER_END = (
        "[data-testid='TODO_dateEnd'], "
        "input[class*='TODO_endDate'], "
        "input[placeholder*='종료'], "
        "input[name*='end'], "
        "input[aria-label*='종료일']"
    )

    # 날짜 필터 적용 버튼 (캘린더 선택 완료 버튼)
    DATE_FILTER_APPLY = (
        "[data-testid='TODO_dateApply'], "
        "button[class*='TODO_applyBtn'], "
        "button:has-text('선택완료'), "
        "button:has-text('적용')"
    )

    # 날짜 역전 입력 오류 메시지
    DATE_ERROR_MSG = (
        "[data-testid='TODO_dateError'], "
        "p[class*='TODO_dateError'], "
        "span:has-text('시작일은 종료일보다'), "
        "div:has-text('올바른 날짜'), "
        "p:has-text('날짜를 확인해')"
    )

    # ── 검색 필터 — 뉴스 타입 ────────────────────────────────────────
    # 뉴스 타입 필터 (컨텐츠 타입 드롭다운 또는 탭)
    # ⚠️ TODO: 타입 필터 class/select 확인 후 교체
    NEWS_TYPE_FILTER = (
        "[data-testid='TODO_newsTypeFilter'], "
        "div[class*='TODO_typeFilter'], "
        "select[class*='TODO_contentType'], "
        "div[class*='TODO_newsType']"
    )

    # 필터 초기화 버튼
    # ⚠️ TODO: 초기화 버튼 class/text 확인 후 교체
    FILTER_RESET_BTN = (
        "[data-testid='TODO_filterReset'], "
        "button[class*='TODO_resetFilter'], "
        "button:has-text('초기화'), "
        "button:has-text('필터 초기화'), "
        "button:has-text('전체')"
    )

    # ── 에러/로그인 감지 ─────────────────────────────────────────────
    ERROR_PAGE           = "p:has-text('이용에 불편을 드려 죄송합니다'), h1:has-text('이용에 불편을 드려 죄송합니다')"
    LOGIN_PAGE_CONTAINER = "main#signInContainer"
    SIGNIN_PATH          = "/user/signin"

    # ── URL 패턴 ────────────────────────────────────────────────────
    SEARCH_MAIN_PATH   = "/search"
    MAIN_PATH          = "/"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def _safe_goto(self, url: str) -> None:
        """about:blank 충돌을 방지하는 안전한 goto
        ※ 이전 내비게이션(about:blank 포함)이 남아 있는 경우 재시도
        """
        for attempt in range(2):
            try:
                self.page.wait_for_timeout(300)
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Exception as e:
                if attempt == 0 and ("about:blank" in str(e) or "interrupted" in str(e)):
                    # about:blank 충돌 시 잠시 대기 후 재시도
                    self.page.wait_for_timeout(800)
                    continue
                raise

    def go_to_main(self) -> None:
        """메인 페이지(/)로 이동"""
        self._safe_goto(self.BASE_URL)
        self.page.wait_for_timeout(500)

    def go_to_search(self) -> None:
        """/search 페이지로 이동
        ※ about:blank 충돌 방지: _safe_goto 사용
        """
        self._safe_goto(f"{self.BASE_URL}{self.SEARCH_MAIN_PATH}")
        self.page.wait_for_timeout(500)

    def go_to_search_result(self, keyword: str) -> None:
        """/search?word={keyword} 결과 페이지로 이동"""
        import urllib.parse
        encoded = urllib.parse.quote(keyword)
        self._safe_goto(f"{self.BASE_URL}{self.SEARCH_MAIN_PATH}?word={encoded}")
        self.page.wait_for_timeout(500)

    def click_gnb_search_icon(self) -> None:
        """GNB 검색 아이콘 클릭 → /search 이동"""
        locator = self.page.locator(self.GNB_SEARCH_ICON).first
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

    def refresh_page(self) -> None:
        """현재 페이지 새로고침"""
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_visible(self) -> bool:
        """GNB 헤더 노출 여부"""
        return self.page.is_visible(self.GNB_HEADER)

    def is_search_page(self) -> bool:
        """현재 페이지가 /search 인지 확인"""
        return self.SEARCH_MAIN_PATH in self.page.url

    def is_search_result_page(self, keyword: str = "") -> bool:
        """현재 URL이 검색 결과 페이지인지 확인"""
        if "word=" not in self.page.url:
            return False
        if keyword:
            import urllib.parse
            return urllib.parse.quote(keyword) in self.page.url or keyword in self.page.url
        return True

    def is_login_page_visible(self) -> bool:
        """로그인 페이지 노출 여부"""
        return (
            self.SIGNIN_PATH in self.page.url
            or self.page.locator(self.LOGIN_PAGE_CONTAINER).count() > 0
        )

    def is_gnb_logged_in_state(self) -> bool:
        """로그인 상태 여부"""
        return self.page.locator(self.GNB_PROFILE_ICON).count() > 0

    def is_error_page_visible(self) -> bool:
        """에러 페이지 노출 여부"""
        return self.page.locator(self.ERROR_PAGE).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  검색 입력창 조작
    # ══════════════════════════════════════════════════════════════════

    def is_search_input_visible(self) -> bool:
        """검색 입력창 노출 여부"""
        return self.page.locator(self.SEARCH_INPUT).count() > 0

    def get_search_input_placeholder(self) -> str:
        """검색 입력창 placeholder 텍스트 반환"""
        try:
            return self.page.locator(self.SEARCH_INPUT).first.get_attribute("placeholder") or ""
        except Exception:
            return ""

    def type_search_keyword(self, keyword: str) -> None:
        """검색창에 키워드 입력 (포커스 후 fill)"""
        input_el = self.page.locator(self.SEARCH_INPUT).first
        input_el.wait_for(state="visible", timeout=5_000)
        input_el.click()
        input_el.fill(keyword)
        self.page.wait_for_timeout(300)

    def search_by_enter(self, keyword: str) -> None:
        """키워드 입력 후 Enter 키로 검색 실행"""
        self.type_search_keyword(keyword)
        self.page.keyboard.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)

    def search_by_button(self, keyword: str) -> None:
        """키워드 입력 후 검색 버튼(돋보기) 클릭으로 검색 실행"""
        self.type_search_keyword(keyword)
        submit_btn = self.page.locator(self.SEARCH_SUBMIT_BTN)
        if submit_btn.count() > 0:
            submit_btn.first.click()
        else:
            self.page.keyboard.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)

    def click_clear_btn(self) -> None:
        """검색 입력값 초기화 버튼(X) 클릭"""
        self.page.locator(self.SEARCH_CLEAR_BTN).first.click()
        self.page.wait_for_timeout(400)

    def is_clear_btn_visible(self) -> bool:
        """초기화(X) 버튼 노출 여부"""
        return self.page.locator(self.SEARCH_CLEAR_BTN).count() > 0

    def get_search_input_value(self) -> str:
        """검색 입력창의 현재 입력값 반환"""
        try:
            return self.page.locator(self.SEARCH_INPUT).first.input_value()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  최근 검색어
    # ══════════════════════════════════════════════════════════════════

    def is_recent_keywords_section_visible(self) -> bool:
        """최근 검색어 섹션 노출 여부"""
        return self.page.locator(self.RECENT_KEYWORDS_SECTION).count() > 0

    def get_recent_keyword_count(self) -> int:
        """최근 검색어 태그 수 반환"""
        return self.page.locator(self.RECENT_KEYWORD_ITEM).count()

    def get_recent_keyword_texts(self) -> list:
        """최근 검색어 태그 텍스트 목록 반환"""
        items = self.page.locator(self.RECENT_KEYWORD_ITEM)
        result = []
        for i in range(items.count()):
            try:
                result.append(items.nth(i).inner_text().strip())
            except Exception:
                pass
        return result

    def click_recent_keyword_item(self, index: int = 0) -> None:
        """최근 검색어 태그 클릭 → 검색 실행"""
        self.page.locator(self.RECENT_KEYWORD_ITEM).nth(index).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)

    def delete_recent_keyword(self, index: int = 0) -> None:
        """특정 최근 검색어 태그의 X 버튼 클릭 → 개별 삭제"""
        delete_btns = self.page.locator(self.RECENT_KEYWORD_DELETE_BTN)
        delete_btns.nth(index).click()
        self.page.wait_for_timeout(400)

    def clear_all_recent_keywords(self) -> None:
        """최근 검색어 전체 삭제 버튼 클릭"""
        self.page.locator(self.RECENT_KEYWORDS_CLEAR_ALL).first.click()
        self.page.wait_for_timeout(400)

    def is_recent_keywords_empty(self) -> bool:
        """최근 검색어가 모두 삭제된 상태인지 확인"""
        return self.get_recent_keyword_count() == 0

    # ══════════════════════════════════════════════════════════════════
    #  인기/추천 검색어
    # ══════════════════════════════════════════════════════════════════

    def is_popular_keywords_visible(self) -> bool:
        """인기/추천 검색어 섹션 노출 여부"""
        return self.page.locator(self.POPULAR_KEYWORDS_SECTION).count() > 0

    def get_popular_keyword_count(self) -> int:
        """인기 검색어 아이템 수 반환"""
        return self.page.locator(self.POPULAR_KEYWORD_ITEM).count()

    def click_popular_keyword_item(self, index: int = 0) -> None:
        """인기 검색어 아이템 클릭 → 검색 실행"""
        self.page.locator(self.POPULAR_KEYWORD_ITEM).nth(index).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  PiCK 뉴스 캐러셀 (초기 상태)
    # ══════════════════════════════════════════════════════════════════

    def is_pick_news_carousel_visible(self) -> bool:
        """PiCK 뉴스 캐러셀 노출 여부"""
        return self.page.locator(self.PICK_NEWS_CAROUSEL).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  검색 결과
    # ══════════════════════════════════════════════════════════════════

    def is_search_result_visible(self) -> bool:
        """검색 결과 컨테이너 노출 여부"""
        return self.page.locator(self.SEARCH_RESULT_CONTAINER).count() > 0

    def get_search_result_count(self) -> int:
        """검색 결과 아이템 수 반환"""
        return self.page.locator(self.SEARCH_RESULT_ITEM).count()

    def click_search_result_item(self, index: int = 0) -> None:
        """검색 결과 아이템 클릭 → 기사 상세 이동"""
        locator = self.page.locator(self.SEARCH_RESULT_ITEM).nth(index)
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

    def is_highlight_visible(self) -> bool:
        """검색어 하이라이트 텍스트 존재 여부"""
        return self.page.locator(self.SEARCH_HIGHLIGHT).count() > 0

    def is_empty_state_visible(self) -> bool:
        """검색 결과 없음(Empty State) UI 노출 여부"""
        if self.page.locator(self.SEARCH_EMPTY_STATE).count() > 0:
            return True
        return "검색 결과가 없습니다" in self.page.content()

    def get_empty_state_text(self) -> str:
        """Empty State 안내 문구 텍스트 반환"""
        try:
            return self.page.locator(self.SEARCH_EMPTY_STATE).first.inner_text().strip()
        except Exception:
            return ""

    def scroll_to_bottom_for_more(self, steps: int = 3) -> None:
        """페이지 하단 스크롤 (무한 스크롤 / 추가 로딩 트리거)"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(800)

    # ══════════════════════════════════════════════════════════════════
    #  검색 필터 — 정렬
    # ══════════════════════════════════════════════════════════════════

    def is_sort_relevance_active(self) -> bool:
        """'관련도순' 버튼이 활성(선택) 상태인지 확인
        ※ HTML 분석 결과:
          활성   → class에 'text-(--ft-default)' 포함  (진한 색상)
          비활성 → class에 'text-(--ft-secondary)' 포함 (흐린 색상)
          예) <button class="... text-(--ft-default)">• 관련도순</button>
        """
        btn = self.page.locator(self.SORT_RELEVANCE_BTN).first
        try:
            cls = btn.get_attribute("class") or ""
            # ft-default = 활성(진한 색), ft-secondary = 비활성(흐린 색)
            return "ft-default" in cls and "ft-secondary" not in cls
        except Exception:
            return False

    def click_sort_relevance(self) -> None:
        """'관련도순' 정렬 버튼 클릭"""
        self.page.locator(self.SORT_RELEVANCE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def click_sort_latest(self) -> None:
        """'최신순' 정렬 버튼 클릭"""
        self.page.locator(self.SORT_LATEST_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_sort_latest_active(self) -> bool:
        """'최신순' 버튼이 활성(선택) 상태인지 확인
        ※ HTML 분석 결과:
          활성   → class에 'text-(--ft-default)' 포함  (진한 색상)
          비활성 → class에 'text-(--ft-secondary)' 포함 (흐린 색상)
          예) <button class="... text-(--ft-default)">• 최신순</button>
        """
        btn = self.page.locator(self.SORT_LATEST_BTN).first
        try:
            cls = btn.get_attribute("class") or ""
            return "ft-default" in cls and "ft-secondary" not in cls
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  검색 필터 — 날짜 범위
    # ══════════════════════════════════════════════════════════════════

    def is_date_filter_visible(self) -> bool:
        """날짜 범위 필터 노출 여부"""
        return self.page.locator(self.DATE_FILTER_CONTAINER).count() > 0

    def set_date_filter_start(self, date_str: str) -> None:
        """날짜 필터 시작일 입력 (예: '2025-01-01')"""
        input_el = self.page.locator(self.DATE_FILTER_START).first
        input_el.wait_for(state="visible", timeout=5_000)
        input_el.fill(date_str)
        self.page.wait_for_timeout(300)

    def set_date_filter_end(self, date_str: str) -> None:
        """날짜 필터 종료일 입력 (예: '2025-03-31')"""
        input_el = self.page.locator(self.DATE_FILTER_END).first
        input_el.wait_for(state="visible", timeout=5_000)
        input_el.fill(date_str)
        self.page.wait_for_timeout(300)

    def click_date_filter_apply(self) -> None:
        """날짜 필터 적용 버튼 클릭"""
        apply = self.page.locator(self.DATE_FILTER_APPLY)
        if apply.count() > 0:
            apply.first.click()
        else:
            self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(600)

    def is_date_error_visible(self) -> bool:
        """날짜 역전 오류 메시지 노출 여부"""
        if self.page.locator(self.DATE_ERROR_MSG).count() > 0:
            return True
        return "시작일은 종료일" in self.page.content() or "올바른 날짜" in self.page.content()

    # ══════════════════════════════════════════════════════════════════
    #  검색 필터 — 뉴스 타입 / 초기화
    # ══════════════════════════════════════════════════════════════════

    def is_news_type_filter_visible(self) -> bool:
        """뉴스 타입 필터 노출 여부"""
        return self.page.locator(self.NEWS_TYPE_FILTER).count() > 0

    def click_filter_reset(self) -> None:
        """필터 초기화 버튼 클릭"""
        self.page.locator(self.FILTER_RESET_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_filter_reset_visible(self) -> bool:
        """필터 초기화 버튼 노출 여부"""
        return self.page.locator(self.FILTER_RESET_BTN).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  알림 배지
    # ══════════════════════════════════════════════════════════════════

    def is_notification_icon_visible(self) -> bool:
        """GNB 알림 아이콘 노출 여부"""
        return self.page.locator(self.GNB_NOTIFICATION_ICON).count() > 0

    def is_notification_badge_visible(self) -> bool:
        """알림 배지 노출 여부 (읽지 않은 알림 존재 시)
        ※ HTML 확인 전 최선 추정: GNB 알림 버튼 내 빨간 점(path fill='#FF4A69') 또는 badge
        """
        if self.page.locator(self.GNB_NOTIFICATION_BADGE).count() > 0:
            return True
        # 폴백: 알림 버튼 내부 HTML에 빨간색 관련 요소 존재 여부
        try:
            btn_html = self.page.locator(self.GNB_NOTIFICATION_ICON).first.inner_html()
            return "FF4A69" in btn_html or "badge" in btn_html.lower()
        except Exception:
            return False