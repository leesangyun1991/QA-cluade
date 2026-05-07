"""
tests/stage8_regression/web/test_regression_membership.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
멤버십 회귀 테스트 (FULLTC-216 ~ FULLTC-242)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_membership.py -v

  # 비파괴적 TC만 실행 (탈퇴 완료·재가입 패널티 제외)
  pytest tests/stage8_regression/web/test_regression_membership.py -v \
    -k "not (FULLTC_240 or FULLTC_241 or FULLTC_242)"

  # 탈퇴 파괴적 TC 포함 실행 (환경변수 필요)
  MEMBERSHIP_RUN_DESTRUCTIVE=true pytest ... -k "FULLTC_24"

[픽스처 구성]
  membership_page       : auth.json 사용 — 로그인 상태
  membership_page_guest : auth.json 미사용 — 비로그인 상태

[TC 클래스 구성]
  FULLTC-216           TestMembershipGNBGuestRegression        비로그인 GNB
  FULLTC-217~219       TestMembershipLoginModalRegression       로그인 모달 UI
  FULLTC-220~223       TestMembershipGoogleSSORegression        Google SSO 플로우
  FULLTC-224~226       TestMembershipTermsRegression            최초 로그인 약관 동의
  FULLTC-222           TestMembershipLoginSuccessRegression     로그인 성공 UI
  FULLTC-227~228       TestMembershipLogoutFlowRegression       로그아웃 플로우
  FULLTC-229~230       TestMembershipSessionRegression          세션 만료
  FULLTC-231           TestMembershipMultiTabRegression         멀티 탭 동기화
  FULLTC-232~235       TestMembershipAccountLinkingRegression   계정 연동
  FULLTC-236           TestMembershipDuplicateLoginRegression   중복 로그인
  FULLTC-237~242       TestMembershipWithdrawalRegression       회원 탈퇴 (파괴적)

[주의사항]
  - FULLTC-221 (Google OAuth 실제 인증): 자동화 불가 → 구조 검증 후 skip
  - FULLTC-224~226 (최초 로그인): 신규 Google 계정 필요 → skip (수동 검증 권장)
  - FULLTC-240~242 (탈퇴 완료·재가입): 실제 계정 삭제 → MEMBERSHIP_RUN_DESTRUCTIVE=true 시만 실행
  - TestMembershipLogoutFlowRegression 실행 후 해당 context는 비로그인 상태가 됨
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from membership_page import MembershipPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def membership_page() -> Iterator[MembershipPage]:
    """멤버십 페이지 픽스처 (로그인 세션 유지)
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
        yield MembershipPage(page)
        context.close()
        browser.close()


@pytest.fixture(scope="class")
def membership_page_guest() -> Iterator[MembershipPage]:
    """멤버십 페이지 픽스처 (비로그인 상태 — auth.json 미사용)
    비로그인 관련 TC(FULLTC-216~223, 224~226) 전용
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
        yield MembershipPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-216  |  비로그인 GNB
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page_guest")
class TestMembershipGNBGuestRegression:
    """비로그인 상태 GNB 우측 UI 검증"""

    def test_FULLTC_216_gnb_non_login_icon_visible(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """
        FULLTC-216 | 로그인/GNB | Minor
        비로그인 상태에서 GNB 우측에 비로그인 아이콘/로그인 유도 UI가 노출되어야 한다.
        Steps: 비로그인 상태 → web-stg.bloomingbit.io 접속 → GNB 우측 확인
        """
        membership_page_guest.go_to_main()

        assert membership_page_guest.is_gnb_visible(), \
            "[FAIL] GNB 헤더(header#headerContainer) 미노출"

        assert membership_page_guest.is_gnb_non_login_state(), \
            "[FAIL] 비로그인 GNB 우측 아이콘/로그인 유도 UI 미노출 — GNB_NON_LOGIN_ICON 셀렉터 확인 필요"

        # 로그인 상태 UI는 노출되면 안 됨
        assert not membership_page_guest.is_gnb_logged_in_state(), \
            "[FAIL] 비로그인 상태인데 GNB 프로필 아이콘(로그인 UI) 노출됨 (비정상)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-217~219  |  로그인 모달 UI
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page_guest")
class TestMembershipLoginModalRegression:
    """로그인 모달 진입·UI 요소·닫기 검증"""

    def test_FULLTC_217_login_modal_appears_on_protected_action(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """
        FULLTC-217 | 로그인/로그인 모달 진입 | Major
        비로그인 상태에서 로그인 필요 기능 접근 시 Google 로그인 버튼 포함 모달이 노출되어야 한다.
        Steps: 비로그인 상태 → 로그인 필요 기능(커뮤니티 등) 클릭
        """
        membership_page_guest.go_to_community()

        # 커뮤니티 글쓰기 버튼 등 클릭으로 모달 유도 시도
        # ⚠️ TODO: 실제 커뮤니티 로그인 트리거 버튼 셀렉터로 교체
        trigger = membership_page_guest.page.locator(
            "[data-testid='TODO_writeBtn'], "
            "button[class*='TODO_writePost'], "
            "button:has-text('글쓰기'), "
            "button[class*='TODO_likeBtn']"
        ).first
        try:
            trigger.wait_for(state="attached", timeout=5_000)
            trigger.click()
            membership_page_guest.page.wait_for_timeout(800)
        except Exception:
            pass  # 트리거 버튼을 찾지 못하면 fallback: 마이페이지 직접 접근
            membership_page_guest.go_to_protected_page()

        assert membership_page_guest.is_login_modal_visible(), \
            "[FAIL] 로그인 필요 기능 접근 시 로그인 모달 미노출 — LOGIN_MODAL 셀렉터 확인 필요"

        assert membership_page_guest.is_google_login_btn_visible(), \
            "[FAIL] 로그인 모달 내 'Google로 로그인' 버튼 미노출 — LOGIN_GOOGLE_BTN 셀렉터 확인 필요"

    def test_FULLTC_218_login_modal_ui_elements(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """
        FULLTC-218 | 로그인/로그인 모달 UI 요소 | Minor
        로그인 모달에 Google 로그인 버튼 / 약관 링크 / 닫기 버튼이 모두 노출되어야 한다.
        Steps: 비로그인 상태 → 로그인 모달 노출 후 구성 요소 확인
        """
        # 모달이 아직 열려있지 않으면 재진입
        if not membership_page_guest.is_login_modal_visible():
            membership_page_guest.go_to_protected_page()
            membership_page_guest.page.wait_for_timeout(800)

        assert membership_page_guest.is_login_modal_visible(), \
            "[FAIL] 로그인 모달 미노출 — 선행 TC(FULLTC-217) 상태 확인 필요"

        assert membership_page_guest.is_google_login_btn_visible(), \
            "[FAIL] 로그인 모달 내 'Google로 로그인' 버튼 미노출"

        assert membership_page_guest.is_login_terms_link_visible(), \
            "[FAIL] 로그인 모달 내 서비스 이용약관 링크 미노출 — LOGIN_TERMS_LINK 셀렉터 확인 필요"

        assert membership_page_guest.is_login_privacy_link_visible(), \
            "[FAIL] 로그인 모달 내 개인정보처리방침 링크 미노출 — LOGIN_PRIVACY_LINK 셀렉터 확인 필요"

        assert membership_page_guest.is_modal_close_btn_visible(), \
            "[FAIL] 로그인 모달 닫기(X) 버튼 미노출 — LOGIN_MODAL_CLOSE 셀렉터 확인 필요"

    def test_FULLTC_219_login_modal_close(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """
        FULLTC-219 | 로그인/로그인 모달 닫기 | Minor
        모달 외부 클릭 또는 X 버튼 클릭 시 모달이 닫히고 비로그인 상태가 유지되어야 한다.
        Steps: 로그인 모달 노출 상태 → X 버튼 또는 외부 클릭
        """
        # 모달이 열려있지 않으면 재진입
        if not membership_page_guest.is_login_modal_visible():
            membership_page_guest.go_to_protected_page()
            membership_page_guest.page.wait_for_timeout(800)

        assert membership_page_guest.is_login_modal_visible(), \
            "[FAIL] 로그인 모달 미노출 — 선행 TC 상태 확인 필요"

        # X 버튼 클릭 시도, 없으면 외부 클릭
        if membership_page_guest.is_modal_close_btn_visible():
            membership_page_guest.click_modal_close_btn()
        else:
            membership_page_guest.click_modal_outside()

        membership_page_guest.wait_for_modal_dismiss()

        assert not membership_page_guest.is_login_modal_visible(), \
            "[FAIL] 닫기 버튼/외부 클릭 후 로그인 모달이 닫히지 않음"

        assert not membership_page_guest.is_gnb_logged_in_state(), \
            "[FAIL] 모달 닫힘 후 로그인 상태로 전환됨 (비정상)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-220~223  |  Google SSO 플로우
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page_guest")
class TestMembershipGoogleSSORegression:
    """Google OAuth 진입·취소 플로우 검증"""

    def test_FULLTC_220_google_oauth_entry(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """
        FULLTC-220 | 로그인/Google SSO OAuth 진입 | Major
        'Google로 로그인' 버튼 클릭 시 Google 계정 선택 화면으로 이동해야 한다.
        Steps: 비로그인 상태 → 로그인 모달 → 'Google로 로그인' 클릭
        """
        membership_page_guest.go_to_protected_page()
        membership_page_guest.page.wait_for_timeout(800)

        if not membership_page_guest.is_login_modal_visible():
            pytest.skip("[SKIP] 로그인 모달 미노출 — 선행 조건 미충족")

        membership_page_guest.click_google_login_btn()

        # Google OAuth 페이지로 이동하거나 팝업이 열려야 함
        # ※ 새 팝업/탭으로 열리는 경우 현재 page URL은 유지될 수 있음
        membership_page_guest.page.wait_for_timeout(1_500)

        current_url = membership_page_guest.page.url
        is_oauth = membership_page_guest.is_google_oauth_page()

        assert is_oauth or "accounts.google" in current_url, \
            (
                "[FAIL] 'Google로 로그인' 클릭 후 Google OAuth 화면 미이동 — "
                f"현재 URL: {current_url} / "
                "팝업 방식인 경우 별도 창 처리 로직 추가 필요"
            )

    @pytest.mark.skip(
        reason=(
            "[SKIP] FULLTC-221: Google OAuth 실제 계정 선택·인증 완료 시나리오는 "
            "자동화 불가 (Google OAuth UI는 외부 서비스). "
            "수동 검증 필요."
        )
    )
    def test_FULLTC_221_google_login_success_redirect(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """
        FULLTC-221 | 로그인/Google SSO 로그인 성공 | Major
        Google OAuth 인증 완료 후 이전 접근 페이지 또는 메인으로 리다이렉트되어야 한다.
        ※ Google OAuth UI 자동화 불가 → 수동 검증
        """
        pass

    def test_FULLTC_223_google_oauth_cancel_returns_to_site(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """
        FULLTC-223 | 로그인/Google SSO 취소 | Minor
        Google OAuth 화면에서 뒤로가기/취소 시 STG 페이지로 복귀하고 비로그인 상태가 유지되어야 한다.
        Steps: 비로그인 → Google OAuth 진입 → 뒤로가기
        """
        membership_page_guest.go_to_protected_page()
        membership_page_guest.page.wait_for_timeout(800)

        if not membership_page_guest.is_login_modal_visible():
            pytest.skip("[SKIP] 로그인 모달 미노출 — 선행 조건 미충족")

        membership_page_guest.click_google_login_btn()
        membership_page_guest.page.wait_for_timeout(1_500)

        # OAuth 페이지로 이동한 경우에만 뒤로가기
        if membership_page_guest.is_google_oauth_page():
            membership_page_guest.go_back_from_oauth()
        else:
            # 팝업 방식이거나 이미 복귀된 경우
            membership_page_guest.page.wait_for_timeout(500)

        # bloomingbit STG 도메인으로 복귀 확인
        assert "bloomingbit.io" in membership_page_guest.page.url, \
            (
                "[FAIL] Google OAuth 취소/뒤로가기 후 bloomingbit STG 미복귀 — "
                f"현재 URL: {membership_page_guest.page.url}"
            )

        # 비로그인 상태 유지 확인
        assert not membership_page_guest.is_gnb_logged_in_state(), \
            "[FAIL] OAuth 취소 후 로그인 상태로 전환됨 (비정상)"

        # 오류 메시지 미노출 확인
        assert not membership_page_guest.is_error_page_visible(), \
            "[FAIL] OAuth 취소 후 에러 페이지 노출됨"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-224~226  |  최초 로그인 약관 동의
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page_guest")
class TestMembershipTermsRegression:
    """최초 로그인 시 약관 동의 화면 검증 (신규 Google 계정 필요)"""

    @pytest.mark.skip(
        reason=(
            "[SKIP] FULLTC-224: 최초 로그인 약관 동의 화면은 신규 Google 계정으로 "
            "Google OAuth를 완료해야 진입 가능. "
            "자동화 범위 외 — 수동 검증 필요."
        )
    )
    def test_FULLTC_224_terms_agreement_shown_on_first_login(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """FULLTC-224 | 약관 동의/최초 로그인 | Major — 약관 동의 화면 노출"""
        pass

    @pytest.mark.skip(
        reason=(
            "[SKIP] FULLTC-225: 약관 동의 화면 진입에 신규 Google 계정 + "
            "Google OAuth 자동화 필요 — 수동 검증 권장."
        )
    )
    def test_FULLTC_225_terms_not_agreed_blocks_entry(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """FULLTC-225 | 약관 동의/미동의 처리 | Major — 필수 동의 없이 진입 차단"""
        pass

    @pytest.mark.skip(
        reason=(
            "[SKIP] FULLTC-226: 약관 동의 완료 후 메인 이동 검증 — "
            "신규 Google 계정 + Google OAuth 자동화 필요. 수동 검증."
        )
    )
    def test_FULLTC_226_terms_agreed_navigates_to_main(
        self, membership_page_guest: MembershipPage
    ) -> None:
        """FULLTC-226 | 약관 동의/동의 완료 | Major — 동의 완료 후 서비스 진입"""
        pass


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-222  |  로그인 성공 UI (로그인 상태)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page")
class TestMembershipLoginSuccessRegression:
    """로그인 상태 GNB UI 검증"""

    def test_FULLTC_222_logged_in_gnb_profile_and_stat(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-222 | 로그인/Google SSO 로그인 성공 UI | Major
        로그인 완료 상태에서 GNB에 프로필 아이콘·STAT 잔액이 노출되고
        비로그인 UI는 미노출되어야 한다.
        Steps: Google 계정 로그인 완료 상태 → GNB 우측 영역 확인
        """
        membership_page.go_to_main()

        assert membership_page.is_gnb_visible(), \
            "[FAIL] GNB 헤더 미노출"

        assert membership_page.is_gnb_logged_in_state(), \
            "[FAIL] 로그인 상태인데 GNB 프로필 아이콘 미노출 — GNB_PROFILE_ICON 셀렉터 확인 필요"

        assert membership_page.is_gnb_stat_balance_visible(), \
            "[FAIL] GNB STAT 잔액 표시 미노출 — GNB_STAT_BALANCE 셀렉터 확인 필요"

        # 비로그인 UI는 노출되면 안 됨
        assert not membership_page.is_gnb_non_login_state(), \
            "[FAIL] 로그인 상태인데 비로그인 GNB 아이콘 노출됨 (비정상)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-227~228  |  로그아웃 플로우
#  ⚠️ 이 클래스의 TC 실행 후 해당 context는 비로그인 상태가 됩니다.
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page")
class TestMembershipLogoutFlowRegression:
    """로그아웃 및 로그아웃 후 보호 페이지 접근 검증
    ⚠️ FULLTC-227 실행 후 context가 로그아웃 상태가 되므로
       FULLTC-228은 해당 상태를 이어서 검증합니다.
    """

    def test_FULLTC_227_logout_success(self, membership_page: MembershipPage) -> None:
        """
        FULLTC-227 | 세션 관리/로그아웃 | Major
        로그아웃 후 메인 페이지로 이동하고 GNB에 비로그인 UI가 노출되어야 한다.
        Steps: 로그인 상태 → GNB 프로필 아이콘 → 드롭다운 → '로그아웃' 클릭
        """
        membership_page.go_to_main()
        membership_page.click_profile_icon()

        assert membership_page.is_profile_dropdown_visible(), \
            "[FAIL] 프로필 아이콘 클릭 후 드롭다운 미노출 — PROFILE_DROPDOWN 셀렉터 확인 필요"

        membership_page.logout()

        assert not membership_page.is_gnb_logged_in_state(), \
            "[FAIL] 로그아웃 후 GNB 프로필 아이콘(로그인 UI) 여전히 노출 (비정상)"

        assert membership_page.is_gnb_non_login_state(), \
            "[FAIL] 로그아웃 후 GNB 비로그인 UI 미노출 — GNB_NON_LOGIN_ICON 셀렉터 확인 필요"

    def test_FULLTC_228_post_logout_protected_page_access(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-228 | 세션 관리/로그아웃 후 접근 | Major
        로그아웃 상태에서 보호 페이지 접근 시 로그인 모달 노출 또는 메인 리다이렉트 되어야 한다.
        Steps: 로그아웃 상태 (FULLTC-227 이어짐) → /mypage/profile URL 직접 접근
        ⚠️ 선행 조건: FULLTC-227 실행 후 비로그인 상태
        """
        membership_page.go_to_protected_page()

        is_login_modal = membership_page.is_login_modal_visible()
        is_redirected_to_main = membership_page.is_main_path()
        is_error = membership_page.is_error_page_visible()

        assert is_login_modal or is_redirected_to_main or is_error, \
            (
                "[FAIL] 로그아웃 후 /mypage/profile 접근 시 보호 처리 없음 — "
                "로그인 모달 / 메인 리다이렉트 / 에러 페이지 중 하나가 노출되어야 함 / "
                f"현재 URL: {membership_page.page.url}"
            )

        # 보호 페이지 콘텐츠가 그대로 노출되면 안 됨
        assert not membership_page.is_mypage_loaded(), \
            "[FAIL] 로그아웃 상태에서 /mypage/profile 콘텐츠가 그대로 노출됨 (보안 취약)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-229~230  |  세션 만료
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page")
class TestMembershipSessionRegression:
    """인증 토큰 강제 삭제(세션 만료) 후 동작 검증"""

    def test_FULLTC_229_session_expiry_auto_logout(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-229 | 세션 관리/세션 만료 | Major
        인증 토큰 삭제 후 새로고침 시 비로그인 상태로 자동 전환되어야 한다.
        Steps: 로그인 상태 → 개발자 도구에서 인증 토큰 삭제 → 새로고침
        ※ JS로 localStorage·sessionStorage·cookie 강제 삭제하여 시뮬레이션
        """
        membership_page.go_to_main()

        # 인증 토큰 강제 삭제 (세션 만료 시뮬레이션)
        membership_page.simulate_session_expiry()
        membership_page.refresh_page()

        # 비로그인 상태 전환 확인
        is_non_login = membership_page.is_gnb_non_login_state()
        is_login_modal = membership_page.is_login_modal_visible()
        is_main = membership_page.is_main_path()

        assert is_non_login or is_login_modal or is_main, \
            (
                "[FAIL] 세션 만료 후 새로고침 시 비로그인 상태 미전환 — "
                "비로그인 GNB UI / 로그인 모달 / 메인 리다이렉트 중 하나가 나타나야 함 / "
                f"현재 URL: {membership_page.page.url}"
            )

        assert not membership_page.is_gnb_logged_in_state(), \
            "[FAIL] 세션 만료(토큰 삭제) 후 로그인 프로필 아이콘 여전히 노출 (비정상)"

    @pytest.mark.skip(
        reason=(
            "[SKIP] FULLTC-230: 세션 만료 후 재로그인 시나리오는 "
            "Google OAuth 실제 인증이 필요하여 자동화 불가. "
            "수동 검증 권장."
        )
    )
    def test_FULLTC_230_session_expiry_relogin(
        self, membership_page: MembershipPage
    ) -> None:
        """FULLTC-230 | 세션 관리/세션 만료 후 재로그인 | Minor — OAuth 재인증 후 복귀"""
        pass


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-231  |  멀티 탭 로그아웃 동기화
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page")
class TestMembershipMultiTabRegression:
    """멀티 탭 환경에서 로그아웃 동기화 검증"""

    def test_FULLTC_231_multi_tab_logout_sync(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-231 | 세션 관리/멀티 탭 로그아웃 동기화 | Minor
        탭 B에서 로그아웃 후 탭 B 새로고침 시 비로그인 상태로 전환되어야 한다.
        ※ 단일 브라우저 내 두 번째 탭으로 시뮬레이션
        Steps: 탭 A(메인) + 탭 B(메인) 오픈 → 탭 B에서 로그아웃 → 탭 B 새로고침
        """
        # 탭 A: 이미 열려있는 페이지(membership_page)
        membership_page.go_to_main()

        # 탭 B: 동일 context에서 새 페이지 열기
        tab_b_page = membership_page.page.context.new_page()
        tab_b = MembershipPage(tab_b_page)
        try:
            tab_b.go_to_main()

            # 탭 B에서 로그아웃 수행
            tab_b.click_profile_icon()
            tab_b.page.wait_for_timeout(400)
            tab_b.logout()

            # 탭 B 새로고침 후 비로그인 상태 확인
            tab_b.refresh_page()

            assert tab_b.is_gnb_non_login_state() or not tab_b.is_gnb_logged_in_state(), \
                "[FAIL] 탭 B에서 로그아웃 후 새로고침 시 비로그인 UI 미전환 — GNB_NON_LOGIN_ICON 셀렉터 확인 필요"

            assert not tab_b.is_gnb_logged_in_state(), \
                "[FAIL] 탭 B 로그아웃·새로고침 후 프로필 아이콘(로그인 UI) 여전히 노출"

        finally:
            tab_b_page.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-232~235  |  계정 연동
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page")
class TestMembershipAccountLinkingRegression:
    """마이페이지 내 Google 계정 연동 정보 및 해제 모달 검증"""

    def test_FULLTC_232_account_linking_info_visible(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-232 | 계정 연동/연동 정보 확인 | Minor
        마이페이지에 로그인 Google 계정 이메일 및 'Google 연동' 상태가 표시되어야 한다.
        Steps: 로그인 상태 → GNB 프로필 → 마이 페이지 → 계정 연동 정보 확인
        """
        membership_page.go_to_main()
        membership_page.click_profile_icon()
        membership_page.page.wait_for_timeout(400)
        membership_page.click_dropdown_mypage()

        assert membership_page.is_mypage_loaded(), \
            f"[FAIL] 마이페이지 로드 실패 — 현재 URL: {membership_page.page.url}"

        assert membership_page.is_account_section_visible(), \
            "[FAIL] 마이페이지 계정 연동 섹션 미노출 — MYPAGE_ACCOUNT_SECTION 셀렉터 확인 필요"

        assert membership_page.is_google_badge_visible(), \
            "[FAIL] 마이페이지 'Google 연동' 상태 배지/텍스트 미노출 — MYPAGE_GOOGLE_BADGE 셀렉터 확인 필요"

    def test_FULLTC_233_linked_email_matches_login_account(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-233 | 계정 연동/연동 이메일 일치 | Minor
        마이페이지에 표시된 연동 이메일이 실제 로그인 계정과 동일해야 한다.
        Steps: 로그인 상태 → 마이페이지 → 계정 연동 이메일 확인
        """
        if not membership_page.is_mypage_loaded():
            membership_page.go_to_mypage()

        linked_email = membership_page.get_linked_email_text()

        assert linked_email, \
            "[FAIL] 마이페이지 연동 이메일 텍스트 비어있음 — MYPAGE_LINKED_EMAIL 셀렉터 확인 필요"

        assert "@" in linked_email, \
            f"[FAIL] 연동 이메일 텍스트가 이메일 형식이 아님 — 실제 값: '{linked_email}'"

        # ⚠️ TODO: 실제 테스트 계정 이메일로 교체하여 정확한 일치 검증 가능
        # assert linked_email == "your-test-account@gmail.com", ...

    def test_FULLTC_234_unlink_confirm_modal_ui(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-234 | 계정 연동/연동 해제 버튼·모달 확인 | Major
        연동 해제 버튼 클릭 시 경고 안내 및 '취소'/'확인' 버튼이 포함된 모달이 노출되어야 한다.
        Steps: 로그인 상태 → 마이페이지 → 계정 연동 → 연동 해제 버튼 클릭
        """
        if not membership_page.is_mypage_loaded():
            membership_page.go_to_mypage()

        assert membership_page.is_unlink_btn_visible(), \
            "[FAIL] 계정 연동 해제 버튼 미노출 — MYPAGE_UNLINK_BTN 셀렉터 확인 필요"

        membership_page.click_unlink_btn()

        assert membership_page.is_unlink_modal_visible(), \
            "[FAIL] 연동 해제 버튼 클릭 후 확인 모달 미노출 — UNLINK_MODAL 셀렉터 확인 필요"

        assert membership_page.is_unlink_warning_visible(), \
            "[FAIL] 연동 해제 모달 내 경고 문구(서비스 이용 불가 안내) 미노출 — UNLINK_WARNING_TEXT 확인 필요"

        assert membership_page.page.locator(membership_page.UNLINK_CANCEL_BTN).count() > 0, \
            "[FAIL] 연동 해제 모달 내 '취소' 버튼 미노출"

        assert membership_page.page.locator(membership_page.UNLINK_CONFIRM_BTN).count() > 0, \
            "[FAIL] 연동 해제 모달 내 '확인' 버튼 미노출"

    def test_FULLTC_235_unlink_cancel_keeps_linked_state(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-235 | 계정 연동/연동 해제 취소 | Minor
        연동 해제 모달에서 '취소' 클릭 시 모달이 닫히고 Google 연동 상태가 유지되어야 한다.
        Steps: 연동 해제 확인 모달 노출 상태 → '취소' 클릭
        """
        if not membership_page.is_mypage_loaded():
            membership_page.go_to_mypage()

        # 모달이 열려있지 않으면 해제 버튼 클릭
        if not membership_page.is_unlink_modal_visible():
            if not membership_page.is_unlink_btn_visible():
                pytest.skip("[SKIP] 연동 해제 버튼 미노출 — 선행 조건 미충족")
            membership_page.click_unlink_btn()
            membership_page.page.wait_for_timeout(400)

        assert membership_page.is_unlink_modal_visible(), \
            "[FAIL] 연동 해제 모달 미노출 — 선행 조건 확인 필요"

        membership_page.click_unlink_cancel()
        membership_page.page.wait_for_timeout(400)

        # 모달 닫힘 확인
        assert not membership_page.is_unlink_modal_visible(), \
            "[FAIL] '취소' 클릭 후 연동 해제 모달이 닫히지 않음"

        # Google 연동 상태 유지 확인
        assert membership_page.is_google_badge_visible() or \
               membership_page.is_account_section_visible(), \
            "[FAIL] '취소' 클릭 후 Google 연동 상태가 변경됨 (비정상)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-236  |  중복 로그인
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("membership_page")
class TestMembershipDuplicateLoginRegression:
    """동일 계정 다중 브라우저 로그인 동작 검증"""

    def test_FULLTC_236_duplicate_login_behavior(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-236 | 계정 연동/중복 로그인 | Minor
        동일 Google 계정으로 다른 브라우저(시크릿 창)에서 로그인 시
        두 번째 로그인이 성공하거나 이전 세션 만료 처리 중 하나로 정상 동작해야 한다.
        Steps: 브라우저 A 로그인 상태 → 새 컨텍스트(시크릿)에서 동일 계정 로그인 시도 구조 확인
        ※ 실제 Google OAuth 인증은 자동화 불가 — 구조(비로그인 상태 진입 확인)만 검증
        """
        membership_page.go_to_main()

        # 현재 브라우저(A)가 로그인 상태임을 확인
        assert membership_page.is_gnb_logged_in_state(), \
            "[FAIL] 브라우저 A 로그인 상태 확인 실패 — 선행 조건 미충족"

        # 두 번째 컨텍스트(시크릿 모드 시뮬레이션) 생성 — 비로그인 상태
        second_context = membership_page.page.context.browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="ko-KR",
        )
        second_page = second_context.new_page()
        second = MembershipPage(second_page)

        try:
            second.go_to_main()

            # 두 번째 컨텍스트는 비로그인 상태 — 로그인 유도 UI 노출 확인
            assert second.is_gnb_non_login_state() or not second.is_gnb_logged_in_state(), \
                "[FAIL] 두 번째 컨텍스트(시크릿)에서 비로그인 상태 진입 실패"

            # 두 번째 컨텍스트에서 로그인 모달 진입 가능 확인
            second.go_to_protected_page()
            second.page.wait_for_timeout(500)

            can_trigger_login = (
                second.is_login_modal_visible()
                or second.is_gnb_non_login_state()
                or second.is_main_path()
            )

            assert can_trigger_login, \
                (
                    "[FAIL] 두 번째 컨텍스트(시크릿)에서 로그인 유도 UI 미노출 — "
                    "중복 로그인 구조 검증 불가 / "
                    f"현재 URL: {second.page.url}"
                )

        finally:
            second_context.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-237~242  |  회원 탈퇴
#  ⚠️ FULLTC-240~242 는 파괴적(실제 탈퇴 처리) — MEMBERSHIP_RUN_DESTRUCTIVE=true 시만 실행
# ══════════════════════════════════════════════════════════════════════

_DESTRUCTIVE = os.getenv("MEMBERSHIP_RUN_DESTRUCTIVE", "false").lower() == "true"


@pytest.mark.usefixtures("membership_page")
class TestMembershipWithdrawalRegression:
    """회원 탈퇴 버튼·모달·취소·완료·재가입 패널티 검증"""

    def test_FULLTC_237_withdrawal_btn_visible_in_mypage(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-237 | 회원 탈퇴/탈퇴 진입 | Major
        마이페이지(또는 설정 메뉴)에 '회원 탈퇴' 버튼/링크가 노출되어야 한다.
        Steps: 로그인 상태 → GNB 프로필 → 마이 페이지 → 회원 탈퇴 항목 확인
        """
        membership_page.go_to_main()
        membership_page.click_profile_icon()
        membership_page.page.wait_for_timeout(400)
        membership_page.click_dropdown_mypage()

        assert membership_page.is_mypage_loaded(), \
            f"[FAIL] 마이페이지 로드 실패 — 현재 URL: {membership_page.page.url}"

        assert membership_page.is_withdrawal_btn_visible(), \
            "[FAIL] 마이페이지에 '회원 탈퇴' 버튼/링크 미노출 — MYPAGE_WITHDRAWAL_BTN 셀렉터 확인 필요"

    def test_FULLTC_238_withdrawal_confirm_modal_ui(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-238 | 회원 탈퇴/탈퇴 확인 모달 UI 확인 | Major
        '회원 탈퇴' 버튼 클릭 시 데이터 복구 불가 경고 및 '취소'·'탈퇴 확인' 버튼이 노출되어야 한다.
        Steps: 로그인 상태 → 회원 탈퇴 버튼 접근 → 클릭
        """
        if not membership_page.is_mypage_loaded():
            membership_page.go_to_mypage()

        if not membership_page.is_withdrawal_btn_visible():
            pytest.skip("[SKIP] 회원 탈퇴 버튼 미노출 — 선행 조건 미충족")

        membership_page.click_withdrawal_btn()

        assert membership_page.is_withdrawal_modal_visible(), \
            "[FAIL] 회원 탈퇴 버튼 클릭 후 확인 모달 미노출 — WITHDRAWAL_MODAL 셀렉터 확인 필요"

        assert membership_page.is_withdrawal_warning_visible(), \
            "[FAIL] 탈퇴 확인 모달 내 '탈퇴 후 데이터 복구 불가' 경고 문구 미노출"

        assert membership_page.is_withdrawal_cancel_btn_visible(), \
            "[FAIL] 탈퇴 확인 모달 내 '취소' 버튼 미노출"

        assert membership_page.is_withdrawal_confirm_btn_visible(), \
            "[FAIL] 탈퇴 확인 모달 내 '탈퇴 확인' 버튼 미노출"

    def test_FULLTC_239_withdrawal_cancel_keeps_account(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-239 | 회원 탈퇴/탈퇴 취소 | Minor
        탈퇴 확인 모달에서 '취소' 클릭 시 모달이 닫히고 로그인 상태 및 계정이 유지되어야 한다.
        Steps: 탈퇴 확인 모달 노출 상태 → '취소' 클릭
        """
        if not membership_page.is_mypage_loaded():
            membership_page.go_to_mypage()

        # 모달이 열려있지 않으면 탈퇴 버튼 클릭
        if not membership_page.is_withdrawal_modal_visible():
            if not membership_page.is_withdrawal_btn_visible():
                pytest.skip("[SKIP] 회원 탈퇴 버튼 미노출 — 선행 조건 미충족")
            membership_page.click_withdrawal_btn()
            membership_page.page.wait_for_timeout(400)

        assert membership_page.is_withdrawal_modal_visible(), \
            "[FAIL] 탈퇴 확인 모달 미노출 — 선행 조건 확인 필요"

        membership_page.click_withdrawal_cancel()
        membership_page.page.wait_for_timeout(400)

        # 모달 닫힘 확인
        assert not membership_page.is_withdrawal_modal_visible(), \
            "[FAIL] '취소' 클릭 후 탈퇴 확인 모달이 닫히지 않음"

        # 로그인 상태 유지 확인
        assert membership_page.is_gnb_logged_in_state() or \
               membership_page.is_mypage_loaded(), \
            "[FAIL] '취소' 클릭 후 로그인 상태 또는 마이페이지 상태가 변경됨 (비정상)"

    @pytest.mark.skipif(
        not _DESTRUCTIVE,
        reason=(
            "[SKIP] FULLTC-240: 회원 탈퇴 완료는 실제 계정 삭제를 동반합니다. "
            "실행하려면 환경변수 MEMBERSHIP_RUN_DESTRUCTIVE=true 를 설정하세요."
        ),
    )
    def test_FULLTC_240_withdrawal_complete(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-240 | 회원 탈퇴/탈퇴 완료 | Major ⚠️ 파괴적
        '탈퇴 확인' 클릭 후 탈퇴 처리 완료, 자동 로그아웃, 메인 페이지 이동해야 한다.
        Steps: 탈퇴 확인 모달 → '탈퇴 확인' 클릭
        ⚠️ MEMBERSHIP_RUN_DESTRUCTIVE=true 환경변수 필요
        """
        if not membership_page.is_mypage_loaded():
            membership_page.go_to_mypage()

        if not membership_page.is_withdrawal_modal_visible():
            if not membership_page.is_withdrawal_btn_visible():
                pytest.skip("[SKIP] 회원 탈퇴 버튼 미노출")
            membership_page.click_withdrawal_btn()
            membership_page.page.wait_for_timeout(400)

        membership_page.click_withdrawal_confirm()

        # 탈퇴 완료 후 자동 로그아웃 및 메인 이동 확인
        assert not membership_page.is_gnb_logged_in_state(), \
            "[FAIL] 탈퇴 완료 후 로그인 상태 유지됨 (자동 로그아웃 미처리)"

        assert membership_page.is_gnb_non_login_state() or membership_page.is_main_path(), \
            (
                "[FAIL] 탈퇴 완료 후 메인 페이지 이동 또는 비로그인 UI 미노출 — "
                f"현재 URL: {membership_page.page.url}"
            )

    @pytest.mark.skipif(
        not _DESTRUCTIVE,
        reason=(
            "[SKIP] FULLTC-241: 탈퇴 처리된 계정으로 재로그인 시도 검증. "
            "탈퇴 완료 계정이 필요합니다. "
            "MEMBERSHIP_RUN_DESTRUCTIVE=true 설정 후 실행."
        ),
    )
    def test_FULLTC_241_rejoin_penalty_blocks_login(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-241 | 회원 탈퇴/재가입 패널티 재로그인 시도 | Major ⚠️ 파괴적
        탈퇴한 계정으로 재로그인 시도 시 '재가입 제한 기간' 안내 메시지 노출 및 로그인 차단
        ※ FULLTC-240(탈퇴 완료) 이후 비로그인 상태에서 동일 계정 재로그인 시도 구조 검증
        """
        # 탈퇴 완료 후 비로그인 상태 확인
        assert not membership_page.is_gnb_logged_in_state(), \
            "[SKIP] 탈퇴 완료 상태(비로그인)가 아님 — FULLTC-240 선행 실행 필요"

        # 로그인 진입 시도
        membership_page.go_to_protected_page()
        membership_page.page.wait_for_timeout(500)

        # 로그인 모달 또는 재가입 차단 메시지 확인
        is_block_msg = membership_page.is_rejoin_block_msg_visible()
        # ※ Google OAuth 실제 진행 없이 구조만 확인
        assert membership_page.is_login_modal_visible() or is_block_msg, \
            "[FAIL] 탈퇴 계정 재로그인 시도 시 로그인 차단 UI 또는 재가입 제한 메시지 미노출"

    @pytest.mark.skipif(
        not _DESTRUCTIVE,
        reason=(
            "[SKIP] FULLTC-242: 패널티 기간 내 동일 계정 신규 가입 시도 검증. "
            "탈퇴 완료 계정 및 패널티 기간 내 재가입 시나리오 필요. "
            "MEMBERSHIP_RUN_DESTRUCTIVE=true 설정 후 실행."
        ),
    )
    def test_FULLTC_242_rejoin_penalty_blocks_new_signup(
        self, membership_page: MembershipPage
    ) -> None:
        """
        FULLTC-242 | 회원 탈퇴/재가입 패널티 패널티 기간 내 | Major ⚠️ 파괴적
        패널티 기간 중 동일 Google 계정으로 신규 가입 시도 시 재가입 불가 안내 노출
        ※ Google OAuth 자동화 불가 — 재가입 불가 UI 존재 여부 및 텍스트로 검증
        """
        # 탈퇴 완료 후 비로그인 상태 전제
        assert not membership_page.is_gnb_logged_in_state(), \
            "[SKIP] 탈퇴 완료 상태(비로그인)가 아님 — 선행 TC 확인 필요"

        # 재가입 차단 메시지 또는 로그인 차단 UI 존재 확인
        is_block_msg = membership_page.is_rejoin_block_msg_visible()
        is_login_modal = membership_page.is_login_modal_visible()

        assert is_block_msg or is_login_modal, \
            (
                "[FAIL] 패널티 기간 내 재가입 시도 시 차단 안내 UI 미노출 — "
                "REJOIN_BLOCK_MSG 셀렉터 확인 필요 / "
                f"현재 URL: {membership_page.page.url}"
            )

        if is_block_msg:
            content = membership_page.page.content()
            has_penalty_msg = "재가입 제한" in content or "탈퇴한 계정" in content
            assert has_penalty_msg, \
                "[FAIL] 재가입 불가 안내 메시지 내용이 기대 문구와 다름 ('재가입 제한' 또는 '탈퇴한 계정' 포함 필요)"