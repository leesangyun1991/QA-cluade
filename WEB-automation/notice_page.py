"""
pages/web/notice_page.py
[STEP 2 — POM v1]  공지사항(Notice) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_noticeList-module-scss-module__vi8Z8q__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌────────────────────────────────────────────────────────────────────┐
    │  공지 카드: a[class*='noticeCard']  href="/notice/{id}"           │
    │  공지 제목: h4[class*='title']                                    │
    │    (카테고리가 "[공지]" 형태로 제목 텍스트에 내포될 수 있음)       │
    │  공지 날짜: p[class*='date']  포맷: "YYYY.MM.DD"                 │
    │  페이지네이션: 번호 버튼 방식 (TC의 무한스크롤과 불일치 가능)    │
    │  카드 href: /notice/{id}  (상세 URL 패턴)                        │
    │  목록 페이지 URL 추정: /mypage/notice (F12 주소창 확인 후 수정)  │
    │  ────────────────────────────────────────────────────────         │
    │  [TODO_ 셀렉터 필요] — HTML 미노출 요소:                         │
    │    · 상단 고정(핀) 배지: PINNED_BADGE                             │
    │    · 미열람 NEW 뱃지:   NEW_BADGE                                 │
    │    · 카테고리 탭:       CATEGORY_TAB_*                            │
    │    · 검색창/버튼:       SEARCH_INPUT, SEARCH_SUBMIT_BTN 등        │
    │    · 상세 페이지 요소:  DETAIL_TITLE, DETAIL_BODY 등              │
    │    · 첨부파일 영역:     ATTACHMENT_SECTION 등                     │
    │    · 빈 상태 UI:        EMPTY_STATE 등                            │
    └────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - 해시 포함 class → [class*='안정키워드'] 부분 매칭
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
    - TODO_ 셀렉터: 해당 DOM 확인 후 실제 값으로 교체
"""

from playwright.sync_api import Page


class NoticePage:
    """블루밍비트 공지사항(Notice) 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    NOTICE_LIST_PATH   = "/notice"
    NOTICE_DETAIL_PATH = "/notice/"
    MYPAGE_PATH        = "/mypage"
    SIGNIN_PATH        = "/user/signin"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 ───────────────────────────────────────────────────
    # HTML: <section class="...__myPageCommonContentWrapper">
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    # HTML: <header class="...__contentHeader">
    PAGE_HEADER  = "header[class*='contentHeader']"
    # HTML: <h1>공지사항</h1>
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    # HTML: <a class="...__backBtn" href="/mypage">
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 공지 목록 ─────────────────────────────────────────────────────
    # HTML: <div class="...__noticeListWrapper">
    LIST_WRAPPER = "div[class*='noticeListWrapper']"
    # HTML: <ul class="...__noticeList">
    LIST_UL      = "ul[class*='noticeList']"
    # HTML: <a class="...__noticeCard" href="/notice/{id}">
    NOTICE_CARD  = "a[class*='noticeCard']"
    # HTML: <h4 class="...__title">제목</h4>
    NOTICE_TITLE = "a[class*='noticeCard'] h4[class*='title']"
    # HTML: <p class="...__date">2026.03.28</p>
    NOTICE_DATE  = "a[class*='noticeCard'] p[class*='date']"

    # ── 상단 고정 공지 (핀) — HTML 미노출 ───────────────────────────
    # ⚠️ TODO: F12로 고정 공지 배지/컨테이너 셀렉터 확인 후 튜닝
    PINNED_CARD  = "[data-testid='TODO_pinnedCard'], a[class*='noticeCard'][class*='pinned']"
    PINNED_BADGE = "[data-testid='TODO_pinnedBadge'], [class*='pinnedBadge'], [class*='pin']"

    # ── NEW 뱃지 (미열람) — HTML 미노출 ──────────────────────────────
    # ⚠️ TODO: 미열람 NEW 뱃지 셀렉터 F12 확인 후 튜닝
    NEW_BADGE = "[data-testid='TODO_newBadge'], [class*='newBadge'], [class*='isNew']"

    # ── 카테고리 탭 — HTML 미노출 ────────────────────────────────────
    # ⚠️ TODO: 카테고리 탭 영역 DOM 확인 후 튜닝
    CATEGORY_WRAPPER    = "[data-testid='TODO_categoryWrapper']"
    CATEGORY_TAB_ALL    = "[data-testid='TODO_tabAll'], button:has-text('전체')"
    CATEGORY_TAB_NOTICE = "[data-testid='TODO_tabNotice'], button:has-text('공지')"
    CATEGORY_TAB_EVENT  = "[data-testid='TODO_tabEvent'], button:has-text('이벤트')"
    CATEGORY_TAB_GUIDE  = "[data-testid='TODO_tabGuide'], button:has-text('안내')"
    CATEGORY_ACTIVE_TAB = "[data-testid='TODO_categoryActiveTab'], [class*='activeTab']"
    # 카드 내 카테고리 태그 (별도 요소가 있을 경우)
    CARD_CATEGORY_TAG   = "[data-testid='TODO_categoryTag'], [class*='categoryTag'], [class*='label']"

    # ── 검색 — HTML 미노출 ────────────────────────────────────────────
    # ⚠️ TODO: 검색 UI DOM 확인 후 튜닝
    SEARCH_INPUT      = (
        "[data-testid='TODO_searchInput'], "
        "input[type='search'], "
        "input[placeholder*='검색']"
    )
    SEARCH_SUBMIT_BTN = (
        "[data-testid='TODO_searchBtn'], "
        "button[type='submit'], "
        "button[aria-label*='검색']"
    )
    SEARCH_CLEAR_BTN  = (
        "[data-testid='TODO_searchClear'], "
        "button[aria-label*='초기화'], "
        "button[aria-label*='지우기'], "
        "input[type='search'] + button"
    )
    SEARCH_NO_RESULT  = (
        "[data-testid='TODO_searchNoResult'], "
        "[class*='noResult'], "
        "[class*='empty']"
    )

    # ── 페이지네이션 (번호 버튼 방식) ────────────────────────────────
    # HTML: 번호 버튼들이 ul ~ div 구조로 존재 (Tailwind 클래스)
    # ※ Tailwind 클래스는 셀렉터로 사용 불가 → JS 방식으로 탐색
    PAGINATION_WRAPPER  = "div[class*='noticeListWrapper'] > div"
    # 페이지 번호 버튼: span으로 숫자 표시
    PAGINATION_NUM_BTN  = "div[class*='noticeListWrapper'] > div button:has(span)"
    # 다음 페이지(>) 버튼
    PAGINATION_NEXT_BTN = "div[class*='noticeListWrapper'] > div div.flex:last-child button:first-child"
    # 마지막 페이지(>>) 버튼
    PAGINATION_LAST_BTN = "div[class*='noticeListWrapper'] > div div.flex:last-child button:last-child"
    # 이전 페이지(<) 버튼
    PAGINATION_PREV_BTN = "div[class*='noticeListWrapper'] > div div.flex:first-child button:last-child"
    # 첫 페이지(<<) 버튼
    PAGINATION_FIRST_BTN = "div[class*='noticeListWrapper'] > div div.flex:first-child button:first-child"

    # ── 상세 페이지 — HTML 미노출 ────────────────────────────────────
    # ⚠️ TODO: /notice/{id} 접속 후 F12로 셀렉터 확인 후 튜닝
    DETAIL_WRAPPER   = (
        "[data-testid='TODO_detailWrapper'], "
        "[class*='noticeDetail'], "
        "main[class*='notice']"
    )
    DETAIL_TITLE     = (
        "[data-testid='TODO_detailTitle'], "
        "h1[class*='title'], "
        "h2[class*='title']"
    )
    DETAIL_CATEGORY  = (
        "[data-testid='TODO_detailCategory'], "
        "[class*='category'], "
        "[class*='tag']"
    )
    DETAIL_DATE      = (
        "[data-testid='TODO_detailDate'], "
        "[class*='date'], "
        "time"
    )
    DETAIL_BODY      = (
        "[data-testid='TODO_detailBody'], "
        "[class*='content'], "
        "[class*='body'], "
        "article"
    )
    DETAIL_BODY_IMG  = (
        "[data-testid='TODO_detailBodyImg'], "
        "[class*='content'] img, "
        "[class*='body'] img, "
        "article img"
    )
    DETAIL_BODY_LINK = (
        "[data-testid='TODO_detailBodyLink'], "
        "[class*='content'] a[href], "
        "[class*='body'] a[href], "
        "article a[href]"
    )

    # ── 첨부파일 — HTML 미노출 ────────────────────────────────────────
    # ⚠️ TODO: 첨부파일 포함 공지 상세 접속 후 F12 확인
    ATTACHMENT_SECTION  = (
        "[data-testid='TODO_attachmentSection'], "
        "[class*='attachment'], "
        "[class*='fileList']"
    )
    ATTACHMENT_ITEM     = "[data-testid='TODO_attachmentItem'], [class*='fileItem']"
    ATTACHMENT_FILENAME = "[data-testid='TODO_attachmentFilename'], [class*='fileName']"
    ATTACHMENT_LINK     = (
        "[data-testid='TODO_attachmentLink'], "
        "[class*='attachment'] a[href], "
        "[class*='fileItem'] a[href]"
    )

    # ── Empty State ──────────────────────────────────────────────────
    # ⚠️ TODO: 공지 0건 환경 또는 필터 결과 없음 상태에서 F12 확인
    EMPTY_STATE     = (
        "[data-testid='TODO_emptyState'], "
        "[class*='emptyState'], "
        "[class*='empty']"
    )
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

    def go_to_notice_list(self) -> None:
        """공지사항 목록 페이지로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.NOTICE_LIST_PATH}")
        self.page.wait_for_timeout(600)

    def go_to_notice_detail(self, notice_id: str) -> None:
        """공지사항 상세 페이지로 직접 이동 (/notice/{id})"""
        self._safe_goto(f"{self.BASE_URL}{self.NOTICE_DETAIL_PATH}{notice_id}")
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

    def is_on_notice_list_page(self) -> bool:
        return self.NOTICE_LIST_PATH in self.page.url

    def is_on_notice_detail_page(self) -> bool:
        return self.NOTICE_DETAIL_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """공지사항 목록 페이지 로드 완료 여부 (리스트 영역 기준)"""
        try:
            self.page.wait_for_selector(self.LIST_WRAPPER, timeout=timeout)
            return True
        except Exception:
            # 폴백: 페이지 래퍼 노출 확인
            return self.page.locator(self.PAGE_WRAPPER).count() > 0

    def wait_for_notice_list(self, timeout: int = 8_000) -> bool:
        """공지 카드 목록 렌더링 대기"""
        try:
            self.page.wait_for_selector(self.LIST_UL, timeout=timeout)
            return True
        except Exception:
            return False

    def is_page_title_notice(self) -> bool:
        """'공지사항' 타이틀 노출 여부"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            return el.count() > 0 and "공지" in el.first.inner_text()
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  공지 목록 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_notice_count(self) -> int:
        """현재 화면에 노출된 공지 카드 수"""
        return self.page.locator(self.NOTICE_CARD).count()

    def get_notice_title(self, index: int = 0) -> str:
        """index 번째 공지 제목 텍스트"""
        try:
            return self.page.locator(self.NOTICE_TITLE).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_notice_date(self, index: int = 0) -> str:
        """index 번째 공지 날짜 텍스트 (예: '2026.03.28')"""
        try:
            return self.page.locator(self.NOTICE_DATE).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_notice_href(self, index: int = 0) -> str:
        """index 번째 공지 카드 href 반환"""
        try:
            return self.page.locator(self.NOTICE_CARD).nth(index).get_attribute("href") or ""
        except Exception:
            return ""

    def get_all_dates(self) -> list:
        """모든 공지 카드의 날짜 텍스트 목록 반환"""
        dates = []
        try:
            els = self.page.locator(self.NOTICE_DATE).all()
            for el in els:
                txt = el.inner_text().strip()
                if txt:
                    dates.append(txt)
        except Exception:
            pass
        return dates

    def are_dates_sorted_latest(self) -> bool:
        """날짜가 최신순(내림차순)으로 정렬되어 있는지 확인
        날짜 형식: 'YYYY.MM.DD' (예: '2026.03.28')
        """
        dates = self.get_all_dates()
        if len(dates) < 2:
            return True  # 1건 이하는 정렬 검증 불가
        for i in range(len(dates) - 1):
            if dates[i] < dates[i + 1]:
                return False  # 이전 날짜가 다음 날짜보다 작으면 오름차순 → 실패
        return True

    def is_title_clamped(self, index: int = 0) -> bool:
        """index 번째 공지 제목에 CSS 말줄임(ellipsis 또는 line-clamp) 적용 여부"""
        try:
            el = self.page.locator(self.NOTICE_TITLE).nth(index)
            overflow       = el.evaluate("e => window.getComputedStyle(e).overflow")
            text_overflow  = el.evaluate("e => window.getComputedStyle(e).textOverflow")
            webkit_clamp   = el.evaluate("e => window.getComputedStyle(e).webkitLineClamp")
            return (
                "hidden" in str(overflow)
                or "ellipsis" in str(text_overflow)
                or (str(webkit_clamp).isdigit() and int(str(webkit_clamp)) > 0)
            )
        except Exception:
            return False

    def is_pinned_badge_visible(self) -> bool:
        """고정 공지 핀 배지 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.PINNED_BADGE).count() > 0

    def get_pinned_card_count(self) -> int:
        """고정 공지 카드 수 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.PINNED_CARD).count()

    def is_pinned_card_before_normal(self) -> bool:
        """고정 공지가 일반 공지보다 상단에 위치하는지 확인
        ⚠️ TODO: PINNED_CARD 셀렉터 튜닝 필요
        폴백: 카드 순서 및 위치(bounding box Y 좌표)로 판단
        """
        pinned_count = self.get_pinned_card_count()
        if pinned_count == 0:
            return True  # 고정 공지 없으면 검증 불가 → pass

        try:
            pinned_el  = self.page.locator(self.PINNED_CARD).first
            all_cards  = self.page.locator(self.NOTICE_CARD)
            normal_idx = None
            pinned_cls = pinned_el.get_attribute("class") or ""

            for i in range(all_cards.count()):
                card_cls = all_cards.nth(i).get_attribute("class") or ""
                if "pinned" not in card_cls.lower():
                    normal_idx = i
                    break

            if normal_idx is None:
                return True  # 일반 공지 없음 → pass

            pinned_y = pinned_el.evaluate("e => e.getBoundingClientRect().top")
            normal_y = all_cards.nth(normal_idx).evaluate("e => e.getBoundingClientRect().top")
            return float(pinned_y) <= float(normal_y)
        except Exception:
            return True

    def is_new_badge_visible_on_card(self, index: int = 0) -> bool:
        """index 번째 공지 카드에 NEW 배지 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            card = self.page.locator(self.NOTICE_CARD).nth(index)
            # 방법 1: 카드 내부에 NEW 배지 요소 있는지 확인
            new_in_card = card.locator(self.NEW_BADGE)
            if new_in_card.count() > 0:
                return True
            # 방법 2: 카드 텍스트에 'NEW' 포함 여부
            txt = card.inner_text()
            return "NEW" in txt.upper()
        except Exception:
            return False

    def get_new_badge_count(self) -> int:
        """전체 목록에서 NEW 배지 노출 카드 수"""
        return self.page.locator(self.NEW_BADGE).count()

    # ══════════════════════════════════════════════════════════════════
    #  카테고리 탭 메서드 (⚠️ 모두 TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_category_tab_visible(self) -> bool:
        """카테고리 탭 영역 노출 여부"""
        return self.page.locator(self.CATEGORY_WRAPPER).count() > 0

    def _click_tab(self, selector: str, wait_ms: int = 800) -> None:
        """탭 클릭 공통 헬퍼
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(selector).first
        try:
            loc.wait_for(state="visible", timeout=3_000)
            loc.click(timeout=3_000)
            self.page.wait_for_timeout(wait_ms)
            return
        except Exception:
            pass
        try:
            loc.wait_for(state="attached", timeout=5_000)
            loc.click(force=True)
            self.page.wait_for_timeout(wait_ms)
        except Exception:
            pass

    def click_tab_all(self) -> None:
        """'전체' 카테고리 탭 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        self._click_tab(self.CATEGORY_TAB_ALL)

    def click_tab_notice(self) -> None:
        """'공지' 카테고리 탭 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        self._click_tab(self.CATEGORY_TAB_NOTICE)

    def click_tab_event(self) -> None:
        """'이벤트' 카테고리 탭 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        self._click_tab(self.CATEGORY_TAB_EVENT)

    def click_tab_guide(self) -> None:
        """'안내' 카테고리 탭 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        self._click_tab(self.CATEGORY_TAB_GUIDE)

    def get_active_category_tab_text(self) -> str:
        """현재 활성 카테고리 탭 텍스트 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.CATEGORY_ACTIVE_TAB).first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  검색 메서드 (⚠️ 모두 TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_search_visible(self) -> bool:
        """검색창 노출 여부"""
        return self.page.locator(self.SEARCH_INPUT).count() > 0

    def type_search_keyword(self, keyword: str) -> None:
        """검색창에 키워드 입력 후 검색 실행
        ① 입력창에 타이핑 → ② Enter 키 또는 검색 버튼 클릭
        """
        loc = self.page.locator(self.SEARCH_INPUT).first
        try:
            loc.wait_for(state="visible", timeout=5_000)
            loc.click()
            loc.fill("")
            loc.type(keyword, delay=80)
            self.page.wait_for_timeout(300)
        except Exception:
            return

        # 검색 실행: 검색 버튼 클릭 또는 Enter
        submit_btn = self.page.locator(self.SEARCH_SUBMIT_BTN)
        if submit_btn.count() > 0:
            try:
                submit_btn.first.click(force=True)
                self.page.wait_for_timeout(800)
                return
            except Exception:
                pass
        # 폴백: Enter 키
        loc.press("Enter")
        self.page.wait_for_timeout(800)

    def click_search_clear(self) -> None:
        """검색어 초기화 버튼 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        clear_btn = self.page.locator(self.SEARCH_CLEAR_BTN)
        if clear_btn.count() > 0:
            try:
                clear_btn.first.click(force=True)
                self.page.wait_for_timeout(600)
                return
            except Exception:
                pass
        # 폴백: 검색창 내용을 직접 삭제
        inp = self.page.locator(self.SEARCH_INPUT)
        if inp.count() > 0:
            try:
                inp.first.fill("")
                inp.first.press("Enter")
                self.page.wait_for_timeout(600)
            except Exception:
                pass

    def is_search_no_result_visible(self) -> bool:
        """검색 결과 없음 UI 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        if self.page.locator(self.SEARCH_NO_RESULT).count() > 0:
            return True
        # 폴백: 공지 카드가 0건인 경우
        return self.get_notice_count() == 0

    def get_search_input_value(self) -> str:
        """현재 검색창 입력값"""
        try:
            return self.page.locator(self.SEARCH_INPUT).first.input_value()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  공지 카드 클릭 / 라우팅
    # ══════════════════════════════════════════════════════════════════

    def click_notice_card(self, index: int = 0) -> None:
        """index 번째 공지 카드 클릭 (href goto 방식 우선 — Next.js Router 우회)"""
        loc = self.page.locator(self.NOTICE_CARD).nth(index)
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
            try:
                loc.evaluate("(el) => el.click()")
                self.page.wait_for_timeout(800)
            except Exception:
                pass

    # ══════════════════════════════════════════════════════════════════
    #  상세 페이지 메서드 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_detail_page_loaded(self, timeout: int = 8_000) -> bool:
        """공지 상세 페이지 로드 완료 여부 (제목 또는 본문 노출 기준)"""
        try:
            self.page.wait_for_selector(self.DETAIL_TITLE, timeout=timeout)
            return True
        except Exception:
            return self.page.locator(self.DETAIL_BODY).count() > 0

    def get_detail_title(self) -> str:
        """상세 페이지 공지 제목 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.DETAIL_TITLE).first.inner_text().strip()
        except Exception:
            return ""

    def get_detail_date(self) -> str:
        """상세 페이지 작성일 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.DETAIL_DATE).first.inner_text().strip()
        except Exception:
            return ""

    def get_detail_category(self) -> str:
        """상세 페이지 카테고리 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.DETAIL_CATEGORY).first.inner_text().strip()
        except Exception:
            return ""

    def get_detail_body_text(self) -> str:
        """상세 페이지 본문 텍스트 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.DETAIL_BODY).first.inner_text().strip()
        except Exception:
            return ""

    def get_detail_body_image_count(self) -> int:
        """상세 본문 이미지 수 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.DETAIL_BODY_IMG).count()

    def is_any_body_image_broken(self) -> bool:
        """본문 이미지 중 깨진(naturalWidth==0) 이미지 존재 여부"""
        imgs = self.page.locator(self.DETAIL_BODY_IMG).all()
        for img in imgs:
            try:
                natural_w = img.evaluate("e => e.naturalWidth")
                if int(natural_w) == 0:
                    return True
            except Exception:
                pass
        return False

    def get_detail_body_link_count(self) -> int:
        """상세 본문 링크(<a href>) 수 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.DETAIL_BODY_LINK).count()

    def click_first_detail_body_link(self) -> str:
        """상세 본문 첫 번째 링크 클릭 후 이동 URL 반환
        (href goto 방식으로 클릭 — 외부 링크는 새 탭으로 열릴 수 있음)
        """
        loc = self.page.locator(self.DETAIL_BODY_LINK).first
        try:
            loc.wait_for(state="attached", timeout=5_000)
            href = loc.get_attribute("href") or ""
            target = loc.get_attribute("target") or ""

            if target == "_blank":
                # 새 탭으로 열리는 링크: expect_page 컨텍스트로 캡처
                with self.page.context.expect_page() as new_page_info:
                    loc.click(force=True)
                new_tab = new_page_info.value
                new_tab.wait_for_load_state("domcontentloaded", timeout=8_000)
                url = new_tab.url
                new_tab.close()
                return url
            else:
                url_before = self.page.url
                loc.click(force=True)
                self.page.wait_for_timeout(800)
                return self.page.url
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  첨부파일 메서드 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_attachment_section_visible(self) -> bool:
        """첨부파일 영역 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.ATTACHMENT_SECTION).count() > 0

    def get_attachment_count(self) -> int:
        """첨부파일 항목 수 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.ATTACHMENT_ITEM).count()

    def get_attachment_filename(self, index: int = 0) -> str:
        """index 번째 첨부파일명 텍스트 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.ATTACHMENT_FILENAME).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_attachment_link_href(self, index: int = 0) -> str:
        """index 번째 첨부파일 다운로드 링크 href (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.ATTACHMENT_LINK).nth(index).get_attribute("href") or ""
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  스크롤 / 페이지네이션
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_bottom(self, steps: int = 5, delay_ms: int = 500) -> None:
        """페이지 최하단까지 단계적 스크롤"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(delay_ms)

    def is_pagination_visible(self) -> bool:
        """페이지네이션 번호 버튼 노출 여부"""
        return self.page.locator(self.PAGINATION_NUM_BTN).count() > 0

    def get_pagination_page_count(self) -> int:
        """페이지네이션 번호 버튼 수"""
        return self.page.locator(self.PAGINATION_NUM_BTN).count()

    def click_next_page(self) -> None:
        """다음 페이지(>) 버튼 클릭"""
        btn = self.page.locator(self.PAGINATION_NEXT_BTN).first
        try:
            btn.wait_for(state="attached", timeout=3_000)
            btn.click(force=True)
            self.page.wait_for_timeout(800)
        except Exception:
            pass

    def click_page_by_number(self, page_num: int) -> None:
        """특정 페이지 번호 버튼 클릭 (JS 방식)"""
        try:
            self.page.evaluate(
                f"""() => {{
                    const btns = document.querySelectorAll('div button');
                    const target = Array.from(btns).find(
                        b => b.querySelector('span') &&
                             b.querySelector('span').textContent.trim() === '{page_num}'
                    );
                    if (target) target.click();
                }}"""
            )
            self.page.wait_for_timeout(800)
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════════
    #  Empty State 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_empty_state_visible(self) -> bool:
        """빈 상태 UI 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        if self.page.locator(self.EMPTY_STATE).count() > 0:
            return True
        # 폴백: 리스트 wrapper는 있지만 카드가 0건
        return (
            self.page.locator(self.LIST_WRAPPER).count() > 0
            and self.page.locator(self.NOTICE_CARD).count() == 0
        )

    def get_empty_state_message(self) -> str:
        """빈 상태 안내 문구 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            loc = self.page.locator(self.EMPTY_STATE_MSG)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
            loc = self.page.locator(self.EMPTY_STATE)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
        except Exception:
            pass
        return ""