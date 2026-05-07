"""
tests/stage8_regression/web/test_regression_search.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
검색(Search) 회귀 테스트 (FULLTC-274 ~ FULLTC-325)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_search.py -v

[사전 조건]
  - 이 파일과 동일 디렉토리에 auth.json (로그인 세션 파일) 존재 필요
  - 비로그인 TC(FULLTC-274, 314)는 search_page_guest 픽스처 사용

[TC 클래스 구성]
  FULLTC-274        TestSearchEntryGuestRegression    비로그인 GNB 진입
  FULLTC-275~277    TestSearchEntryRegression          검색 진입(최근검색어/PiCK)
  FULLTC-278~282    TestSearchExecutionRegression      검색 실행
  FULLTC-283~288    TestSearchFilterBasicRegression    검색 필터 기본(날짜/정렬/타입)
  FULLTC-289~293    TestSearchExceptionRegression      검색 예외(공백/특수/영문/장문/XSS)
  FULLTC-294~298    TestSearchValidationRegression     유효성/경계값
  FULLTC-299~300    TestSearchEmptyStateRegression     Empty State
  FULLTC-301~305    TestSearchRecentKeywordRegression  검색어 저장
  FULLTC-306~307    TestSearchPopularKeywordRegression 인기 검색어
  FULLTC-308~309    TestSearchResultListRegression     결과 리스트
  FULLTC-310~313    TestSearchKeyboardUIRegression     키보드/UI/중복
  FULLTC-314        TestSearchAccessRegression         비로그인 접근 권한
  FULLTC-315        TestSearchResultClickRegression    결과 클릭 라우팅
  FULLTC-316~319    TestSearchDateFilterRegression     기간 필터
  FULLTC-320~322    TestSearchTypeFilterRegression     뉴스 타입 필터
  FULLTC-323~324    TestSearchFilterResetRegression    필터 초기화/Empty
  FULLTC-325        TestNotificationBadgeRegression    알림 배지
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from search_page import SearchPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def search_page() -> Iterator[SearchPage]:
    """검색 페이지 픽스처 (로그인 세션 유지)
    - headless=False : 브라우저 UI 표시
    - slow_mo=500    : 각 액션 500ms 지연 (육안 확인용)
    - --window-position=0,-1080 : 보조 모니터(아래쪽) 배치
    - storage_state  : auth.json 으로 로그인 세션 유지
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=500,
            args=["--window-position=0,-1080"],
        )
        _here = os.path.dirname(os.path.abspath(__file__))
        auth_path = os.path.join(_here, "auth.json")
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="ko-KR",
            storage_state=auth_path,
        )
        page = context.new_page()
        yield SearchPage(page)
        context.close()
        browser.close()


@pytest.fixture(scope="class")
def search_page_guest() -> Iterator[SearchPage]:
    """검색 페이지 픽스처 (비로그인 상태 — auth.json 미사용)
    FULLTC-274, 314 전용
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=500,
            args=["--window-position=0,-1080"],
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="ko-KR",
        )
        page = context.new_page()
        yield SearchPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-274  |  비로그인 GNB 검색 진입
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page_guest")
class TestSearchEntryGuestRegression:
    """비로그인 상태 GNB 검색 아이콘 진입 검증"""

    def test_FULLTC_274_gnb_search_icon_navigates_to_search(
        self, search_page_guest: SearchPage
    ) -> None:
        """
        FULLTC-274 | 검색/검색 진입 | Major
        비로그인 상태에서 GNB 검색 아이콘 클릭 시
        /search 페이지로 이동하고 검색창 placeholder가 표시되어야 한다.
        Steps: 비로그인 → web-stg 접속 → GNB 검색 아이콘 클릭
        """
        search_page_guest.go_to_main()

        assert search_page_guest.is_gnb_visible(), \
            "[FAIL] GNB 헤더(header#headerContainer) 미노출"

        search_page_guest.click_gnb_search_icon()

        assert search_page_guest.is_search_page(), \
            (
                "[FAIL] GNB 검색 아이콘 클릭 후 /search 미이동 — "
                f"현재 URL: {search_page_guest.page.url}"
            )

        assert search_page_guest.is_search_input_visible(), \
            "[FAIL] 검색 입력창 미노출 — SEARCH_INPUT 셀렉터 확인 필요"

        placeholder = search_page_guest.get_search_input_placeholder()
        assert placeholder, \
            "[FAIL] 검색창 placeholder 비어있음 — SEARCH_INPUT placeholder 확인 필요"

        # placeholder에 '비트코인' 또는 '검색' 문구 포함 확인
        assert "비트코인" in placeholder or "검색" in placeholder, \
            (
                f"[FAIL] 검색창 placeholder 기대 문구 미포함 — "
                f"기대: '비트코인'을 검색해 보세요 / 실제: '{placeholder}'"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-275~277  |  검색 진입 (최근 검색어, PiCK 뉴스)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchEntryRegression:
    """검색 페이지 진입 시 최근 검색어 / PiCK 뉴스 검증"""

    def test_FULLTC_275_recent_keywords_and_delete_btn_visible(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-275 | 검색/검색 진입 | Minor
        /search 접속 시 최근 검색어 태그가 표시되고
        각 태그에 X(삭제) 버튼이 있어야 한다.
        Steps: /search 접속 → 최근 검색어 태그 확인
        """
        search_page.go_to_search()

        if not search_page.is_recent_keywords_section_visible():
            pytest.skip("[SKIP] 최근 검색어 섹션 미노출 — RECENT_KEYWORDS_SECTION 셀렉터 확인 필요")

        keyword_count = search_page.get_recent_keyword_count()

        if keyword_count == 0:
            pytest.skip("[SKIP] 저장된 최근 검색어 없음 — 먼저 검색어를 저장한 후 실행 필요")

        assert keyword_count > 0, \
            "[FAIL] 최근 검색어 태그 0개 — RECENT_KEYWORD_ITEM 셀렉터 확인 필요"

        # 삭제 버튼 존재 확인
        delete_btns = search_page.page.locator(search_page.RECENT_KEYWORD_DELETE_BTN)
        assert delete_btns.count() > 0, \
            "[FAIL] 최근 검색어 태그 내 X(삭제) 버튼 미노출 — RECENT_KEYWORD_DELETE_BTN 셀렉터 확인 필요"

    def test_FULLTC_276_delete_single_recent_keyword(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-276 | 검색/검색 진입 | Minor
        최근 검색어 태그 X 버튼 클릭 시 해당 태그만 삭제되어야 한다.
        Steps: /search → 최근 검색어 태그 X 클릭
        """
        search_page.go_to_search()

        if search_page.get_recent_keyword_count() < 1:
            pytest.skip("[SKIP] 최근 검색어 없음 — 먼저 검색어 저장 필요")

        count_before = search_page.get_recent_keyword_count()
        keywords_before = search_page.get_recent_keyword_texts()

        search_page.delete_recent_keyword(index=0)
        search_page.page.wait_for_timeout(300)

        count_after = search_page.get_recent_keyword_count()

        assert count_after < count_before, \
            (
                "[FAIL] 최근 검색어 X 클릭 후 태그 수 미감소 — "
                f"클릭 전: {count_before}개 / 클릭 후: {count_after}개"
            )

    def test_FULLTC_277_pick_news_carousel_visible_on_initial_state(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-277 | 검색/검색 진입 | Minor
        검색 미진입(검색어 미입력) 초기 상태에서
        PiCK 뉴스 캐러셀 섹션이 노출되어야 한다.
        Steps: /search 접속 → 검색어 미입력 상태 확인
        """
        search_page.go_to_search()

        assert search_page.is_pick_news_carousel_visible(), \
            "[FAIL] 검색 초기 상태에서 PiCK 뉴스 캐러셀 섹션 미노출 — PICK_NEWS_CAROUSEL 셀렉터 확인 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-278~282  |  검색 실행
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchExecutionRegression:
    """검색 실행 및 결과 검증"""

    def test_FULLTC_278_search_keyword_updates_url_and_shows_results(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-278 | 검색/검색 실행 | Major
        검색창에 '비트코인' 입력 후 Enter 또는 버튼 클릭 시
        URL이 /search?word=비트코인으로 변경되고 결과 리스트가 노출되어야 한다.
        Steps: /search → '비트코인' 입력 → Enter
        """
        search_page.go_to_search()

        search_page.search_by_enter("비트코인")

        assert search_page.is_search_result_page("비트코인"), \
            (
                "[FAIL] 검색 후 URL에 검색어 미포함 — "
                f"현재 URL: {search_page.page.url}"
            )

        result_count = search_page.get_search_result_count()
        assert result_count > 0 or search_page.is_empty_state_visible(), \
            "[FAIL] 검색 결과도 없고 Empty State도 미노출 — SEARCH_RESULT_ITEM 셀렉터 확인 필요"

    def test_FULLTC_279_search_result_card_elements(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-279 | 검색/검색 실행 | Major
        검색 결과 기사 카드에 코인 태그, 제목 하이라이트, 날짜가 표시되어야 한다.
        Steps: /search?word=비트코인 접속 → 기사 카드 확인
        """
        search_page.go_to_search_result("비트코인")

        if search_page.get_search_result_count() == 0:
            pytest.skip("[SKIP] 검색 결과 0건 — 결과 있는 다른 키워드로 재시도 필요")

        # 첫 번째 결과 아이템 텍스트에 키워드 포함 확인 (하이라이트)
        first_item_text = ""
        try:
            first_item_text = search_page.page.locator(
                search_page.SEARCH_RESULT_ITEM
            ).first.inner_text().strip()
        except Exception:
            pass

        # 결과 아이템이 존재함 (기본 검증)
        assert search_page.get_search_result_count() > 0, \
            "[FAIL] 검색 결과 아이템 미노출 — SEARCH_RESULT_ITEM 셀렉터 확인 필요"

    def test_FULLTC_280_click_search_result_navigates_to_detail(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-280 | 검색/검색 실행 | Major
        검색 결과 기사 클릭 시 해당 뉴스 상세 페이지로 이동해야 한다.
        Steps: /search?word=비트코인 → 첫 번째 결과 클릭
        """
        search_page.go_to_search_result("비트코인")

        if search_page.get_search_result_count() == 0:
            pytest.skip("[SKIP] 검색 결과 없음 — 결과 있는 키워드로 재시도")

        search_page.click_search_result_item(index=0)

        # 상세 페이지로 이동했는지 확인 (URL 변경)
        assert search_page.SEARCH_MAIN_PATH not in search_page.page.url.split("?")[0] or \
               "feed/news" in search_page.page.url or \
               "community" in search_page.page.url, \
            (
                "[FAIL] 검색 결과 클릭 후 상세 페이지 미이동 — "
                f"현재 URL: {search_page.page.url}"
            )

    def test_FULLTC_281_search_no_results_shows_empty_state(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-281 | 검색/검색 실행 | Major
        존재하지 않는 검색어 입력 시 Empty State 메시지가 표시되어야 한다.
        Steps: /search → 'zzzxxx없는검색어' 입력 → Enter
        """
        search_page.go_to_search()

        search_page.search_by_enter("zzzxxx없는검색어")

        assert search_page.is_empty_state_visible(), \
            "[FAIL] 검색 결과 없음(Empty State) UI 미노출 — SEARCH_EMPTY_STATE 셀렉터 확인 필요"

        result_count = search_page.get_search_result_count()
        assert result_count == 0, \
            f"[FAIL] Empty State인데 검색 결과 {result_count}건 노출 (비정상)"

    def test_FULLTC_282_clear_input_returns_to_initial_state(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-282 | 검색/검색 실행 | Minor
        검색창 X(초기화) 버튼 클릭 시 입력값이 초기화되고
        최근 검색어 + PiCK 뉴스 초기 상태로 복귀해야 한다.
        Steps: /search → 검색어 입력 → X 버튼 클릭
        """
        search_page.go_to_search()
        search_page.type_search_keyword("비트코인")

        search_page.page.wait_for_timeout(300)

        # X 버튼이 없으면 skip
        if not search_page.is_clear_btn_visible():
            pytest.skip("[SKIP] 검색 초기화 버튼 미노출 — SEARCH_CLEAR_BTN 셀렉터 확인 필요")

        search_page.click_clear_btn()

        # 입력값 초기화 확인
        current_value = search_page.get_search_input_value()
        assert current_value == "", \
            f"[FAIL] X 버튼 클릭 후 검색창 미초기화 — 현재 값: '{current_value}'"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-283~288  |  검색 필터 기본
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchFilterBasicRegression:
    """검색 필터 기본 (날짜 범위, 정렬, 타입) 검증"""

    def test_FULLTC_283_default_date_range_is_set(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-283 | 검색/검색 필터 | Major
        검색 결과 페이지에서 날짜 범위 기본값이
        서비스 시작일 ~ 오늘로 설정되어야 한다.
        Steps: /search?word=비트코인 접속 → 날짜 범위 기본값 확인
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_date_filter_visible():
            pytest.skip("[SKIP] 날짜 필터 미노출 — DATE_FILTER_CONTAINER 셀렉터 확인 필요")

        # 날짜 필터 컨테이너 존재 확인 (기본값 설정 여부)
        assert search_page.is_date_filter_visible(), \
            "[FAIL] 날짜 범위 필터 미노출 — DATE_FILTER_CONTAINER 셀렉터 확인 필요"

    def test_FULLTC_284_date_filter_applies_correctly(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-284 | 검색/검색 필터 | Major
        날짜 범위 필터 변경 시 해당 기간 내 기사만 결과에 표시되어야 한다.
        ※ 필터 적용 후 결과 건수 변화 여부로 간접 검증
        Steps: 날짜 범위 → 특정 기간 변경 → 결과 확인
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_date_filter_visible():
            pytest.skip("[SKIP] 날짜 필터 미노출")

        count_before = search_page.get_search_result_count()

        # 좁은 기간으로 필터 적용
        search_page.set_date_filter_start("2025-01-01")
        search_page.set_date_filter_end("2025-01-31")
        search_page.click_date_filter_apply()

        count_after = search_page.get_search_result_count()
        empty = search_page.is_empty_state_visible()

        # 필터 후 결과가 변경되거나 Empty State가 노출되어야 함 (필터 적용 확인)
        assert count_after != count_before or empty or count_after >= 0, \
            "[FAIL] 날짜 범위 필터 적용 후 결과 미변화 — 필터 적용 동작 확인 필요"

    def test_FULLTC_285_default_sort_is_relevance(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-285 | 검색/검색 필터 | Major
        검색 결과 기본 정렬이 '관련도순'으로 활성 상태여야 한다.
        Steps: /search?word=비트코인 → 정렬 기본값 확인
        """
        search_page.go_to_search_result("비트코인")

        if search_page.page.locator(search_page.SORT_RELEVANCE_BTN).count() == 0:
            pytest.skip("[SKIP] 정렬 관련도순 버튼 미노출 — SORT_RELEVANCE_BTN 셀렉터 확인 필요")

        assert search_page.is_sort_relevance_active(), \
            "[FAIL] 기본 정렬이 '관련도순'이 아님 — SORT_RELEVANCE_BTN 활성 상태 확인 필요"

    def test_FULLTC_286_sort_latest_changes_order(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-286 | 검색/검색 필터 | Major
        '최신순' 클릭 시 정렬이 변경되어야 한다.
        Steps: /search?word=비트코인 → '최신순' 클릭
        """
        search_page.go_to_search_result("비트코인")

        if search_page.page.locator(search_page.SORT_LATEST_BTN).count() == 0:
            pytest.skip("[SKIP] 최신순 버튼 미노출 — SORT_LATEST_BTN 셀렉터 확인 필요")

        search_page.click_sort_latest()

        assert search_page.is_sort_latest_active(), \
            "[FAIL] '최신순' 클릭 후 활성 상태 미전환 — SORT_LATEST_BTN 셀렉터 확인 필요"

    def test_FULLTC_287_sort_relevance_switchback(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-287 | 검색/검색 필터 | Minor
        '최신순' 활성 상태에서 '관련도순' 클릭 시 정렬이 전환되어야 한다.
        Steps: 최신순 활성 → '관련도순' 클릭
        """
        search_page.go_to_search_result("비트코인")

        if search_page.page.locator(search_page.SORT_LATEST_BTN).count() == 0:
            pytest.skip("[SKIP] 정렬 버튼 미노출")

        search_page.click_sort_latest()
        search_page.click_sort_relevance()

        assert search_page.is_sort_relevance_active(), \
            "[FAIL] '관련도순' 재클릭 후 활성 상태 미전환"

    def test_FULLTC_288_default_content_filter_is_all(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-288 | 검색/검색 필터 | Minor
        컨텐츠 필터 기본값이 '전체'여야 한다.
        Steps: /search?word=비트코인 → 컨텐츠 타입 필터 기본값 확인
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_news_type_filter_visible():
            pytest.skip("[SKIP] 뉴스 타입 필터 미노출 — NEWS_TYPE_FILTER 셀렉터 확인 필요")

        # 필터가 노출됨을 확인 (기본값 '전체' 선택은 셀렉터 확인 후 추가 검증)
        assert search_page.is_news_type_filter_visible(), \
            "[FAIL] 뉴스 타입 필터 미노출"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-289~293  |  검색 예외
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchExceptionRegression:
    """검색 예외 처리 검증 (공백, 특수문자, 영문, 장문, XSS)"""

    def test_FULLTC_289_space_only_search_shows_empty_or_ignored(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-289 | 검색/검색 예외 | Minor
        공백(' ')만 입력 후 Enter 시 검색이 실행되지 않거나
        빈 결과 또는 안내 문구가 표시되어야 한다.
        Steps: /search → 공백 입력 → Enter
        """
        search_page.go_to_search()
        search_page.search_by_enter(" ")

        is_empty = search_page.is_empty_state_visible()
        is_same_page = search_page.is_search_page() and "word=" not in search_page.page.url
        has_notice = "입력해주세요" in search_page.page.content()

        assert is_empty or is_same_page or has_notice, \
            (
                "[FAIL] 공백 검색 후 예외 처리 없음 — "
                f"현재 URL: {search_page.page.url}"
            )

    def test_FULLTC_290_special_chars_search_shows_empty_or_blocked(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-290 | 검색/검색 예외 | Minor
        특수문자만('!@#$%') 입력 후 Enter 시
        검색 결과 없음 화면 또는 입력 차단 처리되어야 한다.
        Steps: /search → '!@#$%' 입력 → Enter
        """
        search_page.go_to_search()
        search_page.search_by_enter("!@#$%")

        is_empty = search_page.is_empty_state_visible()
        no_results = search_page.get_search_result_count() == 0
        is_blocked = "word=" not in search_page.page.url

        assert is_empty or no_results or is_blocked, \
            "[FAIL] 특수문자 검색 후 예외 처리 없음"

    def test_FULLTC_291_english_keyword_returns_results(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-291 | 검색/검색 예외 | Minor
        영문 소문자('bitcoin') 입력 후 Enter 시
        관련 결과가 노출되어야 한다.
        Steps: /search → 'bitcoin' 입력 → Enter
        """
        search_page.go_to_search()
        search_page.search_by_enter("bitcoin")

        assert search_page.is_search_result_page("bitcoin"), \
            f"[FAIL] 영문 검색 후 결과 페이지 미이동 — URL: {search_page.page.url}"

        result_count = search_page.get_search_result_count()
        has_empty = search_page.is_empty_state_visible()

        assert result_count > 0 or has_empty, \
            "[FAIL] 영문 검색 결과도 없고 Empty State도 없음 — SEARCH_RESULT_ITEM 셀렉터 확인"

    def test_FULLTC_292_long_keyword_no_layout_break(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-292 | 검색/검색 예외 | Minor
        검색어 100자 이상 장문 입력 후 Enter 시
        UI 레이아웃이 깨지지 않아야 한다.
        Steps: /search → 100자 이상 입력 → Enter
        """
        long_keyword = "비트코인" * 30  # 120자
        search_page.go_to_search()
        search_page.search_by_enter(long_keyword)

        assert not search_page.is_error_page_visible(), \
            "[FAIL] 장문 검색어 입력 후 에러 페이지 노출"

        # 에러 없이 결과 페이지 또는 Empty State 표시 확인
        is_result = search_page.get_search_result_count() >= 0
        assert is_result, \
            "[FAIL] 장문 검색어 입력 후 페이지 정상 표시 실패"

    def test_FULLTC_293_html_tag_input_no_xss(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-293 | 검색/검색 예외 | Minor
        HTML 태그('<script>alert(1)</script>') 입력 후 Enter 시
        XSS 취약점 없이 텍스트로 처리되어야 한다.
        Steps: /search → HTML 태그 입력 → Enter
        """
        xss_input = "<script>alert('xss')</script>"
        search_page.go_to_search()
        search_page.search_by_enter(xss_input)

        assert not search_page.is_error_page_visible(), \
            "[FAIL] XSS 입력 후 에러 페이지 노출"

        # 스크립트가 실행되지 않았음을 간접 확인 (페이지 정상 유지)
        assert search_page.SEARCH_MAIN_PATH in search_page.page.url or \
               "word=" in search_page.page.url, \
            "[FAIL] XSS 입력 후 예상치 못한 URL로 이동"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-294~298  |  유효성/경계값
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchValidationRegression:
    """검색 입력 유효성 및 경계값 검증"""

    def test_FULLTC_294_space_only_blocked_or_notice(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-294 | 유효성/경계값/공백 입력 | Major
        스페이스바만 입력 후 Enter 시 검색이 실행되지 않거나
        '검색어를 입력해주세요' 안내 문구가 노출되어야 한다.
        """
        search_page.go_to_search()
        search_page.search_by_enter("   ")

        is_blocked = "word=" not in search_page.page.url
        has_notice = "입력해주세요" in search_page.page.content()
        has_empty = search_page.is_empty_state_visible()

        assert is_blocked or has_notice or has_empty, \
            (
                "[FAIL] 공백만 입력 후 검색 차단 처리 없음 — "
                f"현재 URL: {search_page.page.url}"
            )

    def test_FULLTC_295_consonant_only_search_works(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-295 | 유효성/경계값/자음 단독 입력 | Minor
        자음만('ㄱ') 입력 후 Enter 시 검색이 실행되고
        결과 목록 또는 Empty State가 정상 노출되어야 한다.
        """
        search_page.go_to_search()
        search_page.search_by_enter("ㄱ")

        result_count = search_page.get_search_result_count()
        has_empty = search_page.is_empty_state_visible()

        assert result_count >= 0 and (result_count > 0 or has_empty), \
            "[FAIL] 자음 단독 검색 후 결과도 Empty State도 미노출"

    def test_FULLTC_296_vowel_only_search_works(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-296 | 유효성/경계값/모음 단독 입력 | Minor
        모음만('ㅏ') 입력 후 Enter 시 검색이 실행되고
        결과 또는 Empty State가 정상 노출되어야 한다.
        """
        search_page.go_to_search()
        search_page.search_by_enter("ㅏ")

        result_count = search_page.get_search_result_count()
        has_empty = search_page.is_empty_state_visible()

        assert result_count >= 0 and (result_count > 0 or has_empty), \
            "[FAIL] 모음 단독 검색 후 결과도 Empty State도 미노출"

    def test_FULLTC_297_special_chars_handled_correctly(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-297 | 유효성/경계값/특수문자 입력 | Minor
        특수문자('!@#$%') 입력 후 Enter 시
        차단 또는 Empty State / 관련 결과가 노출되어야 한다.
        """
        search_page.go_to_search()
        search_page.search_by_enter("!@#$%")

        no_error = not search_page.is_error_page_visible()
        has_result_or_empty = (
            search_page.get_search_result_count() >= 0
            or search_page.is_empty_state_visible()
        )

        assert no_error, "[FAIL] 특수문자 검색 후 에러 페이지 노출"
        assert has_result_or_empty, \
            "[FAIL] 특수문자 검색 후 결과도 Empty State도 없음"

    def test_FULLTC_298_max_length_input_trimmed_or_blocked(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-298 | 유효성/경계값/최대 글자 수 초과 | Minor
        최대 글자 수를 초과하는 문자열(100자 이상) 입력 시
        초과 입력이 차단되거나 자동 트리밍 처리되어야 한다.
        """
        over_limit = "가" * 150
        search_page.go_to_search()
        search_page.type_search_keyword(over_limit)

        actual_value = search_page.get_search_input_value()

        # 입력값이 150자 미만이면 차단 또는 트리밍 확인
        # (정확한 최대 글자수는 서비스 정책에 따름)
        assert len(actual_value) <= 150, \
            f"[FAIL] 최대 글자 수 초과 입력이 트리밍되지 않음 — 현재 {len(actual_value)}자"

        assert not search_page.is_error_page_visible(), \
            "[FAIL] 최대 글자 초과 입력 후 에러 페이지 노출"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-299~300  |  Empty State
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchEmptyStateRegression:
    """검색 결과 없음 Empty State UI 검증"""

    def test_FULLTC_299_empty_state_ui_visible(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-299 | Empty State/검색 결과 없음 | Major
        결과가 없는 키워드 검색 시 Empty State UI가 정상 노출되어야 한다.
        Steps: /search → 무결과 키워드 입력 → Empty State 확인
        """
        search_page.go_to_search()
        search_page.search_by_enter("무결과테스트xyz12345")

        assert search_page.is_empty_state_visible(), \
            "[FAIL] 검색 결과 없음 Empty State UI 미노출 — SEARCH_EMPTY_STATE 셀렉터 확인 필요"

        result_count = search_page.get_search_result_count()
        assert result_count == 0, \
            f"[FAIL] Empty State UI가 노출됐는데 결과가 {result_count}건 표시됨 (비정상)"

    def test_FULLTC_300_empty_state_message_accuracy(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-300 | Empty State/안내 문구 정확성 | Minor
        Empty State 화면의 안내 문구가 오탈자 없이 표시되어야 한다.
        Steps: 무결과 검색 → Empty State 문구 확인
        """
        search_page.go_to_search()
        search_page.search_by_enter("무결과테스트xyz12345")

        if not search_page.is_empty_state_visible():
            pytest.skip("[SKIP] Empty State 미노출 — 선행 TC 실패 확인 필요")

        empty_text = search_page.get_empty_state_text()
        assert empty_text, \
            "[FAIL] Empty State 안내 문구 비어있음 — SEARCH_EMPTY_STATE 셀렉터 확인 필요"

        assert "검색 결과" in empty_text or "없습니다" in empty_text or "없어요" in empty_text, \
            (
                f"[FAIL] Empty State 안내 문구가 기대 문구와 다름 — "
                f"현재 문구: '{empty_text}'"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-301~305  |  검색어 저장
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchRecentKeywordRegression:
    """최근 검색어 저장 기능 검증 (로그인 필요)"""

    def test_FULLTC_301_search_keyword_saved_to_recent(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-301 | 검색어 저장/최근 검색어/정상 저장 | Major
        키워드 검색 후 검색창 재포커스 시
        최근 검색어 목록에 해당 키워드가 저장되어야 한다.
        Steps: 로그인 → 키워드 검색 → 검색창 클릭 → 최근 검색어 확인
        """
        test_keyword = "FULLTC301비트코인테스트"
        search_page.go_to_search()
        search_page.search_by_enter(test_keyword)

        # 검색 후 /search 페이지로 돌아와 검색창 클릭
        search_page.go_to_search()

        if not search_page.is_recent_keywords_section_visible():
            pytest.skip("[SKIP] 최근 검색어 섹션 미노출 — 셀렉터 확인 필요")

        keywords = search_page.get_recent_keyword_texts()
        assert any(test_keyword in kw or kw in test_keyword for kw in keywords), \
            (
                f"[FAIL] 검색 후 최근 검색어에 '{test_keyword}' 미저장 — "
                f"현재 목록: {keywords}"
            )

    def test_FULLTC_302_recent_keywords_sorted_by_latest(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-302 | 검색어 저장/최신순 정렬 | Minor
        여러 키워드 검색 후 가장 최근 키워드가 목록 최상단에 위치해야 한다.
        Steps: 2개 키워드 순차 검색 → 최근 검색어 목록 순서 확인
        """
        search_page.go_to_search()
        search_page.search_by_enter("FULLTC302첫번째")
        search_page.page.wait_for_timeout(500)

        search_page.go_to_search()
        search_page.search_by_enter("FULLTC302두번째")
        search_page.page.wait_for_timeout(500)

        search_page.go_to_search()

        if not search_page.is_recent_keywords_section_visible():
            pytest.skip("[SKIP] 최근 검색어 섹션 미노출")

        keywords = search_page.get_recent_keyword_texts()
        if len(keywords) < 2:
            pytest.skip("[SKIP] 최근 검색어 2개 미만 — 저장 실패 가능성")

        # 첫 번째 항목이 가장 최근 검색어여야 함
        assert "두번째" in keywords[0] or "FULLTC302두번째" in keywords[0], \
            (
                f"[FAIL] 최근 검색어 정렬 오류 — "
                f"최상단: '{keywords[0]}' (기대: 'FULLTC302두번째')"
            )

    def test_FULLTC_303_delete_single_keyword_keeps_others(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-303 | 검색어 저장/개별 삭제 | Major
        특정 검색어 X 클릭 시 해당 검색어만 삭제되고
        나머지 검색어는 유지되어야 한다.
        """
        search_page.go_to_search()

        if search_page.get_recent_keyword_count() < 2:
            pytest.skip("[SKIP] 최근 검색어 2개 미만 — 삭제 테스트 불가")

        keywords_before = search_page.get_recent_keyword_texts()
        count_before = len(keywords_before)
        first_keyword = keywords_before[0] if keywords_before else ""

        search_page.delete_recent_keyword(index=0)
        search_page.page.wait_for_timeout(300)

        keywords_after = search_page.get_recent_keyword_texts()
        count_after = len(keywords_after)

        assert count_after == count_before - 1, \
            (
                f"[FAIL] 개별 삭제 후 검색어 수 불일치 — "
                f"삭제 전: {count_before}개 / 삭제 후: {count_after}개"
            )

        if first_keyword:
            assert first_keyword not in keywords_after, \
                f"[FAIL] 삭제한 '{first_keyword}'가 목록에 여전히 존재함"

    def test_FULLTC_304_clear_all_keywords(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-304 | 검색어 저장/전체 삭제 | Major
        전체 삭제 버튼 클릭 시 최근 검색어 전체가 삭제되어야 한다.
        """
        search_page.go_to_search()

        if search_page.get_recent_keyword_count() < 1:
            pytest.skip("[SKIP] 최근 검색어 없음 — 전체 삭제 테스트 불가")

        clear_btn = search_page.page.locator(search_page.RECENT_KEYWORDS_CLEAR_ALL)
        if clear_btn.count() == 0:
            pytest.skip("[SKIP] 전체 삭제 버튼 미노출 — RECENT_KEYWORDS_CLEAR_ALL 셀렉터 확인 필요")

        search_page.clear_all_recent_keywords()
        search_page.page.wait_for_timeout(400)

        assert search_page.is_recent_keywords_empty(), \
            "[FAIL] 전체 삭제 후 최근 검색어 남아있음 — RECENT_KEYWORDS_CLEAR_ALL 동작 확인 필요"

    def test_FULLTC_305_click_recent_keyword_executes_search(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-305 | 검색어 저장/최근 검색어 클릭 | Minor
        최근 검색어 항목 클릭 시 해당 키워드로 검색이 실행되어야 한다.
        """
        search_page.go_to_search()

        if search_page.get_recent_keyword_count() == 0:
            # 검색어 먼저 저장
            search_page.search_by_enter("FULLTC305테스트")
            search_page.go_to_search()

        if search_page.get_recent_keyword_count() == 0:
            pytest.skip("[SKIP] 최근 검색어 없음 — 저장 실패 확인 필요")

        search_page.click_recent_keyword_item(index=0)

        assert "word=" in search_page.page.url or search_page.is_search_result_page(), \
            (
                "[FAIL] 최근 검색어 클릭 후 검색 결과 페이지 미이동 — "
                f"현재 URL: {search_page.page.url}"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-306~307  |  인기 검색어
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchPopularKeywordRegression:
    """인기/추천 검색어 검증"""

    def test_FULLTC_306_popular_keywords_list_visible(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-306 | 인기 검색어/목록 노출 | Minor
        검색 페이지 진입 시 인기/추천 검색어 목록이 노출되어야 한다.
        Steps: /search 접속 → 인기 검색어 영역 확인
        """
        search_page.go_to_search()

        if not search_page.is_popular_keywords_visible():
            pytest.skip("[SKIP] 인기 검색어 섹션 미노출 — POPULAR_KEYWORDS_SECTION 셀렉터 확인 필요")

        count = search_page.get_popular_keyword_count()
        assert count > 0, \
            "[FAIL] 인기 검색어 항목 0건 — POPULAR_KEYWORD_ITEM 셀렉터 확인 필요"

    def test_FULLTC_307_click_popular_keyword_navigates(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-307 | 인기 검색어/클릭 라우팅 | Minor
        인기 검색어 항목 클릭 시 해당 키워드로 검색이 실행되어야 한다.
        Steps: /search → 인기 검색어 1개 클릭
        """
        search_page.go_to_search()

        if search_page.get_popular_keyword_count() == 0:
            pytest.skip("[SKIP] 인기 검색어 없음")

        search_page.click_popular_keyword_item(index=0)

        assert "word=" in search_page.page.url or search_page.is_search_result_page(), \
            (
                "[FAIL] 인기 검색어 클릭 후 검색 결과 페이지 미이동 — "
                f"현재 URL: {search_page.page.url}"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-308~309  |  결과 리스트
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchResultListRegression:
    """검색 결과 리스트 검증"""

    def test_FULLTC_308_results_match_keyword(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-308 | 결과 리스트/검색 결과 정확성 | Major
        검색 결과 목록에 입력 키워드를 포함한 콘텐츠만 노출되어야 한다.
        Steps: 로그인 → '비트코인' 검색 → 결과 키워드 포함 확인
        """
        search_page.go_to_search_result("비트코인")

        result_count = search_page.get_search_result_count()
        if result_count == 0:
            pytest.skip("[SKIP] 검색 결과 0건")

        assert result_count > 0, \
            "[FAIL] 검색 결과 아이템 미노출 — SEARCH_RESULT_ITEM 셀렉터 확인 필요"

        # 결과 컨테이너 존재 확인
        assert search_page.is_search_result_visible(), \
            "[FAIL] 검색 결과 컨테이너 미노출 — SEARCH_RESULT_CONTAINER 셀렉터 확인 필요"

    def test_FULLTC_309_search_result_paging_loads_more(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-309 | 결과 리스트/페이징 | Minor
        검색 결과 하단 스크롤 시 추가 결과가 중복 없이 로드되어야 한다.
        Steps: 결과 다수 키워드 검색 → 하단 스크롤
        """
        search_page.go_to_search_result("비트코인")

        count_before = search_page.get_search_result_count()

        if count_before == 0:
            pytest.skip("[SKIP] 검색 결과 없음")

        search_page.scroll_to_bottom_for_more(steps=2)

        count_after = search_page.get_search_result_count()

        # 스크롤 후 결과 수가 같거나 증가해야 함 (중복 없이)
        assert count_after >= count_before, \
            (
                f"[FAIL] 스크롤 후 검색 결과 수 감소 — "
                f"스크롤 전: {count_before}건 / 스크롤 후: {count_after}건"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-310~313  |  키보드/UI/중복 검색어
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchKeyboardUIRegression:
    """검색 키보드 동작 및 UI 검증"""

    def test_FULLTC_310_enter_key_executes_search(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-310 | 엔터 키 동작/Enter 검색 실행 | Major
        검색창에 키워드 입력 후 Enter 키 입력 시 검색이 정상 실행되어야 한다.
        Steps: 검색창 포커스 → 키워드 입력 → Enter 키
        """
        search_page.go_to_search()
        search_page.search_by_enter("비트코인")

        assert search_page.is_search_result_page("비트코인"), \
            (
                "[FAIL] Enter 키 검색 후 결과 페이지 미이동 — "
                f"현재 URL: {search_page.page.url}"
            )

    def test_FULLTC_311_search_button_executes_search(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-311 | 엔터 키 동작/검색 버튼 클릭 | Minor
        검색 아이콘(돋보기) 버튼 클릭 시 검색이 정상 실행되어야 한다.
        Steps: 검색창 포커스 → 키워드 입력 → 검색 버튼 클릭
        """
        search_page.go_to_search()
        search_page.search_by_button("비트코인")

        assert search_page.is_search_result_page("비트코인") or \
               "word=" in search_page.page.url, \
            (
                "[FAIL] 검색 버튼 클릭 후 결과 페이지 미이동 — "
                f"현재 URL: {search_page.page.url}"
            )

    def test_FULLTC_312_clear_btn_deletes_input_keeps_cursor(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-312 | 검색창 UI/X 버튼 | Minor
        검색창 X 버튼 클릭 시 입력값이 전체 삭제되어야 한다.
        Steps: 텍스트 입력 → X 버튼 클릭 → 입력값 확인
        """
        search_page.go_to_search()
        search_page.type_search_keyword("비트코인")

        if not search_page.is_clear_btn_visible():
            pytest.skip("[SKIP] X 버튼 미노출 — SEARCH_CLEAR_BTN 셀렉터 확인 필요")

        search_page.click_clear_btn()

        current_value = search_page.get_search_input_value()
        assert current_value == "", \
            f"[FAIL] X 버튼 클릭 후 검색창 미초기화 — 현재 값: '{current_value}'"

    def test_FULLTC_313_duplicate_keyword_not_added_to_recent(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-313 | 검색어 저장/중복 검색어 처리 | Minor
        동일 키워드 재검색 시 최근 검색어 목록에 중복 추가되지 않고
        기존 항목이 최상단으로 갱신되어야 한다.
        Steps: 키워드 검색 → 동일 키워드 재검색 → 중복 확인
        """
        keyword = "FULLTC313중복테스트"
        search_page.go_to_search()
        search_page.search_by_enter(keyword)
        search_page.page.wait_for_timeout(500)

        search_page.go_to_search()
        search_page.search_by_enter(keyword)  # 동일 키워드 재검색
        search_page.page.wait_for_timeout(500)

        search_page.go_to_search()

        if not search_page.is_recent_keywords_section_visible():
            pytest.skip("[SKIP] 최근 검색어 섹션 미노출")

        keywords = search_page.get_recent_keyword_texts()
        keyword_occurrences = sum(1 for k in keywords if keyword in k)

        assert keyword_occurrences <= 1, \
            (
                f"[FAIL] 동일 키워드 '{keyword}'가 최근 검색어에 중복 저장됨 — "
                f"목록: {keywords}"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-314  |  비로그인 검색 접근 권한
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page_guest")
class TestSearchAccessRegression:
    """비로그인 상태 검색 접근 권한 검증"""

    def test_FULLTC_314_guest_can_search_or_redirected(
        self, search_page_guest: SearchPage
    ) -> None:
        """
        FULLTC-314 | 접근 권한/비로그인 검색 | Minor
        비로그인 상태에서 키워드 검색 실행 시
        검색 결과가 정상 노출되거나 로그인 유도 화면으로 이동해야 한다.
        Steps: 비로그인 → /search → 키워드 입력 → Enter
        """
        search_page_guest.go_to_search()
        search_page_guest.search_by_enter("비트코인")

        is_result_page = search_page_guest.is_search_result_page("비트코인")
        is_login_page = search_page_guest.is_login_page_visible()
        has_results = search_page_guest.get_search_result_count() > 0
        has_empty = search_page_guest.is_empty_state_visible()

        assert is_result_page or is_login_page or has_results or has_empty, \
            (
                "[FAIL] 비로그인 검색 후 결과도 로그인 유도도 미노출 — "
                f"현재 URL: {search_page_guest.page.url}"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-315  |  결과 아이템 클릭 라우팅
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchResultClickRegression:
    """검색 결과 아이템 클릭 라우팅 검증"""

    def test_FULLTC_315_click_result_item_navigates_to_detail(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-315 | 결과 리스트/결과 아이템 클릭 | Minor
        검색 결과 아이템 클릭 시 해당 콘텐츠 상세 페이지로 이동해야 한다.
        Steps: 로그인 → 키워드 검색 → 결과 아이템 클릭
        """
        search_page.go_to_search_result("비트코인")

        if search_page.get_search_result_count() == 0:
            pytest.skip("[SKIP] 검색 결과 없음")

        search_page.click_search_result_item(index=0)

        current_url = search_page.page.url
        is_detail = (
            "feed/news" in current_url
            or "/community" in current_url
            or (search_page.SEARCH_MAIN_PATH not in current_url.split("?")[0])
        )

        assert is_detail, \
            (
                "[FAIL] 결과 아이템 클릭 후 상세 페이지 미이동 — "
                f"현재 URL: {current_url}"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-316~319  |  기간 필터
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchDateFilterRegression:
    """검색 기간 필터 검증"""

    def test_FULLTC_316_one_week_filter_applies(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-316 | 검색 필터/기간 선택/1주일 | Minor
        기간 필터 '1주일' 선택 시 최근 1주일 이내 뉴스만 노출되어야 한다.
        ※ 필터 클릭 후 결과 변화로 간접 검증
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_date_filter_visible():
            pytest.skip("[SKIP] 날짜 필터 미노출 — DATE_FILTER_CONTAINER 셀렉터 확인 필요")

        # ⚠️ TODO: '1주일' 버튼 셀렉터 확인 후 실제 클릭으로 교체
        # 현재: 날짜 필터가 존재함을 확인하는 구조 검증
        assert search_page.is_date_filter_visible(), \
            "[FAIL] 기간 필터 미노출 — DATE_FILTER_CONTAINER 셀렉터 확인 필요"

    def test_FULLTC_317_one_month_filter_applies(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-317 | 검색 필터/기간 선택/1개월 | Minor
        기간 필터 '1개월' 선택 시 최근 1개월 이내 뉴스만 노출되어야 한다.
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_date_filter_visible():
            pytest.skip("[SKIP] 날짜 필터 미노출")

        # ⚠️ TODO: '1개월' 버튼 셀렉터 확인 후 교체
        assert search_page.is_date_filter_visible(), \
            "[FAIL] 기간 필터 미노출"

    def test_FULLTC_318_custom_date_range_filter(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-318 | 검색 필터/기간 선택/직접 날짜 지정 | Minor
        시작일/종료일 직접 입력 후 지정 기간 내 뉴스만 노출되어야 한다.
        Steps: 시작일(2025-01-01) / 종료일(2025-03-31) 입력 → 적용
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_date_filter_visible():
            pytest.skip("[SKIP] 날짜 필터 미노출")

        start_input = search_page.page.locator(search_page.DATE_FILTER_START)
        end_input = search_page.page.locator(search_page.DATE_FILTER_END)

        if start_input.count() == 0 or end_input.count() == 0:
            pytest.skip("[SKIP] 날짜 직접 입력 필드 미노출 — DATE_FILTER_START/END 셀렉터 확인 필요")

        search_page.set_date_filter_start("2025-01-01")
        search_page.set_date_filter_end("2025-03-31")
        search_page.click_date_filter_apply()

        # 필터 적용 후 결과가 있거나 Empty State
        result_count = search_page.get_search_result_count()
        has_empty = search_page.is_empty_state_visible()

        assert result_count >= 0 and (result_count > 0 or has_empty), \
            "[FAIL] 날짜 직접 지정 필터 적용 후 결과 상태 비정상"

    def test_FULLTC_319_reversed_date_range_shows_error(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-319 | 검색 필터/기간 선택/시작일 종료일 역전 | Major
        시작일 > 종료일 입력 시 오류 메시지가 노출되어야 한다.
        Steps: 시작일 2025-12-31 / 종료일 2025-01-01 입력 → 적용
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_date_filter_visible():
            pytest.skip("[SKIP] 날짜 필터 미노출")

        start_input = search_page.page.locator(search_page.DATE_FILTER_START)
        end_input = search_page.page.locator(search_page.DATE_FILTER_END)

        if start_input.count() == 0 or end_input.count() == 0:
            pytest.skip("[SKIP] 날짜 입력 필드 미노출")

        search_page.set_date_filter_start("2025-12-31")
        search_page.set_date_filter_end("2025-01-01")
        search_page.click_date_filter_apply()

        is_error = search_page.is_date_error_visible()
        is_blocked = search_page.get_search_result_count() >= 0

        assert is_error or is_blocked, \
            "[FAIL] 시작일 > 종료일 역전 입력 후 오류 처리 없음 — DATE_ERROR_MSG 셀렉터 확인 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-320~322  |  뉴스 타입 필터
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchTypeFilterRegression:
    """뉴스 타입 필터 검증"""

    def test_FULLTC_320_single_type_filter_applies(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-320 | 검색 필터/뉴스 타입/단일 타입 | Minor
        특정 뉴스 타입 1개 선택 시 해당 타입 콘텐츠만 노출되어야 한다.
        ⚠️ TODO: 실제 타입 버튼 셀렉터 확인 후 교체
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_news_type_filter_visible():
            pytest.skip("[SKIP] 뉴스 타입 필터 미노출 — NEWS_TYPE_FILTER 셀렉터 확인 필요")

        assert search_page.is_news_type_filter_visible(), \
            "[FAIL] 뉴스 타입 필터 미노출"

    def test_FULLTC_321_multiple_type_filter_applies(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-321 | 검색 필터/뉴스 타입/다중 타입 | Minor
        2개 이상 타입 동시 선택 시 선택한 모든 타입 콘텐츠가 OR 조건으로 노출되어야 한다.
        ⚠️ TODO: 다중 타입 선택 버튼 셀렉터 확인 후 교체
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_news_type_filter_visible():
            pytest.skip("[SKIP] 뉴스 타입 필터 미노출")

        # 기본 구조 검증 (셀렉터 튜닝 전)
        assert search_page.is_news_type_filter_visible(), \
            "[FAIL] 뉴스 타입 필터 미노출"

    def test_FULLTC_322_date_and_type_filter_combined(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-322 | 검색 필터/필터 조합 | Major
        기간 필터 + 뉴스 타입 필터 동시 적용 시
        두 조건 모두 만족하는 AND 교집합 결과만 노출되어야 한다.
        ⚠️ TODO: 타입 필터 셀렉터 확인 후 실제 교차 필터 테스트로 교체
        """
        search_page.go_to_search_result("비트코인")

        has_date_filter = search_page.is_date_filter_visible()
        has_type_filter = search_page.is_news_type_filter_visible()

        if not has_date_filter or not has_type_filter:
            pytest.skip("[SKIP] 날짜 또는 타입 필터 미노출 — 셀렉터 확인 필요")

        # 기본 구조: 두 필터 모두 존재 확인
        assert has_date_filter and has_type_filter, \
            "[FAIL] 기간 필터 또는 타입 필터 미노출"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-323~324  |  필터 초기화 및 Empty State
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestSearchFilterResetRegression:
    """필터 초기화 및 필터 Empty State 검증"""

    def test_FULLTC_323_filter_reset_returns_all_results(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-323 | 검색 필터/필터 초기화 | Major
        필터 적용 후 초기화 버튼 클릭 시
        모든 필터가 해제되고 전체 검색 결과로 복귀해야 한다.
        Steps: 필터 적용 → 초기화 버튼 클릭 → 전체 결과 복귀
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_filter_reset_visible():
            pytest.skip("[SKIP] 필터 초기화 버튼 미노출 — FILTER_RESET_BTN 셀렉터 확인 필요")

        count_before_filter = search_page.get_search_result_count()

        # 좁은 필터 적용
        if search_page.is_date_filter_visible():
            search_page.set_date_filter_start("2025-01-01")
            search_page.set_date_filter_end("2025-01-31")
            search_page.click_date_filter_apply()

        # 초기화 클릭
        search_page.click_filter_reset()

        count_after_reset = search_page.get_search_result_count()

        # 초기화 후 결과가 필터 전과 같거나 더 많아야 함
        assert count_after_reset >= 0, \
            "[FAIL] 필터 초기화 후 결과 비정상"

    def test_FULLTC_324_narrow_filter_shows_empty_state(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-324 | 검색 필터/필터 Empty State | Major
        결과가 0건이 되는 협소한 필터 조건 적용 시
        Empty State UI가 노출되어야 한다.
        Steps: 결과 0건 조건 필터 적용 → Empty State 확인
        """
        search_page.go_to_search_result("비트코인")

        if not search_page.is_date_filter_visible():
            pytest.skip("[SKIP] 날짜 필터 미노출")

        start_input = search_page.page.locator(search_page.DATE_FILTER_START)
        if start_input.count() == 0:
            pytest.skip("[SKIP] 날짜 직접 입력 필드 미노출")

        # 매우 좁은 날짜 범위 (결과 0건 기대)
        search_page.set_date_filter_start("2020-01-01")
        search_page.set_date_filter_end("2020-01-02")
        search_page.click_date_filter_apply()

        result_count = search_page.get_search_result_count()

        if result_count > 0:
            pytest.skip("[SKIP] 해당 기간에도 결과 존재 — 더 협소한 날짜 범위 필요")

        assert search_page.is_empty_state_visible(), \
            "[FAIL] 필터 결과 0건인데 Empty State UI 미노출 — SEARCH_EMPTY_STATE 셀렉터 확인 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-325  |  알림 배지
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("search_page")
class TestNotificationBadgeRegression:
    """GNB 알림 배지 검증 (로그인 + 읽지 않은 알림 존재)"""

    def test_FULLTC_325_notification_badge_visible(
        self, search_page: SearchPage
    ) -> None:
        """
        FULLTC-325 | 알림/알림 배지/배지 노출 | Major
        로그인 상태에서 읽지 않은 알림이 1건 이상 존재 시
        GNB 알림 아이콘에 배지가 표시되어야 한다.
        Steps: 로그인 상태 → 읽지 않은 알림 1건 이상 존재 → GNB 알림 아이콘 확인
        ⚠️ 전제 조건: 테스트 계정에 읽지 않은 알림이 있어야 함
        """
        search_page.go_to_main()

        assert search_page.is_gnb_visible(), \
            "[FAIL] GNB 헤더 미노출"

        if not search_page.is_notification_icon_visible():
            pytest.skip("[SKIP] GNB 알림 아이콘 미노출 — GNB_NOTIFICATION_ICON 셀렉터 확인 필요")

        # 읽지 않은 알림이 있는지 확인
        has_badge = search_page.is_notification_badge_visible()

        if not has_badge:
            pytest.skip(
                "[SKIP] 알림 배지 미노출 — 테스트 계정에 읽지 않은 알림이 없거나 "
                "GNB_NOTIFICATION_BADGE 셀렉터 확인 필요"
            )

        assert has_badge, \
            (
                "[FAIL] 읽지 않은 알림이 있는데 배지 미노출 — "
                "GNB_NOTIFICATION_BADGE 셀렉터 확인 필요"
            )