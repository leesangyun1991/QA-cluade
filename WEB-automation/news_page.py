"""
pages/web/news_page.py
[STEP 2 — POM 최신화]  뉴스 도메인 Page Object
실제 STG HTML(2026-04-22) 기반 CSS 셀렉터 전면 적용
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  주의사항:
    - CSS Modules 해시 클래스(_feedPick-module-scss-module__XXX__)는 빌드마다
      변경되므로 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > 시맨틱 태그+구조 > 안정 CSS 클래스
    - 뉴스 상세 URL 패턴: /feed/news/{id}  (NOT /news/{id})
    - "Only 블루밍비트" 섹션의 실제 ID: feedDeepDiveContainer
    - 랭킹 페이지 네비게이션 버튼은 aria-label 없음 → :not(.rankingNewsSwiper) 구조 활용
"""

from playwright.sync_api import Page


class NewsPage:
    """블루밍비트 뉴스 홈 / 상세 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS
    # ══════════════════════════════════════════════════════════════════

    # ── GNB (글로벌 내비게이션 바) ─────────────────────────────────────
    # HTML 근거: <header id="headerContainer">
    GNB_HEADER         = "header#headerContainer"

    # <a data-label="뉴스" href="..."> in nav
    GNB_NEWS_TAB       = "#menuWithMySettingContainer nav a[data-label='뉴스']"

    # 전체 GNB 탭 링크 목록
    GNB_TAB_LIST       = "#menuWithMySettingContainer nav ul li a"

    # 검색 아이콘 — desktop: <a href="/search"> in mySettingsHeader
    # mobile: <button aria-label="go to search page">
    GNB_SEARCH_ICON       = "#menuWithMySettingContainer a[href='/search']"
    GNB_SEARCH_ICON_MOBILE = "button[aria-label='go to search page']"

    # 햄버거+프로필 드롭다운 버튼 — <div class="myInfo"> 내부 <button>
    GNB_HAMBURGER_ICON = "div.myInfo button"

    # 프로필 이미지 — <div class="userProfileImage"> 내부
    GNB_PROFILE_ICON   = "div.myInfo .userProfileImage"

    # 블루밍비트 로고 — <a href="/"> in #logoWithStatLiveContainer
    GNB_LOGO           = "#logoWithStatLiveContainer > a[href='/']"

    # 언어 선택 — sr-only <ul> 내부, data-locale 속성 활용
    # (실제 언어 전환은 URL 변경으로 이루어짐)
    GNB_LANG_PANEL     = "header ul.sr-only"
    GNB_LANG_KO        = "header li[data-locale='ko'] a"
    GNB_LANG_EN        = "header li[data-locale='en'] a"
    GNB_LANG_JA        = "header li[data-locale='ja'] a"

    # STAT Live 버튼 — aria-label로 식별
    GNB_STAT_LIVE_BTN  = "button[aria-label='Open STAT Live in new window']"

    # ── PiCK 뉴스 섹션 ─────────────────────────────────────────────────
    # HTML 근거: <section id="feedPickContainer">
    PICK_SECTION          = "section#feedPickContainer"
    PICK_SECTION_TITLE    = "section#feedPickContainer h2"

    # PiCK 뱃지 — h2 내부의 SVG 체크마크 아이콘
    PICK_BADGE            = "#feedPickContainer h2 svg"

    # Swiper 슬라이드 — 활성 슬라이드 기준
    PICK_ACTIVE_SLIDE     = "#feedPickContainer .swiper-slide-active"
    PICK_HEADLINE_LINK    = "#feedPickContainer .swiper-slide-active > a"
    PICK_HEADLINE_TITLE   = "#feedPickContainer .swiper-slide-active > a h3"
    PICK_HEADLINE_DATE    = "#feedPickContainer .swiper-slide-active > a p"
    PICK_HEADLINE_IMG     = "#feedPickContainer .swiper-slide-active > a img"

    # 하위 호환 별칭
    CARD_THUMBNAIL        = "#feedPickContainer .swiper-slide-active > a img"

    # 서브라인 카드 (헤드라인 하단 2개)
    PICK_SUBLINE_LINKS    = "#feedPickContainer .swiper-slide-active > div a"
    PICK_SUBLINE_TITLE    = "#feedPickContainer .swiper-slide-active > div a h3"

    # Swiper 인디케이터 (pagination bullets)
    PICK_PAGINATION       = "#feedPickContainer .swiper-pagination"
    PICK_PAGINATION_BULLET = "#feedPickContainer .swiper-pagination-bullet"
    PICK_ACTIVE_BULLET    = "#feedPickContainer .swiper-pagination-bullet-active"

    # PiCK 네비게이션 — 화살표 없이 bullet 방식.
    # "다음"은 비활성 bullet, "이전"도 비활성 bullet 클릭 방식으로 처리
    PICK_NEXT_BTN  = "#feedPickContainer .swiper-pagination-bullet:not(.swiper-pagination-bullet-active)"
    PICK_PREV_BTN  = "#feedPickContainer .swiper-pagination-bullet:not(.swiper-pagination-bullet-active)"

    # ── 랭킹 뉴스 섹션 ─────────────────────────────────────────────────
    # HTML 근거: <section id="feedRankingContainer">
    RANKING_SECTION       = "section#feedRankingContainer"
    RANKING_SECTION_TITLE = "section#feedRankingContainer h2"
    # feedRankingSwiperContainer 는 CSS 모듈 해시 없는 plain 클래스
    RANKING_SWIPER        = ".feedRankingSwiperContainer"

    RANKING_ITEM          = "#feedRankingContainer .swiper-slide a"
    # 순위 숫자 — <a> > <div> 의 첫 번째 <span>
    RANKING_BADGE         = "#feedRankingContainer .swiper-slide a > div > span:first-child"
    RANKING_ITEM_TITLE    = "#feedRankingContainer .swiper-slide a h3"
    RANKING_ITEM_DATE     = "#feedRankingContainer .swiper-slide a section > span:last-child"
    RANKING_ITEM_IMG      = "#feedRankingContainer .swiper-slide a img"

    # 페이지네이션 컨트롤 — aria-label 속성 활용
    # <span aria-label="current index">, <span aria-label="total index">
    RANKING_PAGINATION    = "#feedRankingContainer span[aria-label='current index']"
    RANKING_PAGE_LABEL    = "#feedRankingContainer span[aria-label='current index']"

    # 이전/다음 페이지 버튼 — rankingNewsSwiper가 아닌 형제 div의 첫/마지막 버튼
    RANKING_PREV_PAGE     = "#feedRankingContainer .feedRankingSwiperContainer > div:not(.rankingNewsSwiper) button:first-child"
    RANKING_NEXT_PAGE     = "#feedRankingContainer .feedRankingSwiperContainer > div:not(.rankingNewsSwiper) button:last-child"

    # ── Only 블루밍비트 섹션 ─────────────────────────────────────────────
    # HTML 근거: <section id="feedDeepDiveContainer">  (NOT "only-bloomingbit")
    ONLY_SECTION          = "section#feedDeepDiveContainer"
    # 타이틀 — <h2><span>Only 블루밍비트</span></h2>
    ONLY_SECTION_TITLE    = "#feedDeepDiveContainer h2 span"
    # 서브타이틀 — <h3>크립토 전문기자의<span>딥다이브를...</span></h3>
    ONLY_SECTION_SUBTITLE = "#feedDeepDiveContainer > div h3"
    # 카드 — plain class "onlyCardList" (CSS 모듈 해시 없음)
    ONLY_CARD             = "#feedDeepDiveContainer .onlyCardList"
    # 카드 클릭 대상 — <a> 없이 div.onlyCardList를 JS 클릭
    ONLY_CARD_LINK        = "#feedDeepDiveContainer .onlyCardList"
    # 코인 태그 — .onlyCardInfoBox 내부 <button>
    ONLY_COIN_TAG         = "#feedDeepDiveContainer .onlyCardInfoBox button"
    # 날짜 — .onlyCardInfoBox > div > span
    ONLY_CARD_DATE        = "#feedDeepDiveContainer .onlyCardInfoBox div span"
    # 이미지
    ONLY_CARD_IMG         = "#feedDeepDiveContainer .onlyCardList img"

    # Only 섹션 네비게이션 버튼
    # feedDeepDiveSwiperContainer 내 마지막 button = next
    ONLY_NEXT_BTN         = "#feedDeepDiveContainer .feedDeepDiveSwiperContainer > button:last-of-type"
    # feedDeepDiveSwiperContainer 내 첫 번째 button = prev (1440px 기준 hidden)
    ONLY_PREV_BTN         = "#feedDeepDiveContainer .feedDeepDiveSwiperContainer > button:first-of-type"

    # ── 실시간 뉴스 섹션 ────────────────────────────────────────────────
    # HTML 근거: <section id="feedRealTimeContainer">
    REALTIME_SECTION         = "section#feedRealTimeContainer"

    # 가상 스크롤 리스트 — data-testid 안정적으로 유지
    REALTIME_VIRTUAL_LIST    = "[data-testid='virtuoso-item-list']"

    # 날짜 헤더 — virtual list 내 role="button" div의 첫 번째 <span>
    REALTIME_DATE_HEADER     = "#feedRealTimeContainer div[role='button'] > span"

    # 카드 컨테이너 — plain class "feedRealTimeCardContainer"
    REALTIME_CARD_CONTAINER  = "section.feedRealTimeCardContainer"
    REALTIME_CARD_LINK       = "section.feedRealTimeCardContainer a"
    REALTIME_CARD_TITLE      = "section.feedRealTimeCardContainer h4"
    REALTIME_CARD_SUMMARY    = "section.feedRealTimeCardContainer p"

    # 뉴스 타입 span — <span class="opacity-70">시간</span> 다음의 span
    # 예: "거래소 공지", "속보", "시세 급변동" 등
    REALTIME_CARD_TYPE_SPAN  = "section.feedRealTimeCardContainer a div div span + span"

    # 탭 버튼
    # 전체 탭 — li[class*='totalTab'] (CSS module에 'totalTab' 문자열 포함)
    REALTIME_TAB_ALL      = "#feedRealTimeContainer #feedRealTimeHeader li[class*='totalTab'] button"
    # PiCK 탭 — plain class 'pickTab' 보유
    REALTIME_TAB_PICK     = "#feedRealTimeContainer li.pickTab button"
    # REALTIME_TAB_ALLNEWS: 현재 UI에 별도 "전체뉴스" 탭 없음, 전체 탭과 동일
    REALTIME_TAB_ALLNEWS  = "#feedRealTimeContainer #feedRealTimeHeader li[class*='totalTab'] button"
    # 활성 탭 — li[class*='active'] (CSS module에 'active' 문자열 포함)
    REALTIME_ACTIVE_TAB   = "#feedRealTimeContainer #feedRealTimeHeader li[class*='active'] button"

    # 뉴스 타입 배지 — type span (text 필터는 테스트 메서드에서 처리)
    REALTIME_BREAKING_BADGE  = "section.feedRealTimeCardContainer a div div span + span"
    REALTIME_EXCHANGE_BADGE  = "section.feedRealTimeCardContainer a div div span + span"

    # 코인 태그 — 카드 상단 flex-wrap 영역 (콘텐츠에 따라 없을 수 있음)
    REALTIME_COIN_TAG        = "section.feedRealTimeCardContainer div.flex.flex-wrap button"

    # "더 보기" — 가상 스크롤이므로 별도 버튼 없음; 스크롤 다운으로 로드
    REALTIME_LOAD_MORE       = "[data-testid='virtuoso-item-list']"

    # ── 뉴스 상세 페이지 ────────────────────────────────────────────────
    DETAIL_TITLE          = "h1"
    DETAIL_BODY           = "article"
    DETAIL_DATE           = "time, [class*='date'], [class*='Date'], [class*='publish'], [class*='createdAt']"
    DETAIL_COIN_TICKER    = "button[class*='ticker'], span[class*='ticker']"
    AI_ANALYST_CARD       = "div[class*='analyst'], section[class*='analyst']"

    # ── 사이드바 위젯 ────────────────────────────────────────────────────
    # HTML 근거: <aside id="feedTrendingCoinsContainer">
    TRENDING_SECTION      = "aside#feedTrendingCoinsContainer"
    # 코인 버튼 — plain class "feedTrendingCoinsBox" 내부 <button>
    TRENDING_COIN_ITEM    = "#feedTrendingCoinsContainer .feedTrendingCoinsBox button"
    TRENDING_COIN_TITLE   = "#feedTrendingCoinsContainer h2"

    # HTML 근거: <section id="hotPeopleEntrySection">
    HOTPERSON_SECTION     = "section#hotPeopleEntrySection"
    # 전체 보기 링크
    HOTPERSON_VIEW_ALL    = "section#hotPeopleEntrySection a[href='/people/list']"
    # 핫피플 카드 링크
    HOTPERSON_CARD        = "#hotPeopleEntrySection .hotPeopleEntryContainer .swiper-slide a"

    # ── URL 패턴 ────────────────────────────────────────────────────────
    NEWS_HOME_PATH          = "/"
    NEWS_DETAIL_URL_PATTERN = "/feed/news/"
    SEARCH_URL_PATTERN      = "/search"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def go_to_news_home(self) -> None:
        """뉴스 홈으로 이동 (루트 URL)"""
        self.page.goto(f"{self.BASE_URL}{self.NEWS_HOME_PATH}", wait_until="networkidle")

    def go_to_news_detail(self, article_id: str) -> None:
        """뉴스 상세 직접 이동 (실제 패턴: /feed/news/{id})"""
        self.page.goto(f"{self.BASE_URL}/feed/news/{article_id}", wait_until="networkidle")

    def scroll_to_bottom(self, steps: int = 5) -> None:
        """페이지를 단계적으로 스크롤 다운"""
        for _ in range(steps):
            self.page.keyboard.press("PageDown")
            self.page.wait_for_timeout(400)

    def scroll_to_element(self, selector: str) -> None:
        """특정 엘리먼트까지 스크롤"""
        self.page.locator(selector).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)

    # ══════════════════════════════════════════════════════════════════
    #  홈 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self) -> bool:
        """뉴스 홈 로드 완료 여부 (PiCK 섹션 노출 기준)"""
        try:
            self.page.wait_for_selector(self.PICK_SECTION, timeout=8_000)
            return True
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  GNB 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_visible(self) -> bool:
        """GNB(header) 노출 여부"""
        return self.page.is_visible(self.GNB_HEADER)

    def is_gnb_sticky(self) -> bool:
        """스크롤 후 GNB sticky 고정 여부 (헤더 top 위치 확인)"""
        top = self.page.locator(self.GNB_HEADER).first.evaluate(
            "el => el.getBoundingClientRect().top"
        )
        return float(top) <= 5  # 화면 상단 5px 이내에 위치하면 sticky

    def get_gnb_tab_count(self) -> int:
        """GNB 탭 수"""
        return self.page.locator(self.GNB_TAB_LIST).count()

    def is_news_tab_active(self) -> bool:
        """뉴스 탭 활성 상태 여부 — data-label='뉴스' 링크 존재 확인"""
        return self.page.locator(self.GNB_NEWS_TAB).count() > 0

    def is_search_icon_visible(self) -> bool:
        return self.page.is_visible(self.GNB_SEARCH_ICON)

    def is_hamburger_icon_visible(self) -> bool:
        return self.page.is_visible(self.GNB_HAMBURGER_ICON)

    def is_profile_icon_visible(self) -> bool:
        return self.page.is_visible(self.GNB_PROFILE_ICON)

    def click_logo(self) -> None:
        """GNB 로고 클릭 — href goto 방식"""
        locator = self.page.locator(self.GNB_LOGO).first
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="networkidle")
        else:
            locator.click(force=True)
            self.page.wait_for_load_state("networkidle")

    def click_search_icon(self) -> None:
        """GNB 검색 아이콘 클릭 → /search 이동"""
        locator = self.page.locator(self.GNB_SEARCH_ICON).first
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="networkidle")
        else:
            locator.click()
            self.page.wait_for_load_state("networkidle")

    def click_hamburger_icon(self) -> None:
        """GNB 햄버거/프로필 드롭다운 버튼 클릭"""
        self.page.locator(self.GNB_HAMBURGER_ICON).first.click()
        self.page.wait_for_timeout(500)

    def is_lang_panel_visible(self) -> bool:
        """언어 패널 DOM 존재 여부 (sr-only이지만 DOM에는 항상 존재)"""
        return self.page.locator(self.GNB_LANG_PANEL).count() > 0

    def click_lang_en(self) -> None:
        """English 언어로 전환 → en URL로 직접 이동"""
        self.page.goto(self.BASE_URL_EN, wait_until="networkidle")

    def click_lang_ja(self) -> None:
        """日本語 언어로 전환 → ja URL로 직접 이동"""
        self.page.goto(self.BASE_URL_JA, wait_until="networkidle")

    def click_stat_live(self) -> None:
        """STAT Live 버튼 클릭"""
        self.page.locator(self.GNB_STAT_LIVE_BTN).first.click()

    def is_stat_live_btn_visible(self) -> bool:
        return self.page.is_visible(self.GNB_STAT_LIVE_BTN)

    # ══════════════════════════════════════════════════════════════════
    #  PiCK 뉴스 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_pick_section_visible(self) -> bool:
        return self.page.is_visible(self.PICK_SECTION)

    def get_pick_section_title_text(self) -> str:
        return self.page.locator(self.PICK_SECTION_TITLE).inner_text()

    def get_pick_slide_count(self) -> int:
        """Swiper 전체 슬라이드 수 (duplicate 제외)"""
        return self.page.locator(
            "#feedPickContainer .swiper-slide:not(.swiper-slide-duplicate)"
        ).count()

    def get_pick_card_count(self) -> int:
        """PiCK 활성 슬라이드 카드 수 (헤드라인 + 서브라인)"""
        headline = self.page.locator(self.PICK_HEADLINE_LINK).count()
        sublines = self.page.locator(self.PICK_SUBLINE_LINKS).count()
        return headline + sublines

    def get_first_pick_card_title(self) -> str:
        return self.page.locator(self.PICK_HEADLINE_TITLE).first.inner_text()

    def get_pick_headline_date(self) -> str:
        return self.page.locator(self.PICK_HEADLINE_DATE).first.inner_text()

    def get_pick_indicator_count(self) -> int:
        """인디케이터 점(dots) 수"""
        return self.page.locator(self.PICK_PAGINATION_BULLET).count()

    def get_active_indicator_index(self) -> int:
        """현재 활성 인디케이터 인덱스 (0-based)"""
        bullets = self.page.locator(self.PICK_PAGINATION_BULLET).all()
        for i, bullet in enumerate(bullets):
            classes = bullet.get_attribute("class") or ""
            if "active" in classes:
                return i
        return -1

    def click_pick_indicator(self, index: int) -> None:
        """index 번째 인디케이터 점 클릭"""
        self.page.locator(self.PICK_PAGINATION_BULLET).nth(index).click()
        self.page.wait_for_timeout(600)

    def click_pick_next(self) -> None:
        """PiCK 다음 슬라이드 — 비활성 bullet 클릭"""
        bullets = self.page.locator(self.PICK_PAGINATION_BULLET).all()
        for bullet in bullets:
            cls = bullet.get_attribute("class") or ""
            if "swiper-pagination-bullet-active" not in cls:
                bullet.click()
                self.page.wait_for_timeout(600)
                return

    def click_pick_prev(self) -> None:
        """PiCK 이전 슬라이드 — click_pick_next와 동일 토글 방식"""
        self.click_pick_next()

    def is_pick_next_btn_disabled(self) -> bool:
        """비활성 bullet 없으면 '다음' 불가 (마지막 슬라이드)"""
        return self.page.locator(
            "#feedPickContainer .swiper-pagination-bullet:not(.swiper-pagination-bullet-active)"
        ).count() == 0

    def is_pick_prev_btn_disabled(self) -> bool:
        return self.is_pick_next_btn_disabled()

    def click_first_pick_card(self) -> None:
        """헤드라인 PiCK 카드 클릭 → href goto 방식"""
        locator = self.page.locator(self.PICK_HEADLINE_LINK).first
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="networkidle")
        else:
            locator.click(force=True)

    def click_pick_subline_card(self, index: int = 0) -> None:
        """서브라인 카드 클릭 → href goto 방식"""
        locator = self.page.locator(self.PICK_SUBLINE_LINKS).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="networkidle")
        else:
            locator.click(force=True)

    def is_pick_headline_img_visible(self) -> bool:
        return self.page.locator(self.PICK_HEADLINE_IMG).first.is_visible()

    def is_pick_badge_visible(self) -> bool:
        """PiCK 뱃지 SVG 노출 여부"""
        return self.page.locator(self.PICK_BADGE).first.is_visible()

    def get_pick_subline_count(self) -> int:
        return self.page.locator(self.PICK_SUBLINE_LINKS).count()

    def get_pick_headline_title_text(self) -> str:
        return self.page.locator(self.PICK_HEADLINE_TITLE).first.inner_text()

    # ══════════════════════════════════════════════════════════════════
    #  랭킹 뉴스 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_ranking_section_visible(self) -> bool:
        return self.page.is_visible(self.RANKING_SECTION)

    def get_ranking_items(self):
        return self.page.locator(self.RANKING_ITEM).all()

    def get_ranking_badge_text(self, index: int = 0) -> str:
        return self.page.locator(self.RANKING_BADGE).nth(index).inner_text().strip()

    def get_ranking_item_title(self, index: int = 0) -> str:
        return self.page.locator(self.RANKING_ITEM_TITLE).nth(index).inner_text()

    def get_ranking_item_date(self, index: int = 0) -> str:
        return self.page.locator(self.RANKING_ITEM_DATE).nth(index).inner_text().strip()

    def click_ranking_item(self, index: int = 0) -> None:
        """href goto 방식 — Next.js Router 우회"""
        locator = self.page.locator(self.RANKING_ITEM).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="networkidle")
        else:
            locator.scroll_into_view_if_needed()
            locator.click(force=True)

    def is_ranking_pagination_visible(self) -> bool:
        """현재 페이지 표시 span 노출 여부"""
        return self.page.locator(self.RANKING_PAGINATION).count() > 0

    def get_ranking_page_label_text(self) -> str:
        """현재 페이지 번호 텍스트 (예: "1")"""
        return self.page.locator(self.RANKING_PAGE_LABEL).first.inner_text().strip()

    def click_ranking_next_page(self) -> None:
        self.page.locator(self.RANKING_NEXT_PAGE).first.click()
        self.page.wait_for_timeout(800)

    def click_ranking_prev_page(self) -> None:
        self.page.locator(self.RANKING_PREV_PAGE).first.click()
        self.page.wait_for_timeout(800)

    def is_ranking_prev_btn_disabled(self) -> bool:
        attr = self.page.locator(self.RANKING_PREV_PAGE).first.get_attribute("disabled")
        cls = self.page.locator(self.RANKING_PREV_PAGE).first.get_attribute("class") or ""
        return attr is not None or "disabled" in cls

    def is_ranking_next_btn_disabled(self) -> bool:
        attr = self.page.locator(self.RANKING_NEXT_PAGE).first.get_attribute("disabled")
        cls = self.page.locator(self.RANKING_NEXT_PAGE).first.get_attribute("class") or ""
        return attr is not None or "disabled" in cls

    # ══════════════════════════════════════════════════════════════════
    #  Only 블루밍비트 메서드
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_only_section(self) -> None:
        """Only 블루밍비트 섹션까지 스크롤"""
        self.page.locator(self.ONLY_SECTION).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(400)

    def is_only_section_visible(self) -> bool:
        return self.page.is_visible(self.ONLY_SECTION)

    def get_only_section_title(self) -> str:
        """'Only 블루밍비트' 타이틀 텍스트"""
        return self.page.locator(self.ONLY_SECTION_TITLE).first.inner_text().strip()

    def get_only_section_subtitle(self) -> str:
        """'크립토 전문기자의 딥다이브를 모았어요!' 텍스트"""
        return self.page.locator(self.ONLY_SECTION_SUBTITLE).first.inner_text().strip()

    def get_only_card_count(self) -> int:
        return self.page.locator(self.ONLY_CARD).count()

    def click_first_only_card(self) -> None:
        """첫 번째 Only 카드 클릭 — <a> 없음, JS click + URL 변화 대기"""
        locator = self.page.locator(self.ONLY_CARD_LINK).first
        locator.wait_for(state="attached", timeout=5_000)
        locator.click()
        self.page.wait_for_load_state("networkidle")

    def is_only_coin_tag_visible(self) -> bool:
        """코인 태그 버튼 노출 여부"""
        return self.page.locator(self.ONLY_COIN_TAG).first.is_visible()

    def get_only_card_date_text(self, index: int = 0) -> str:
        return self.page.locator(self.ONLY_CARD_DATE).nth(index).inner_text().strip()

    def is_only_card_img_visible(self, index: int = 0) -> bool:
        return self.page.locator(self.ONLY_CARD_IMG).nth(index).is_visible()

    def scroll_only_section_horizontal(self) -> None:
        """Only 블루밍비트 섹션 가로 스크롤 (JS 사용)"""
        swiper = self.page.locator("#feedDeepDiveContainer .swiper-wrapper").first
        swiper.evaluate("el => { el.scrollLeft += 300; }")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  실시간 뉴스 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_realtime_section_visible(self) -> bool:
        return self.page.is_visible(self.REALTIME_SECTION)

    def scroll_to_realtime_section(self) -> None:
        self.page.locator(self.REALTIME_SECTION).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(400)

    def wait_for_realtime_list(self, timeout: int = 8_000) -> bool:
        try:
            self.page.wait_for_selector(self.REALTIME_VIRTUAL_LIST, timeout=timeout)
            return True
        except Exception:
            return False

    def get_realtime_card_count(self) -> int:
        return self.page.locator(self.REALTIME_CARD_LINK).count()

    def get_first_realtime_card_title(self) -> str:
        return self.page.locator(self.REALTIME_CARD_TITLE).first.inner_text()

    def click_first_realtime_card(self) -> None:
        """첫 번째 실시간 카드 클릭 → href goto 방식"""
        locator = self.page.locator(self.REALTIME_CARD_LINK).first
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="networkidle")
        else:
            locator.click(force=True)

    def is_realtime_tab_all_visible(self) -> bool:
        return self.page.locator(self.REALTIME_TAB_ALL).count() > 0

    def click_realtime_tab_pick(self) -> None:
        self.page.locator(self.REALTIME_TAB_PICK).first.click()
        self.page.wait_for_timeout(800)

    def click_realtime_tab_allnews(self) -> None:
        self.page.locator(self.REALTIME_TAB_ALLNEWS).first.click()
        self.page.wait_for_timeout(800)

    def click_realtime_tab_all(self) -> None:
        self.page.locator(self.REALTIME_TAB_ALL).first.click()
        self.page.wait_for_timeout(800)

    def is_realtime_breaking_badge_visible(self) -> bool:
        """속보 타입 뉴스 카드 존재 여부 — 텍스트 필터링"""
        return (
            self.page.locator(self.REALTIME_CARD_CONTAINER)
            .filter(has_text="속보")
            .count() > 0
        )

    def is_realtime_exchange_badge_visible(self) -> bool:
        """거래소 공지 타입 뉴스 카드 존재 여부 — 텍스트 필터링"""
        return (
            self.page.locator(self.REALTIME_CARD_CONTAINER)
            .filter(has_text="거래소 공지")
            .count() > 0
        )

    def is_realtime_coin_tag_visible(self) -> bool:
        """코인 태그 표시 여부 (카드 상단 flex-wrap 영역)"""
        try:
            return self.page.locator(self.REALTIME_COIN_TAG).first.is_visible()
        except Exception:
            return False

    def get_realtime_date_header_text(self) -> str:
        """날짜 구분 헤더 텍스트 (예: '오늘, 2026. 4. 22. 수요일')"""
        return self.page.locator(self.REALTIME_DATE_HEADER).first.inner_text().strip()

    def is_realtime_load_more_visible(self) -> bool:
        """가상 스크롤 구조이므로 virtual list 존재 여부로 판단"""
        return self.page.locator(self.REALTIME_VIRTUAL_LIST).count() > 0

    def click_realtime_load_more(self) -> None:
        """가상 스크롤 — 스크롤 다운으로 추가 로드 유도"""
        self.scroll_to_bottom(steps=3)

    # ══════════════════════════════════════════════════════════════════
    #  뉴스 상세 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_detail_loaded(self) -> bool:
        if self.NEWS_DETAIL_URL_PATTERN not in self.page.url:
            return False
        try:
            self.page.wait_for_selector("h1", timeout=8_000)
            return True
        except Exception:
            return False

    def get_detail_title(self) -> str:
        return self.page.locator(self.DETAIL_TITLE).first.inner_text()

    def get_detail_body_text(self) -> str:
        return self.page.locator(self.DETAIL_BODY).first.inner_text()

    def is_detail_date_visible(self) -> bool:
        return self.page.locator(self.DETAIL_DATE).first.is_visible()

    def is_ai_analyst_card_visible(self) -> bool:
        return self.page.locator(self.AI_ANALYST_CARD).first.is_visible()

    def get_coin_ticker_count(self) -> int:
        return self.page.locator(self.DETAIL_COIN_TICKER).count()

    # ══════════════════════════════════════════════════════════════════
    #  사이드바 위젯 메서드
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_trending_section(self) -> None:
        self.page.locator(self.TRENDING_SECTION).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(400)

    def is_trending_section_visible(self) -> bool:
        return self.page.is_visible(self.TRENDING_SECTION)

    def get_trending_coin_count(self) -> int:
        return self.page.locator(self.TRENDING_COIN_ITEM).count()

    def click_trending_coin(self, index: int = 0) -> None:
        """트렌딩 코인 버튼 클릭 — 뉴스 필터링 트리거 (페이지 이동 없음)"""
        locator = self.page.locator(self.TRENDING_COIN_ITEM).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        locator.click()
        self.page.wait_for_timeout(800)

    def scroll_to_hotperson_section(self) -> None:
        self.page.locator(self.HOTPERSON_SECTION).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(400)

    def is_hotperson_section_visible(self) -> bool:
        return self.page.is_visible(self.HOTPERSON_SECTION)

    def is_hotperson_view_all_visible(self) -> bool:
        return self.page.is_visible(self.HOTPERSON_VIEW_ALL)