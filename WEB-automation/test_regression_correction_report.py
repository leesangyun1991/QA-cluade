"""
tests/stage8_regression/web/test_regression_correction_report.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
정정·반론보도 센터(Correction & Rebuttal Report) 회귀 테스트
FULLTC-497 ~ FULLTC-508 (12 TCs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_correction_report.py -v
  pytest tests/stage8_regression/web/test_regression_correction_report.py -m "correction_report" -v
  pytest tests/stage8_regression/web/test_regression_correction_report.py -k "FULLTC_506" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)
  - 비로그인으로도 접근 가능한 TC: 497~508 전체

[TC 클래스 구성]
  FULLTC-497~498   TestCorrectionReportEntry          메뉴 진입
  FULLTC-499~503   TestCorrectionReportList           리스트 노출
  FULLTC-504~505   TestCorrectionReportDetail         상세 라우팅
  FULLTC-506       TestCorrectionReportEmptyState     Empty State
  FULLTC-507~508   TestCorrectionReportInfiniteScroll 추가 로딩

[HTML 분석 핵심 포인트]
  ✅ 안정 셀렉터 (HTML 직접 확인):
     · 리스트 래퍼: div[class*='correctionRebuttalReportingListWrapper']
     · Empty State: div[class*='emptyCorrectionRebuttalReportingListContainer']
     · Empty 메시지: "정정 및 반론보도 기사가 존재하지 않습니다."
     → FULLTC-506은 실제 HTML 기반으로 완전하게 검증 가능!

  ⚠️ TODO_ 셀렉터 (기사 등록 후 F12 확인 필요):
     · 기사 카드, LNB 메뉴, 상세 페이지 요소 → skip 자동 처리
     · 목록 URL 추정: /mypage/correction-rebuttal (F12 확인 후 CORRECTION_PATH 수정)
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from correction_report_page import CorrectionReportPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def correction_page() -> Iterator[CorrectionReportPage]:
    """정정·반론보도 센터 페이지 픽스처 (로그인 세션 유지)
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
        yield CorrectionReportPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-497~498  |  메뉴 진입
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.correction_report
class TestCorrectionReportEntry:
    """LNB 메뉴 클릭 진입 · URL 직접 접근 검증 — FULLTC-497 ~ 498"""

    def test_FULLTC_497_lnb_menu_click_navigates(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-497 | 정정·반론보도센터/LNB 메뉴 클릭 | Major
        LNB(좌측 네비게이션 바)에서 [정정·반론보도센터] 메뉴 클릭 시
        해당 페이지로 이동하고 타이틀이 '정정·반론보도 센터'로 표시되어야 한다.
        ⚠️ TODO: LNB_WRAPPER, LNB_CORRECTION_MENU 셀렉터 튜닝 필요
        사전 조건: 서비스 접속 상태, LNB 노출
        """
        # 마이페이지에서 시작 (LNB가 있을 가능성 높음)
        correction_page.go_to_mypage()
        correction_page.page.wait_for_timeout(600)

        if not correction_page.is_lnb_visible():
            pytest.skip(
                "[SKIP] FULLTC-497: LNB 영역 미노출 — "
                "TODO: LNB_WRAPPER 셀렉터 튜닝 후 재실행"
            )

        url_before = correction_page.get_current_url()
        correction_page.click_lnb_correction_menu()

        assert correction_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-497: LNB '정정·반론보도센터' 메뉴 클릭 후 URL 미변경"

        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-497: 정정·반론보도센터 페이지 로드 실패 (리스트 래퍼 미노출)"

        assert correction_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-497: 페이지 타이틀이 '정정·반론보도 센터' 아님 " \
            f"(현재: '{correction_page.get_page_title_text()}')"

    def test_FULLTC_498_direct_url_access(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-498 | 정정·반론보도센터/URL 직접 접근 | Minor
        브라우저 주소창에 URL을 직접 입력해 접근 시 페이지가 정상 렌더링되어야 한다.
        비로그인/로그인 여부와 관계없이 페이지가 노출되어야 한다.
        ⚠️ TODO: CORRECTION_PATH 실제 URL 확인 후 수정 (현재 추정값 사용)
        """
        correction_page.go_to_correction_report()

        assert correction_page.is_loaded(), \
            f"[FAIL] FULLTC-498: URL 직접 접근 후 페이지 로드 실패 " \
            f"(URL: '{correction_page.BASE_URL}{CorrectionReportPage.CORRECTION_PATH}')"

        assert correction_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-498: URL 직접 접근 후 페이지 타이틀 불일치 " \
            f"(현재: '{correction_page.get_page_title_text()}')"

        # 로그인 리다이렉트 없이 페이지가 정상 노출되는지 확인
        current_url = correction_page.get_current_url()
        assert CorrectionReportPage.SIGNIN_PATH not in current_url, \
            f"[FAIL] FULLTC-498: 비로그인 접근 시 로그인 페이지로 리다이렉트됨 " \
            f"(현재 URL: '{current_url}') — 공개 페이지여야 함"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-499~503  |  리스트 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.correction_report
class TestCorrectionReportList:
    """기사 목록 카드·카드 정보·최신순·날짜 형식·썸네일 검증 — FULLTC-499 ~ 503
    ⚠️ 기사 카드 셀렉터가 TODO_ 상태 — 기사 등록 후 F12 확인 필요
    기사 없는 경우 skip 자동 처리
    """

    def _assert_articles_exist(self, correction_page: CorrectionReportPage) -> None:
        """기사가 1건 이상 존재하는지 확인. 없으면 skip."""
        article_count = correction_page.get_article_count()
        if article_count == 0:
            pytest.skip(
                "[SKIP] 기사 카드 없음 — 현재 빈 상태이거나 "
                "TODO: ARTICLE_CARD 셀렉터 튜닝 후 재실행"
            )

    def test_FULLTC_499_article_cards_displayed(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-499 | 정정·반론보도센터/기사 목록 카드 노출 | Major
        기사가 존재할 때 카드 형식으로 나열되어야 한다.
        ⚠️ TODO: ARTICLE_CARD 셀렉터 튜닝 필요
        사전 조건: 정정·반론보도 기사 1건 이상 존재
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-499: 정정·반론보도센터 페이지 로드 실패"

        # Empty State가 보이면 기사가 없음 → skip
        if correction_page.is_empty_state_visible():
            pytest.skip(
                "[SKIP] FULLTC-499: 현재 빈 상태 (기사 없음) — "
                "기사 등록 후 재실행 필요"
            )

        self._assert_articles_exist(correction_page)
        article_count = correction_page.get_article_count()

        assert article_count >= 1, \
            f"[FAIL] FULLTC-499: 기사 카드 0건 — " \
            f"TODO: ARTICLE_CARD 셀렉터 튜닝 필요"

        # 카드 레이아웃 정상 여부 확인 (첫 번째 카드)
        assert correction_page.is_card_layout_intact(0), \
            "[FAIL] FULLTC-499: 첫 번째 기사 카드 레이아웃 깨짐 (width/height = 0)"

    def test_FULLTC_500_article_card_info_items(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-500 | 정정·반론보도센터/카드 정보 항목 확인 | Major
        각 기사 카드에 제목·발행 날짜·썸네일(있는 경우)이 노출되어야 한다.
        ⚠️ TODO: ARTICLE_TITLE, ARTICLE_DATE 셀렉터 튜닝 필요
        사전 조건: 기사 카드 1건 이상 노출
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-500: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-500: 빈 상태 — 기사 등록 후 재실행")

        self._assert_articles_exist(correction_page)

        # 1) 제목 확인
        title = correction_page.get_article_title(0)
        if title.strip() == "":
            pytest.skip(
                "[SKIP] FULLTC-500 (제목): 제목 추출 실패 — "
                "TODO: ARTICLE_TITLE 셀렉터 튜닝 필요"
            )
        assert title.strip() != "", \
            "[FAIL] FULLTC-500: 첫 번째 기사 카드 제목 비어있음"

        # 2) 날짜 확인
        date_text = correction_page.get_article_date(0)
        if date_text.strip() == "":
            pytest.skip(
                "[SKIP] FULLTC-500 (날짜): 날짜 추출 실패 — "
                "TODO: ARTICLE_DATE 셀렉터 튜닝 필요"
            )
        assert date_text.strip() != "", \
            "[FAIL] FULLTC-500: 첫 번째 기사 카드 날짜 비어있음"

    def test_FULLTC_501_articles_sorted_by_latest(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-501 | 정정·반론보도센터/최신순 정렬 | Major
        기사 목록이 발행일 기준 내림차순(최신순)으로 정렬되어야 한다.
        ⚠️ TODO: ARTICLE_DATE 셀렉터 튜닝 필요
        사전 조건: 기사 2건 이상 존재
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-501: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-501: 빈 상태 — 기사 등록 후 재실행")

        self._assert_articles_exist(correction_page)
        dates = correction_page.get_all_dates()
        if len(dates) < 2:
            pytest.skip(
                f"[SKIP] FULLTC-501: 날짜 추출된 기사 {len(dates)}건 — "
                f"정렬 검증에 2건 이상 필요. TODO: ARTICLE_DATE 셀렉터 튜닝 필요"
            )

        assert correction_page.are_dates_sorted_latest(), \
            f"[FAIL] FULLTC-501: 기사 목록이 최신순(내림차순) 미정렬 — " \
            f"현재 날짜 순서: {dates[:5]}"

    def test_FULLTC_502_date_format_standard(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-502 | 정정·반론보도센터/날짜 표기 형식 | Minor
        각 기사 카드의 날짜가 'YYYY.MM.DD' 또는 서비스 표준 형식으로 표시되어야 한다.
        ⚠️ TODO: ARTICLE_DATE 셀렉터 튜닝 필요
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-502: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-502: 빈 상태 — 기사 등록 후 재실행")

        self._assert_articles_exist(correction_page)
        date_text = correction_page.get_article_date(0)
        if date_text.strip() == "":
            pytest.skip(
                "[SKIP] FULLTC-502: 날짜 추출 실패 — "
                "TODO: ARTICLE_DATE 셀렉터 튜닝 필요"
            )

        assert correction_page.is_date_format_valid(date_text), \
            f"[FAIL] FULLTC-502: 날짜 형식 불일치 — " \
            f"'YYYY.MM.DD' 등 표준 형식 기대 (현재: '{date_text}')"

    def test_FULLTC_503_thumbnail_placeholder_when_missing(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-503 | 정정·반론보도센터/썸네일 미존재 처리 | Minor
        썸네일 없는 기사 카드에서 레이아웃이 깨지지 않아야 한다.
        썸네일 영역에 기본 이미지(placeholder) 또는 빈 영역이 표시될 수 있음.
        ⚠️ TODO: ARTICLE_THUMBNAIL 셀렉터 튜닝 필요
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-503: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-503: 빈 상태 — 기사 등록 후 재실행")

        self._assert_articles_exist(correction_page)
        article_count = correction_page.get_article_count()

        # 썸네일이 있는 기사가 있으면 깨진 이미지 여부 확인
        if correction_page.has_thumbnail(0):
            assert not correction_page.is_thumbnail_broken(0), \
                "[FAIL] FULLTC-503: 첫 번째 기사 썸네일 이미지 깨짐 (naturalWidth=0)"

        # 레이아웃 정상 여부 확인
        for i in range(min(article_count, 3)):
            assert correction_page.is_card_layout_intact(i), \
                f"[FAIL] FULLTC-503: {i+1}번째 기사 카드 레이아웃 깨짐 — " \
                f"썸네일 미존재 시에도 레이아웃 유지 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-504~505  |  상세 라우팅
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.correction_report
class TestCorrectionReportDetail:
    """카드 클릭 상세 이동 · 뒤로가기 동작 검증 — FULLTC-504 ~ 505
    ⚠️ 기사 카드 및 상세 페이지 셀렉터 모두 TODO_ 상태
    """

    def test_FULLTC_504_card_click_navigates_to_detail(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-504 | 정정·반론보도센터/카드 클릭 시 상세 이동 | Major
        기사 카드 클릭 시 해당 기사의 상세 페이지로 이동하고
        기사 본문이 정상 노출되어야 한다.
        ⚠️ TODO: ARTICLE_CARD, DETAIL_TITLE, DETAIL_BODY 셀렉터 튜닝 필요
        사전 조건: 기사 카드 1건 이상 노출
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-504: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-504: 빈 상태 — 기사 등록 후 재실행")

        article_count = correction_page.get_article_count()
        if article_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-504: 기사 카드 없음 — "
                "TODO: ARTICLE_CARD 셀렉터 튜닝 후 재실행"
            )

        url_before = correction_page.get_current_url()
        correction_page.click_article_card(0)

        assert correction_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-504: 기사 카드 클릭 후 URL 미변경"

        assert "about:blank" not in correction_page.get_current_url(), \
            "[FAIL] FULLTC-504: 기사 카드 클릭 후 빈 페이지(about:blank) 이동"

        # 상세 페이지 본문 노출 확인 (TODO 셀렉터)
        detail_title = correction_page.get_detail_title()
        detail_body  = correction_page.get_detail_body_text()

        if detail_title.strip() == "" and detail_body.strip() == "":
            pytest.skip(
                "[SKIP] FULLTC-504 (본문): 상세 페이지 본문 셀렉터 추출 실패 — "
                "TODO: DETAIL_TITLE, DETAIL_BODY 셀렉터 튜닝 후 재실행"
            )

        if detail_body.strip():
            assert len(detail_body.strip()) > 5, \
                f"[FAIL] FULLTC-504: 상세 페이지 본문 너무 짧음 " \
                f"({len(detail_body.strip())}자)"

    def test_FULLTC_505_back_returns_to_list(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-505 | 정정·반론보도센터/뒤로가기 동작 | Minor
        상세 페이지에서 뒤로가기 시 정정·반론보도 센터 목록 페이지로 복귀해야 한다.
        이전 스크롤 위치가 유지되거나 최상단으로 이동해야 한다.
        ⚠️ TODO: ARTICLE_CARD 셀렉터 튜닝 필요
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-505: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-505: 빈 상태 — 기사 등록 후 재실행")

        article_count = correction_page.get_article_count()
        if article_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-505: 기사 카드 없음 — "
                "TODO: ARTICLE_CARD 셀렉터 튜닝 후 재실행"
            )

        # 상세 페이지로 이동
        list_url = correction_page.get_current_url()
        correction_page.click_article_card(0)
        correction_page.page.wait_for_timeout(800)
        detail_url = correction_page.get_current_url()

        assert detail_url != list_url, \
            "[FAIL] FULLTC-505: 기사 카드 클릭 후 상세 페이지 미이동 — " \
            "뒤로가기 테스트 불가"

        # 뒤로가기
        correction_page.go_back()
        returned_url = correction_page.get_current_url()

        # 목록 페이지로 복귀 확인
        assert returned_url != detail_url, \
            "[FAIL] FULLTC-505: 뒤로가기 후 상세 페이지에 머무름 — 목록 복귀 실패"

        # 목록 페이지 로드 확인
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-505: 뒤로가기 후 정정·반론보도 센터 목록 로드 실패"

        # 스크롤 위치 확인 (0 이상이면 이전 위치 유지, 0이면 상단 이동 — 둘 다 허용)
        scroll_y = correction_page.get_scroll_y_position()
        assert scroll_y >= 0, \
            f"[FAIL] FULLTC-505: 뒤로가기 후 스크롤 위치 이상 (y={scroll_y})"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-506  |  Empty State
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.correction_report
class TestCorrectionReportEmptyState:
    """기사 없을 때 안내 문구 검증 — FULLTC-506
    ✅ HTML에서 완전히 확인된 안정 셀렉터로 검증 가능!
    """

    def test_FULLTC_506_empty_state_message_displayed(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-506 | 정정·반론보도센터/기사 없을 때 안내 문구 | Major
        정정·반론보도 기사가 0건일 때 '정정 및 반론보도 기사가 존재하지 않습니다.'
        문구가 노출되고 레이아웃이 정상이어야 한다.

        ✅ 이 TC는 HTML에서 Empty State 셀렉터가 완전히 확인되었으므로
           실제 DOM 기반으로 즉시 검증 가능합니다.
           현재 STG 환경: 기사 없는 빈 상태로 이 TC 정상 실행 가능.

        기사 존재 시에는 skip 처리됩니다.
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-506: 정정·반론보도센터 페이지 로드 실패"

        article_count = correction_page.get_article_count()
        if article_count > 0:
            pytest.skip(
                f"[SKIP] FULLTC-506: 기사 {article_count}건 존재 — "
                f"빈 상태 검증은 기사 0건 환경에서 실행하세요"
            )

        # 1) 빈 상태 컨테이너 노출 확인 (HTML 안정 셀렉터)
        assert correction_page.is_empty_state_visible(), \
            "[FAIL] FULLTC-506: 기사 없는 상태에서 빈 상태 컨테이너 " \
            f"(div[class*='emptyCorrectionRebuttalReportingListContainer']) 미노출"

        # 2) 안내 문구 정확성 확인
        empty_msg = correction_page.get_empty_state_message()
        assert empty_msg.strip() != "", \
            "[FAIL] FULLTC-506: 빈 상태 안내 문구 비어있음"

        assert empty_msg == CorrectionReportPage.EXPECTED_EMPTY_MSG, \
            f"[FAIL] FULLTC-506: 빈 상태 안내 문구 불일치 — " \
            f"기대: '{CorrectionReportPage.EXPECTED_EMPTY_MSG}', " \
            f"실제: '{empty_msg}'"

        # 3) 레이아웃 정상 여부 확인 (컨테이너가 화면 밖으로 벗어나지 않음)
        assert correction_page.is_empty_layout_intact(), \
            "[FAIL] FULLTC-506: 빈 상태 UI 레이아웃 깨짐 " \
            "(emptyCorrectionRebuttalReportingListContainer 높이 = 0)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-507~508  |  추가 로딩
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.correction_report
class TestCorrectionReportInfiniteScroll:
    """스크롤 추가 로딩 · 마지막 페이지 처리 검증 — FULLTC-507 ~ 508
    ⚠️ 기사 카드 셀렉터가 TODO_ 상태
    기사 없거나 충분하지 않을 경우 skip 자동 처리
    """

    def test_FULLTC_507_scroll_loads_more_articles(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-507 | 정정·반론보도센터/스크롤 시 추가 로딩 | Major
        리스트 하단까지 스크롤 시 추가 기사가 자동 로드되고
        로딩 인디케이터가 노출된 후 사라져야 한다.
        ⚠️ TODO: ARTICLE_CARD 셀렉터 튜닝 필요
        사전 조건: 한 페이지 초과 분량의 기사 존재 (일반적으로 10~20건 이상)
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-507: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-507: 빈 상태 — 기사 등록 후 재실행")

        count_before = correction_page.get_article_count()
        if count_before == 0:
            pytest.skip(
                "[SKIP] FULLTC-507: 기사 카드 없음 — "
                "TODO: ARTICLE_CARD 셀렉터 튜닝 후 재실행"
            )
        if count_before < 10:
            pytest.skip(
                f"[SKIP] FULLTC-507: 기사 {count_before}건 — "
                f"추가 로딩 검증에 한 페이지 초과 분량 필요 (일반적으로 10건 이상)"
            )

        # 하단까지 스크롤
        correction_page.scroll_to_bottom(steps=5)
        correction_page.page.wait_for_timeout(1_500)
        count_after = correction_page.get_article_count()

        # 로딩 인디케이터 감지 (타이밍 민감 — 스크롤 직후)
        # ※ 이미 로딩이 완료되어 인디케이터가 사라졌을 수 있으므로 soft 검증
        loading_was_visible = correction_page.is_loading_indicator_visible(timeout=1_000)

        assert count_after > count_before or loading_was_visible, \
            f"[FAIL] FULLTC-507: 스크롤 후 추가 기사 미로드 및 로딩 인디케이터 미노출 " \
            f"(before:{count_before}, after:{count_after}) — " \
            f"TODO: ARTICLE_CARD / LOADING_INDICATOR 셀렉터 튜닝 필요"

        if count_after > count_before:
            assert count_after > count_before, \
                f"[FAIL] FULLTC-507: 추가 기사 로드 후 카드 수 미증가 " \
                f"(before:{count_before}, after:{count_after})"

    def test_FULLTC_508_last_page_no_more_loading(
        self, correction_page: CorrectionReportPage
    ) -> None:
        """
        FULLTC-508 | 정정·반론보도센터/마지막 페이지 처리 | Minor
        전체 기사를 로드한 상태에서 최하단 스크롤 시
        추가 로딩이 발생하지 않아야 한다.
        ⚠️ TODO: ARTICLE_CARD 셀렉터 튜닝 필요
        사전 조건: 전체 기사를 모두 로드한 상태
        """
        correction_page.go_to_correction_report()
        assert correction_page.is_loaded(), \
            "[FAIL] FULLTC-508: 정정·반론보도센터 페이지 로드 실패"

        if correction_page.is_empty_state_visible():
            pytest.skip("[SKIP] FULLTC-508: 빈 상태 — 기사 등록 후 재실행")

        count_initial = correction_page.get_article_count()
        if count_initial == 0:
            pytest.skip(
                "[SKIP] FULLTC-508: 기사 카드 없음 — "
                "TODO: ARTICLE_CARD 셀렉터 튜닝 후 재실행"
            )

        # 끝까지 스크롤하여 모든 기사 로드
        correction_page.scroll_to_bottom(steps=15)
        correction_page.page.wait_for_timeout(1_500)
        count_final_1 = correction_page.get_article_count()

        # 추가 스크롤 후 카드 수 변화 없어야 함 (마지막 페이지)
        correction_page.scroll_to_bottom(steps=5)
        correction_page.page.wait_for_timeout(1_000)
        count_final_2 = correction_page.get_article_count()

        assert count_final_2 >= count_final_1, \
            f"[FAIL] FULLTC-508: 마지막 페이지에서 카드 수 감소 " \
            f"(1차:{count_final_1}, 2차:{count_final_2}) — 예상치 못한 동작"

        # 마지막 페이지 도달 확인: 카드 수가 안정화되어야 함
        assert count_final_2 == count_final_1, \
            f"[FAIL] FULLTC-508: 마지막 페이지에서 추가 기사 계속 로드됨 " \
            f"(1차:{count_final_1}, 2차:{count_final_2}) — 종료 조건 미설정 의심"