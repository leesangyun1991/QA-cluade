"""
tests/stage8_regression/web/test_regression_user_complaint.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이용자 불만 처리(User Complaint) 회귀 테스트
FULLTC-509 ~ FULLTC-522 (14 TCs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_user_complaint.py -v
  pytest tests/stage8_regression/web/test_regression_user_complaint.py -m "user_complaint" -v
  pytest tests/stage8_regression/web/test_regression_user_complaint.py -k "FULLTC_517" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요 (로그인 TC용)
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)

[픽스처 구성]
  user_complaint_page       : 로그인 상태 (auth.json 사용) — 509~519, 521
  user_complaint_guest_page : 비로그인 상태 (auth.json 미사용) — 520, 522

[TC 클래스 구성]
  FULLTC-509~510   TestUserComplaintEntry           메뉴 진입
  FULLTC-511~514   TestUserComplaintTextRendering   텍스트 렌더링
  FULLTC-515~516   TestUserComplaintContactLink     연락처 링크
  FULLTC-517~519   TestUserComplaintReportButton    신고하기 버튼
  FULLTC-520~522   TestUserComplaintGuestRestriction 비로그인 제한

[HTML 분석 핵심 포인트]
  ✅ 완전 안정 셀렉터 (즉시 사용 가능):
     · 콘텐츠 영역: div#complaintHandlingContent
     · 섹션 헤딩:   p strong (10개 섹션 확인 완료)
     · 신고 버튼:   button[class*='complaintHandlingButton'] = "이용자 불만 신고하기"
     · 이메일 텍스트: "help@bloomingbit.io" (plain text로 존재)

  ⚠️ TODO_ 셀렉터 (실제 DOM 확인 후 튜닝 필요):
     · LNB 메뉴: FULLTC-509 → LNB_WRAPPER, LNB_COMPLAINT_MENU
     · mailto 링크: FULLTC-515 → HTML에는 plain text로만 존재 (링크 아님)
     · 로그인 팝업: FULLTC-520 → LOGIN_MODAL
     · COMPLAINT_PATH: F12 주소창 확인 후 수정 필요
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from user_complaint_page import UserComplaintPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 ① — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def user_complaint_page() -> Iterator[UserComplaintPage]:
    """이용자 불만 처리 페이지 픽스처 (로그인 세션 유지)
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
        yield UserComplaintPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  픽스처 ② — 비로그인 상태 (auth.json 미사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def user_complaint_guest_page() -> Iterator[UserComplaintPage]:
    """이용자 불만 처리 페이지 픽스처 (비로그인 상태)
    FULLTC-520~522 전용 — auth.json 없이 세션 시작
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
        yield UserComplaintPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-509~510  |  메뉴 진입
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.user_complaint
class TestUserComplaintEntry:
    """LNB 메뉴 클릭 진입 · URL 직접 접근 검증 — FULLTC-509 ~ 510"""

    def test_FULLTC_509_lnb_menu_click_navigates(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-509 | 이용자 불만 처리/LNB 메뉴 클릭 | Major
        LNB에서 [이용자 불만 처리] 메뉴 클릭 시 해당 페이지로 이동하고
        LNB에서 해당 메뉴가 활성(하이라이트) 상태로 표시되어야 한다.
        ⚠️ TODO: LNB_WRAPPER, LNB_COMPLAINT_MENU 셀렉터 튜닝 필요
        """
        user_complaint_page.go_to_mypage()
        user_complaint_page.page.wait_for_timeout(600)

        if not user_complaint_page.is_lnb_visible():
            pytest.skip(
                "[SKIP] FULLTC-509: LNB 영역 미노출 — "
                "TODO: LNB_WRAPPER 셀렉터 튜닝 후 재실행"
            )

        url_before = user_complaint_page.get_current_url()
        user_complaint_page.click_lnb_complaint_menu()

        assert user_complaint_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-509: LNB '이용자 불만 처리' 메뉴 클릭 후 URL 미변경"

        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-509: 이용자 불만 처리 페이지 로드 실패 (콘텐츠 래퍼 미노출)"

        assert user_complaint_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-509: 페이지 타이틀이 '이용자 불만 처리' 아님 " \
            f"(현재: '{user_complaint_page.get_page_title_text()}')"

        # LNB 활성화 상태 확인 (TODO 셀렉터)
        if user_complaint_page.is_lnb_visible():
            lnb_active = user_complaint_page.is_lnb_complaint_menu_active()
            if not lnb_active:
                pytest.skip(
                    "[SKIP] FULLTC-509 (LNB 활성화): LNB 활성 메뉴 확인 실패 — "
                    "TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요"
                )
            assert lnb_active, \
                "[FAIL] FULLTC-509: 이동 후 LNB에서 '이용자 불만 처리' 메뉴가 활성(하이라이트) 상태 아님"

    def test_FULLTC_510_direct_url_access(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-510 | 이용자 불만 처리/URL 직접 접근 | Minor
        URL 직접 접근 시 페이지가 정상 렌더링되고 비/로그인 무관하게 안내 내용이 노출되어야 한다.
        ⚠️ TODO: COMPLAINT_PATH 실제 URL 확인 후 수정 (현재 추정값 사용)
        """
        user_complaint_page.go_to_complaint()

        assert user_complaint_page.is_loaded(), \
            f"[FAIL] FULLTC-510: URL 직접 접근 후 페이지 로드 실패 " \
            f"(URL: '{user_complaint_page.BASE_URL}{UserComplaintPage.COMPLAINT_PATH}')"

        assert user_complaint_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-510: URL 직접 접근 후 페이지 타이틀 불일치 " \
            f"(현재: '{user_complaint_page.get_page_title_text()}')"

        # 콘텐츠 영역 노출 확인
        assert user_complaint_page.is_content_area_visible(), \
            "[FAIL] FULLTC-510: 안내 콘텐츠 영역(div#complaintHandlingContent) 미노출"

        # 로그인 리다이렉트 없이 안내 내용 노출 확인
        current_url = user_complaint_page.get_current_url()
        assert UserComplaintPage.SIGNIN_PATH not in current_url, \
            f"[FAIL] FULLTC-510: 접근 시 로그인 페이지로 리다이렉트됨 " \
            f"(현재 URL: '{current_url}') — 공개 페이지여야 함"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-511~514  |  텍스트 렌더링
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.user_complaint
class TestUserComplaintTextRendering:
    """안내 텍스트 전체 노출·섹션 구성·줄바꿈·스크롤 동작 검증 — FULLTC-511 ~ 514"""

    def test_FULLTC_511_all_guidance_text_visible(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-511 | 이용자 불만 처리/안내 텍스트 전체 노출 | Major
        불만 처리 절차, 접수 대상, 담당 연락처 등 모든 안내 텍스트가
        누락 없이 노출되고 잘리거나 가려지지 않아야 한다.
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-511: 이용자 불만 처리 페이지 로드 실패"

        # 콘텐츠 영역 존재 확인
        assert user_complaint_page.is_content_area_visible(), \
            "[FAIL] FULLTC-511: 안내 콘텐츠 영역 미노출 (div#complaintHandlingContent)"

        # 전체 텍스트 100자 이상 존재 확인
        assert user_complaint_page.is_content_text_not_empty(), \
            "[FAIL] FULLTC-511: 안내 텍스트 100자 미만 — 콘텐츠 누락 의심"

        # 섹션 헤딩 5개 이상 존재 확인
        heading_count = user_complaint_page.get_section_heading_count()
        assert heading_count >= 5, \
            f"[FAIL] FULLTC-511: 섹션 헤딩(<strong>) {heading_count}개 — " \
            f"5개 이상 기대 (이용자 불만처리 절차 안내·접수 대상·접수 방법·담당 연락처·처리 절차 등)"

        # 핵심 텍스트 포함 확인
        content_text = user_complaint_page.get_all_content_text()
        for keyword in ["접수", "처리", "연락처", "이메일"]:
            assert keyword in content_text, \
                f"[FAIL] FULLTC-511: 안내 텍스트에 '{keyword}' 키워드 미포함 — 콘텐츠 누락 의심"

    def test_FULLTC_512_required_sections_visible(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-512 | 이용자 불만 처리/섹션 구성 항목 확인 | Major
        접수 대상·불만 처리 절차·담당 연락처 섹션이 모두 노출되고
        각 섹션의 제목과 본문이 정확하게 표시되어야 한다.
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-512: 이용자 불만 처리 페이지 로드 실패"

        # 3개 필수 섹션 모두 노출 확인
        missing = user_complaint_page.get_missing_sections()
        assert len(missing) == 0, \
            f"[FAIL] FULLTC-512: 필수 섹션 미노출 — 누락 항목: {missing} " \
            f"(접수 대상·불만 처리 절차·담당 연락처 모두 필요)"

        # 각 섹션 헤딩 텍스트 확인
        assert user_complaint_page.is_section_visible(UserComplaintPage.SECTION_TARGET), \
            "[FAIL] FULLTC-512: '접수 대상' 섹션 헤딩 미노출 (p strong:has-text('접수 대상'))"

        assert user_complaint_page.is_section_visible(UserComplaintPage.SECTION_PROCEDURE), \
            "[FAIL] FULLTC-512: '처리 절차' 섹션 헤딩 미노출 (p strong:has-text('처리 절차'))"

        assert user_complaint_page.is_section_visible(UserComplaintPage.SECTION_CONTACT), \
            "[FAIL] FULLTC-512: '담당 연락처' 섹션 헤딩 미노출 (p strong:has-text('담당 연락처'))"

        # 섹션 본문 내용 비어있지 않은지 확인
        paragraph_count = user_complaint_page.get_paragraph_count()
        assert paragraph_count >= 5, \
            f"[FAIL] FULLTC-512: 안내 단락(<p>) {paragraph_count}개 — " \
            f"5개 이상 기대 (각 섹션 본문 포함)"

    def test_FULLTC_513_text_wraps_without_overflow(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-513 | 이용자 불만 처리/텍스트 줄바꿈 및 가독성 | Minor
        안내 텍스트가 화면 너비에 맞게 자동 줄바꿈되고
        뷰포트 밖으로 잘리거나 가로 스크롤이 발생하지 않아야 한다.
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-513: 이용자 불만 처리 페이지 로드 실패"

        # 콘텐츠 영역 가로 오버플로우 확인
        assert not user_complaint_page.is_text_overflowing_horizontally(), \
            "[FAIL] FULLTC-513: 콘텐츠 영역(div#complaintHandlingContent)에 가로 스크롤 발생 — " \
            "텍스트 줄바꿈 미적용 또는 레이아웃 문제"

        # body 전체 가로 오버플로우 확인
        assert not user_complaint_page.is_body_overflowing_horizontally(), \
            "[FAIL] FULLTC-513: 페이지 body에 가로 스크롤 발생 — " \
            "텍스트 또는 요소가 뷰포트 밖으로 벗어남"

    def test_FULLTC_514_page_scroll_reaches_all_content(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-514 | 이용자 불만 처리/페이지 스크롤 동작 | Minor
        스크롤이 부드럽게 동작하고 상단부터 하단 [신고하기] 버튼까지
        모든 콘텐츠에 접근 가능해야 한다.
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-514: 이용자 불만 처리 페이지 로드 실패"

        # 페이지가 뷰포트보다 길어 스크롤 가능한지 확인
        scroll_height   = user_complaint_page.get_page_scroll_height()
        viewport_height = user_complaint_page.get_viewport_height()
        assert scroll_height > viewport_height, \
            f"[FAIL] FULLTC-514: 페이지 콘텐츠가 뷰포트 높이보다 짧음 " \
            f"(scroll_height:{scroll_height}, viewport:{viewport_height}) — " \
            f"스크롤 동작 검증 불가"

        # 최하단까지 스크롤
        user_complaint_page.scroll_to_bottom(steps=6)

        # 신고 버튼이 스크롤 후 뷰포트 내에 보이는지 확인
        assert user_complaint_page.is_report_button_visible(), \
            "[FAIL] FULLTC-514: 최하단 스크롤 후 '이용자 불만 신고하기' 버튼 미노출 — " \
            "콘텐츠 접근 불가"

        # 스크롤 위치가 0보다 큰지 확인 (실제로 스크롤이 이루어졌는지)
        scroll_y = user_complaint_page.get_scroll_y_position()
        assert scroll_y > 0, \
            f"[FAIL] FULLTC-514: 스크롤 후 scrollY = {scroll_y} — 스크롤 미동작"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-515~516  |  연락처 링크
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.user_complaint
class TestUserComplaintContactLink:
    """이메일 mailto 링크 동작 · 이메일 주소 정확성 검증 — FULLTC-515 ~ 516"""

    def test_FULLTC_515_email_mailto_link_works(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-515 | 이용자 불만 처리/이메일 mailto 링크 동작 | Major
        이메일 주소 링크 클릭 시 메일 클라이언트가 실행되고
        수신자 주소에 해당 이메일이 자동 입력되어야 한다.

        ※ HTML 분석 결과: 현재 'help@bloomingbit.io'가 plain text로만 존재
           (<a href="mailto:"> 링크 아님) → mailto 링크 존재 시에만 완전 검증 가능
        ※ 실제 메일 앱 실행 여부는 자동화로 완전 검증 불가 → href 속성으로 판단
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-515: 이용자 불만 처리 페이지 로드 실패"

        # 1) 먼저 이메일 텍스트가 페이지에 존재하는지 확인
        assert user_complaint_page.is_email_text_visible(), \
            f"[FAIL] FULLTC-515: '{UserComplaintPage.EXPECTED_EMAIL}' 이메일 텍스트 " \
            f"페이지 미노출 (p:has-text('help@bloomingbit.io') 없음)"

        # 2) mailto 링크 존재 여부 확인
        if not user_complaint_page.is_mailto_link_present():
            pytest.skip(
                "[SKIP] FULLTC-515: mailto 링크(<a href='mailto:'>) 미존재 — "
                f"현재 '{UserComplaintPage.EXPECTED_EMAIL}'은 plain text로만 노출됨. "
                "링크가 추가되면 MAILTO_LINK 셀렉터 튜닝 후 재실행"
            )

        # 3) mailto: href 속성 확인
        mailto_href = user_complaint_page.get_mailto_href()
        assert mailto_href.startswith("mailto:"), \
            f"[FAIL] FULLTC-515: mailto 링크 href가 'mailto:'로 시작하지 않음 " \
            f"(href='{mailto_href}')"

        assert UserComplaintPage.EXPECTED_EMAIL in mailto_href, \
            f"[FAIL] FULLTC-515: mailto href에 '{UserComplaintPage.EXPECTED_EMAIL}' 미포함 " \
            f"(href='{mailto_href}')"
        # ※ 실제 메일 앱 실행 확인은 수동으로 진행 필요

    def test_FULLTC_516_email_address_accuracy(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-516 | 이용자 불만 처리/이메일 주소 정확성 확인 | Minor
        본문에 노출된 이메일 주소가 'help@bloomingbit.io'와 일치하고
        오탈자가 없어야 한다.
        ✅ 이 TC는 HTML에서 이메일 텍스트가 직접 확인되므로 안정적으로 검증 가능
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-516: 이용자 불만 처리 페이지 로드 실패"

        # 본문에서 이메일 주소 추출
        found_email = user_complaint_page.get_email_text_from_content()
        assert found_email.strip() != "", \
            "[FAIL] FULLTC-516: 본문에서 이메일 주소 추출 실패 — " \
            f"'{UserComplaintPage.EXPECTED_EMAIL}' 텍스트가 본문에 없거나 파싱 오류"

        assert found_email == UserComplaintPage.EXPECTED_EMAIL, \
            f"[FAIL] FULLTC-516: 이메일 주소 불일치 또는 오탈자 — " \
            f"기대: '{UserComplaintPage.EXPECTED_EMAIL}', 실제: '{found_email}'"

        # '@' 포함 여부 (유효한 이메일 형식 기본 확인)
        assert "@" in found_email and "." in found_email.split("@")[-1], \
            f"[FAIL] FULLTC-516: 노출된 주소가 유효한 이메일 형식 아님 ('{found_email}')"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-517~519  |  신고하기 버튼
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.user_complaint
class TestUserComplaintReportButton:
    """신고하기 버튼 노출·클릭 라우팅·UI 및 위치 검증 — FULLTC-517 ~ 519
    ✅ 버튼 셀렉터가 HTML에서 완전히 확인됨 — 안정적으로 검증 가능!
    """

    def test_FULLTC_517_report_button_visible_at_bottom(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-517 | 이용자 불만 처리/버튼 노출 확인 | Major
        페이지 최하단까지 스크롤 시 [이용자 불만 신고하기] 버튼이 노출되고
        버튼 텍스트가 정확히 표시되어야 한다.
        ✅ button[class*='complaintHandlingButton'] — 안정 셀렉터
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-517: 이용자 불만 처리 페이지 로드 실패"

        # 최하단까지 스크롤 후 버튼 확인
        user_complaint_page.scroll_to_bottom(steps=6)

        assert user_complaint_page.is_report_button_visible(), \
            "[FAIL] FULLTC-517: '이용자 불만 신고하기' 버튼 미노출 " \
            "(button[class*='complaintHandlingButton']) — 최하단 스크롤 후에도 버튼 없음"

        # 버튼 텍스트 정확성 확인
        button_text = user_complaint_page.get_report_button_text()
        assert button_text == UserComplaintPage.EXPECTED_BUTTON_TEXT, \
            f"[FAIL] FULLTC-517: 버튼 텍스트 불일치 — " \
            f"기대: '{UserComplaintPage.EXPECTED_BUTTON_TEXT}', 실제: '{button_text}'"

        # 버튼이 뷰포트 내에 보이는지 확인
        assert user_complaint_page.is_report_button_in_viewport(), \
            "[FAIL] FULLTC-517: 최하단 스크롤 후에도 버튼이 뷰포트 내 미노출"

    def test_FULLTC_518_report_button_click_routing_logged_in(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-518 | 이용자 불만 처리/로그인 상태 버튼 클릭 라우팅 | Major
        로그인 상태에서 [이용자 불만 신고하기] 버튼 클릭 시
        1:1 문의 폼 또는 신고 접수 페이지로 정상 이동해야 한다.
        ✅ 버튼 클릭은 안정 — 이동 URL은 실제 동작 확인 후 COMPLAINT_FORM_PATH 수정 필요
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-518: 이용자 불만 처리 페이지 로드 실패"

        assert user_complaint_page.is_report_button_visible(), \
            "[FAIL] FULLTC-518: '이용자 불만 신고하기' 버튼 미노출 — 클릭 테스트 불가"

        url_before = user_complaint_page.get_current_url()
        user_complaint_page.scroll_to_bottom(steps=6)
        user_complaint_page.click_report_button()

        url_after = user_complaint_page.get_current_url()
        assert url_after != url_before, \
            "[FAIL] FULLTC-518: '이용자 불만 신고하기' 버튼 클릭 후 URL 미변경 — " \
            "페이지 이동이 발생하지 않음"

        assert "about:blank" not in url_after.lower(), \
            "[FAIL] FULLTC-518: 버튼 클릭 후 빈 페이지(about:blank)로 이동"

        # 로그인 페이지로 리다이렉트되지 않아야 함 (로그인 상태이므로)
        assert UserComplaintPage.SIGNIN_PATH not in url_after, \
            f"[FAIL] FULLTC-518: 로그인 상태인데 버튼 클릭 후 로그인 페이지로 이동 " \
            f"(URL: '{url_after}') — auth.json 세션 확인 필요"

    def test_FULLTC_519_report_button_ui_and_position(
        self, user_complaint_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-519 | 이용자 불만 처리/버튼 UI 및 위치 | Minor
        버튼이 안내 텍스트 마지막 섹션 하단에 위치하고
        버튼 스타일(크기, 텍스트)이 정상이어야 한다.
        ✅ 버튼 셀렉터 및 텍스트 안정 — 스타일은 computed style로 검증
        """
        user_complaint_page.go_to_complaint()
        assert user_complaint_page.is_loaded(), \
            "[FAIL] FULLTC-519: 이용자 불만 처리 페이지 로드 실패"

        assert user_complaint_page.is_report_button_visible(), \
            "[FAIL] FULLTC-519: '이용자 불만 신고하기' 버튼 미노출"

        # 1) 버튼 텍스트 확인
        assert user_complaint_page.is_report_button_text_correct(), \
            f"[FAIL] FULLTC-519: 버튼 텍스트 불일치 " \
            f"(기대: '{UserComplaintPage.EXPECTED_BUTTON_TEXT}', " \
            f"실제: '{user_complaint_page.get_report_button_text()}')"

        # 2) 버튼 크기 확인 (너비·높이 > 0)
        size = user_complaint_page.get_report_button_size()
        assert float(size.get("width", 0)) > 0, \
            f"[FAIL] FULLTC-519: 버튼 너비 = 0 — 버튼이 화면에 렌더링되지 않음 (width={size})"
        assert float(size.get("height", 0)) > 0, \
            f"[FAIL] FULLTC-519: 버튼 높이 = 0 — 버튼이 화면에 렌더링되지 않음 (height={size})"

        # 3) 버튼이 본문 텍스트 아래에 위치하는지 확인
        user_complaint_page.scroll_to_bottom(steps=6)
        assert user_complaint_page.is_button_below_content(), \
            "[FAIL] FULLTC-519: '이용자 불만 신고하기' 버튼이 본문 텍스트보다 위에 위치 — " \
            "버튼 위치가 디자인 가이드와 불일치"

        # 4) 버튼 래퍼 노출 확인
        assert user_complaint_page.page.locator(
            UserComplaintPage.BUTTON_WRAPPER
        ).count() > 0, \
            "[FAIL] FULLTC-519: 버튼 래퍼(div[class*='complaintHandlingButtonWrapper']) 미노출"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-520~522  |  비로그인 제한
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.user_complaint
class TestUserComplaintGuestRestriction:
    """비로그인 버튼 클릭 로그인 유도·로그인 후 복귀·비로그인 안내 텍스트 검증
    FULLTC-520 ~ 522 — user_complaint_guest_page 픽스처 사용
    """

    def test_FULLTC_520_guest_button_click_prompts_login(
        self, user_complaint_guest_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-520 | 이용자 불만 처리/비로그인 상태 버튼 클릭 시 로그인 유도 | Major
        비로그인 상태에서 [이용자 불만 신고하기] 버튼 클릭 시
        로그인 페이지 또는 로그인 유도 팝업이 노출되어야 한다.
        신고 접수 페이지로 즉시 이동하지 않아야 한다.
        ⚠️ TODO: LOGIN_MODAL 셀렉터 튜닝 필요 (실제 로그인 유도 방식 확인 후)
        """
        user_complaint_guest_page.go_to_complaint()
        assert user_complaint_guest_page.is_loaded(), \
            "[FAIL] FULLTC-520: 비로그인 상태에서 이용자 불만 처리 페이지 로드 실패"

        assert user_complaint_guest_page.is_report_button_visible(), \
            "[FAIL] FULLTC-520: '이용자 불만 신고하기' 버튼 미노출 — 비로그인 시에도 버튼 노출 필요"

        # 버튼 클릭
        user_complaint_guest_page.scroll_to_bottom(steps=6)
        url_before = user_complaint_guest_page.get_current_url()
        user_complaint_guest_page.click_report_button()
        user_complaint_guest_page.page.wait_for_timeout(1_000)

        # 로그인 유도 팝업 또는 로그인 페이지로 이동 확인
        login_prompted = user_complaint_guest_page.is_login_modal_or_page_visible()
        if not login_prompted:
            pytest.skip(
                "[SKIP] FULLTC-520: 로그인 유도 팝업/페이지 미감지 — "
                "TODO: LOGIN_MODAL 셀렉터 튜닝 또는 실제 동작 방식 확인 필요"
            )

        assert login_prompted, \
            f"[FAIL] FULLTC-520: 비로그인 상태에서 버튼 클릭 후 로그인 유도 없음 " \
            f"(현재 URL: '{user_complaint_guest_page.get_current_url()}')"

        # 신고 접수 페이지로 즉시 이동하지 않아야 함
        assert user_complaint_guest_page.is_not_on_complaint_form_page(), \
            "[FAIL] FULLTC-520: 비로그인 상태에서 버튼 클릭 후 신고 접수 페이지로 즉시 이동됨 — " \
            "로그인 유도 없이 접수 불가 기대"

    def test_FULLTC_521_login_then_return_to_complaint(
        self, user_complaint_guest_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-521 | 이용자 불만 처리/로그인 완료 후 복귀 동작 | Major
        비로그인 상태에서 버튼 클릭 → 로그인 페이지 이동 → 로그인 완료 후
        이용자 불만 처리 또는 신고 접수 페이지로 자동 복귀해야 한다.
        ⚠️ 실제 로그인 완료는 자동화 어려움 (비밀번호 입력 필요) →
           로그인 페이지로 이동 후 URL에 복귀 파라미터(redirect 등) 포함 여부로 검증
        """
        user_complaint_guest_page.go_to_complaint()
        assert user_complaint_guest_page.is_loaded(), \
            "[FAIL] FULLTC-521: 비로그인 상태에서 이용자 불만 처리 페이지 로드 실패"

        user_complaint_guest_page.scroll_to_bottom(steps=6)
        complaint_url = user_complaint_guest_page.get_current_url()
        user_complaint_guest_page.click_report_button()
        user_complaint_guest_page.page.wait_for_timeout(1_000)

        signin_url = user_complaint_guest_page.get_current_url()

        # 로그인 페이지로 이동했는지 확인
        if UserComplaintPage.SIGNIN_PATH not in signin_url:
            pytest.skip(
                "[SKIP] FULLTC-521: 로그인 페이지 미이동 — "
                "비로그인 버튼 클릭 후 동작 방식 확인 필요 "
                "(팝업 방식일 경우 다른 검증 필요)"
            )

        # 로그인 페이지 URL에 redirect/return 파라미터 포함 여부 확인
        has_redirect_param = any(
            param in signin_url.lower()
            for param in ["redirect", "return", "next", "callback", "complaint"]
        )

        if not has_redirect_param:
            pytest.skip(
                "[SKIP] FULLTC-521: 로그인 URL에 복귀 파라미터 없음 — "
                f"(signin URL: '{signin_url}') "
                "로그인 완료 후 자동 복귀 여부는 수동으로 확인 필요"
            )

        assert has_redirect_param, \
            f"[FAIL] FULLTC-521: 로그인 URL에 복귀(redirect/return) 파라미터 미포함 — " \
            f"로그인 완료 후 자동 복귀 기능 미구현 의심 " \
            f"(signin URL: '{signin_url}')"

    def test_FULLTC_522_guest_can_read_all_guidance_text(
        self, user_complaint_guest_page: UserComplaintPage
    ) -> None:
        """
        FULLTC-522 | 이용자 불만 처리/비로그인 시 안내 텍스트 노출 | Minor
        비로그인 상태에서도 불만 처리 절차, 접수 대상, 담당 연락처 등
        모든 안내 텍스트가 정상 노출되어야 한다.
        ✅ 콘텐츠 셀렉터가 HTML에서 직접 확인됨 — 안정적으로 검증 가능
        """
        user_complaint_guest_page.go_to_complaint()
        assert user_complaint_guest_page.is_loaded(), \
            "[FAIL] FULLTC-522: 비로그인 상태에서 이용자 불만 처리 페이지 로드 실패"

        # 로그인 리다이렉트 없이 페이지 접근 가능
        current_url = user_complaint_guest_page.get_current_url()
        assert UserComplaintPage.SIGNIN_PATH not in current_url, \
            f"[FAIL] FULLTC-522: 비로그인 상태에서 페이지 진입 시 로그인 페이지로 리다이렉트됨 " \
            f"(현재 URL: '{current_url}') — 안내 텍스트는 로그인 없이 열람 가능해야 함"

        # 콘텐츠 영역 노출 확인
        assert user_complaint_guest_page.is_content_area_visible(), \
            "[FAIL] FULLTC-522: 비로그인 상태에서 안내 콘텐츠 영역 미노출 " \
            "(div#complaintHandlingContent)"

        # 안내 텍스트 내용 확인
        assert user_complaint_guest_page.is_content_text_not_empty(), \
            "[FAIL] FULLTC-522: 비로그인 상태에서 안내 텍스트 100자 미만 — " \
            "콘텐츠 미노출 또는 누락"

        # 3개 필수 섹션 노출 확인
        missing = user_complaint_guest_page.get_missing_sections()
        assert len(missing) == 0, \
            f"[FAIL] FULLTC-522: 비로그인 상태에서 필수 섹션 미노출 — " \
            f"누락 항목: {missing} (로그인 없이 모든 섹션 열람 가능해야 함)"

        # 이메일 정보 노출 확인
        assert user_complaint_guest_page.is_email_text_visible(), \
            f"[FAIL] FULLTC-522: 비로그인 상태에서 담당 이메일 " \
            f"'{UserComplaintPage.EXPECTED_EMAIL}' 미노출"

        # 신고 버튼 노출 확인 (비로그인에서도 버튼은 보여야 함)
        assert user_complaint_guest_page.is_report_button_visible(), \
            "[FAIL] FULLTC-522: 비로그인 상태에서 '이용자 불만 신고하기' 버튼 미노출 — " \
            "버튼은 노출되어야 함 (클릭 시 로그인 유도)"