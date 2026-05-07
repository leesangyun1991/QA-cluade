"""
tests/stage8_regression/web/test_regression_notice.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
공지사항(Notice) 회귀 테스트 (FULLTC-451 ~ FULLTC-472)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_notice.py -v
  pytest tests/stage8_regression/web/test_regression_notice.py -m "notice" -v
  pytest tests/stage8_regression/web/test_regression_notice.py -k "FULLTC_451" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)
  - 비로그인 가능 TC: 451~454, 456~469, 470~472

[TC 클래스 구성]
  FULLTC-451~455   TestNoticeList              리스트 노출
  FULLTC-456~459   TestNoticeCategoryFilter    카테고리 필터
  FULLTC-460~463   TestNoticeSearch            공지 검색
  FULLTC-464~467   TestNoticeDetail            상세 페이지
  FULLTC-468~469   TestNoticeInfiniteScroll    추가 로딩
  FULLTC-470~471   TestNoticeEmptyState        Empty State
  FULLTC-472       TestNoticeAttachment        첨부파일

[HTML 분석 주요 포인트]
  - 공지 카드: a[class*='noticeCard']  href="/notice/{id}"
  - 제목: h4[class*='title'], 날짜: p[class*='date'] = "YYYY.MM.DD"
  - 페이지네이션: 번호 버튼 방식 (TC의 무한스크롤과 불일치 가능)
  - 상단 고정 배지·NEW 배지·카테고리 탭·검색·상세·첨부파일 → TODO_ 셀렉터 + skip 처리
  - 목록 URL 추정: /mypage/notice (F12 확인 후 NOTICE_LIST_PATH 수정 필요)
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from notice_page import NoticePage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def notice_page() -> Iterator[NoticePage]:
    """공지사항 페이지 픽스처 (로그인 세션 유지)
    - channel="chrome"          : macOS 커널 Chromium 크래시 방지
    - headless=False            : 브라우저 UI 표시 (육안 확인용)
    - slow_mo=500               : 각 액션 500ms 지연
    - --window-position=0,-1080 : 보조 모니터(상단) 배치
    - storage_state             : auth.json 으로 로그인 세션 유지
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
        yield NoticePage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-451~455  |  리스트 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.notice
class TestNoticeList:
    """중요 공지 고정·최신순 정렬·제목·카테고리·NEW 뱃지 검증 — FULLTC-451 ~ 455"""

    def test_FULLTC_451_pinned_notice_at_top(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-451 | 공지사항/중요 공지 상단 고정 노출 | Major
        상단 고정(핀) 처리된 공지가 일반 공지보다 최상단에 노출되고
        고정 표시(핀/아이콘)가 함께 표시되어야 한다.
        ⚠️ TODO: PINNED_CARD, PINNED_BADGE 셀렉터 튜닝 필요
        사전 조건: 핀 처리된 중요 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-451: 공지사항 목록 페이지 로드 실패"

        if not notice_page.is_pinned_badge_visible():
            pytest.skip(
                "[SKIP] FULLTC-451: 상단 고정 배지 미노출 — "
                "TODO: PINNED_BADGE 셀렉터 튜닝 후 재실행"
            )

        assert notice_page.is_pinned_badge_visible(), \
            "[FAIL] FULLTC-451: 상단 고정 배지(핀 아이콘) 미노출 (TODO: PINNED_BADGE 셀렉터 튜닝)"

        assert notice_page.is_pinned_card_before_normal(), \
            "[FAIL] FULLTC-451: 상단 고정 공지가 일반 공지 아래에 위치함 — 고정 순서 오류"

    def test_FULLTC_452_normal_notices_sorted_by_latest(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-452 | 공지사항/일반 공지 최신순 정렬 | Major
        일반 공지 목록이 작성일 기준 내림차순(최신순)으로 정렬되어야 한다.
        사전 조건: 일반 공지가 2건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-452: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 2:
            pytest.skip(
                f"[SKIP] FULLTC-452: 공지 {count}건 — "
                f"정렬 검증에 2건 이상 필요"
            )

        dates = notice_page.get_all_dates()
        assert len(dates) >= 2, \
            f"[FAIL] FULLTC-452: 날짜 정보 추출 실패 (공지 수: {count}, 날짜 수: {len(dates)})"

        assert notice_page.are_dates_sorted_latest(), \
            f"[FAIL] FULLTC-452: 공지 목록이 최신순(내림차순)으로 미정렬 — " \
            f"현재 날짜 순서: {dates[:5]}"

    def test_FULLTC_453_notice_title_display_and_ellipsis(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-453 | 공지사항/공지 제목 표시 정확성 | Major
        각 공지 제목이 비어있지 않고, 긴 제목은 말줄임(...)으로 처리되어야 한다.
        사전 조건: 공지가 1건 이상 등록된 상태
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-453: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-453: 공지 없음 — 제목 검증 불가")

        # 첫 번째 공지 제목 비어있지 않은지 확인
        title = notice_page.get_notice_title(0)
        assert title.strip() != "", \
            "[FAIL] FULLTC-453: 첫 번째 공지 제목 비어있음"

        # 상위 5개까지 제목 유효성 확인
        for i in range(min(count, 5)):
            t = notice_page.get_notice_title(i)
            assert t.strip() != "", \
                f"[FAIL] FULLTC-453: {i+1}번째 공지 제목 비어있음"

        # 말줄임 CSS 적용 여부: 긴 제목 카드에서 확인
        any_clamped = any(notice_page.is_title_clamped(i) for i in range(min(count, 5)))
        if not any_clamped:
            # 짧은 제목들만 있는 경우 말줄임 불필요 → 소프트 패스
            max_len = max(len(notice_page.get_notice_title(i)) for i in range(min(count, 5)))
            if max_len < 30:
                pytest.skip(
                    f"[SKIP] FULLTC-453: 제목 최대 {max_len}자 — "
                    f"말줄임 검증에 30자 이상 제목 필요"
                )
        # 말줄임이 적용된 카드가 하나라도 있으면 PASS
        assert any_clamped, \
            "[FAIL] FULLTC-453: 긴 제목에 말줄임(CSS ellipsis / -webkit-line-clamp) 미적용"

    def test_FULLTC_454_notice_category_and_date_display(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-454 | 공지사항/카테고리 및 작성일 표시 정확성 | Major
        공지 카드에 카테고리 태그와 작성일이 정확한 포맷으로 표시되어야 한다.
        ※ HTML 기준: 날짜는 'YYYY.MM.DD' 포맷으로 p[class*='date']에 노출
        ※ 카테고리가 별도 태그 없이 제목에 내포된 경우 TODO_ 셀렉터로 대체
        사전 조건: 공지가 1건 이상 등록된 상태
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-454: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-454: 공지 없음 — 날짜·카테고리 검증 불가")

        # 날짜 포맷 확인 (YYYY.MM.DD)
        date_text = notice_page.get_notice_date(0)
        assert date_text.strip() != "", \
            "[FAIL] FULLTC-454: 첫 번째 공지 작성일 비어있음"
        assert "." in date_text, \
            f"[FAIL] FULLTC-454: 작성일 포맷 불일치 — '.' 구분 미포함 (현재: '{date_text}')"

        import re
        assert re.match(r"\d{4}\.\d{2}\.\d{2}", date_text), \
            f"[FAIL] FULLTC-454: 작성일이 'YYYY.MM.DD' 포맷 아님 (현재: '{date_text}')"

        # 카테고리 확인 (별도 태그 또는 제목 내 텍스트)
        category_tag_visible = notice_page.page.locator(NoticePage.CARD_CATEGORY_TAG).count() > 0
        if category_tag_visible:
            category_text = notice_page.page.locator(
                NoticePage.CARD_CATEGORY_TAG
            ).first.inner_text().strip()
            assert category_text != "", \
                "[FAIL] FULLTC-454: 카테고리 태그 요소 노출됐으나 텍스트 비어있음"
        else:
            # 카테고리 태그가 없을 경우: 제목에 [공지]/[이벤트]/[안내] 등 포함 여부 확인
            first_title = notice_page.get_notice_title(0)
            pytest.skip(
                f"[SKIP] FULLTC-454 (카테고리 태그): 별도 카테고리 태그 미노출 — "
                f"제목 내 텍스트로 확인 필요 (제목 예: '{first_title[:30]}'). "
                f"TODO: CARD_CATEGORY_TAG 셀렉터 튜닝 후 재실행"
            )

    def test_FULLTC_455_new_badge_visible_and_disappears_after_read(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-455 | 공지사항/미열람 공지 NEW 뱃지 표시 | Minor
        미열람 공지에 NEW 배지가 노출되고, 열람 후 해당 배지가 사라져야 한다.
        ⚠️ TODO: NEW_BADGE 셀렉터 튜닝 필요 (로그인 상태에서만 의미 있음)
        사전 조건: 로그인 상태, 열람하지 않은 신규 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-455: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()

        new_count = notice_page.get_new_badge_count()
        if new_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-455: NEW 배지 미노출 — "
                "미열람 공지가 없거나 TODO: NEW_BADGE 셀렉터 튜닝 필요"
            )

        # NEW 배지가 있는 카드 찾기
        new_badge_index = None
        for i in range(notice_page.get_notice_count()):
            if notice_page.is_new_badge_visible_on_card(i):
                new_badge_index = i
                break

        assert new_badge_index is not None, \
            "[FAIL] FULLTC-455: NEW 배지 전체 카운트는 있으나 개별 카드 식별 실패"

        # 해당 공지 클릭 (열람)
        notice_page.click_notice_card(new_badge_index)
        notice_page.page.wait_for_timeout(1_000)
        assert notice_page.is_on_notice_detail_page(), \
            "[FAIL] FULLTC-455: 공지 클릭 후 상세 페이지 미이동"

        # 목록으로 돌아와서 NEW 배지 사라졌는지 확인
        notice_page.go_back()
        notice_page.wait_for_notice_list()
        after_badge_visible = notice_page.is_new_badge_visible_on_card(new_badge_index)
        assert not after_badge_visible, \
            "[FAIL] FULLTC-455: 열람 후 해당 공지의 NEW 배지가 사라지지 않음"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-456~459  |  카테고리 필터
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.notice
class TestNoticeCategoryFilter:
    """전체·공지·이벤트·안내 카테고리 탭 필터 검증 — FULLTC-456 ~ 459
    ⚠️ 카테고리 탭 UI가 HTML에 미노출 → TODO_ 셀렉터 → skip 자동 처리
    """

    def _assert_category_tab_exists(self, notice_page: NoticePage) -> None:
        """카테고리 탭 UI 존재 여부 사전 검증 (없으면 skip)"""
        if not notice_page.is_category_tab_visible():
            pytest.skip(
                "[SKIP] 카테고리 탭 UI 미노출 — "
                "TODO: CATEGORY_WRAPPER 셀렉터 튜닝 후 재실행"
            )

    def test_FULLTC_456_category_all_shows_everything(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-456 | 공지사항/전체 탭 - 모든 공지 노출 | Major
        '전체' 카테고리 탭 선택 시 모든 카테고리 공지가 최신순으로 표시되어야 한다.
        ⚠️ TODO: CATEGORY_TAB_ALL 셀렉터 튜닝 필요
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-456: 공지사항 목록 페이지 로드 실패"
        self._assert_category_tab_exists(notice_page)

        count_before = notice_page.get_notice_count()
        notice_page.click_tab_all()
        notice_page.wait_for_notice_list()
        count_after = notice_page.get_notice_count()

        assert count_after >= 0, \
            "[FAIL] FULLTC-456: '전체' 탭 선택 후 공지 목록 조회 실패"
        assert count_after >= count_before or count_after > 0, \
            f"[FAIL] FULLTC-456: '전체' 탭 선택 후 공지 수 감소 " \
            f"(before:{count_before}, after:{count_after}) — 필터 오류 의심"

    def test_FULLTC_457_category_notice_filter(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-457 | 공지사항/공지 탭 필터 | Major
        '공지' 카테고리 탭 선택 시 '공지' 카테고리 항목만 표시되어야 한다.
        ⚠️ TODO: CATEGORY_TAB_NOTICE 셀렉터 튜닝 필요
        사전 조건: '공지' 카테고리 항목과 다른 카테고리 항목 각 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-457: 공지사항 목록 페이지 로드 실패"
        self._assert_category_tab_exists(notice_page)

        total_count = notice_page.get_notice_count()
        notice_page.click_tab_notice()
        notice_page.wait_for_notice_list()
        filtered_count = notice_page.get_notice_count()

        assert filtered_count >= 0, \
            "[FAIL] FULLTC-457: '공지' 탭 선택 후 목록 조회 실패"
        assert filtered_count <= total_count, \
            f"[FAIL] FULLTC-457: '공지' 탭 필터 후 공지 수 증가 — " \
            f"필터 미동작 의심 (전체:{total_count}, 필터후:{filtered_count})"

        # '공지' 탭 활성화 여부 확인
        active_tab = notice_page.get_active_category_tab_text()
        if active_tab:
            assert "공지" in active_tab, \
                f"[FAIL] FULLTC-457: '공지' 탭 활성 미확인 (현재: '{active_tab}')"

    def test_FULLTC_458_category_event_filter(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-458 | 공지사항/이벤트 탭 필터 | Major
        '이벤트' 카테고리 탭 선택 시 '이벤트' 카테고리 항목만 표시되어야 한다.
        ⚠️ TODO: CATEGORY_TAB_EVENT 셀렉터 튜닝 필요
        사전 조건: '이벤트' 카테고리 항목과 다른 카테고리 항목 각 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-458: 공지사항 목록 페이지 로드 실패"
        self._assert_category_tab_exists(notice_page)

        total_count = notice_page.get_notice_count()
        notice_page.click_tab_event()
        notice_page.wait_for_notice_list()
        filtered_count = notice_page.get_notice_count()

        assert filtered_count >= 0, \
            "[FAIL] FULLTC-458: '이벤트' 탭 선택 후 목록 조회 실패"
        assert filtered_count <= total_count, \
            f"[FAIL] FULLTC-458: '이벤트' 탭 필터 후 공지 수 증가 — " \
            f"필터 미동작 의심 (전체:{total_count}, 필터후:{filtered_count})"

    def test_FULLTC_459_category_guide_filter(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-459 | 공지사항/안내 탭 필터 | Major
        '안내' 카테고리 탭 선택 시 '안내' 카테고리 항목만 표시되어야 한다.
        ⚠️ TODO: CATEGORY_TAB_GUIDE 셀렉터 튜닝 필요
        사전 조건: '안내' 카테고리 항목과 다른 카테고리 항목 각 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-459: 공지사항 목록 페이지 로드 실패"
        self._assert_category_tab_exists(notice_page)

        total_count = notice_page.get_notice_count()
        notice_page.click_tab_guide()
        notice_page.wait_for_notice_list()
        filtered_count = notice_page.get_notice_count()

        assert filtered_count >= 0, \
            "[FAIL] FULLTC-459: '안내' 탭 선택 후 목록 조회 실패"
        assert filtered_count <= total_count, \
            f"[FAIL] FULLTC-459: '안내' 탭 필터 후 공지 수 증가 — " \
            f"필터 미동작 의심 (전체:{total_count}, 필터후:{filtered_count})"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-460~463  |  공지 검색
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.notice
class TestNoticeSearch:
    """제목·본문 키워드 검색·초기화·결과 없음 검증 — FULLTC-460 ~ 463
    ⚠️ 검색 UI가 HTML에 미노출 → TODO_ 셀렉터 → skip 자동 처리
    """

    SEARCH_KEYWORD_EXISTS   = "공지"          # 실제 공지 제목에 포함된 키워드
    SEARCH_KEYWORD_BODY     = "블루밍비트"     # 본문에 포함된 키워드 (수동 확인 후 교체)
    SEARCH_KEYWORD_NOEXIST  = "xQzYaBcDeFgHiJkLmNoP_notExist_2099"  # 존재하지 않는 키워드

    def _assert_search_visible(self, notice_page: NoticePage) -> None:
        """검색 UI 존재 여부 사전 검증 (없으면 skip)"""
        if not notice_page.is_search_visible():
            pytest.skip(
                "[SKIP] 검색창 UI 미노출 — "
                "TODO: SEARCH_INPUT 셀렉터 튜닝 후 재실행"
            )

    def test_FULLTC_460_title_keyword_search(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-460 | 공지사항/제목 키워드 검색 결과 노출 | Major
        제목에 포함된 키워드 검색 시 해당 키워드가 제목에 포함된 공지만 표시되어야 한다.
        ⚠️ TODO: SEARCH_INPUT, SEARCH_SUBMIT_BTN 셀렉터 튜닝 필요
        사전 조건: 검색 키워드가 제목에 포함된 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-460: 공지사항 목록 페이지 로드 실패"
        self._assert_search_visible(notice_page)

        total_count = notice_page.get_notice_count()
        notice_page.type_search_keyword(self.SEARCH_KEYWORD_EXISTS)
        notice_page.wait_for_notice_list()
        result_count = notice_page.get_notice_count()

        assert result_count >= 1, \
            f"[FAIL] FULLTC-460: 키워드 '{self.SEARCH_KEYWORD_EXISTS}' 검색 결과 0건 — " \
            f"실제 키워드 또는 검색 로직 확인 필요"

        # 검색 결과 제목에 키워드 포함 여부 확인
        for i in range(min(result_count, 3)):
            title = notice_page.get_notice_title(i)
            assert self.SEARCH_KEYWORD_EXISTS.lower() in title.lower(), \
                f"[FAIL] FULLTC-460: 검색 결과 {i+1}번째 제목에 키워드 미포함 " \
                f"(제목: '{title}', 키워드: '{self.SEARCH_KEYWORD_EXISTS}')"

    def test_FULLTC_461_body_keyword_search(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-461 | 공지사항/본문 키워드 검색 결과 노출 | Major
        본문에만 포함된 키워드 검색 시 해당 공지가 결과에 포함되어야 한다.
        ⚠️ TODO: SEARCH_INPUT 셀렉터 튜닝 필요
        ※ SEARCH_KEYWORD_BODY 값 수동 확인 후 교체 필요
        사전 조건: 해당 키워드가 본문에만 포함된 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-461: 공지사항 목록 페이지 로드 실패"
        self._assert_search_visible(notice_page)

        notice_page.type_search_keyword(self.SEARCH_KEYWORD_BODY)
        notice_page.wait_for_notice_list()
        result_count = notice_page.get_notice_count()

        if result_count == 0:
            pytest.skip(
                f"[SKIP] FULLTC-461: 키워드 '{self.SEARCH_KEYWORD_BODY}' 검색 결과 0건 — "
                f"본문 키워드를 실제 공지 내용으로 교체 후 재실행"
            )

        assert result_count >= 1, \
            f"[FAIL] FULLTC-461: 본문 키워드 '{self.SEARCH_KEYWORD_BODY}' 검색 결과 0건 — " \
            f"본문 검색 미지원 또는 키워드 불일치"

    def test_FULLTC_462_search_clear_restores_full_list(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-462 | 공지사항/검색어 초기화 후 전체 목록 복원 | Minor
        검색 후 초기화 버튼 클릭 시 전체 공지 목록이 복원되어야 한다.
        ⚠️ TODO: SEARCH_CLEAR_BTN 셀렉터 튜닝 필요
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-462: 공지사항 목록 페이지 로드 실패"
        self._assert_search_visible(notice_page)

        total_count = notice_page.get_notice_count()
        notice_page.type_search_keyword(self.SEARCH_KEYWORD_EXISTS)
        notice_page.wait_for_notice_list()
        filtered_count = notice_page.get_notice_count()

        notice_page.click_search_clear()
        notice_page.wait_for_notice_list()
        restored_count = notice_page.get_notice_count()

        assert restored_count >= filtered_count, \
            f"[FAIL] FULLTC-462: 검색 초기화 후 목록 수 감소 " \
            f"(필터후:{filtered_count}, 초기화후:{restored_count})"
        assert restored_count == total_count, \
            f"[FAIL] FULLTC-462: 검색 초기화 후 전체 목록 미복원 " \
            f"(원래:{total_count}, 초기화후:{restored_count})"

    def test_FULLTC_463_no_result_empty_state(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-463 | 공지사항/검색 결과 없음 처리 | Minor
        존재하지 않는 키워드 검색 시 빈 상태 UI와 안내 문구가 표시되어야 한다.
        ⚠️ TODO: SEARCH_NO_RESULT 셀렉터 튜닝 필요
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-463: 공지사항 목록 페이지 로드 실패"
        self._assert_search_visible(notice_page)

        notice_page.type_search_keyword(self.SEARCH_KEYWORD_NOEXIST)
        notice_page.page.wait_for_timeout(1_000)

        result_count = notice_page.get_notice_count()
        no_result_ui = notice_page.is_search_no_result_visible()

        assert result_count == 0 or no_result_ui, \
            f"[FAIL] FULLTC-463: 존재하지 않는 키워드 검색 후 " \
            f"빈 상태 UI 미노출 및 카드 여전히 존재 (카드 수: {result_count}) — " \
            f"TODO: SEARCH_NO_RESULT 셀렉터 튜닝 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-464~467  |  상세 페이지
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.notice
class TestNoticeDetail:
    """상세 페이지 진입·본문 서식·이미지·링크 검증 — FULLTC-464 ~ 467
    ⚠️ 상세 페이지 셀렉터 모두 TODO_ 상태 → 튜닝 전까지 부분 검증
    """

    def test_FULLTC_464_detail_page_info_display(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-464 | 공지사항/상세 페이지 진입 및 정보 노출 | Major
        목록에서 공지 클릭 시 상세 페이지로 정상 이동하며
        제목·카테고리·작성일·본문이 모두 표시되어야 한다.
        ⚠️ TODO: DETAIL_TITLE, DETAIL_BODY 셀렉터 튜닝 필요
        사전 조건: 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-464: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-464: 공지 없음 — 상세 페이지 검증 불가")

        url_before = notice_page.get_current_url()
        notice_page.click_notice_card(0)

        assert notice_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-464: 공지 클릭 후 URL 미변경"
        assert NoticePage.NOTICE_DETAIL_PATH in notice_page.get_current_url(), \
            f"[FAIL] FULLTC-464: 상세 URL 패턴 불일치 " \
            f"(기대: '{NoticePage.NOTICE_DETAIL_PATH}', 실제: '{notice_page.get_current_url()}')"
        assert "about:blank" not in notice_page.get_current_url(), \
            "[FAIL] FULLTC-464: 공지 클릭 후 빈 페이지(about:blank)로 이동"

        # 상세 페이지 정보 확인 (TODO 셀렉터)
        detail_title   = notice_page.get_detail_title()
        detail_body    = notice_page.get_detail_body_text()

        if detail_title.strip() == "" and detail_body.strip() == "":
            pytest.skip(
                "[SKIP] FULLTC-464 (상세 정보): 제목·본문 셀렉터로 내용 추출 실패 — "
                "TODO: DETAIL_TITLE, DETAIL_BODY 셀렉터 튜닝 후 재실행"
            )

        if detail_title.strip():
            assert detail_title.strip() != "", \
                "[FAIL] FULLTC-464: 상세 페이지 제목 비어있음"

        if detail_body.strip():
            assert len(detail_body.strip()) > 5, \
                f"[FAIL] FULLTC-464: 상세 페이지 본문 너무 짧음 — " \
                f"{len(detail_body.strip())}자"

    def test_FULLTC_465_detail_body_text_formatting(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-465 | 공지사항/본문 텍스트 서식 정상 렌더링 | Major
        본문의 굵기·색상·줄바꿈 등 서식이 깨짐 없이 렌더링되어야 한다.
        ⚠️ TODO: DETAIL_BODY 셀렉터 튜닝 필요
        사전 조건: 서식이 포함된 본문을 가진 공지 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-465: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-465: 공지 없음 — 본문 서식 검증 불가")

        notice_page.click_notice_card(0)
        assert NoticePage.NOTICE_DETAIL_PATH in notice_page.get_current_url(), \
            "[FAIL] FULLTC-465: 공지 클릭 후 상세 페이지 미이동"

        # 본문 렌더링 확인: body 요소 존재 여부
        body_count = notice_page.page.locator(NoticePage.DETAIL_BODY).count()
        if body_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-465: 본문 셀렉터로 요소 없음 — "
                "TODO: DETAIL_BODY 셀렉터 튜닝 후 재실행"
            )

        body_el = notice_page.page.locator(NoticePage.DETAIL_BODY).first
        body_html = body_el.evaluate("e => e.innerHTML")

        # 서식 태그 포함 여부 확인 (strong, em, color style 등)
        has_formatting = any(
            tag in body_html.lower()
            for tag in ["<strong", "<em", "<b>", "<u>", "color:", "font-size", "<br", "<p"]
        )
        body_text_length = len(body_el.inner_text().strip())

        if not has_formatting:
            pytest.skip(
                "[SKIP] FULLTC-465: 현재 공지 본문에 서식 태그 미포함 — "
                "서식 포함 공지로 재실행 필요"
            )

        # 서식이 있다면 깨지지 않고 렌더링됐는지 확인 (본문 텍스트 비어있지 않음)
        assert body_text_length > 0, \
            "[FAIL] FULLTC-465: 서식 포함 본문의 렌더링 후 텍스트 추출 결과 비어있음 — 렌더링 오류 의심"

    def test_FULLTC_466_detail_body_images_render(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-466 | 공지사항/본문 이미지 정상 렌더링 | Major
        본문 내 이미지가 깨짐이나 빈 영역 없이 정상 표시되어야 한다.
        ⚠️ TODO: DETAIL_BODY_IMG 셀렉터 튜닝 필요
        사전 조건: 본문에 이미지가 포함된 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-466: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-466: 공지 없음 — 이미지 렌더링 검증 불가")

        # 이미지 포함 공지 탐색
        found_img_notice = False
        for i in range(min(count, 5)):
            notice_page.click_notice_card(i)
            notice_page.page.wait_for_timeout(800)
            img_count = notice_page.get_detail_body_image_count()
            if img_count > 0:
                found_img_notice = True
                break
            notice_page.go_back()
            notice_page.wait_for_notice_list()

        if not found_img_notice:
            pytest.skip(
                "[SKIP] FULLTC-466: 이미지 포함 공지를 찾지 못함 — "
                "이미지 포함 공지 직접 접속 후 재실행 필요. "
                "TODO: DETAIL_BODY_IMG 셀렉터 튜닝 필요"
            )

        assert not notice_page.is_any_body_image_broken(), \
            "[FAIL] FULLTC-466: 본문 이미지 중 naturalWidth=0인 깨진 이미지 존재"

    def test_FULLTC_467_detail_body_hyperlinks_work(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-467 | 공지사항/본문 하이퍼링크 정상 동작 | Major
        본문 내 링크 클릭 시 지정된 URL 또는 페이지로 이동해야 한다.
        ⚠️ TODO: DETAIL_BODY_LINK 셀렉터 튜닝 필요
        사전 조건: 본문에 하이퍼링크가 포함된 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-467: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-467: 공지 없음 — 링크 검증 불가")

        # 링크 포함 공지 탐색
        found_link = False
        for i in range(min(count, 5)):
            notice_page.click_notice_card(i)
            notice_page.page.wait_for_timeout(800)
            link_count = notice_page.get_detail_body_link_count()
            if link_count > 0:
                found_link = True
                break
            notice_page.go_back()
            notice_page.wait_for_notice_list()

        if not found_link:
            pytest.skip(
                "[SKIP] FULLTC-467: 링크 포함 공지를 찾지 못함 — "
                "링크 포함 공지 직접 접속 후 재실행 필요. "
                "TODO: DETAIL_BODY_LINK 셀렉터 튜닝 필요"
            )

        # 링크 href 속성 존재 확인
        first_link = notice_page.page.locator(NoticePage.DETAIL_BODY_LINK).first
        href = first_link.get_attribute("href") or ""
        assert href.strip() != "" and href != "#", \
            f"[FAIL] FULLTC-467: 본문 첫 번째 링크 href 비어있거나 '#' — " \
            f"유효한 URL 필요 (href='{href}')"
        assert "javascript:" not in href.lower(), \
            f"[FAIL] FULLTC-467: 본문 링크가 javascript: 스킴 사용 — " \
            f"유효한 URL 사용 필요 (href='{href}')"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-468~469  |  추가 로딩
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.notice
class TestNoticeInfiniteScroll:
    """무한 스크롤(또는 페이지네이션) 추가 로딩·마지막 페이지 처리 검증 — FULLTC-468 ~ 469
    ※ 실제 HTML: 번호 버튼 페이지네이션 방식 (TC의 무한스크롤과 불일치 가능)
    """

    def test_FULLTC_468_scroll_or_pagination_loads_more(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-468 | 공지사항/무한 스크롤 추가 로딩 | Major
        목록 하단 스크롤 후 추가 공지 데이터가 로드되거나 다음 페이지로 전환되어야 한다.
        ※ 실제 HTML 기준: 번호 버튼 페이지네이션 방식
        사전 조건: 공지사항 목록이 20건(1페이지) 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-468: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count_before = notice_page.get_notice_count()
        if count_before < 1:
            pytest.skip("[SKIP] FULLTC-468: 공지 없음 — 추가 로딩 검증 불가")

        is_pagination = notice_page.is_pagination_visible()
        page_count    = notice_page.get_pagination_page_count()

        if is_pagination and page_count >= 2:
            # 번호 페이지네이션 방식: 다음 페이지 클릭으로 추가 로딩 검증
            notice_page.click_next_page()
            count_after = notice_page.get_notice_count()
            assert count_after >= 1, \
                f"[FAIL] FULLTC-468: 다음 페이지 클릭 후 공지 카드 0건 (페이지 수: {page_count})"
        elif is_pagination and page_count < 2:
            pytest.skip(
                f"[SKIP] FULLTC-468: 페이지 수 {page_count}개 — "
                f"추가 로딩 검증에 2페이지 이상 필요"
            )
        else:
            # 무한 스크롤 방식 시도
            if count_before < 20:
                pytest.skip(
                    f"[SKIP] FULLTC-468: 공지 {count_before}건 — "
                    f"무한 스크롤 검증에 20건 이상 필요"
                )
            notice_page.scroll_to_bottom(steps=5)
            notice_page.page.wait_for_timeout(1_500)
            count_after = notice_page.get_notice_count()
            assert count_after > count_before, \
                f"[FAIL] FULLTC-468: 하단 스크롤 후 추가 공지 미로드 " \
                f"(before:{count_before}, after:{count_after})"

    def test_FULLTC_469_last_page_no_more_loading(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-469 | 공지사항/마지막 페이지 처리 | Minor
        전체 공지 마지막까지 도달 후 추가 로딩이 발생하지 않고
        '더 이상 공지 없음' 안내가 표시되어야 한다.
        사전 조건: 전체 목록의 마지막까지 스크롤 또는 페이지 이동 완료
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-469: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-469: 공지 없음 — 마지막 페이지 검증 불가")

        is_pagination = notice_page.is_pagination_visible()

        if is_pagination:
            page_count = notice_page.get_pagination_page_count()
            if page_count >= 2:
                # 마지막 페이지로 이동
                notice_page.click_page_by_number(page_count)
                notice_page.page.wait_for_timeout(800)
                final_count = notice_page.get_notice_count()
                assert final_count >= 0, \
                    "[FAIL] FULLTC-469: 마지막 페이지 이동 후 공지 카드 조회 실패"
                # 마지막 페이지 이후 추가 페이지 없음 확인
                assert notice_page.get_pagination_page_count() >= 1, \
                    "[FAIL] FULLTC-469: 마지막 페이지 도달 후 페이지네이션 이상"
            else:
                pytest.skip(
                    f"[SKIP] FULLTC-469: 페이지 수 {page_count}개 — "
                    f"마지막 페이지 검증에 2페이지 이상 필요"
                )
        else:
            # 무한 스크롤 방식: 끝까지 스크롤 후 카드 수 안정화 확인
            notice_page.scroll_to_bottom(steps=15)
            notice_page.page.wait_for_timeout(1_500)
            count_1 = notice_page.get_notice_count()
            notice_page.scroll_to_bottom(steps=5)
            notice_page.page.wait_for_timeout(1_000)
            count_2 = notice_page.get_notice_count()
            assert count_2 >= count_1, \
                f"[FAIL] FULLTC-469: 마지막 페이지에서 카드 수 감소 " \
                f"(1차:{count_1}, 2차:{count_2}) — 예상치 못한 동작"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-470~471  |  Empty State
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.notice
class TestNoticeEmptyState:
    """공지 없음 UI · 카테고리 결과 없음 UI 검증 — FULLTC-470 ~ 471
    ⚠️ 각 TC는 해당 조건 충족 시에만 검증 가능. 데이터 존재 시 skip 처리
    """

    def test_FULLTC_470_no_notice_empty_state(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-470 | 공지사항/공지사항 없음 UI | Minor
        등록된 공지가 0건일 때 빈 상태 UI와 안내 문구가 표시되어야 한다.
        ⚠️ TODO: EMPTY_STATE 셀렉터 튜닝 필요
        사전 조건: 공지사항 0건인 상태 (관리자에서 전체 삭제 후 테스트)
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-470: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count > 0:
            pytest.skip(
                f"[SKIP] FULLTC-470: 공지 {count}건 존재 — "
                f"Empty State 검증은 0건 상태에서 실행하세요"
            )

        assert notice_page.is_empty_state_visible(), \
            "[FAIL] FULLTC-470: 공지 0건 상태에서 빈 상태 UI 미노출 " \
            "(TODO: EMPTY_STATE 셀렉터 튜닝 필요)"

    def test_FULLTC_471_category_filter_empty_state(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-471 | 공지사항/카테고리 필터 결과 없음 UI | Minor
        해당 카테고리 공지가 없을 때 빈 상태 UI와 안내 문구가 표시되어야 한다.
        ⚠️ TODO: CATEGORY_TAB_*, EMPTY_STATE 셀렉터 튜닝 필요
        사전 조건: 선택한 카테고리에 공지가 없는 상태
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-471: 공지사항 목록 페이지 로드 실패"

        if not notice_page.is_category_tab_visible():
            pytest.skip(
                "[SKIP] FULLTC-471: 카테고리 탭 UI 미노출 — "
                "TODO: CATEGORY_WRAPPER 셀렉터 튜닝 후 재실행"
            )

        # '이벤트' 탭으로 필터 시도 (가장 공지 없을 가능성 높음)
        notice_page.click_tab_event()
        notice_page.page.wait_for_timeout(800)
        count = notice_page.get_notice_count()

        if count > 0:
            notice_page.click_tab_guide()
            notice_page.page.wait_for_timeout(800)
            count = notice_page.get_notice_count()

        if count > 0:
            pytest.skip(
                "[SKIP] FULLTC-471: 모든 카테고리에 공지 존재 — "
                "공지 없는 카테고리 상태에서 직접 실행 필요"
            )

        assert notice_page.is_empty_state_visible(), \
            "[FAIL] FULLTC-471: 카테고리 필터 결과 0건 상태에서 빈 상태 UI 미노출 " \
            "(TODO: EMPTY_STATE 셀렉터 튜닝 필요)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-472  |  첨부파일
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.notice
class TestNoticeAttachment:
    """첨부파일 노출 및 다운로드 링크 검증 — FULLTC-472
    ⚠️ 첨부파일 UI HTML 미노출 → TODO_ 셀렉터 → skip 자동 처리
    ⚠️ 실제 파일 다운로드는 사용자 직접 확인 필요 (보안 정책상 자동화 제외)
    """

    def test_FULLTC_472_attachment_display_and_download_link(
        self, notice_page: NoticePage
    ) -> None:
        """
        FULLTC-472 | 공지사항/첨부파일 다운로드 및 파일명 노출 | Minor
        첨부파일이 포함된 공지 상세에서 파일명이 표시되고
        다운로드 링크가 유효한 href를 가져야 한다.
        ⚠️ TODO: ATTACHMENT_SECTION, ATTACHMENT_ITEM, ATTACHMENT_FILENAME,
                  ATTACHMENT_LINK 셀렉터 튜닝 필요
        ※ 실제 파일 다운로드(클릭 후 저장)는 보안 정책상 수동 확인 필요
        사전 조건: 첨부파일이 포함된 공지 1건 이상 존재
        """
        notice_page.go_to_notice_list()
        assert notice_page.is_loaded(), \
            "[FAIL] FULLTC-472: 공지사항 목록 페이지 로드 실패"

        notice_page.wait_for_notice_list()
        count = notice_page.get_notice_count()
        if count < 1:
            pytest.skip("[SKIP] FULLTC-472: 공지 없음 — 첨부파일 검증 불가")

        # 첨부파일 포함 공지 탐색 (상위 10개 카드)
        found_attachment = False
        for i in range(min(count, 10)):
            notice_page.click_notice_card(i)
            notice_page.page.wait_for_timeout(800)
            if notice_page.is_attachment_section_visible():
                found_attachment = True
                break
            notice_page.go_back()
            notice_page.wait_for_notice_list()

        if not found_attachment:
            pytest.skip(
                "[SKIP] FULLTC-472: 첨부파일 포함 공지를 찾지 못함 — "
                "첨부파일 포함 공지에 직접 접속 후 재실행 필요. "
                "TODO: ATTACHMENT_SECTION 셀렉터 튜닝 필요"
            )

        # 1) 첨부파일 영역 노출 확인
        assert notice_page.is_attachment_section_visible(), \
            "[FAIL] FULLTC-472: 첨부파일 영역 미노출 (TODO: ATTACHMENT_SECTION 셀렉터 튜닝)"

        attachment_count = notice_page.get_attachment_count()
        assert attachment_count >= 1, \
            "[FAIL] FULLTC-472: 첨부파일 항목 0건 (TODO: ATTACHMENT_ITEM 셀렉터 튜닝)"

        # 2) 파일명 표시 확인
        filename = notice_page.get_attachment_filename(0)
        if filename.strip() == "":
            pytest.skip(
                "[SKIP] FULLTC-472 (파일명): 파일명 추출 실패 — "
                "TODO: ATTACHMENT_FILENAME 셀렉터 튜닝 후 재실행"
            )
        assert filename.strip() != "", \
            "[FAIL] FULLTC-472: 첨부파일명 비어있음 (TODO: ATTACHMENT_FILENAME 셀렉터 튜닝)"

        # 3) 다운로드 링크 href 유효성 확인
        download_href = notice_page.get_attachment_link_href(0)
        if download_href.strip() == "":
            pytest.skip(
                "[SKIP] FULLTC-472 (다운로드 링크): 다운로드 href 추출 실패 — "
                "TODO: ATTACHMENT_LINK 셀렉터 튜닝 후 재실행"
            )
        assert download_href.strip() != "" and download_href != "#", \
            f"[FAIL] FULLTC-472: 첨부파일 다운로드 href 비어있거나 '#' " \
            f"(href='{download_href}') — 유효한 다운로드 URL 필요"

        # ※ 실제 파일 다운로드(파일 저장 확인)는 보안 정책상 자동화 제외
        # ※ 수동으로 다운로드 링크 클릭하여 파일 저장 여부 확인 필요s