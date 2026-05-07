"""
tests/stage8_regression/web/test_regression_ai_report.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI 리포트 회귀 테스트 (FULLTC-206 ~ FULLTC-215)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_ai_report.py -v

[사전 조건]
  - 이 파일과 동일 디렉토리에 auth.json (로그인 세션 파일) 존재 필요
    → 비로그인 TC(FULLTC-212)는 ai_report_page_guest 픽스처를 별도 사용

[TC 구성]
  FULLTC-206~207  TestAiReportGNBRegression         GNB 탭 노출 및 클릭 이동
  FULLTC-208~213  TestAiReportSuspensionRegression   서비스 일시 중단 페이지 UI 검증
  FULLTC-214~215  TestAiReportSubPathRegression      서브 경로 에러 페이지 검증
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from ai_report_page import AiReportPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def ai_report_page() -> Iterator[AiReportPage]:
    """AI 리포트 페이지 픽스처 (로그인 세션 유지)
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
        yield AiReportPage(page)
        context.close()
        browser.close()


@pytest.fixture(scope="class")
def ai_report_page_guest() -> Iterator[AiReportPage]:
    """AI 리포트 페이지 픽스처 (비로그인 상태 — auth.json 미사용)
    FULLTC-212 전용: 로그인 유도 없이 서비스 중단 페이지 노출 검증
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
            # storage_state 미설정 → 비로그인 상태
        )
        page = context.new_page()
        yield AiReportPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-206 ~ 207  |  GNB 탭 검증
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("ai_report_page")
class TestAiReportGNBRegression:
    """GNB 'AI 리포트' 탭 노출 및 네비게이션 검증"""

    def test_FULLTC_206_gnb_aireport_tab_visible(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-206 | GNB | Minor
        GNB 상단 메뉴에 'AI 리포트' 탭이 노출되어야 한다.
        Steps: web-stg.bloomingbit.io 접속 → GNB 상단 메뉴 확인
        """
        ai_report_page.go_to_aireport_main()

        assert ai_report_page.is_gnb_visible(), \
            "[FAIL] GNB 헤더(header#headerContainer) 미노출"

        assert ai_report_page.is_gnb_aireport_tab_visible(), \
            "[FAIL] GNB에 'AI 리포트' 탭 미노출 — GNB_AIREPORT_TAB 셀렉터 확인 필요"

    def test_FULLTC_207_gnb_aireport_tab_click_navigates(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-207 | GNB | Major
        GNB 'AI 리포트' 탭 클릭 시 /report 페이지로 정상 이동해야 한다.
        Steps: web-stg.bloomingbit.io 접속 → GNB 'AI 리포트' 탭 클릭
        """
        # 메인 홈에서 출발 (GNB 탭 클릭 시나리오)
        ai_report_page.page.goto(
            ai_report_page.BASE_URL,
            wait_until="domcontentloaded",
        )
        ai_report_page.page.wait_for_timeout(500)

        ai_report_page.click_gnb_aireport_tab()

        assert ai_report_page.AIREPORT_MAIN_PATH in ai_report_page.page.url, \
            (
                f"[FAIL] GNB 'AI 리포트' 탭 클릭 후 /report 미이동 — "
                f"현재 URL: {ai_report_page.page.url}"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-208 ~ 213  |  서비스 일시 중단 페이지 UI 검증
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("ai_report_page")
class TestAiReportSuspensionRegression:
    """서비스 일시 중단 안내 페이지 UI 요소 및 접근 시나리오 검증"""

    def test_FULLTC_208_suspension_page_dark_bg_visible(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-208 | 서비스 일시 중단 | Major
        /report 접속 시 서비스 일시 중단 안내 페이지(다크 배경 전체 화면)가 노출되어야 한다.
        Steps: web-stg.bloomingbit.io/report 접속
        """
        ai_report_page.go_to_aireport_main()

        assert ai_report_page.is_suspension_page_visible(), \
            "[FAIL] 서비스 일시 중단 안내 페이지 미노출 — SUSPENSION_WRAPPER / MAIN_HEADING 셀렉터 확인 필요"

        assert ai_report_page.is_dark_background_visible(), \
            "[FAIL] 다크 배경 전체 화면 미노출 — SUSPENSION_WRAPPER 셀렉터 확인 필요"

    def test_FULLTC_209_suspension_pill_badge_visible(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-209 | 서비스 일시 중단 | Minor
        '서비스 일시 중단 및 전면 개편 안내' 필(pill) 배지가 노출되어야 한다.
        Steps: web-stg.bloomingbit.io/report 접속 → 페이지 상단 배지 요소 확인
        """
        ai_report_page.go_to_aireport_main()

        assert ai_report_page.is_suspension_badge_visible(), \
            "[FAIL] '서비스 일시 중단 및 전면 개편 안내' 필 배지 미노출 — SUSPENSION_BADGE 셀렉터 확인 필요"

        badge_text = ai_report_page.get_suspension_badge_text()
        if badge_text:
            assert ai_report_page.TEXT_BADGE in badge_text, \
                (
                    f"[FAIL] 필 배지 텍스트 불일치 — "
                    f"기대: '{ai_report_page.TEXT_BADGE}' / 실제: '{badge_text}'"
                )

    def test_FULLTC_210_brand_title_visible(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-210 | 서비스 일시 중단 | Minor
        'Ai Report by. STAT' 브랜드 타이틀이 노출되어야 한다.
        Steps: web-stg.bloomingbit.io/report 접속 → 페이지 브랜드 타이틀 확인
        """
        ai_report_page.go_to_aireport_main()

        assert ai_report_page.is_brand_title_visible(), \
            "[FAIL] 'Ai Report by. STAT' 브랜드 타이틀 미노출 — BRAND_TITLE 셀렉터 확인 필요"

        brand_text = ai_report_page.get_brand_title_text()
        if brand_text:
            assert ai_report_page.TEXT_BRAND_TITLE in brand_text, \
                (
                    f"[FAIL] 브랜드 타이틀 텍스트 불일치 — "
                    f"기대: '{ai_report_page.TEXT_BRAND_TITLE}' / 실제: '{brand_text}'"
                )

    def test_FULLTC_211_main_heading_and_body_text_visible(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-211 | 서비스 일시 중단 | Minor
        메인 제목과 안내 본문이 모두 노출되어야 한다.
        - 메인 제목 : 'AI 리포트, 더 강력한 모습으로 돌아옵니다'
        - 안내 본문 : '서비스 고도화를 위한 전면 개편을 잠시 준비 중이며...'
        Steps: web-stg.bloomingbit.io/report 접속 → 페이지 내 텍스트 요소 확인
        """
        ai_report_page.go_to_aireport_main()

        # 1) 메인 제목 검증
        assert ai_report_page.is_main_heading_visible(), \
            "[FAIL] 메인 제목 'AI 리포트, 더 강력한 모습으로 돌아옵니다' 미노출 — MAIN_HEADING 셀렉터 확인 필요"

        heading_text = ai_report_page.get_main_heading_text()
        if heading_text:
            assert ai_report_page.TEXT_MAIN_HEADING in heading_text, \
                (
                    f"[FAIL] 메인 제목 텍스트 불일치 — "
                    f"기대: '{ai_report_page.TEXT_MAIN_HEADING}' / 실제: '{heading_text}'"
                )

        # 2) 안내 본문 검증
        assert ai_report_page.is_body_text_visible(), \
            "[FAIL] 안내 본문 텍스트 '서비스 고도화를 위한 전면 개편' 미노출 — BODY_TEXT 셀렉터 확인 필요"

        body_text = ai_report_page.get_body_text()
        if body_text:
            assert ai_report_page.TEXT_BODY_SNIPPET in body_text, \
                (
                    f"[FAIL] 안내 본문 텍스트 불일치 — "
                    f"기대 포함: '{ai_report_page.TEXT_BODY_SNIPPET}' / 실제: '{body_text}'"
                )

    def test_FULLTC_213_logged_in_sees_suspension_page(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-213 | 서비스 일시 중단 | Minor
        로그인 상태에서 /report 직접 접속 시 서비스 일시 중단 페이지가 노출되어야 한다.
        (로그인/비로그인 구분 없이 동일한 중단 페이지 노출)
        Steps: 로그인 상태 → web-stg.bloomingbit.io/report URL 직접 입력 접속
        """
        ai_report_page.go_to_aireport_main()

        # 로그인 후에도 서비스 중단 페이지가 노출되어야 함
        assert ai_report_page.is_suspension_page_visible(), \
            "[FAIL] 로그인 상태에서 /report 접속 시 서비스 일시 중단 페이지 미노출"

        # 로그인 유도 모달이 떠서는 안 됨
        assert not ai_report_page.is_login_modal_visible(), \
            "[FAIL] 로그인 상태에서 /report 접속 시 로그인 모달이 노출됨 (비정상)"

        # 서비스 중단 페이지와 에러 페이지가 동시에 노출되면 안 됨
        assert not ai_report_page.is_error_page_visible(), \
            "[FAIL] 로그인 상태에서 /report 접속 시 에러 페이지 노출 (서비스 중단 페이지 정상 노출 기대)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-212  |  비로그인 접속 (guest 픽스처)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("ai_report_page_guest")
class TestAiReportGuestAccessRegression:
    """비로그인 상태 접속 검증 — ai_report_page_guest 픽스처 사용"""

    def test_FULLTC_212_guest_sees_suspension_page_no_login_modal(
        self, ai_report_page_guest: AiReportPage
    ) -> None:
        """
        FULLTC-212 | 서비스 일시 중단 | Minor
        비로그인 상태에서 /report 직접 접속 시 로그인 유도 없이
        서비스 일시 중단 안내 페이지가 정상 노출되어야 한다.
        Steps: 비로그인 상태 → web-stg.bloomingbit.io/report URL 직접 입력 접속
        """
        ai_report_page_guest.go_to_aireport_main()

        # 서비스 중단 페이지 노출 확인
        assert ai_report_page_guest.is_suspension_page_visible(), \
            "[FAIL] 비로그인 상태에서 /report 접속 시 서비스 일시 중단 안내 페이지 미노출"

        # 로그인 유도 모달이 노출되면 안 됨
        assert not ai_report_page_guest.is_login_modal_visible(), \
            "[FAIL] 비로그인 접속 시 로그인 유도 모달 노출 — /report는 비로그인도 중단 페이지 접근 가능해야 함"

        # 에러 페이지로 리다이렉트되면 안 됨
        assert not ai_report_page_guest.is_error_page_visible(), \
            "[FAIL] 비로그인 접속 시 에러 페이지 노출 (서비스 중단 페이지 정상 노출 기대)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-214 ~ 215  |  서브 경로 에러 페이지 검증
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("ai_report_page")
class TestAiReportSubPathRegression:
    """서브 경로(/report/list, /report/{id}) 접근 시 에러 페이지 노출 검증"""

    def test_FULLTC_214_report_list_path_shows_error_page(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-214 | 서브 경로 접근 | Minor
        /report/list 접속 시 에러 페이지('이용에 불편을 드려 죄송합니다...') 가 노출되어야 한다.
        Steps: web-stg.bloomingbit.io/report/list URL 직접 입력 접속
        """
        ai_report_page.go_to_aireport_list()

        assert ai_report_page.is_error_page_visible(), \
            (
                "[FAIL] /report/list 접속 시 에러 페이지 미노출 — "
                "ERROR_PAGE 셀렉터 또는 ERROR_TEXT_SNIPPET 확인 필요 / "
                f"현재 URL: {ai_report_page.page.url}"
            )

        # 서비스 중단 페이지(정상 /report 페이지)로 리디렉션 되면 안 됨
        assert not ai_report_page.is_url_report_main(), \
            "[FAIL] /report/list 접속 시 /report 메인으로 리디렉션됨 (에러 페이지 노출 기대)"

    def test_FULLTC_215_report_invalid_id_shows_error_page(self, ai_report_page: AiReportPage) -> None:
        """
        FULLTC-215 | 서브 경로 접근 | Minor
        존재하지 않는 리포트 ID(/report/999999) 접속 시 에러 페이지가 노출되어야 한다.
        정상 페이지로 리디렉션 되면 안 된다.
        Steps: web-stg.bloomingbit.io/report/999999 URL 직접 입력 접속
        """
        ai_report_page.go_to_aireport_invalid_id("999999")

        assert ai_report_page.is_error_page_visible(), \
            (
                "[FAIL] /report/999999 접속 시 에러 페이지 미노출 — "
                "ERROR_PAGE 셀렉터 또는 ERROR_TEXT_SNIPPET 확인 필요 / "
                f"현재 URL: {ai_report_page.page.url}"
            )

        # /report 메인(서비스 중단 페이지)으로 리디렉션 되면 안 됨
        assert not ai_report_page.is_url_report_main(), \
            "[FAIL] /report/999999 접속 시 /report 메인으로 리디렉션됨 (에러 페이지 노출 기대)"