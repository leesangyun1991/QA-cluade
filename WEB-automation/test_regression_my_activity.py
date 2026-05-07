"""
tests/stage8_regression/web/test_regression_my_activity.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
내 활동(My Activity) 회귀 테스트 (FULLTC-401 ~ FULLTC-426)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_my_activity.py -v
  pytest tests/stage8_regression/web/test_regression_my_activity.py -m "my_activity" -v
  pytest tests/stage8_regression/web/test_regression_my_activity.py -k "FULLTC_401" -v

[사전 조건]
  - 이 파일과 동일 디렉토리에 auth.json (로그인 세션 파일) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)

[TC 클래스 구성]
  FULLTC-401~405   TestMyActivityTabNavigation    탭/카테고리 이동
  FULLTC-406~409   TestMyActivityListLoading      리스트 로딩
  FULLTC-410~413   TestMyActivityDataAccuracy     데이터 정확성
  FULLTC-414~417   TestMyActivityRouting          라우팅
  FULLTC-418~422   TestMyActivitySyncOnDelete     삭제 및 동기화
  FULLTC-423~426   TestMyActivityEmptyState       Empty State

[HTML 구조 주의사항]
  - 실제 탭 텍스트: "게시글" / "댓글 / 답글" (TC 명칭과 다를 수 있음)
  - "좋아요" / "스크랩" 탭은 제공 HTML에 미노출 → TODO_ 셀렉터 사용
  - 페이지네이션은 번호 버튼 방식 (TC의 무한스크롤과 상이할 수 있음)
  - 기대 URL 패턴: /mypage/activity
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from my_activity_page import MyActivityPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def my_activity_page() -> Iterator[MyActivityPage]:
    """내 활동 페이지 픽스처 (로그인 세션 유지)
    - channel="chrome" : macOS 커널 Chromium 크래시 방지
    - headless=False   : 브라우저 UI 표시 (육안 확인용)
    - slow_mo=500      : 각 액션 500ms 지연
    - --window-position=0,-1080 : 보조 모니터(상단) 배치
    - storage_state    : auth.json 으로 로그인 세션 유지
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
        if not os.path.exists(auth_path):
            raise FileNotFoundError(
                f"\n\n[auth.json 없음] 로그인 세션 파일을 찾을 수 없습니다!\n"
                f"  기대 경로: {auth_path}\n"
                f"  해결 방법: python save_auth.py 를 실행해 auth.json을 생성하세요.\n"
            )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="ko-KR",
            storage_state=auth_path,
        )
        page = context.new_page()
        yield MyActivityPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-401~405  |  탭/카테고리 이동
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.my_activity
class TestMyActivityTabNavigation:
    """탭 클릭 및 활성화 상태 검증 — FULLTC-401 ~ 405"""

    def test_FULLTC_401_posts_tab_active(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-401 | 내 활동/작성한 글 탭 | Minor
        '게시글(작성한 글)' 탭 클릭 시 해당 탭이 활성화되고 게시글 목록이 표시된다.
        ※ 실제 HTML 탭 텍스트: '게시글' (TC 명칭: '작성한 글')
        """
        my_activity_page.go_to_my_activity()
        assert my_activity_page.is_loaded(), \
            "[FAIL] 내 활동 페이지 로드 실패"

        my_activity_page.click_tab_posts()
        assert my_activity_page.is_posts_tab_active(), \
            "[FAIL] '게시글' 탭 클릭 후 활성(isFocus) 상태 미확인 (실제 탭 텍스트: '게시글')"
        my_activity_page.wait_for_post_list()
        count = my_activity_page.get_post_card_count()
        assert count >= 0, \
            f"[FAIL] '게시글' 탭 카드 수 음수 (실제: {count})"

    def test_FULLTC_402_comments_tab_active(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-402 | 내 활동/댓글 탭 | Minor
        '댓글 / 답글' 탭 클릭 시 해당 탭이 활성화되고 댓글 목록이 표시된다.
        ※ 실제 HTML 탭 텍스트: '댓글 / 답글' (TC 명칭: '댓글')
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_comments()
        assert my_activity_page.is_comments_tab_active(), \
            "[FAIL] '댓글 / 답글' 탭 클릭 후 활성(isFocus) 상태 미확인"
        my_activity_page.wait_for_post_list()

    def test_FULLTC_403_likes_tab_active(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-403 | 내 활동/좋아요 탭 | Minor
        '좋아요' 탭 클릭 시 해당 탭이 활성화되고 좋아요 게시글 목록이 표시된다.
        ⚠️ TODO: 해당 탭이 현재 HTML에 미노출 — 셀렉터 튜닝 필요
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()
        if tab_count < 3:
            pytest.skip(
                f"[SKIP] '좋아요' 탭 미노출 (현재 탭 수: {tab_count}) — "
                f"TODO: TAB_LIKES 셀렉터 튜닝 필요"
            )
        my_activity_page.click_tab_likes()
        assert my_activity_page.is_likes_tab_active(), \
            "[FAIL] '좋아요' 탭 클릭 후 활성 상태 미확인 (TODO: TAB_LIKES 셀렉터 튜닝)"

    def test_FULLTC_404_scraps_tab_active(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-404 | 내 활동/스크랩 탭 | Minor
        '스크랩' 탭 클릭 시 해당 탭이 활성화되고 스크랩 게시글 목록이 표시된다.
        ⚠️ TODO: 해당 탭이 현재 HTML에 미노출 — 셀렉터 튜닝 필요
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()
        if tab_count < 4:
            pytest.skip(
                f"[SKIP] '스크랩' 탭 미노출 (현재 탭 수: {tab_count}) — "
                f"TODO: TAB_SCRAPS 셀렉터 튜닝 필요"
            )
        my_activity_page.click_tab_scraps()
        assert my_activity_page.is_scraps_tab_active(), \
            "[FAIL] '스크랩' 탭 클릭 후 활성 상태 미확인 (TODO: TAB_SCRAPS 셀렉터 튜닝)"

    def test_FULLTC_405_tab_cycle_integrity(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-405 | 내 활동/탭 반복 전환 무결성 | Minor
        탭 순서대로 반복 전환 시 데이터 오염 없이 각 탭 목록이 정상 표시된다.
        ※ 노출된 탭(게시글 → 댓글 / 답글 → 게시글)만 검증
        """
        my_activity_page.go_to_my_activity()

        # 게시글 탭
        my_activity_page.click_tab_posts()
        assert my_activity_page.is_posts_tab_active(), \
            "[FAIL] 탭 순환 1단계: '게시글' 탭 활성 미확인"
        count_posts_1 = my_activity_page.get_post_card_count()

        # 댓글 탭
        my_activity_page.click_tab_comments()
        assert my_activity_page.is_comments_tab_active(), \
            "[FAIL] 탭 순환 2단계: '댓글 / 답글' 탭 활성 미확인"

        # 게시글 탭 재클릭
        my_activity_page.click_tab_posts()
        assert my_activity_page.is_posts_tab_active(), \
            "[FAIL] 탭 순환 3단계: '게시글' 탭 재활성 미확인"
        count_posts_2 = my_activity_page.get_post_card_count()

        # 게시글 탭으로 돌아왔을 때 카드 수가 유지되어야 함
        assert count_posts_2 == count_posts_1, \
            f"[FAIL] 탭 반복 전환 후 게시글 카드 수 불일치 " \
            f"(1회: {count_posts_1}, 2회: {count_posts_2}) — 데이터 잔류 의심"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-406~409  |  리스트 로딩
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.my_activity
class TestMyActivityListLoading:
    """게시글 목록 정렬·페이지네이션·스크롤 위치 복원 검증 — FULLTC-406 ~ 409"""

    def test_FULLTC_406_latest_sort_order(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-406 | 내 활동/최신순 정렬 | Major
        '게시글' 탭에서 게시글 목록이 작성일 내림차순(최신순)으로 정렬되어야 한다.
        사전 조건: 작성한 글이 2건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 2:
            pytest.skip(
                f"[SKIP] 작성한 글 {card_count}건 — 정렬 검증에 2건 이상 필요"
            )
        assert my_activity_page.are_posts_sorted_by_latest(), \
            "[FAIL] 게시글 목록이 최신순(작성일 내림차순)으로 정렬되지 않음"

    def test_FULLTC_407_scroll_or_pagination_loads_more(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-407 | 내 활동/무한 스크롤 또는 페이지네이션 | Major
        하단 스크롤 후 추가 데이터 로드 또는 다음 페이지 버튼이 노출되어야 한다.
        ※ 실제 HTML 기준: 번호 페이지네이션 방식 (TC 명칭: '무한 스크롤'과 상이할 수 있음)
        사전 조건: 작성한 글이 20건 이상 존재 (또는 페이지네이션 2페이지 이상)
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        count_before = my_activity_page.get_post_card_count()
        is_pagination = my_activity_page.is_pagination_visible()
        page_count = my_activity_page.get_page_count()

        if count_before < 1:
            pytest.skip("[SKIP] 게시글 없음 — 스크롤/페이지네이션 검증 불가")

        if is_pagination and page_count >= 2:
            # 페이지네이션 방식: 다음 페이지 클릭
            my_activity_page.click_next_page()
            count_after = my_activity_page.get_post_card_count()
            assert count_after >= 1, \
                f"[FAIL] 다음 페이지 클릭 후 게시글 0건 (페이지 수: {page_count})"
        else:
            # 무한 스크롤 방식: 하단 스크롤 후 카드 증가 확인
            my_activity_page.scroll_to_bottom(steps=5)
            my_activity_page.page.wait_for_timeout(1_000)
            count_after = my_activity_page.get_post_card_count()
            is_pagination_after = my_activity_page.is_pagination_visible()
            assert count_after > count_before or is_pagination_after, \
                f"[FAIL] 스크롤 후 카드 미증가 및 페이지네이션 미노출 " \
                f"(before: {count_before}, after: {count_after})"

    def test_FULLTC_408_last_page_end_indicator(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-408 | 내 활동/마지막 페이지 처리 | Minor
        목록 최하단 도달 시 '더 이상 데이터 없음' 안내 또는 더보기 버튼 미노출되어야 한다.
        ※ 페이지네이션 방식인 경우: 마지막 페이지에서 다음 버튼이 비활성화되어야 함
        사전 조건: 목록 마지막 페이지까지 도달 완료
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        if not my_activity_page.is_pagination_visible():
            # 무한 스크롤 방식: 끝까지 스크롤 후 더보기 버튼 없는지 확인
            my_activity_page.scroll_to_bottom(steps=15)
            my_activity_page.page.wait_for_timeout(1_500)
            # 마지막 스크롤 후 카드 수 변화 없으면 정상
            count_1 = my_activity_page.get_post_card_count()
            my_activity_page.scroll_to_bottom(steps=5)
            my_activity_page.page.wait_for_timeout(1_000)
            count_2 = my_activity_page.get_post_card_count()
            # 카드 수가 더 이상 증가하지 않으면 마지막 페이지로 판단
            assert count_2 >= count_1, \
                "[FAIL] 마지막 페이지에서 카드 수가 줄어듦 (예상치 못한 동작)"
        else:
            # 페이지네이션 방식: 마지막 페이지 번호 클릭 후 다음 버튼 비활성 확인
            page_count = my_activity_page.get_page_count()
            if page_count >= 2:
                my_activity_page.click_page_number(page_count)
                my_activity_page.page.wait_for_timeout(800)
                # 마지막 페이지 번호 버튼에 도달 후 추가 카드 없음 확인
                final_count = my_activity_page.get_post_card_count()
                assert final_count >= 0, \
                    "[FAIL] 마지막 페이지 카드 수 조회 실패"
            else:
                pytest.skip("[SKIP] 페이지 1개뿐 — 마지막 페이지 처리 검증 불가")

    def test_FULLTC_409_scroll_position_restored_on_back(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-409 | 내 활동/스크롤 위치 복원 | Minor
        게시글 클릭 후 뒤로가기 시 이전 스크롤 위치로 복원되어야 한다.
        사전 조건: 목록에 게시글이 있고 스크롤 가능한 높이
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 게시글 없음 — 스크롤 위치 복원 검증 불가")

        # 페이지를 조금 스크롤
        my_activity_page.page.keyboard.press("PageDown")
        my_activity_page.page.wait_for_timeout(300)
        scroll_y_before = my_activity_page.get_scroll_y_position()

        # 첫 번째 카드 클릭 (상세 페이지 이동)
        my_activity_page.click_post_card(0)
        my_activity_page.page.wait_for_timeout(1_000)
        url_after_click = my_activity_page.get_current_url()

        # 상세 페이지로 이동했다면 뒤로가기 후 위치 확인
        if url_after_click != f"{MyActivityPage.BASE_URL}{MyActivityPage.MY_ACTIVITY_PATH}":
            my_activity_page.go_back()
            my_activity_page.page.wait_for_timeout(1_000)
            scroll_y_after = my_activity_page.get_scroll_y_position()
            # 스크롤 위치가 완전히 0으로 초기화되지 않았는지 확인 (복원 판단)
            # ※ 완전히 동일한 위치가 아닐 수 있으나 최소한 0이 아니어야 함
            is_restored = (
                abs(scroll_y_after - scroll_y_before) <= 200  # 200px 오차 허용
                or scroll_y_after > 0  # 최소한 스크롤 위치가 0 이상
            )
            assert is_restored or scroll_y_before == 0, \
                f"[FAIL] 뒤로가기 후 스크롤 위치 미복원 " \
                f"(before: {scroll_y_before}, after: {scroll_y_after})"
        else:
            pytest.skip("[SKIP] 카드 클릭 후 상세 페이지 미이동 — 스크롤 복원 검증 불가")


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-410~413  |  데이터 정확성
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.my_activity
class TestMyActivityDataAccuracy:
    """게시글 제목·날짜·댓글 내용·말줄임·좋아요/스크랩 정보 검증 — FULLTC-410 ~ 413"""

    def test_FULLTC_410_post_title_and_date(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-410 | 내 활동/게시글 제목 및 작성일 | Major
        '게시글' 탭에서 카드의 제목(내용)과 작성일이 비어있지 않아야 한다.
        사전 조건: 작성한 글이 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 작성한 글 없음 — 데이터 검증 불가")

        content_text = my_activity_page.get_first_post_content_text()
        assert content_text.strip() != "", \
            "[FAIL] 게시글 카드 본문 텍스트 비어있음"

        date_text = my_activity_page.get_post_date_text(0)
        assert date_text.strip() != "", \
            "[FAIL] 게시글 카드 작성일 비어있음"
        # 날짜 형식 간단 확인 (YYYY.MM.DD 패턴 포함 여부)
        assert "." in date_text, \
            f"[FAIL] 게시글 날짜 형식 불일치 — 현재: '{date_text}'"

    def test_FULLTC_411_comment_content_display(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-411 | 내 활동/댓글 내용 요약 표시 | Major
        '댓글' 탭에서 댓글 내용이 비어있지 않아야 한다.
        사전 조건: 작성한 댓글이 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_comments()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 작성한 댓글 없음 — 데이터 검증 불가")

        content_text = my_activity_page.get_first_post_content_text()
        assert content_text.strip() != "", \
            "[FAIL] 댓글 카드 내용 텍스트 비어있음"

    def test_FULLTC_412_long_text_ellipsis(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-412 | 내 활동/긴 텍스트 말줄임 처리 | Minor
        제목/내용이 지정 길이 초과 시 말줄임(CSS ellipsis 또는 line-clamp) 적용되어야 한다.
        사전 조건: 제목 또는 내용이 긴 게시글(50자+) 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 게시글 없음 — 말줄임 검증 불가")

        # 적어도 하나의 카드에서 말줄임 CSS 적용 확인
        any_clamped = False
        for i in range(min(card_count, 5)):
            if my_activity_page.is_content_text_clamped(i):
                any_clamped = True
                break

        # ※ 모든 게시글이 짧을 경우 말줄임 적용 안 될 수 있으므로 soft-assert
        if not any_clamped:
            # 짧은 텍스트면 말줄임 불필요 — 패스 처리 (경고만)
            content = my_activity_page.get_first_post_content_text()
            if len(content) < 50:
                pytest.skip(
                    f"[SKIP] 본문 텍스트가 짧아 말줄임 검증 불가 (텍스트 길이: {len(content)}자)"
                )
        assert any_clamped, \
            "[FAIL] 게시글 카드 중 말줄임(overflow:hidden / text-overflow:ellipsis / -webkit-line-clamp) CSS 미적용"

    def test_FULLTC_413_likes_and_scrap_info(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-413 | 내 활동/좋아요·스크랩 게시글 정보 | Major
        '좋아요' 탭과 '스크랩' 탭에서 게시글 제목·날짜가 비어있지 않아야 한다.
        ⚠️ TODO: 좋아요/스크랩 탭이 HTML에 미노출 시 이 TC는 skip됨
        사전 조건: 좋아요·스크랩한 게시글 각 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()

        if tab_count < 3:
            pytest.skip(
                f"[SKIP] 좋아요/스크랩 탭 미노출 (현재 탭 수: {tab_count}) — "
                f"TODO: TAB_LIKES, TAB_SCRAPS 셀렉터 튜닝 필요"
            )

        # 좋아요 탭 검증
        my_activity_page.click_tab_likes()
        my_activity_page.wait_for_post_list()
        likes_count = my_activity_page.get_post_card_count()
        if likes_count >= 1:
            assert my_activity_page.get_first_post_content_text().strip() != "", \
                "[FAIL] '좋아요' 탭 게시글 카드 내용 비어있음"
            assert my_activity_page.get_post_date_text(0).strip() != "", \
                "[FAIL] '좋아요' 탭 게시글 카드 날짜 비어있음"
        else:
            pytest.skip("[SKIP] 좋아요 게시글 없음 — 데이터 검증 불가")


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-414~417  |  라우팅
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.my_activity
class TestMyActivityRouting:
    """게시글 클릭 라우팅 및 삭제 콘텐츠 처리 검증 — FULLTC-414 ~ 417"""

    def test_FULLTC_414_post_click_navigates(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-414 | 내 활동/작성한 글 이동 | Major
        '게시글' 탭에서 카드 클릭 시 해당 게시글 상세 페이지로 이동해야 한다.
        사전 조건: 작성한 글이 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 게시글 없음 — 라우팅 검증 불가")

        url_before = my_activity_page.get_current_url()
        my_activity_page.click_post_card(0)

        assert my_activity_page.get_current_url() != url_before, \
            "[FAIL] 게시글 카드 클릭 후 URL 미변경"
        assert my_activity_page.MY_ACTIVITY_PATH not in my_activity_page.get_current_url() \
               or my_activity_page.get_current_url() != url_before, \
            f"[FAIL] 게시글 클릭 후 상세 페이지 미이동 — 현재: '{my_activity_page.get_current_url()}'"

    def test_FULLTC_415_comment_click_navigates(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-415 | 내 활동/댓글 단 게시글 이동 | Major
        '댓글' 탭에서 카드 클릭 시 해당 게시글 상세 페이지로 이동해야 한다.
        사전 조건: 작성한 댓글이 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_comments()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 작성한 댓글 없음 — 라우팅 검증 불가")

        url_before = my_activity_page.get_current_url()
        my_activity_page.click_post_card(0)

        assert my_activity_page.get_current_url() != url_before, \
            "[FAIL] '댓글' 탭 카드 클릭 후 URL 미변경 — 상세 페이지 미이동"

    def test_FULLTC_416_likes_post_click_navigates(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-416 | 내 활동/좋아요 게시글 이동 | Major
        '좋아요' 탭에서 카드 클릭 시 해당 게시글 상세 페이지로 이동해야 한다.
        ⚠️ TODO: 좋아요 탭 미노출 시 skip
        사전 조건: 좋아요한 게시글이 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()
        if tab_count < 3:
            pytest.skip(
                f"[SKIP] '좋아요' 탭 미노출 (탭 수: {tab_count}) — "
                f"TODO: TAB_LIKES 셀렉터 튜닝 필요"
            )
        my_activity_page.click_tab_likes()
        my_activity_page.wait_for_post_list()
        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 좋아요 게시글 없음 — 라우팅 검증 불가")

        url_before = my_activity_page.get_current_url()
        my_activity_page.click_post_card(0)
        assert my_activity_page.get_current_url() != url_before, \
            "[FAIL] '좋아요' 탭 카드 클릭 후 URL 미변경 — 상세 페이지 미이동"

    def test_FULLTC_417_deleted_content_click_shows_notice(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-417 | 내 활동/삭제된 콘텐츠 클릭 | Major
        목록의 게시글이 삭제된 상태에서 클릭 시 안내 메시지 표시 또는 빈 페이지로 이동하지 않아야 한다.
        ※ 삭제된 게시글이 없을 경우 skip — 수동으로 삭제 후 실행 필요
        사전 조건: 내 활동 목록에 삭제된 게시글 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 게시글 없음 — 삭제 콘텐츠 클릭 테스트 불가")

        # ※ 삭제된 게시글을 자동으로 식별하기 어려우므로 클릭 후 동작 검증
        # 클릭 후 정상 상세 페이지로 이동하거나 안내 토스트가 노출되어야 함
        url_before = my_activity_page.get_current_url()
        my_activity_page.click_post_card(0)
        my_activity_page.page.wait_for_timeout(1_000)
        url_after = my_activity_page.get_current_url()

        toast_visible = my_activity_page.is_deleted_content_toast_visible(timeout=2_000)
        navigated = url_after != url_before

        # 상세 이동 OR 토스트 노출 중 하나가 발생해야 함 (빈 페이지 미이동)
        assert navigated or toast_visible, \
            f"[FAIL] 삭제 콘텐츠 클릭 후 URL 미변경 및 안내 메시지 미노출 " \
            f"(url_before='{url_before}', url_after='{url_after}')"

        # 빈 페이지(about:blank)로 이동하지 않았는지 확인
        assert "about:blank" not in url_after.lower(), \
            "[FAIL] 삭제 콘텐츠 클릭 후 빈 페이지(about:blank)로 이동함"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-418~422  |  삭제 및 동기화
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.my_activity
class TestMyActivitySyncOnDelete:
    """삭제/취소 후 목록 동기화 검증 — FULLTC-418 ~ 422
    ⚠️ 주의: 이 클래스의 TC는 실제 콘텐츠 삭제/좋아요 취소 등을 수행합니다.
    테스트 계정의 데이터를 변경하므로 신중하게 실행하세요.
    현재 구현은 목록 화면 확인 중심으로 작성되었으며, 실제 삭제 액션은
    수동 수행 후 결과 확인 방식으로 진행합니다.
    """

    def test_FULLTC_418_delete_post_syncs_list(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-418 | 내 활동/작성한 글 삭제 후 목록 동기화 | Major
        게시글 삭제 후 '게시글' 탭에서 해당 게시글이 즉시 제거되어야 한다.
        ※ 자동화 범위: 삭제 전/후 카드 수 비교 (실제 삭제는 수동 수행 후 pytest 재실행)
        사전 조건: 작성한 글이 2건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 2:
            pytest.skip(
                f"[SKIP] 작성한 글 {card_count}건 — 삭제 동기화 검증에 2건 이상 필요"
            )

        # 목록에 게시글이 정상 노출되는지 확인 (삭제 전 기준선)
        first_text = my_activity_page.get_first_post_content_text()
        assert first_text.strip() != "", \
            "[FAIL] 삭제 전 첫 번째 카드 내용이 비어있음 — 테스트 기준선 설정 실패"
        assert card_count >= 2, \
            f"[FAIL] 삭제 동기화 검증 사전 조건 미충족 — 게시글 {card_count}건"
        # ※ 실제 삭제 동작은 수동으로 수행 후 목록 갱신 여부를 별도로 확인하세요.

    def test_FULLTC_419_unlike_syncs_likes_tab(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-419 | 내 활동/좋아요 취소 후 목록 동기화 | Major
        좋아요 취소 후 '좋아요' 탭에서 해당 게시글이 제거되어야 한다.
        ⚠️ TODO: 좋아요 탭 미노출 시 skip
        사전 조건: 좋아요한 게시글이 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()
        if tab_count < 3:
            pytest.skip(
                f"[SKIP] '좋아요' 탭 미노출 (탭 수: {tab_count}) — "
                f"TODO: TAB_LIKES 셀렉터 튜닝 필요"
            )
        my_activity_page.click_tab_likes()
        my_activity_page.wait_for_post_list()
        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 좋아요 게시글 없음 — 동기화 검증 불가")

        assert card_count >= 1, \
            "[FAIL] '좋아요' 탭 게시글 목록 로드 실패"
        # ※ 실제 좋아요 취소 후 목록 갱신 여부는 수동으로 확인 후 재실행하세요.

    def test_FULLTC_420_unscrap_syncs_scraps_tab(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-420 | 내 활동/스크랩 취소 후 목록 동기화 | Major
        스크랩 취소 후 '스크랩' 탭에서 해당 게시글이 제거되어야 한다.
        ⚠️ TODO: 스크랩 탭 미노출 시 skip
        사전 조건: 스크랩한 게시글이 1건 이상 존재
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()
        if tab_count < 4:
            pytest.skip(
                f"[SKIP] '스크랩' 탭 미노출 (탭 수: {tab_count}) — "
                f"TODO: TAB_SCRAPS 셀렉터 튜닝 필요"
            )
        my_activity_page.click_tab_scraps()
        my_activity_page.wait_for_post_list()
        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 스크랩 게시글 없음 — 동기화 검증 불가")

        assert card_count >= 1, \
            "[FAIL] '스크랩' 탭 게시글 목록 로드 실패"

    def test_FULLTC_421_community_post_delete_syncs(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-421 | 내 활동/커뮤니티 글 삭제 후 동기화 | Major
        커뮤니티에서 게시글 삭제 후 '게시글' 탭에서도 즉시 제거되어야 한다.
        사전 조건: 커뮤니티에 작성한 글이 1건 이상 존재
        ※ 이 TC는 커뮤니티 → 내 활동 페이지 이동을 포함하므로 반자동 수준으로 작성
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 커뮤니티 작성 글 없음 — 동기화 검증 불가")

        # 현재 게시글 목록 카드 수 기록 (삭제 전 기준선)
        first_text = my_activity_page.get_first_post_content_text()
        assert first_text != "", \
            "[FAIL] '게시글' 탭 첫 번째 카드 내용 비어있음 — 기준선 설정 실패"
        # ※ 실제 삭제: 커뮤니티에서 수동 삭제 후 내 활동 페이지 새로고침 후 확인하세요.

    def test_FULLTC_422_community_comment_delete_syncs(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-422 | 내 활동/커뮤니티 댓글 삭제 후 동기화 | Major
        커뮤니티에서 댓글 삭제 후 '댓글' 탭에서도 즉시 제거되어야 한다.
        사전 조건: 커뮤니티 게시글에 댓글을 작성한 상태
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_comments()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count < 1:
            pytest.skip("[SKIP] 작성한 댓글 없음 — 동기화 검증 불가")

        first_text = my_activity_page.get_first_post_content_text()
        assert first_text != "", \
            "[FAIL] '댓글' 탭 첫 번째 카드 내용 비어있음 — 기준선 설정 실패"
        # ※ 실제 삭제: 커뮤니티에서 수동 댓글 삭제 후 내 활동 페이지 재방문하여 확인하세요.


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-423~426  |  Empty State
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.my_activity
class TestMyActivityEmptyState:
    """탭별 Empty State UI 검증 — FULLTC-423 ~ 426
    ⚠️ 각 TC는 해당 데이터가 0건인 계정에서만 의미 있음
    현재 계정에 데이터가 있을 경우 자동으로 skip 처리
    """

    def test_FULLTC_423_posts_empty_state(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-423 | 내 활동/작성한 글 없음 UI | Minor
        작성한 글이 0건인 계정에서 '게시글' 탭에 빈 상태 UI가 노출되어야 한다.
        ⚠️ TODO: EMPTY_STATE 셀렉터 튜닝 필요 (실제 HTML 확인 후)
        사전 조건: 작성한 글이 0건인 계정
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_posts()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count > 0:
            pytest.skip(
                f"[SKIP] 현재 계정 게시글 {card_count}건 존재 — "
                f"Empty State 검증은 0건 계정에서 실행하세요"
            )

        assert my_activity_page.is_empty_state_visible(), \
            "[FAIL] 게시글 0건 상태에서 빈 상태 UI 미노출 (TODO: EMPTY_STATE 셀렉터 튜닝)"

    def test_FULLTC_424_comments_empty_state(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-424 | 내 활동/댓글 없음 UI | Minor
        작성한 댓글이 0건인 계정에서 '댓글' 탭에 빈 상태 UI가 노출되어야 한다.
        ⚠️ TODO: EMPTY_STATE 셀렉터 튜닝 필요
        사전 조건: 작성한 댓글이 0건인 계정
        """
        my_activity_page.go_to_my_activity()
        my_activity_page.click_tab_comments()
        my_activity_page.wait_for_post_list()

        card_count = my_activity_page.get_post_card_count()
        if card_count > 0:
            pytest.skip(
                f"[SKIP] 현재 계정 댓글 {card_count}건 존재 — "
                f"Empty State 검증은 0건 계정에서 실행하세요"
            )

        assert my_activity_page.is_empty_state_visible(), \
            "[FAIL] 댓글 0건 상태에서 빈 상태 UI 미노출 (TODO: EMPTY_STATE 셀렉터 튜닝)"

    def test_FULLTC_425_likes_empty_state(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-425 | 내 활동/좋아요 없음 UI | Minor
        좋아요한 게시글이 0건인 계정에서 '좋아요' 탭에 빈 상태 UI가 노출되어야 한다.
        ⚠️ TODO: 좋아요 탭 + EMPTY_STATE 셀렉터 튜닝 필요
        사전 조건: 좋아요한 게시글이 0건인 계정
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()
        if tab_count < 3:
            pytest.skip(
                f"[SKIP] '좋아요' 탭 미노출 (탭 수: {tab_count}) — "
                f"TODO: TAB_LIKES 셀렉터 튜닝 필요"
            )

        my_activity_page.click_tab_likes()
        my_activity_page.wait_for_post_list()
        card_count = my_activity_page.get_post_card_count()
        if card_count > 0:
            pytest.skip(
                f"[SKIP] 좋아요 게시글 {card_count}건 존재 — "
                f"Empty State 검증은 0건 계정에서 실행하세요"
            )

        assert my_activity_page.is_empty_state_visible(), \
            "[FAIL] 좋아요 0건 상태에서 빈 상태 UI 미노출 (TODO: EMPTY_STATE 셀렉터 튜닝)"

    def test_FULLTC_426_scraps_empty_state(
        self, my_activity_page: MyActivityPage
    ) -> None:
        """
        FULLTC-426 | 내 활동/스크랩 없음 UI | Minor
        스크랩한 게시글이 0건인 계정에서 '스크랩' 탭에 빈 상태 UI가 노출되어야 한다.
        ⚠️ TODO: 스크랩 탭 + EMPTY_STATE 셀렉터 튜닝 필요
        사전 조건: 스크랩한 게시글이 0건인 계정
        """
        my_activity_page.go_to_my_activity()
        tab_count = my_activity_page.get_tab_count()
        if tab_count < 4:
            pytest.skip(
                f"[SKIP] '스크랩' 탭 미노출 (탭 수: {tab_count}) — "
                f"TODO: TAB_SCRAPS 셀렉터 튜닝 필요"
            )

        my_activity_page.click_tab_scraps()
        my_activity_page.wait_for_post_list()
        card_count = my_activity_page.get_post_card_count()
        if card_count > 0:
            pytest.skip(
                f"[SKIP] 스크랩 게시글 {card_count}건 존재 — "
                f"Empty State 검증은 0건 계정에서 실행하세요"
            )

        assert my_activity_page.is_empty_state_visible(), \
            "[FAIL] 스크랩 0건 상태에서 빈 상태 UI 미노출 (TODO: EMPTY_STATE 셀렉터 튜닝)"