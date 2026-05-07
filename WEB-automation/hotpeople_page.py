"""
pages/web/hotpeople_page.py
[STEP 2 — POM v2]  핫피플 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
셀렉터 전략:
    - CSS Modules 해시 클래스 직접 사용 금지 → [class*='...'] 부분 매칭
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > 시맨틱 태그+구조 > 안정 CSS 클래스
    - Next.js SPA 링크: locator.get_attribute("href") + page.goto() 방식
    - Portal 모달: 블루밍비트는 모달을 <div id="portal-modal"> 내부에 렌더링
    - domcontentloaded 사용 — Next.js SPA + 서드파티 스크립트로 networkidle 30초 타임아웃 발생
    - v2: STG 실제 DOM HTML 분석 기반으로 모든 TODO_ 셀렉터 교체

    핫피플 URL 패턴:
        메인       : /people
        인물 상세   : /people?seq={id}
        전체 목록   : /people/list

v2 변경 이력 (2025-04):
    - HOTPEOPLE_MAIN: main#peopleMainPageContainer (ID 직접 매핑)
    - SLIDER_SECTION: div.peopleMainLayoutHeaderSwiper (Swiper 래퍼 클래스 직접 매핑)
    - SLIDER_ITEM: .peopleMainLayoutHeaderSwiper .swiper-slide
    - SLIDER_ITEM_IMG: .peopleMainLayoutHeaderSwiper .swiper-slide img
    - SLIDER_NEW_BADGE: [class*='etc-green'] (Tailwind 임의값 클래스 → 부분 매칭)
    - SLIDER_NEXT_BTN: div.peopleMainLayoutHeaderSwiper + div > button
    - SLIDER_PREV_BTN: div[class*='flex-none'][class*='invisible'] > button
      → click_slider_prev() 에서 force=True 필수 (Tailwind invisible = visibility:hidden)
    - PERSON_NAME: h2[class*='peopleMainHeaderTitle']
    - PERSON_AFFILIATION: p[class*='peopleMainHeaderDescription']
    - PERSON_PROFILE_IMG: div[class*='peopleMainContentImage'] img, img.basicImage
    - NEWS_SLIDER_SECTION: div.peopleMainRepresentativeNewsSwiper
    - NEWS_CARD: div.peopleMainRepresentativeNewsSwiperSlide a
    - NEWS_CARD_TITLE: div.peopleMainRepresentativeNewsSwiperSlide a h3
    - NEWS_SLIDER_PREV/NEXT: div[class*='slider-left/right'] button
    - VOTE_SECTION: div[class*='peopleMainSupportRateContainer']
    - VOTE_TITLE: p[class*='peopleMainSupportRateTitle']
    - VOTE_PARTICIPANT_COUNT: p[class*='peopleMainSupportRateParticipantCount']
    - VOTE_RATE_BAR: div[class*='peopleMainSupportRateBarWrapper']
    - VOTE_SUPPORT_BTN / VOTE_OPPOSE_BTN: button[class*='peopleMainSupportRateVoteButton']
    - VOTE_SUPPORT_PCT / VOTE_OPPOSE_PCT: span[class*='peopleMainSupportRateVoteRateValue']
    - RANKING_PANEL: aside#peopleMainAsideContainer 등
    - RANKING_PANEL_TITLE: p[class*='peopleMainLayoutAsidePeopleListTitle']
    - RANKING_ITEM: a[class*='peopleListItemLink']
    - RANKING_ITEM_IMG: figure[class*='peopleListItemProfileImage'] img
    - RANKING_ITEM_NAME: p[class*='peopleListItemName']
    - RANKING_VIEW_ALL: button[class*='peopleMainLayoutAsidePeopleListMoreButton']
    - PEOPLE_CARD: article[class*='peopleListItem'], a[class*='peopleListItemLink']
    - PEOPLE_CARD_NAME: p[class*='peopleListItemName']
    - PEOPLE_SEARCH_INPUT: input[placeholder*='검색'], input[type='search']
    - NEWS_DETAIL_PATTERN: "/feed/news/" (이전: "/news/")
    - scroll_to_vote_section(): page.keyboard.press("End") 선행 후 try/except
    - click_slider_prev(): force=True 추가
"""

from playwright.sync_api import Page


class HotPeoplePage:
    """블루밍비트 핫피플(Hot People) 도메인 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS
    # ══════════════════════════════════════════════════════════════════

    # ── GNB ──────────────────────────────────────────────────────────
    GNB_HEADER          = "header#headerContainer"
    GNB_HOTPEOPLE_TAB   = (
        "#menuWithMySettingContainer nav a[data-label='핫 피플'], "
        "#menuWithMySettingContainer nav a[href*='/people']"
    )
    GNB_LOGO            = "#logoWithStatLiveContainer > a[href='/']"

    # ── 핫피플 메인 페이지 컨테이너 ─────────────────────────────────────
    # HTML: <main id="peopleMainPageContainer" ...>
    HOTPEOPLE_MAIN      = "main#peopleMainPageContainer"

    # ── 썸네일 슬라이더 섹션 ─────────────────────────────────────────
    # HTML: <div class="peopleMainLayoutHeaderSwiper swiper ...">
    SLIDER_SECTION      = "div.peopleMainLayoutHeaderSwiper"

    # 개별 슬라이드 아이템 (클릭 가능한 인물 썸네일 카드)
    # Swiper가 .swiper-slide 클래스를 각 슬라이드에 추가
    SLIDER_ITEM         = "div.peopleMainLayoutHeaderSwiper .swiper-slide"

    # 썸네일 이미지
    SLIDER_ITEM_IMG     = "div.peopleMainLayoutHeaderSwiper .swiper-slide img"

    # 'new' 뱃지 — Tailwind 임의값 bg-(--etc-green) → class 속성에 'etc-green' 포함
    # HTML: <div class="... bg-(--etc-green) ...">NEW</div>
    SLIDER_NEW_BADGE    = (
        "div.peopleMainLayoutHeaderSwiper .swiper-slide div[class*='etc-green'], "
        "div.peopleMainLayoutHeaderSwiper .swiper-slide span[class*='etc-green'], "
        "div.peopleMainLayoutHeaderSwiper .swiper-slide div[class*='new' i]"
    )

    # 슬라이더 우측 이동 화살표 버튼
    # HTML: Swiper 래퍼 바로 다음 형제 div 내부 button
    # 구조: <div class="peopleMainLayoutHeaderSwiper ..."> + <div ...><button>...</button></div>
    SLIDER_NEXT_BTN     = "div.peopleMainLayoutHeaderSwiper + div > button"

    # 슬라이더 좌측 이동 화살표 버튼
    # HTML: <div class="... flex-none ... invisible ..."> 래퍼 안의 button
    # ⚠️ Tailwind 'invisible' = visibility:hidden → click() 시 force=True 필수
    SLIDER_PREV_BTN     = (
        "div[class*='flex-none'][class*='invisible'] > button, "
        "div[class*='flex-none'] > button[class*='prev'], "
        "div[class*='flex-none'] > button[aria-label*='이전']"
    )

    # ── 인물 상세 — 기본 정보 ────────────────────────────────────────
    # HTML: <h2 class="... peopleMainHeaderTitle ...">인물명</h2>
    PERSON_NAME         = "h2[class*='peopleMainHeaderTitle']"

    # HTML: <p class="... peopleMainHeaderDescription ...">소속</p>
    PERSON_AFFILIATION  = "p[class*='peopleMainHeaderDescription']"

    # HTML: <div class="... peopleMainContentImage ..."><img ...></div>
    #       또는 <img class="basicImage ...">
    PERSON_PROFILE_IMG  = (
        "div[class*='peopleMainContentImage'] img, "
        "img.basicImage"
    )

    # ── 인물 상세 — 관련 뉴스 슬라이더 ─────────────────────────────────
    # HTML: <div class="peopleMainRepresentativeNewsSwiper swiper ...">
    NEWS_SLIDER_SECTION = "div.peopleMainRepresentativeNewsSwiper"

    # 개별 뉴스 카드 — 슬라이드 내부 <a href="/feed/news/{id}">
    # HTML: <div class="... peopleMainRepresentativeNewsSwiperSlide ..."><a href="...">
    NEWS_CARD           = "div.peopleMainRepresentativeNewsSwiperSlide a"

    # 뉴스 카드 제목 텍스트
    NEWS_CARD_TITLE     = "div.peopleMainRepresentativeNewsSwiperSlide a h3"

    # 뉴스 슬라이더 이전/다음 화살표
    # HTML: <div class="... slider-left ..."><button>...</button></div>
    NEWS_SLIDER_PREV    = "div[class*='slider-left'] button"
    NEWS_SLIDER_NEXT    = "div[class*='slider-right'] button"

    # ── 지지율 투표 섹션 ─────────────────────────────────────────────
    # HTML: <div class="... peopleMainSupportRateContainer ...">
    VOTE_SECTION        = "div[class*='peopleMainSupportRateContainer']"

    # HTML: <p class="... peopleMainSupportRateTitle ...">
    VOTE_TITLE          = "p[class*='peopleMainSupportRateTitle']"

    # HTML: <p class="... peopleMainSupportRateParticipantCount ...">
    VOTE_PARTICIPANT_COUNT = "p[class*='peopleMainSupportRateParticipantCount']"

    # HTML: <div class="... peopleMainSupportRateBarWrapper ...">
    VOTE_RATE_BAR       = "div[class*='peopleMainSupportRateBarWrapper']"

    # '지지해요' 버튼
    # HTML: <button class="... peopleMainSupportRateVoteButton ..."><p>지지해요</p></button>
    VOTE_SUPPORT_BTN    = (
        "button[class*='peopleMainSupportRateVoteButton']:has(p:text-is('지지해요')), "
        "button:has-text('지지해요')"
    )

    # '아쉬워요' 버튼
    VOTE_OPPOSE_BTN     = (
        "button[class*='peopleMainSupportRateVoteButton']:has(p:text-is('아쉬워요')), "
        "button:has-text('아쉬워요')"
    )

    # 투표 후 갱신된 지지율 % 텍스트 (지지해요 쪽)
    # HTML: <span class="... peopleMainSupportRateVoteRateValue ... support ...">
    VOTE_SUPPORT_PCT    = (
        "span[class*='peopleMainSupportRateVoteRateValue'][class*='support'], "
        "span[class*='peopleMainSupportRateVoteRateValue']:first-of-type"
    )

    # 투표 후 갱신된 아쉬워요 % 텍스트
    VOTE_OPPOSE_PCT     = (
        "span[class*='peopleMainSupportRateVoteRateValue'][class*='dislike'], "
        "span[class*='peopleMainSupportRateVoteRateValue']:last-of-type"
    )

    # 투표 버튼 활성(선택됨) 상태 클래스 확인용 키워드 목록
    # is_support_btn_active() / is_oppose_btn_active() 내부에서 class 속성에 포함 여부 검사
    VOTE_ACTIVE_KEYWORDS = ["isVoted", "voted", "active", "selected", "isSelected", "checked"]

    # ── 우측 랭킹 패널 ─────────────────────────────────────────────
    # HTML: <aside id="peopleMainAsideContainer" ...>
    #       또는 <div class="... peopleMainLayoutAsidePeopleListContainer ...">
    RANKING_PANEL       = (
        "aside#peopleMainAsideContainer, "
        "div[class*='peopleMainLayoutAsidePeopleListContainer']"
    )

    # '지금 가장 뜨거운 인물' 패널 타이틀
    # HTML: <p class="... peopleMainLayoutAsidePeopleListTitle ...">
    RANKING_PANEL_TITLE = "p[class*='peopleMainLayoutAsidePeopleListTitle']"

    # 랭킹 개별 인물 항목 — <a class="... peopleListItemLink ...">
    RANKING_ITEM        = "a[class*='peopleListItemLink']"

    # 랭킹 인물 썸네일
    # HTML: <figure class="... peopleListItemProfileImage ..."><img ...></figure>
    RANKING_ITEM_IMG    = "figure[class*='peopleListItemProfileImage'] img"

    # 랭킹 인물 이름 텍스트
    # HTML: <p class="... peopleListItemName ...">
    RANKING_ITEM_NAME   = "p[class*='peopleListItemName']"

    # '전체 보기 >' 버튼 (a 태그가 아닌 button 태그)
    # HTML: <button class="... peopleMainLayoutAsidePeopleListMoreButton ...">전체 보기</button>
    RANKING_VIEW_ALL    = (
        "button[class*='peopleMainLayoutAsidePeopleListMoreButton'], "
        "button:has-text('전체 보기')"
    )

    # ── 전체 인물 목록 페이지 (/people/list) ────────────────────────────
    # HTML: article[class*='peopleListItem'] 카드가 반복됨
    PEOPLE_LIST_CONTAINER = (
        "main[id*='peopleList'], "
        "main[class*='peopleList'], "
        "article[class*='peopleListItem']"
    )

    # 인물 카드 (썸네일·이름·N명 참여중·최신 뉴스 제목·게시 시간)
    PEOPLE_CARD         = (
        "article[class*='peopleListItem'], "
        "a[class*='peopleListItemLink']"
    )

    # 인물 카드 내 이름 텍스트
    PEOPLE_CARD_NAME    = "p[class*='peopleListItemName']"

    # 인물 카드 내 '참여중' 카운트 — 지지율 섹션과 동일 클래스 구조일 가능성 있음
    PEOPLE_CARD_COUNT   = (
        "p[class*='peopleListItemParticipantCount'], "
        "span[class*='participantCount'], "
        "p[class*='participantCount']"
    )

    # 인물 검색 입력창
    PEOPLE_SEARCH_INPUT = (
        "input[placeholder*='검색'], "
        "input[placeholder*='인물'], "
        "input[type='search']"
    )

    # 검색 결과 없음 Empty State UI
    PEOPLE_EMPTY_STATE  = (
        "div[class*='emptyState'], "
        "p[class*='empty'], "
        "span:has-text('검색 결과가 없습니다'), "
        "p:has-text('등록된 인물이 없습니다')"
    )

    # ── 이미지 Fallback 아바타 ──────────────────────────────────────
    # basicImage 클래스를 공유하는 이미지가 깨질 경우 fallback svg/div가 렌더됨
    IMG_FALLBACK_AVATAR = (
        "img[class*='fallback'], "
        "div[class*='defaultAvatar'], "
        "div[class*='emptyProfile'], "
        "svg[class*='avatar']"
    )

    # ── 로그인 유도 모달 ──────────────────────────────────────────────
    LOGIN_MODAL         = (
        "#portal-modal div[class*='loginModal'], "
        "div[role='dialog'][class*='loginModal']"
    )
    LOGIN_MODAL_CONFIRM = (
        "#portal-modal button[class*='confirm'], "
        "#portal-modal button:first-of-type"
    )

    # ── URL 패턴 ────────────────────────────────────────────────────
    HOTPEOPLE_MAIN_PATH      = "/people"
    HOTPEOPLE_LIST_PATH      = "/people/list"
    HOTPEOPLE_DETAIL_PATTERN = "/people"    # ?seq={id} 쿼리 포함
    NEWS_DETAIL_PATTERN      = "/feed/news/"   # v2 수정: /news/ → /feed/news/

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def go_to_hotpeople_main(self) -> None:
        """핫피플 메인(/people)으로 이동
        ※ wait_until='domcontentloaded' — Next.js SPA + 서드파티 스크립트로
          'networkidle' 30초 타임아웃 발생 방지
        """
        self.page.goto(
            f"{self.BASE_URL}{self.HOTPEOPLE_MAIN_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_hotpeople_list(self) -> None:
        """전체 인물 목록(/people/list)으로 이동"""
        self.page.goto(
            f"{self.BASE_URL}{self.HOTPEOPLE_LIST_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_person_detail(self, seq: str) -> None:
        """인물 상세(/people?seq={id})로 이동"""
        self.page.goto(
            f"{self.BASE_URL}{self.HOTPEOPLE_MAIN_PATH}?seq={seq}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def scroll_to_bottom(self, steps: int = 5) -> None:
        """페이지를 단계적으로 스크롤 다운 (무한 스크롤 트리거용)"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(600)

    def scroll_to_element(self, selector: str) -> None:
        """특정 엘리먼트까지 스크롤"""
        self.page.locator(selector).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_main_loaded(self) -> bool:
        """핫피플 메인 로드 완료 여부"""
        try:
            self.page.wait_for_selector(self.HOTPEOPLE_MAIN, timeout=8_000)
            return True
        except Exception:
            # fallback: URL 기준 확인
            return self.HOTPEOPLE_MAIN_PATH in self.page.url

    def is_list_loaded(self) -> bool:
        """전체 목록 페이지 로드 완료 여부
        ※ /people/list URL 확인 + PEOPLE_CARD count 폴백
        """
        if self.HOTPEOPLE_LIST_PATH not in self.page.url:
            return False
        try:
            # 카드가 1개 이상 렌더되면 로드 완료로 간주
            self.page.wait_for_selector(self.PEOPLE_CARD, timeout=8_000)
            return True
        except Exception:
            return self.HOTPEOPLE_LIST_PATH in self.page.url

    def is_gnb_visible(self) -> bool:
        """GNB 헤더 노출 여부"""
        return self.page.is_visible(self.GNB_HEADER)

    # ══════════════════════════════════════════════════════════════════
    #  GNB 메서드
    # ══════════════════════════════════════════════════════════════════

    def click_gnb_hotpeople_tab(self) -> None:
        """GNB '핫 피플' 탭 클릭 → href goto 방식"""
        locator = self.page.locator(self.GNB_HOTPEOPLE_TAB).first
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
    #  썸네일 슬라이더 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_slider_section_visible(self) -> bool:
        """썸네일 슬라이더 섹션 노출 여부"""
        return self.page.locator(self.SLIDER_SECTION).count() > 0

    def get_slider_item_count(self) -> int:
        """슬라이더 내 인물 썸네일 아이템 수"""
        return self.page.locator(self.SLIDER_ITEM).count()

    def is_new_badge_visible(self) -> bool:
        """'new' 뱃지 노출 여부 (최신 등록 인물)"""
        return self.page.locator(self.SLIDER_NEW_BADGE).count() > 0

    def click_slider_next(self) -> None:
        """슬라이더 우측 '>' 화살표 버튼 클릭"""
        self.page.locator(self.SLIDER_NEXT_BTN).first.click()
        self.page.wait_for_timeout(600)

    def click_slider_prev(self) -> None:
        """슬라이더 좌측 '<' 화살표 버튼 클릭
        ※ Tailwind 'invisible' (visibility:hidden) 클래스로 초기에 숨겨진 상태이므로
          force=True 로 강제 클릭
        """
        self.page.locator(self.SLIDER_PREV_BTN).first.click(force=True)
        self.page.wait_for_timeout(600)

    def click_slider_item(self, index: int = 0) -> None:
        """슬라이더 index 번째 인물 썸네일 클릭 → href goto 방식"""
        locator = self.page.locator(self.SLIDER_ITEM).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if not href:
            # 부모 <a> 탐색 fallback
            href = locator.locator("xpath=ancestor-or-self::a").first.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    def get_slider_item_img_src(self, index: int = 0) -> str:
        """index 번째 슬라이더 이미지 src 속성"""
        return (
            self.page.locator(self.SLIDER_ITEM_IMG).nth(index).get_attribute("src") or ""
        )

    def is_slider_img_loaded(self, index: int = 0) -> bool:
        """index 번째 슬라이더 이미지가 정상 로드되었는지 확인
        (naturalWidth > 0 이면 이미지 로드 성공)
        """
        img_locator = self.page.locator(self.SLIDER_ITEM_IMG).nth(index)
        try:
            natural_width = self.page.evaluate(
                "(img) => img.naturalWidth", img_locator.element_handle()
            )
            return natural_width is not None and natural_width > 0
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  인물 상세 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_person_name_text(self) -> str:
        """현재 상세에 노출된 인물 이름 텍스트"""
        return self.page.locator(self.PERSON_NAME).first.inner_text().strip()

    def get_person_affiliation_text(self) -> str:
        """인물 소속/직함 텍스트"""
        return self.page.locator(self.PERSON_AFFILIATION).first.inner_text().strip()

    def is_person_profile_img_visible(self) -> bool:
        """인물 대형 프로필 이미지 노출 여부"""
        return self.page.locator(self.PERSON_PROFILE_IMG).count() > 0

    def is_url_person_detail(self) -> bool:
        """현재 URL이 인물 상세 패턴(/people?seq=...)인지 확인"""
        return "seq=" in self.page.url and self.HOTPEOPLE_MAIN_PATH in self.page.url

    # ── 관련 뉴스 슬라이더 ────────────────────────────────────────────

    def is_news_slider_visible(self) -> bool:
        """관련 뉴스 슬라이더 섹션 노출 여부"""
        return self.page.locator(self.NEWS_SLIDER_SECTION).count() > 0

    def get_news_card_count(self) -> int:
        """관련 뉴스 카드 수"""
        return self.page.locator(self.NEWS_CARD).count()

    def click_news_slider_next(self) -> None:
        """뉴스 슬라이더 다음 버튼 클릭"""
        self.page.locator(self.NEWS_SLIDER_NEXT).first.click()
        self.page.wait_for_timeout(600)

    def click_news_slider_prev(self) -> None:
        """뉴스 슬라이더 이전 버튼 클릭"""
        self.page.locator(self.NEWS_SLIDER_PREV).first.click()
        self.page.wait_for_timeout(600)

    def click_first_news_card(self) -> None:
        """첫 번째 뉴스 카드 클릭 → href goto 방식
        ※ 뉴스 링크 패턴: /feed/news/{id}
        """
        locator = self.page.locator(self.NEWS_CARD).first
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if not href:
            href = locator.locator("xpath=ancestor-or-self::a").first.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    def is_url_news_detail(self) -> bool:
        """현재 URL이 뉴스 상세 패턴(/feed/news/)인지 확인
        ※ v2 수정: /news/ → /feed/news/ (실제 HTML href="/feed/news/72476" 기반)
        """
        return self.NEWS_DETAIL_PATTERN in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  지지율 투표 메서드
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_vote_section(self) -> None:
        """지지율 투표 섹션까지 스크롤
        ※ v2 수정: scroll_into_view_if_needed() 단독 호출 시 timeout 발생 가능
          → 페이지 End 키 선행 후 try/except 로 안전하게 처리
        """
        # 1) 페이지 최하단으로 스크롤하여 섹션을 뷰포트 근처로 유도
        self.page.keyboard.press("End")
        self.page.wait_for_timeout(600)
        # 2) 섹션을 뷰포트 내로 정렬
        try:
            self.page.locator(self.VOTE_SECTION).first.scroll_into_view_if_needed(
                timeout=5_000
            )
        except Exception:
            pass
        self.page.wait_for_timeout(400)

    def is_vote_section_visible(self) -> bool:
        """지지율 섹션 노출 여부"""
        return self.page.locator(self.VOTE_SECTION).count() > 0

    def get_vote_title_text(self) -> str:
        """지지율 섹션 제목 텍스트 (예: '{인물명}의 지지율은?')"""
        return self.page.locator(self.VOTE_TITLE).first.inner_text().strip()

    def get_vote_participant_text(self) -> str:
        """참여자 수 텍스트 (예: '100명 참여중')"""
        return self.page.locator(self.VOTE_PARTICIPANT_COUNT).first.inner_text().strip()

    def is_vote_support_btn_visible(self) -> bool:
        """'지지해요' 버튼 노출 여부"""
        return self.page.locator(self.VOTE_SUPPORT_BTN).count() > 0

    def is_vote_oppose_btn_visible(self) -> bool:
        """'아쉬워요' 버튼 노출 여부"""
        return self.page.locator(self.VOTE_OPPOSE_BTN).count() > 0

    def get_support_pct_text(self) -> str:
        """지지율 % 텍스트"""
        try:
            return self.page.locator(self.VOTE_SUPPORT_PCT).first.inner_text().strip()
        except Exception:
            return ""

    def get_oppose_pct_text(self) -> str:
        """아쉬워요 % 텍스트"""
        try:
            return self.page.locator(self.VOTE_OPPOSE_PCT).first.inner_text().strip()
        except Exception:
            return ""

    def click_vote_support(self) -> None:
        """'지지해요' 버튼 클릭"""
        self.page.locator(self.VOTE_SUPPORT_BTN).first.click()
        self.page.wait_for_timeout(800)

    def click_vote_oppose(self) -> None:
        """'아쉬워요' 버튼 클릭"""
        self.page.locator(self.VOTE_OPPOSE_BTN).first.click()
        self.page.wait_for_timeout(800)

    def is_login_modal_visible(self) -> bool:
        """로그인 유도 모달 노출 여부"""
        return self.page.locator(self.LOGIN_MODAL).count() > 0

    def is_support_btn_active(self) -> bool:
        """'지지해요' 버튼이 투표됨(활성) 상태인지 확인"""
        btn = self.page.locator(self.VOTE_SUPPORT_BTN).first
        cls = btn.get_attribute("class") or ""
        aria = btn.get_attribute("aria-pressed") or ""
        return any(kw in cls for kw in self.VOTE_ACTIVE_KEYWORDS) or aria == "true"

    def is_oppose_btn_active(self) -> bool:
        """'아쉬워요' 버튼이 투표됨(활성) 상태인지 확인"""
        btn = self.page.locator(self.VOTE_OPPOSE_BTN).first
        cls = btn.get_attribute("class") or ""
        aria = btn.get_attribute("aria-pressed") or ""
        return any(kw in cls for kw in self.VOTE_ACTIVE_KEYWORDS) or aria == "true"

    # ══════════════════════════════════════════════════════════════════
    #  우측 랭킹 패널 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_ranking_panel_visible(self) -> bool:
        """우측 랭킹 패널 노출 여부"""
        return self.page.locator(self.RANKING_PANEL).count() > 0

    def get_ranking_item_count(self) -> int:
        """랭킹 패널 내 인물 항목 수"""
        return self.page.locator(self.RANKING_ITEM).count()

    def click_ranking_item(self, index: int = 0) -> None:
        """랭킹 패널 index 번째 인물 클릭 → href goto 방식"""
        locator = self.page.locator(self.RANKING_ITEM).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if not href:
            href = locator.locator("xpath=ancestor-or-self::a").first.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    def is_ranking_view_all_visible(self) -> bool:
        """'전체 보기 >' 버튼 노출 여부"""
        return self.page.locator(self.RANKING_VIEW_ALL).count() > 0

    def click_ranking_view_all(self) -> None:
        """'전체 보기 >' 버튼 클릭
        ※ '전체 보기' 는 <button> 태그 (href 없음) → locator.click() 직접 사용
        """
        locator = self.page.locator(self.RANKING_VIEW_ALL).first
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            # button 태그이므로 직접 클릭 후 네비게이션 대기
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  전체 인물 목록 페이지 메서드 (/people/list)
    # ══════════════════════════════════════════════════════════════════

    def get_people_card_count(self) -> int:
        """전체 목록 내 인물 카드 수"""
        return self.page.locator(self.PEOPLE_CARD).count()

    def click_people_card(self, index: int = 0) -> None:
        """목록 index 번째 인물 카드 클릭 → href goto 방식"""
        locator = self.page.locator(self.PEOPLE_CARD).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if not href:
            href = locator.locator("xpath=ancestor-or-self::a").first.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    def search_people(self, keyword: str) -> None:
        """인물 검색창에 키워드 입력"""
        search = self.page.locator(self.PEOPLE_SEARCH_INPUT).first
        search.wait_for(state="visible", timeout=5_000)
        search.click()
        search.fill(keyword)
        self.page.wait_for_timeout(800)

    def clear_people_search(self) -> None:
        """검색창 내용 초기화"""
        self.page.locator(self.PEOPLE_SEARCH_INPUT).first.fill("")
        self.page.wait_for_timeout(500)

    def is_empty_state_visible(self) -> bool:
        """검색 결과 없음 Empty State UI 노출 여부"""
        return self.page.locator(self.PEOPLE_EMPTY_STATE).count() > 0

    def scroll_people_list(self, steps: int = 3) -> None:
        """전체 인물 목록 스크롤 (무한 스크롤 트리거)"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(800)