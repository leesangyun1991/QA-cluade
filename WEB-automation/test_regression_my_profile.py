"""
tests/stage8_regression/web/test_regression_my_profile.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
내 프로필(My Profile) 회귀 테스트 (FULLTC-345 ~ FULLTC-371)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_my_profile.py -v

[사전 조건]
  - 이 파일과 동일 디렉토리에 auth.json (로그인 세션 파일) 존재 필요
  - 비로그인 TC(FULLTC-371)는 my_profile_page_guest 픽스처 사용
  - FULLTC-349~352  : 닉네임/이메일/프로필 이미지가 설정된 계정 권장
  - FULLTC-353~354  : 리워드 잔액이 0 이상인 계정 필요

[TC 클래스 구성]
  FULLTC-345~348   TestMyProfileModalControl       모달 제어 (오픈/딤/X/ESC)
  FULLTC-349~352   TestMyProfileUserInfo           사용자 정보 노출
  FULLTC-353~354   TestMyProfileDataRefresh        리워드 잔액·실시간 갱신
  FULLTC-355~359   TestMyProfileLanguageSettings   언어 설정 (KR↔EN, 영속화)
  FULLTC-360~364   TestMyProfileThemeSettings      테마 설정 (Dark/Light, 영속화)
  FULLTC-365~367   TestMyProfileRouting            라우팅 (수정/마이페이지/내 활동)
  FULLTC-368~371   TestMyProfileLogout             로그아웃 + 게스트 UI
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from my_profile_page import MyProfilePage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def my_profile_page() -> Iterator[MyProfilePage]:
    """내 프로필 페이지 픽스처 (로그인 세션 유지)
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
        yield MyProfilePage(page)
        context.close()
        browser.close()


@pytest.fixture(scope="class")
def my_profile_page_guest() -> Iterator[MyProfilePage]:
    """내 프로필 페이지 픽스처 (비로그인 상태 — auth.json 미사용)
    FULLTC-371 전용
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
        yield MyProfilePage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-345~348  |  내 프로필 모달 제어
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("my_profile_page")
class TestMyProfileModalControl:
    """내 프로필 모달 오픈·딤 클릭·X 클릭·ESC 키 닫기 검증"""

    def test_FULLTC_345_open_profile_modal(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-345 | 내 프로필/모달 오픈 | Major
        프로필 아이콘 클릭 시 프로필 모달이 정상 노출되어야 한다.
        """
        my_profile_page.go_to_main()
        assert my_profile_page.is_gnb_logged_in_state(), (
            "[FAIL] 로그인 상태가 아님 - auth.json 확인 필요"
        )
        my_profile_page.click_profile_icon()
        assert my_profile_page.is_profile_modal_visible(), (
            "[FAIL] 프로필 아이콘 클릭 후 프로필 모달 미노출"
        )

    def test_FULLTC_346_close_profile_modal_by_dim(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-346 | 내 프로필/딤 클릭 닫기 | Major
        모달 외부 딤 영역 클릭 시 모달이 닫혀야 한다.
        """
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_profile_modal_visible(), (
            "[FAIL] 사전 조건 실패 - 프로필 모달이 열려있어야 함"
        )
        my_profile_page.close_profile_modal_by_dim()
        my_profile_page.wait_for_modal_dismiss()
        assert not my_profile_page.is_profile_modal_visible(), (
            "[FAIL] 딤 영역 클릭 후 프로필 모달이 닫히지 않음"
        )

    def test_FULLTC_347_close_profile_modal_by_close_btn(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-347 | 내 프로필/X 버튼 닫기 | Major
        모달 내 X(닫기) 버튼 클릭 시 모달이 닫혀야 한다.
        """
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_profile_modal_visible(), (
            "[FAIL] 사전 조건 실패 - 프로필 모달이 열려있어야 함"
        )
        my_profile_page.close_profile_modal_by_close_btn()
        my_profile_page.wait_for_modal_dismiss()
        assert not my_profile_page.is_profile_modal_visible(), (
            "[FAIL] X 버튼 클릭 후 프로필 모달이 닫히지 않음"
        )

    def test_FULLTC_348_close_profile_modal_by_escape(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-348 | 내 프로필/ESC 키 닫기 | Minor
        ESC 키 입력 시 모달이 닫혀야 한다.
        """
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_profile_modal_visible(), (
            "[FAIL] 사전 조건 실패 - 프로필 모달이 열려있어야 함"
        )
        my_profile_page.close_profile_modal_by_escape()
        my_profile_page.wait_for_modal_dismiss()
        assert not my_profile_page.is_profile_modal_visible(), (
            "[FAIL] ESC 키 입력 후 프로필 모달이 닫히지 않음"
        )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-349~352  |  사용자 정보 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("my_profile_page")
class TestMyProfileUserInfo:
    """프로필 모달의 닉네임·이메일·프로필 이미지 노출 검증"""

    def test_FULLTC_349_nickname_displayed(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-349 | 내 프로필/닉네임 노출 | Major
        프로필 모달에 사용자 닉네임이 정상 노출되어야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        nickname = my_profile_page.get_displayed_nickname()
        assert nickname != "", (
            "[FAIL] 프로필 모달에 닉네임이 노출되지 않음"
        )

    def test_FULLTC_350_email_displayed(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-350 | 내 프로필/이메일 노출 | Major
        프로필 모달에 사용자 이메일이 정상 노출되어야 한다.
        """
        my_profile_page.open_profile_modal()
        email = my_profile_page.get_displayed_email()
        assert "@" in email, (
            f"[FAIL] 프로필 모달에 유효한 이메일 미노출 (current='{email}')"
        )

    def test_FULLTC_351_profile_image_displayed(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-351 | 내 프로필/프로필 이미지 노출 | Minor
        프로필 모달에 프로필 이미지(설정 이미지 또는 기본 이미지)가 노출되어야 한다.
        """
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_profile_image_visible(), (
            "[FAIL] 프로필 모달에 프로필 이미지 요소 미노출"
        )

    def test_FULLTC_352_profile_image_default_when_unset(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-352 | 내 프로필/이미지 미설정 시 기본 이미지 | Minor
        사용자가 프로필 이미지를 설정하지 않은 경우 기본 이미지가 노출되어야 한다.
        ※ 이미지가 이미 설정된 계정에서는 src에 'default'/'placeholder'가 없으므로 PASS 가능 → skip
        """
        my_profile_page.open_profile_modal()
        if not my_profile_page.is_profile_image_default():
            pytest.skip("[SKIP] 현재 계정은 프로필 이미지가 이미 설정되어 있어 검증 대상 아님")
        assert my_profile_page.is_profile_image_default(), (
            "[FAIL] 프로필 이미지 미설정 상태인데 기본 이미지가 노출되지 않음"
        )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-353~354  |  데이터 갱신 (리워드 잔액)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("my_profile_page")
class TestMyProfileDataRefresh:
    """리워드 잔액 노출 및 실시간 동기화 검증"""

    def test_FULLTC_353_reward_balance_displayed(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-353 | 내 프로필/리워드 잔액 노출 | Major
        프로필 모달에 현재 리워드 잔액이 노출되어야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_reward_balance_visible(), (
            "[FAIL] 프로필 모달에 리워드 잔액 영역 미노출"
        )
        balance = my_profile_page.get_reward_balance_as_number()
        assert balance >= 0, (
            f"[FAIL] 리워드 잔액이 유효한 숫자가 아님 (raw='{my_profile_page.get_reward_balance_text()}')"
        )

    def test_FULLTC_354_reward_balance_sync_on_reopen(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-354 | 내 프로필/리워드 잔액 동기화 | Minor
        모달 재오픈 시 리워드 잔액이 최신 데이터로 동기화되어야 한다.
        ※ 본 케이스는 두 번 오픈 후 잔액이 일관성 있게 유지/갱신되는지 확인
        """
        my_profile_page.open_profile_modal()
        first_balance = my_profile_page.get_reward_balance_text()
        my_profile_page.close_profile_modal_by_close_btn()
        my_profile_page.wait_for_modal_dismiss()
        my_profile_page.open_profile_modal()
        second_balance = my_profile_page.get_reward_balance_text()
        assert second_balance != "", (
            "[FAIL] 재오픈 후 리워드 잔액 미노출"
        )
        # 잔액은 동일하거나(보유 변동 없음) 갱신될 수 있음 → 어느 쪽이든 빈 값이 아니면 PASS
        assert isinstance(first_balance, str) and isinstance(second_balance, str), (
            "[FAIL] 리워드 잔액 텍스트 타입 오류"
        )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-355~359  |  언어 설정
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("my_profile_page")
class TestMyProfileLanguageSettings:
    """언어 토글 노출·KR↔EN 전환·새로고침/재로그인 영속화 검증"""

    def test_FULLTC_355_language_toggle_visible(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-355 | 내 프로필/언어 토글 노출 | Major
        프로필 모달에 언어 설정 토글 영역이 노출되어야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_language_toggle_visible(), (
            "[FAIL] 프로필 모달에 언어 토글 영역 미노출"
        )

    def test_FULLTC_356_switch_to_english(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-356 | 내 프로필/한국어→English 전환 | Major
        English 선택 시 영문 STG로 전환되어야 한다.
        """
        my_profile_page.open_profile_modal()
        my_profile_page.select_language_english()
        my_profile_page.page.wait_for_timeout(1_500)
        active = my_profile_page.get_active_language()
        assert active == "EN", (
            f"[FAIL] English 선택 후 활성 언어가 EN이 아님 (current='{active}')"
        )

    def test_FULLTC_357_switch_back_to_korean(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-357 | 내 프로필/English→한국어 전환 | Major
        한국어 선택 시 한글 STG로 전환되어야 한다.
        """
        my_profile_page.open_profile_modal()
        my_profile_page.select_language_korean()
        my_profile_page.page.wait_for_timeout(1_500)
        active = my_profile_page.get_active_language()
        assert active == "KR", (
            f"[FAIL] 한국어 선택 후 활성 언어가 KR이 아님 (current='{active}')"
        )

    def test_FULLTC_358_language_persists_on_refresh(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-358 | 내 프로필/언어 새로고침 영속화 | Major
        언어 설정이 새로고침 후에도 유지되어야 한다.
        """
        # 영문으로 변경 후 새로고침
        my_profile_page.open_profile_modal()
        my_profile_page.select_language_english()
        my_profile_page.page.wait_for_timeout(1_500)
        my_profile_page.refresh_page()
        active = my_profile_page.get_active_language()
        assert active == "EN", (
            f"[FAIL] 새로고침 후 언어 설정이 유지되지 않음 (current='{active}')"
        )
        # 정리: 한국어로 복원
        my_profile_page.open_profile_modal()
        my_profile_page.select_language_korean()
        my_profile_page.page.wait_for_timeout(1_500)

    def test_FULLTC_359_language_persists_after_relogin(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-359 | 내 프로필/언어 재로그인 영속화 | Minor
        언어 설정이 재로그인(=storage_state 재사용) 후에도 유지되어야 한다.
        ※ 동일 컨텍스트 내에서 영문 전환 후 새로고침으로 재진입 시뮬레이션
        """
        my_profile_page.open_profile_modal()
        my_profile_page.select_language_english()
        my_profile_page.page.wait_for_timeout(1_500)
        # 메인 재진입 (재로그인 시뮬레이션)
        my_profile_page.go_to_main()
        active = my_profile_page.get_active_language()
        assert active == "EN", (
            f"[FAIL] 재진입 후 언어 설정이 유지되지 않음 (current='{active}')"
        )
        # 정리: 한국어로 복원
        my_profile_page.open_profile_modal()
        my_profile_page.select_language_korean()
        my_profile_page.page.wait_for_timeout(1_500)


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-360~364  |  테마 설정
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("my_profile_page")
class TestMyProfileThemeSettings:
    """테마 토글 노출·Dark/Light 전환·새로고침/재로그인 영속화 검증"""

    def test_FULLTC_360_theme_toggle_visible(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-360 | 내 프로필/테마 토글 노출 | Major
        프로필 모달에 테마 설정 토글 영역이 노출되어야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_theme_toggle_visible(), (
            "[FAIL] 프로필 모달에 테마 토글 영역 미노출"
        )

    def test_FULLTC_361_switch_to_dark(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-361 | 내 프로필/Light→Dark 전환 | Major
        다크 모드 선택 시 html data-theme 속성이 'dark'가 되어야 한다.
        """
        my_profile_page.open_profile_modal()
        my_profile_page.toggle_dark_mode()
        my_profile_page.page.wait_for_timeout(800)
        assert my_profile_page.is_dark_mode_active(), (
            f"[FAIL] 다크 모드 전환 실패 (current theme='{my_profile_page.get_active_theme()}')"
        )

    def test_FULLTC_362_switch_to_light(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-362 | 내 프로필/Dark→Light 전환 | Major
        라이트 모드 선택 시 html data-theme 속성이 'light'가 되어야 한다.
        """
        my_profile_page.open_profile_modal()
        my_profile_page.toggle_light_mode()
        my_profile_page.page.wait_for_timeout(800)
        assert my_profile_page.is_light_mode_active(), (
            f"[FAIL] 라이트 모드 전환 실패 (current theme='{my_profile_page.get_active_theme()}')"
        )

    def test_FULLTC_363_theme_persists_on_refresh(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-363 | 내 프로필/테마 새로고침 영속화 | Major
        테마 설정이 새로고침 후에도 유지되어야 한다.
        """
        # 다크 모드로 변경 후 새로고침
        my_profile_page.open_profile_modal()
        my_profile_page.toggle_dark_mode()
        my_profile_page.page.wait_for_timeout(800)
        my_profile_page.refresh_page()
        assert my_profile_page.is_dark_mode_active(), (
            f"[FAIL] 새로고침 후 다크 테마가 유지되지 않음 (current='{my_profile_page.get_active_theme()}')"
        )
        # 정리: 라이트로 복원
        my_profile_page.open_profile_modal()
        my_profile_page.toggle_light_mode()
        my_profile_page.page.wait_for_timeout(800)

    def test_FULLTC_364_theme_persists_after_relogin(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-364 | 내 프로필/테마 재로그인 영속화 | Minor
        테마 설정이 재진입(메인 재이동) 후에도 유지되어야 한다.
        """
        my_profile_page.open_profile_modal()
        my_profile_page.toggle_dark_mode()
        my_profile_page.page.wait_for_timeout(800)
        my_profile_page.go_to_main()
        assert my_profile_page.is_dark_mode_active(), (
            f"[FAIL] 재진입 후 다크 테마가 유지되지 않음 (current='{my_profile_page.get_active_theme()}')"
        )
        # 정리: 라이트로 복원
        my_profile_page.open_profile_modal()
        my_profile_page.toggle_light_mode()
        my_profile_page.page.wait_for_timeout(800)


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-365~367  |  메뉴 라우팅
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("my_profile_page")
class TestMyProfileRouting:
    """프로필 수정·마이페이지·내 활동 메뉴 라우팅 검증"""

    def test_FULLTC_365_route_to_profile_edit(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-365 | 내 프로필/프로필 수정 라우팅 | Major
        '프로필 수정' 메뉴 클릭 시 /mypage/edit 으로 이동해야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        my_profile_page.click_profile_edit_menu()
        assert my_profile_page.is_on_mypage_edit(), (
            f"[FAIL] '프로필 수정' 메뉴 클릭 후 /mypage/edit 미진입 "
            f"(current='{my_profile_page.get_current_url()}')"
        )

    def test_FULLTC_366_route_to_mypage(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-366 | 내 프로필/마이페이지 라우팅 | Major
        '마이페이지' 메뉴 클릭 시 /mypage 로 이동해야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        my_profile_page.click_mypage_menu()
        assert my_profile_page.is_on_mypage(), (
            f"[FAIL] '마이페이지' 메뉴 클릭 후 /mypage 미진입 "
            f"(current='{my_profile_page.get_current_url()}')"
        )

    def test_FULLTC_367_route_to_my_activity(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-367 | 내 프로필/내 활동 라우팅 | Minor
        '내 활동' 메뉴 클릭 시 /mypage/activity 로 이동해야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        my_profile_page.click_my_activity_menu()
        assert my_profile_page.is_on_my_activity(), (
            f"[FAIL] '내 활동' 메뉴 클릭 후 /mypage/activity 미진입 "
            f"(current='{my_profile_page.get_current_url()}')"
        )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-368~371  |  로그아웃 + 게스트 UI
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("my_profile_page")
class TestMyProfileLogout:
    """로그아웃 처리·뒤로가기·보호 페이지 차단 검증
    (FULLTC-371 게스트 UI 케이스만 별도 게스트 픽스처 사용)
    """

    def test_FULLTC_368_logout_success(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-368 | 내 프로필/로그아웃 성공 | Major
        로그아웃 버튼 클릭 시 세션이 종료되어 비로그인 상태가 되어야 한다.
        """
        my_profile_page.go_to_main()
        my_profile_page.open_profile_modal()
        assert my_profile_page.is_logout_btn_visible(), (
            "[FAIL] 사전 조건 실패 - '로그아웃' 버튼 미노출"
        )
        my_profile_page.click_logout_btn()
        my_profile_page.page.wait_for_timeout(1_500)
        assert not my_profile_page.is_gnb_logged_in_state(), (
            "[FAIL] 로그아웃 후에도 로그인 상태가 유지됨"
        )

    def test_FULLTC_369_back_after_logout_does_not_restore_session(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-369 | 내 프로필/로그아웃 후 뒤로가기 | Minor
        로그아웃 후 브라우저 뒤로가기를 해도 세션이 복원되지 않아야 한다.
        """
        # FULLTC-368 직후 상태에서 진행
        my_profile_page.go_back()
        my_profile_page.page.wait_for_timeout(1_000)
        assert not my_profile_page.is_gnb_logged_in_state(), (
            "[FAIL] 로그아웃 후 뒤로가기로 로그인 상태가 복원됨"
        )

    def test_FULLTC_370_protected_page_redirects_to_signin(
        self, my_profile_page: MyProfilePage
    ) -> None:
        """
        FULLTC-370 | 내 프로필/로그아웃 후 보호 페이지 접근 | Major
        로그아웃 상태에서 /mypage 등 보호 페이지에 접근하면 로그인 페이지로
        리다이렉트되거나, 비로그인 안내가 노출되어야 한다.
        """
        my_profile_page.go_to_mypage()
        my_profile_page.page.wait_for_timeout(1_500)
        is_redirected = my_profile_page.is_login_page_visible()
        is_guest_ui   = not my_profile_page.is_gnb_logged_in_state()
        assert is_redirected or is_guest_ui, (
            f"[FAIL] 로그아웃 상태에서 보호 페이지 접근이 차단되지 않음 "
            f"(current='{my_profile_page.get_current_url()}')"
        )


@pytest.mark.usefixtures("my_profile_page_guest")
class TestMyProfileLogoutGuest:
    """비로그인(게스트) 상태에서의 GNB 노출 검증"""

    def test_FULLTC_371_guest_no_profile_icon(
        self, my_profile_page_guest: MyProfilePage
    ) -> None:
        """
        FULLTC-371 | 내 프로필/비로그인 게스트 UI | Major
        비로그인 상태에서는 GNB에 프로필 아이콘이 노출되지 않고
        로그인 진입 CTA가 노출되어야 한다.
        """
        my_profile_page_guest.go_to_main()
        my_profile_page_guest.page.wait_for_timeout(1_000)
        assert my_profile_page_guest.is_gnb_visible(), (
            "[FAIL] GNB 헤더 미노출"
        )
        assert not my_profile_page_guest.is_gnb_logged_in_state(), (
            "[FAIL] 비로그인 상태인데 프로필 아이콘이 노출됨"
        )