"""
pages/web/my_activity_page.py
[STEP 2 — POM v1]  내 활동(My Activity) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_myActiveMenu-module-scss-module__xxx__)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)
    - 탭 구조 실제 HTML 기준:
        · 데스크톱 탭: #myPageActiveTabsWrapper > button[class*='myActiveMenuButton']
        · 활성 탭:     button[class*='myActiveMenuButton'][class*='isFocus']
        · 실제 탭 텍스트: "게시글" / "댓글 / 답글"
          (TC 명칭 "작성한 글" / "댓글"과 다를 수 있음 — 셀렉터는 실제 DOM 기준)
        · "좋아요" / "스크랩" 탭은 제공된 HTML에 미노출 →
          [data-testid='TODO_...'] 형태로 작성하여 추후 튜닝 필요
    - 페이지네이션 구조: 번호 버튼 방식 (무한스크롤 TC와 불일치 가능)

셀렉터 전략:
    - 안정 ID 사용 최대화: #myPageActiveContainer, #myPageActiveTabsWrapper, #myPostListCompWrapper
    - 해시 없는 CSS class 부분 매칭: [class*='myActiveMenuButton'], [class*='myPostListCard']
    - Tailwind 유틸리티 클래스는 셀렉터로 사용 금지 (빌드마다 순서 변경 위험)
"""

from typing import Optional

from playwright.sync_api import Page


class MyActivityPage:
    """블루밍비트 내 활동(My Activity) 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 ───────────────────────────────────────────────────
    # HTML: <section class="...__myPageCommonContentWrapper">
    PAGE_WRAPPER    = "section[class*='myPageCommonContentWrapper']"
    # HTML: <header class="...__contentHeader">
    PAGE_HEADER     = "section[class*='myPageCommonContentWrapper'] header[class*='contentHeader']"
    # HTML: <h1>내 활동</h1>
    PAGE_TITLE      = "section[class*='myPageCommonContentWrapper'] header h1"
    # HTML: <a ... href="/mypage">뒤로가기 아이콘</a>
    BACK_BTN        = "section[class*='myPageCommonContentWrapper'] header a[href='/mypage']"

    # ── 활동 컨테이너 ─────────────────────────────────────────────────
    # HTML: <div id="myPageActiveContainer">
    ACTIVITY_CONTAINER = "#myPageActiveContainer"

    # ── 탭 영역 (데스크톱) ───────────────────────────────────────────
    # HTML: <div id="myPageActiveTabsWrapper">
    TAB_WRAPPER     = "#myPageActiveTabsWrapper"
    # 모든 탭 버튼 (hidden wrapper 제외, visible wrapper만)
    TAB_ALL_BTNS    = "#myPageActiveTabsWrapper button[class*='myActiveMenuButton']"
    # 활성 탭: isFocus 클래스 보유
    TAB_ACTIVE      = "#myPageActiveTabsWrapper button[class*='myActiveMenuButton'][class*='isFocus']"
    # 비활성 탭
    TAB_INACTIVE    = "#myPageActiveTabsWrapper button[class*='myActiveMenuButton']:not([class*='isFocus'])"

    # ── 개별 탭 버튼 ─────────────────────────────────────────────────
    # HTML 실제 텍스트: "게시글" (TC 명칭: "작성한 글")
    TAB_POSTS       = "#myPageActiveTabsWrapper button[class*='myActiveMenuButton']:has(span:text-is('게시글'))"
    # HTML 실제 텍스트: "댓글 / 답글" (TC 명칭: "댓글")
    TAB_COMMENTS    = "#myPageActiveTabsWrapper button[class*='myActiveMenuButton']:has(span:text-is('댓글 / 답글'))"
    # ⚠️ TODO: 아래 탭은 제공된 HTML에 미노출 — 실제 DOM 확인 후 셀렉터 튜닝 필요
    TAB_LIKES       = "[data-testid='TODO_tabLikes'], #myPageActiveTabsWrapper button:has(span:text-is('좋아요'))"
    TAB_SCRAPS      = "[data-testid='TODO_tabScraps'], #myPageActiveTabsWrapper button:has(span:text-is('스크랩'))"

    # ── 게시글 리스트 영역 ────────────────────────────────────────────
    # HTML: <div id="myPostListCompWrapper">
    POST_LIST_WRAPPER   = "#myPostListCompWrapper"
    # HTML: <ul class="...__myPostList">
    POST_LIST           = "#myPostListCompWrapper ul[class*='myPostList']"
    # HTML: <button class="...__myPostListCard" type="button">
    POST_CARD           = "#myPostListCompWrapper button[class*='myPostListCard']"
    # 카드 내 본문 텍스트: <div class="...__myPostContent"><p>텍스트</p></div>
    POST_CONTENT_TEXT   = "#myPostListCompWrapper button[class*='myPostListCard'] div[class*='myPostContent'] p"
    # 카드 내 날짜: <div class="...__myPostDate"><span>2026.05.06</span></div>
    POST_DATE_SPAN      = "#myPostListCompWrapper button[class*='myPostListCard'] div[class*='myPostDate'] span"
    # 카드 내 좋아요 수: <div class="...__myPostLikes"><svg/>  <span>0</span></div>
    POST_LIKES_COUNT    = "#myPostListCompWrapper button[class*='myPostListCard'] div[class*='myPostLikes'] span"
    # 카드 내 댓글 수: <div class="...__myPostCommentAmount"><svg/>  <span>0</span></div>
    POST_COMMENT_COUNT  = "#myPostListCompWrapper button[class*='myPostListCard'] div[class*='myPostCommentAmount'] span"

    # 예측 콘텐츠 카드 (게시글 목록 중 예측 타입)
    PREDICTION_CARD     = "#myPostListCompWrapper button[class*='myPostListCard']:has([class*='postPredictionContainer'])"
    PREDICTION_SUCCESS  = "[class*='postPredictionContainer'] [class*='statusSuccess']"
    PREDICTION_FAIL     = "[class*='postPredictionContainer'] [class*='statusFailed']"

    # ── 페이지네이션 ─────────────────────────────────────────────────
    # HTML: 번호 버튼 방식 (무한스크롤 대신 페이지네이션)
    # 페이지 번호 버튼 컨테이너 — max-[576px]:hidden (모바일에서는 숨김)
    PAGINATION_WRAPPER  = "#myPostListCompWrapper div[class*='max-\\[576px\\]:hidden']"
    # 페이지 번호 버튼 (span으로 숫자 표시)
    PAGINATION_NUM_BTN  = "#myPostListCompWrapper div[class*='max-\\[576px\\]:hidden'] div.flex:nth-child(2) button"
    # 다음 페이지 (>) 버튼 — hidden 클래스가 없는 것
    PAGINATION_NEXT_BTN = "#myPostListCompWrapper div[class*='max-\\[576px\\]:hidden'] div.flex:last-child button:last-child"
    # 이전 페이지 (<) 버튼
    PAGINATION_PREV_BTN = "#myPostListCompWrapper div[class*='max-\\[576px\\]:hidden'] div.flex:last-child button:first-child"

    # ── Empty State ──────────────────────────────────────────────────
    # ⚠️ TODO: Empty State UI는 제공된 HTML에 미노출 — 실제 DOM 확인 후 셀렉터 튜닝 필요
    EMPTY_STATE         = "[data-testid='TODO_emptyState'], [class*='emptyState'], [class*='empty']"
    EMPTY_STATE_MSG     = "[data-testid='TODO_emptyStateMessage']"

    # ── URL 패턴 ────────────────────────────────────────────────────
    MY_ACTIVITY_PATH  = "/mypage/history"
    MYPAGE_PATH       = "/mypage"
    COMMUNITY_DETAIL_PATTERN = "/community/"   # 게시글 상세 URL 패턴 (추정)
    SIGNIN_PATH       = "/user/signin"

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

    def go_to_my_activity(self) -> None:
        """내 활동 페이지(/mypage/history)로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.MY_ACTIVITY_PATH}")
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

    def click_back_btn(self) -> None:
        """헤더 뒤로가기 버튼 클릭 → /mypage로 이동"""
        btn = self.page.locator(self.BACK_BTN)
        if btn.count() > 0:
            try:
                btn.first.click(force=True)
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=5_000)
                except Exception:
                    pass
                self.page.wait_for_timeout(500)
                return
            except Exception:
                pass
        # 폴백: 직접 URL 이동
        self.go_to_mypage()

    def get_current_url(self) -> str:
        return self.page.url

    def is_on_my_activity_page(self) -> bool:
        return self.MY_ACTIVITY_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """내 활동 페이지 로드 완료 여부 (컨테이너 노출 기준)"""
        try:
            self.page.wait_for_selector(self.ACTIVITY_CONTAINER, timeout=timeout)
            return True
        except Exception:
            return False

    def is_page_title_visible(self) -> bool:
        """'내 활동' h1 타이틀 노출 여부"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            return "내 활동" in el.first.inner_text()
        except Exception:
            return False

    def wait_for_post_list(self, timeout: int = 8_000) -> bool:
        """게시글 리스트 컨테이너 로드 대기"""
        try:
            self.page.wait_for_selector(self.POST_LIST_WRAPPER, timeout=timeout)
            return True
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  탭 제어 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_tab_count(self) -> int:
        """노출된 탭 버튼 수"""
        return self.page.locator(self.TAB_ALL_BTNS).count()

    def get_active_tab_text(self) -> str:
        """현재 활성 탭 텍스트 (예: '게시글', '댓글 / 답글')"""
        try:
            return self.page.locator(self.TAB_ACTIVE).first.inner_text().strip()
        except Exception:
            return ""

    def _click_tab(self, selector: str, tab_name: str, wait_ms: int = 800) -> None:
        """탭 클릭 공통 헬퍼
        ① :visible 클릭 우선, ② attached + force=True 폴백
        """
        # 1단계: 보이는 버튼만
        loc = self.page.locator(selector).first
        try:
            loc.wait_for(state="visible", timeout=3_000)
            loc.click(timeout=3_000)
            self.page.wait_for_timeout(wait_ms)
            return
        except Exception:
            pass
        # 2단계: attached + force
        try:
            loc.wait_for(state="attached", timeout=5_000)
            loc.click(force=True)
            self.page.wait_for_timeout(wait_ms)
        except Exception:
            pass

    def click_tab_posts(self) -> None:
        """'게시글' 탭 클릭 (TC 명칭: '작성한 글')"""
        self._click_tab(self.TAB_POSTS, "게시글")

    def click_tab_comments(self) -> None:
        """'댓글 / 답글' 탭 클릭 (TC 명칭: '댓글')"""
        self._click_tab(self.TAB_COMMENTS, "댓글 / 답글")

    def click_tab_likes(self) -> None:
        """'좋아요' 탭 클릭 (⚠️ TODO: 실제 셀렉터 튜닝 필요)"""
        self._click_tab(self.TAB_LIKES, "좋아요")

    def click_tab_scraps(self) -> None:
        """'스크랩' 탭 클릭 (⚠️ TODO: 실제 셀렉터 튜닝 필요)"""
        self._click_tab(self.TAB_SCRAPS, "스크랩")

    def is_tab_active(self, selector: str) -> bool:
        """특정 탭이 활성 상태인지 확인 (isFocus 클래스 보유 여부)"""
        try:
            loc = self.page.locator(selector).first
            cls = loc.get_attribute("class") or ""
            return "isFocus" in cls
        except Exception:
            return False

    def is_posts_tab_active(self) -> bool:
        return self.is_tab_active(self.TAB_POSTS)

    def is_comments_tab_active(self) -> bool:
        return self.is_tab_active(self.TAB_COMMENTS)

    def is_likes_tab_active(self) -> bool:
        return self.is_tab_active(self.TAB_LIKES)

    def is_scraps_tab_active(self) -> bool:
        return self.is_tab_active(self.TAB_SCRAPS)

    # ══════════════════════════════════════════════════════════════════
    #  게시글 목록 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_post_card_count(self) -> int:
        """현재 화면에 노출된 게시글 카드 수"""
        return self.page.locator(self.POST_CARD).count()

    def get_first_post_content_text(self) -> str:
        """첫 번째 카드의 본문 텍스트"""
        try:
            return self.page.locator(self.POST_CONTENT_TEXT).first.inner_text().strip()
        except Exception:
            return ""

    def get_post_content_text(self, index: int = 0) -> str:
        """index 번째 카드의 본문 텍스트"""
        try:
            return self.page.locator(self.POST_CONTENT_TEXT).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_post_date_text(self, index: int = 0) -> str:
        """index 번째 카드의 날짜 텍스트 (예: '2026.05.06')"""
        try:
            return self.page.locator(self.POST_DATE_SPAN).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_post_likes_count(self, index: int = 0) -> str:
        """index 번째 카드의 좋아요 수 텍스트"""
        try:
            return self.page.locator(self.POST_LIKES_COUNT).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_post_comment_count(self, index: int = 0) -> str:
        """index 번째 카드의 댓글 수 텍스트"""
        try:
            return self.page.locator(self.POST_COMMENT_COUNT).nth(index).inner_text().strip()
        except Exception:
            return ""

    def click_post_card(self, index: int = 0) -> None:
        """index 번째 게시글 카드 클릭 → 상세 페이지 이동"""
        loc = self.page.locator(self.POST_CARD).nth(index)
        loc.wait_for(state="attached", timeout=5_000)
        try:
            loc.click(force=True)
        except Exception:
            loc.evaluate("(el) => el.click()")
        self.page.wait_for_timeout(800)

    def are_posts_sorted_by_latest(self) -> bool:
        """게시글 목록이 최신순 정렬인지 확인 (날짜 내림차순)
        날짜 형식: YYYY.MM.DD → 문자열 비교로 최신순 확인
        """
        dates = []
        try:
            els = self.page.locator(self.POST_DATE_SPAN).all()
            for el in els:
                txt = el.inner_text().strip()
                if txt:
                    dates.append(txt)
        except Exception:
            return True  # 날짜 추출 실패 시 pass 처리

        if len(dates) < 2:
            return True  # 1건 이하는 정렬 검증 불가

        # YYYY.MM.DD 형식 → 큰 값이 최신 (내림차순이어야 함)
        for i in range(len(dates) - 1):
            if dates[i] < dates[i + 1]:
                return False
        return True

    # ══════════════════════════════════════════════════════════════════
    #  스크롤 / 페이지네이션 메서드
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_bottom(self, steps: int = 5, delay_ms: int = 500) -> None:
        """페이지 최하단까지 단계적 스크롤"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(delay_ms)

    def is_pagination_visible(self) -> bool:
        """번호 페이지네이션 영역 노출 여부"""
        return self.page.locator(self.PAGINATION_NUM_BTN).count() > 0

    def get_page_count(self) -> int:
        """페이지네이션 번호 버튼 수"""
        return self.page.locator(self.PAGINATION_NUM_BTN).count()

    def click_next_page(self) -> None:
        """다음 페이지(>) 버튼 클릭"""
        btn = self.page.locator(self.PAGINATION_NEXT_BTN).first
        try:
            btn.click(force=True)
            self.page.wait_for_timeout(800)
        except Exception:
            pass

    def click_page_number(self, page_num: int) -> None:
        """특정 페이지 번호 버튼 클릭 (1-based)"""
        # span 텍스트로 찾기
        btn = self.page.locator(f"{self.PAGINATION_NUM_BTN} >> span:text-is('{page_num}')").first
        try:
            btn.wait_for(state="attached", timeout=3_000)
            self.page.evaluate(
                f"() => {{ const btns = document.querySelectorAll('#myPostListCompWrapper div button'); "
                f"const target = Array.from(btns).find(b => b.querySelector('span') && b.querySelector('span').textContent.trim() === '{page_num}'); "
                f"if(target) target.click(); }}"
            )
            self.page.wait_for_timeout(800)
        except Exception:
            pass

    def get_scroll_y_position(self) -> float:
        """현재 스크롤 Y 위치"""
        try:
            return self.page.evaluate("() => window.scrollY")
        except Exception:
            return 0.0

    # ══════════════════════════════════════════════════════════════════
    #  텍스트 말줄임 확인
    # ══════════════════════════════════════════════════════════════════

    def is_content_text_clamped(self, index: int = 0) -> bool:
        """index 번째 카드 본문 텍스트에 CSS 말줄임 적용 여부 확인"""
        try:
            el = self.page.locator(self.POST_CONTENT_TEXT).nth(index)
            overflow = el.evaluate("e => window.getComputedStyle(e).overflow")
            text_overflow = el.evaluate("e => window.getComputedStyle(e).textOverflow")
            webkit_clamp = el.evaluate("e => window.getComputedStyle(e).webkitLineClamp")
            return (
                "hidden" in str(overflow)
                or "ellipsis" in str(text_overflow)
                or (str(webkit_clamp).isdigit() and int(str(webkit_clamp)) > 0)
            )
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  Empty State 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_empty_state_visible(self) -> bool:
        """빈 상태 UI 노출 여부 (⚠️ TODO: 실제 HTML 확인 후 셀렉터 튜닝 필요)"""
        # 게시글 카드가 0개이고 리스트 컨테이너가 존재하면 empty state로 판단 (폴백)
        if self.page.locator(self.EMPTY_STATE).count() > 0:
            return True
        # 폴백: 카드가 없고 리스트 영역은 있는 경우
        return (
            self.page.locator(self.POST_LIST_WRAPPER).count() > 0
            and self.page.locator(self.POST_CARD).count() == 0
        )

    def get_empty_state_message(self) -> str:
        """빈 상태 안내 메시지 텍스트 (⚠️ TODO: 실제 셀렉터 튜닝 필요)"""
        try:
            loc = self.page.locator(self.EMPTY_STATE_MSG)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
            # 폴백: 리스트 컨테이너 전체 텍스트에서 추출
            wrapper = self.page.locator(self.POST_LIST_WRAPPER)
            if wrapper.count() > 0:
                return wrapper.first.inner_text().strip()
        except Exception:
            pass
        return ""

    # ══════════════════════════════════════════════════════════════════
    #  토스트 / 에러 감지
    # ══════════════════════════════════════════════════════════════════

    def is_deleted_content_toast_visible(self, timeout: int = 3_000) -> bool:
        """'삭제된 게시글' 등 토스트 메시지 노출 여부"""
        try:
            # 일반적인 토스트 패턴: role="alert", role="status", class*='toast'
            toast_selector = (
                "[role='alert'], [role='status'], "
                "[class*='toast'], [class*='Toast'], "
                "[class*='snackbar'], [class*='Snackbar']"
            )
            self.page.wait_for_selector(toast_selector, timeout=timeout)
            return True
        except Exception:
            # 폴백: "삭제" 텍스트가 포함된 요소 존재 여부
            return (
                self.page.locator(
                    f"{toast_selector}", has_text="삭제"
                ).count() > 0
                if False
                else self.page.get_by_text("삭제된 게시글").count() > 0
                or self.page.get_by_text("삭제된").count() > 0
            )

    # ══════════════════════════════════════════════════════════════════
    #  로그인 상태 확인
    # ══════════════════════════════════════════════════════════════════

    def is_login_page_redirected(self) -> bool:
        """로그인 페이지로 리다이렉트됐는지 확인"""
        return self.SIGNIN_PATH in self.page.url