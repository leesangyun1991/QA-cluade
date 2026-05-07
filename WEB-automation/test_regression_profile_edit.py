"""
피처명: 프로필 편집(Profile Edit) — Full TC 자동화 (FULLTC-372 ~ FULLTC-400) / Final
플랫폼: WEB (Playwright)
STG: https://web-stg.bloomingbit.io
실행: pytest tests/test_web/test_regression_profile_edit.py -v --html=reports/profile_edit_report.html

[Final 병합 사항]
  1) PROFILE_EDIT_URL → /mypage/profile (PageObject 측 수정 반영)
  2) 실 HTML 셀렉터 전면 적용
  3) navigate_profile_edit() 안전 대기 적용
  4) FULLTC-392: is_save_btn_disabled() 단일 검증으로 최적화

[fixture 옵션] headless=False, slow_mo=500, --window-position=0,-1080, storage_state='auth.json'
[비고] 본 페이지 미존재 영역(소개글 / 이탈팝업)은 사전 체크 헬퍼로 skip 처리
"""
import pytest
from playwright.sync_api import sync_playwright
from profile_edit_page import ProfileEditWebPage


# ════════════════════════════════════════════════
# 픽스처
# ════════════════════════════════════════════════

@pytest.fixture(scope="function")
def page_logged_in_profile():
    """
    로그인 상태 브라우저 페이지 (auth.json 세션 재사용)
      - headless=False
      - slow_mo=500
      - args=['--window-position=0,-1080']
      - storage_state='auth.json'
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=500,
            args=["--window-position=0,-1080"],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            storage_state="auth.json",
        )
        page = context.new_page()
        yield page
        context.close()
        browser.close()


# ════════════════════════════════════════════════
# 영역 1 — 프로필 이미지 (FULLTC-372 ~ 377)
# ════════════════════════════════════════════════

class TestProfileImage:

    def test_fulltc_372_upload_valid_image(self, page_logged_in_profile):
        """FULLTC-372 | 정상 이미지 업로드 (JPG/PNG, 허용 용량 이하) — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            before_src = page.get_preview_src()
            page.upload_profile_image(ProfileEditWebPage.SAMPLE_IMAGE_VALID_JPG)
            page_logged_in_profile.wait_for_timeout(500)
            after_src = page.get_preview_src()
            assert after_src and after_src != before_src, \
                "[FAIL] FULLTC-372: 이미지 업로드 후 미리보기 src 미변경"
        except Exception as e:
            page.take_screenshot("FULLTC-372_failure")
            raise e

    def test_fulltc_373_invalid_format_blocked(self, page_logged_in_profile):
        """FULLTC-373 | 비허용 파일 형식(PDF/GIF) 업로드 차단 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.upload_profile_image(ProfileEditWebPage.SAMPLE_IMAGE_INVALID_PDF)
            page_logged_in_profile.wait_for_timeout(500)
            assert page_logged_in_profile.is_visible(page.IMAGE_FORMAT_ERROR), \
                "[FAIL] FULLTC-373: 비허용 파일 형식 업로드 시 형식 오류 메시지 미노출"
        except Exception as e:
            page.take_screenshot("FULLTC-373_failure")
            raise e

    def test_fulltc_374_oversize_blocked(self, page_logged_in_profile):
        """FULLTC-374 | 허용 용량 초과 파일 업로드 차단 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.upload_profile_image(ProfileEditWebPage.SAMPLE_IMAGE_OVERSIZE)
            page_logged_in_profile.wait_for_timeout(500)
            assert page_logged_in_profile.is_visible(page.IMAGE_SIZE_ERROR), \
                "[FAIL] FULLTC-374: 용량 초과 업로드 시 용량 오류 메시지 미노출"
        except Exception as e:
            page.take_screenshot("FULLTC-374_failure")
            raise e

    def test_fulltc_375_image_replace(self, page_logged_in_profile):
        """FULLTC-375 | 기존 이미지 → 새 이미지 교체 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.upload_profile_image(ProfileEditWebPage.SAMPLE_IMAGE_VALID_JPG)
            page_logged_in_profile.wait_for_timeout(500)
            first_src = page.get_preview_src()

            page.upload_profile_image(ProfileEditWebPage.SAMPLE_IMAGE_VALID_PNG)
            page_logged_in_profile.wait_for_timeout(500)
            second_src = page.get_preview_src()

            assert second_src and first_src != second_src, \
                f"[FAIL] FULLTC-375: 이미지 교체 시 미리보기 src 미변경 (before='{first_src}', after='{second_src}')"
        except Exception as e:
            page.take_screenshot("FULLTC-375_failure")
            raise e

    def test_fulltc_376_image_delete_to_default(self, page_logged_in_profile):
        """FULLTC-376 | 이미지 삭제 → 기본 이미지로 변경 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            if page_logged_in_profile.locator(page.IMAGE_DELETE_BTN).count() == 0:
                pytest.skip("FULLTC-376: 본 페이지 DOM에 이미지 삭제 버튼 미존재 (skip)")
            page.upload_profile_image(ProfileEditWebPage.SAMPLE_IMAGE_VALID_JPG)
            page_logged_in_profile.wait_for_timeout(500)

            page.click_image_delete()
            page_logged_in_profile.wait_for_timeout(500)
            assert page_logged_in_profile.is_visible(page.PROFILE_IMAGE_DEFAULT), \
                "[FAIL] FULLTC-376: 이미지 삭제 후 기본 이미지로 전환 미반영"
        except Exception as e:
            page.take_screenshot("FULLTC-376_failure")
            raise e

    def test_fulltc_377_preview_before_save(self, page_logged_in_profile):
        """FULLTC-377 | 저장 전임에도 선택 이미지 미리보기 즉시 반영 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            before = page.get_preview_src()
            page.upload_profile_image(ProfileEditWebPage.SAMPLE_IMAGE_VALID_JPG)
            page_logged_in_profile.wait_for_timeout(500)
            after = page.get_preview_src()
            assert after and after != before, \
                "[FAIL] FULLTC-377: 저장 전 선택 이미지 미리보기 즉시 반영 안 됨"
        except Exception as e:
            page.take_screenshot("FULLTC-377_failure")
            raise e


# ════════════════════════════════════════════════
# 영역 2 — 닉네임(유저 아이디) 수정 (FULLTC-378 ~ 385)
# ════════════════════════════════════════════════

class TestNicknameEdit:

    def test_fulltc_378_valid_input_and_duplicate_check(self, page_logged_in_profile):
        """FULLTC-378 | 유효 닉네임 + 중복확인 통과 → 저장 가능 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("test_user")  # 영문/숫자/_ 4~15자
            page.click_duplicate_check()
            assert page_logged_in_profile.is_visible(page.NICKNAME_DUP_MSG_OK), \
                "[FAIL] FULLTC-378: 사용 가능 닉네임 안내 메시지 미노출"
            assert page.is_save_btn_enabled(), \
                "[FAIL] FULLTC-378: 유효 닉네임 입력 후 저장 버튼 비활성화"
        except Exception as e:
            page.take_screenshot("FULLTC-378_failure")
            raise e

    def test_fulltc_379_max_length_truncate(self, page_logged_in_profile):
        """FULLTC-379 | 최대 글자 수(15자) 초과 입력 차단/트리밍 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            over_max = "a" * (ProfileEditWebPage.NICKNAME_MAX_LENGTH + 5)
            page.fill_nickname(over_max)
            actual = page.get_nickname_value()
            assert len(actual) <= ProfileEditWebPage.NICKNAME_MAX_LENGTH, \
                f"[FAIL] FULLTC-379: 닉네임 입력 글자 수 제한 초과 차단 미동작 (실제 길이: {len(actual)})"
        except Exception as e:
            page.take_screenshot("FULLTC-379_failure")
            raise e

    def test_fulltc_380_min_length_error(self, page_logged_in_profile):
        """FULLTC-380 | 최소 글자 수(4자) 미달 → 에러 + 저장 차단 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("a")  # 최소 미달
            page_logged_in_profile.wait_for_timeout(300)
            assert page.is_save_btn_disabled(), \
                "[FAIL] FULLTC-380: 최소 미달 상태에서 저장 버튼 활성화"
        except Exception as e:
            page.take_screenshot("FULLTC-380_failure")
            raise e

    @pytest.mark.parametrize("special_char", ["!", "@", "#", "$", "%"])
    def test_fulltc_381_special_char_blocked(self, page_logged_in_profile, special_char):
        """FULLTC-381 | 특수문자 입력 차단 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname(f"user{special_char}")
            page_logged_in_profile.wait_for_timeout(300)
            blocked = (
                special_char not in page.get_nickname_value()
                or page.is_save_btn_disabled()
            )
            assert blocked, \
                f"[FAIL] FULLTC-381: 특수문자 '{special_char}' 입력 차단/저장 차단 미동작"
        except Exception as e:
            page.take_screenshot(f"FULLTC-381_{special_char}_failure")
            raise e

    def test_fulltc_382_blank_only_blocked(self, page_logged_in_profile):
        """FULLTC-382 | 공백만 입력 → 저장 차단 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("     ")
            page_logged_in_profile.wait_for_timeout(300)
            assert page.is_save_btn_disabled(), \
                "[FAIL] FULLTC-382: 공백만 입력 시 저장 버튼 활성화"
        except Exception as e:
            page.take_screenshot("FULLTC-382_failure")
            raise e

    def test_fulltc_383_forbidden_word_blocked(self, page_logged_in_profile):
        """FULLTC-383 | 금칙어 닉네임 → 안내 + 저장 차단 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("admin")  # TODO: 실 금칙어 사전 매칭 단어로 교체
            page.click_duplicate_check()
            page_logged_in_profile.wait_for_timeout(500)
            forbidden_visible = page_logged_in_profile.is_visible(page.NICKNAME_FORBIDDEN_ERROR)
            disabled = page.is_save_btn_disabled()
            assert forbidden_visible or disabled, \
                "[FAIL] FULLTC-383: 금칙어 닉네임 입력 시 안내 미노출 + 저장 활성화"
        except Exception as e:
            page.take_screenshot("FULLTC-383_failure")
            raise e

    def test_fulltc_384_duplicate_check_available(self, page_logged_in_profile):
        """FULLTC-384 | 중복확인 — 사용 가능 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("uniq_user_42")  # TODO: 미사용 닉네임으로 교체
            page.click_duplicate_check()
            assert page_logged_in_profile.is_visible(page.NICKNAME_DUP_MSG_OK), \
                "[FAIL] FULLTC-384: '사용 가능한 닉네임' 안내 미노출"
        except Exception as e:
            page.take_screenshot("FULLTC-384_failure")
            raise e

    def test_fulltc_385_duplicate_check_taken(self, page_logged_in_profile):
        """FULLTC-385 | 중복확인 — 이미 사용 중 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("taken_user")  # TODO: 실제 사용 중 닉네임으로 교체
            page.click_duplicate_check()
            assert page_logged_in_profile.is_visible(page.NICKNAME_DUP_MSG_FAIL), \
                "[FAIL] FULLTC-385: '이미 사용 중인 닉네임' 안내 미노출"
            assert page.is_save_btn_disabled(), \
                "[FAIL] FULLTC-385: 중복 닉네임 상태에서 저장 버튼 활성화"
        except Exception as e:
            page.take_screenshot("FULLTC-385_failure")
            raise e


# ════════════════════════════════════════════════
# 영역 3 — 소개글 (FULLTC-386 ~ 388) [본 페이지 미존재 → skip]
# ════════════════════════════════════════════════

class TestBio:

    def test_fulltc_386_valid_bio_input(self, page_logged_in_profile):
        """FULLTC-386 | 정상 소개글 입력 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            if not page.is_bio_field_present():
                pytest.skip("FULLTC-386: 본 페이지 DOM에 소개글 영역 미존재 (skip)")
            sample = "안녕하세요, 테스트 소개글입니다."
            page.fill_bio(sample)
            assert page.get_bio_value() == sample, \
                f"[FAIL] FULLTC-386: 입력된 소개글 미반영 (실제: '{page.get_bio_value()}')"
            assert page.is_save_btn_enabled(), \
                "[FAIL] FULLTC-386: 정상 소개글 입력 후 저장 버튼 비활성화"
        except Exception as e:
            page.take_screenshot("FULLTC-386_failure")
            raise e

    def test_fulltc_387_bio_max_length_truncate(self, page_logged_in_profile):
        """FULLTC-387 | 소개글 최대 글자 수 초과 차단/트리밍 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            if not page.is_bio_field_present():
                pytest.skip("FULLTC-387: 본 페이지 DOM에 소개글 영역 미존재 (skip)")
            over = "가" * (ProfileEditWebPage.BIO_MAX_LENGTH + 20)
            page.fill_bio(over)
            actual = page.get_bio_value()
            assert len(actual) <= ProfileEditWebPage.BIO_MAX_LENGTH, \
                f"[FAIL] FULLTC-387: 소개글 글자 수 제한 초과 차단 미동작 (실제 길이: {len(actual)})"
        except Exception as e:
            page.take_screenshot("FULLTC-387_failure")
            raise e

    def test_fulltc_388_bio_counter_realtime(self, page_logged_in_profile):
        """FULLTC-388 | 소개글 글자 수 카운터 실시간 표시 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            if not page.is_bio_field_present():
                pytest.skip("FULLTC-388: 본 페이지 DOM에 소개글 영역 미존재 (skip)")
            sample = "테스트소개글입니다바이오"  # 12자
            page.fill_bio(sample)
            page_logged_in_profile.wait_for_timeout(200)
            counter_text = page.get_bio_counter_text()
            assert (
                str(len(sample)) in counter_text
                and str(ProfileEditWebPage.BIO_MAX_LENGTH) in counter_text
            ), (
                f"[FAIL] FULLTC-388: 소개글 카운터 실시간 표시 불일치. "
                f"기대 '{len(sample)}/{ProfileEditWebPage.BIO_MAX_LENGTH}', 실제: '{counter_text}'"
            )
        except Exception as e:
            page.take_screenshot("FULLTC-388_failure")
            raise e


# ════════════════════════════════════════════════
# 영역 4 — 변경 저장 (FULLTC-389 ~ 392)
# ════════════════════════════════════════════════

class TestSaveChanges:

    def test_fulltc_389_save_success_toast(self, page_logged_in_profile):
        """FULLTC-389 | 저장 성공 Toast 표시 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("save_user_01")  # TODO: 실 미사용 닉네임으로 교체
            page.click_save()
            page_logged_in_profile.wait_for_selector(page.SAVE_SUCCESS_TOAST, timeout=5000)
            assert page_logged_in_profile.is_visible(page.SAVE_SUCCESS_TOAST), \
                "[FAIL] FULLTC-389: 저장 성공 Toast 미노출"
        except Exception as e:
            page.take_screenshot("FULLTC-389_failure")
            raise e

    def test_fulltc_390_persist_after_refresh(self, page_logged_in_profile):
        """FULLTC-390 | 새로고침(F5) 후 저장 데이터 유지 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            target = "f5_user_01"
            page.fill_nickname(target)
            page.click_save()
            page_logged_in_profile.wait_for_timeout(1000)

            page_logged_in_profile.reload()
            page_logged_in_profile.wait_for_load_state("networkidle")
            page.navigate_profile_edit()
            assert page.get_nickname_value() == target, \
                f"[FAIL] FULLTC-390: 새로고침 후 저장값 미유지 (실제: '{page.get_nickname_value()}')"
        except Exception as e:
            page.take_screenshot("FULLTC-390_failure")
            raise e

    def test_fulltc_391_persist_after_relogin(self, page_logged_in_profile):
        """FULLTC-391 | 로그아웃 → 재로그인 후 저장 데이터 유지 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            target = "relog_user01"
            page.fill_nickname(target)
            page.click_save()
            page_logged_in_profile.wait_for_timeout(1000)

            # TODO: 실 STG 계정 정보로 교체
            page.relogin_and_return("qa-test@bloomingbit.io", "password1234!")
            assert page.get_nickname_value() == target, \
                f"[FAIL] FULLTC-391: 재로그인 후 저장값 미유지 (실제: '{page.get_nickname_value()}')"
        except Exception as e:
            page.take_screenshot("FULLTC-391_failure")
            raise e

    def test_fulltc_392_save_btn_disabled_when_no_changes(self, page_logged_in_profile):
        """
        FULLTC-392 | 변경 없이 저장 버튼 → 비활성(disabled) — Minor
        Given: 로그인 + 프로필 편집 진입, 어떠한 변경도 없는 초기 상태
        When:  '저장하기' 버튼 상태 확인
        Then:  저장 버튼이 disabled 상태여야 함 (메시지 검사 없음)
        """
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            assert page.is_save_btn_disabled(), \
                "[FAIL] FULLTC-392: 변경 없는 상태에서 저장 버튼이 비활성화(disabled) 되지 않음"
        except Exception as e:
            page.take_screenshot("FULLTC-392_failure")
            raise e


# ════════════════════════════════════════════════
# 영역 5 — 이탈 방지 (FULLTC-393 ~ 397) [본 페이지 미존재 → skip]
# ════════════════════════════════════════════════

class TestLeaveGuard:

    def test_fulltc_393_cancel_with_changes_shows_warning(self, page_logged_in_profile):
        """FULLTC-393 | 변경 후 취소 → 미저장 경고 팝업 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("leave_test1")
            page.click_cancel()
            page_logged_in_profile.wait_for_timeout(500)
            if not page.is_leave_popup_supported():
                pytest.skip("FULLTC-393: 본 페이지 DOM에 이탈 방지 팝업 미지원 (skip)")
            assert page.is_leave_popup_visible(), \
                "[FAIL] FULLTC-393: 변경 후 취소 클릭 시 미저장 경고 팝업 미노출"
        except Exception as e:
            page.take_screenshot("FULLTC-393_failure")
            raise e

    def test_fulltc_394_browser_back_with_changes_shows_warning(self, page_logged_in_profile):
        """FULLTC-394 | 변경 후 뒤로가기 → 미저장 경고 팝업 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("leave_test2")
            page.click_browser_back()
            page_logged_in_profile.wait_for_timeout(500)
            if not page.is_leave_popup_supported():
                pytest.skip("FULLTC-394: 본 페이지 DOM에 이탈 방지 팝업 미지원 (skip)")
            assert page.is_leave_popup_visible(), \
                "[FAIL] FULLTC-394: 뒤로가기 시 미저장 경고 팝업 미노출"
        except Exception as e:
            page.take_screenshot("FULLTC-394_failure")
            raise e

    def test_fulltc_395_continue_edit_keeps_page(self, page_logged_in_profile):
        """FULLTC-395 | '계속 수정' → 팝업 닫힘 + 편집 페이지 유지 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.fill_nickname("leave_test3")
            page.click_cancel()
            page_logged_in_profile.wait_for_timeout(500)
            if not page.is_leave_popup_supported():
                pytest.skip("FULLTC-395: 본 페이지 DOM에 이탈 방지 팝업 미지원 (skip)")
            page.click_continue_edit()
            page_logged_in_profile.wait_for_timeout(500)

            assert not page.is_leave_popup_visible(), \
                "[FAIL] FULLTC-395: '계속 수정' 클릭 후에도 경고 팝업 미닫힘"
            assert "/mypage/profile" in page_logged_in_profile.url, \
                f"[FAIL] FULLTC-395: '계속 수정' 후 편집 페이지 미유지 (현재 URL: {page_logged_in_profile.url})"
        except Exception as e:
            page.take_screenshot("FULLTC-395_failure")
            raise e

    def test_fulltc_396_leave_discards_changes(self, page_logged_in_profile):
        """FULLTC-396 | '나가기' → 변경 폐기 + 이전 페이지 이동 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            before_url = page_logged_in_profile.url
            page.fill_nickname("leave_test4")
            page.click_cancel()
            page_logged_in_profile.wait_for_timeout(500)
            if not page.is_leave_popup_supported():
                pytest.skip("FULLTC-396: 본 페이지 DOM에 이탈 방지 팝업 미지원 (skip)")
            page.click_leave()
            page_logged_in_profile.wait_for_timeout(1000)

            assert page_logged_in_profile.url != before_url, \
                "[FAIL] FULLTC-396: '나가기' 클릭 후 페이지 이동 미동작"
        except Exception as e:
            page.take_screenshot("FULLTC-396_failure")
            raise e

    def test_fulltc_397_cancel_without_changes_no_warning(self, page_logged_in_profile):
        """FULLTC-397 | 변경 없이 취소 → 경고 없이 정상 이동 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            before_url = page_logged_in_profile.url
            page.click_cancel()
            page_logged_in_profile.wait_for_timeout(500)

            assert not page.is_leave_popup_visible(), \
                "[FAIL] FULLTC-397: 변경 없는 상태에서 취소 시 불필요한 경고 팝업 노출"
            assert page_logged_in_profile.url != before_url, \
                "[FAIL] FULLTC-397: 변경 없는 상태 취소 시 페이지 이동 미동작"
        except Exception as e:
            page.take_screenshot("FULLTC-397_failure")
            raise e


# ════════════════════════════════════════════════
# 영역 6 — UI/UX (FULLTC-398 ~ 400)
# ════════════════════════════════════════════════

class TestUIUX:

    @pytest.mark.parametrize("field_attr, tc_id, skip_if_missing", [
        ("NICKNAME_INPUT", "FULLTC-398a", False),
        ("BIO_INPUT",      "FULLTC-398b", True),
    ])
    def test_fulltc_398_input_focus_ui(self, page_logged_in_profile, field_attr, tc_id, skip_if_missing):
        """FULLTC-398 | 입력 필드 포커스 시 시각 효과 표시 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            selector = getattr(ProfileEditWebPage, field_attr)
            if skip_if_missing and page_logged_in_profile.locator(selector).count() == 0:
                pytest.skip(f"{tc_id}: 본 페이지 DOM에 {field_attr} 미존재 (skip)")

            page_logged_in_profile.click(selector)
            page_logged_in_profile.wait_for_timeout(200)

            element = page_logged_in_profile.locator(selector).first
            class_attr = element.get_attribute("class") or ""
            data_state = element.get_attribute("data-state") or ""
            is_active_element = element.evaluate("el => el === document.activeElement")
            focused = (
                "focused" in class_attr.lower()
                or data_state == "focused"
                or is_active_element
            )
            assert focused, (
                f"[FAIL] {tc_id}: 입력 필드 포커스 효과 미반영 "
                f"(class='{class_attr}', data-state='{data_state}', activeElement={is_active_element})"
            )
        except Exception as e:
            page.take_screenshot(f"{tc_id}_failure")
            raise e

    def test_fulltc_399_save_disabled_when_required_missing(self, page_logged_in_profile):
        """FULLTC-399 | 필수값(닉네임) 비어 있을 때 저장 버튼 비활성 — Major"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            page.clear_nickname()
            page_logged_in_profile.wait_for_timeout(200)
            assert page.is_save_btn_disabled(), \
                "[FAIL] FULLTC-399: 닉네임 비어 있을 때 저장 버튼 비활성화 미동작"
        except Exception as e:
            page.take_screenshot("FULLTC-399_failure")
            raise e

    def test_fulltc_400_nickname_counter_realtime(self, page_logged_in_profile):
        """FULLTC-400 | 닉네임 글자 수 카운터 실시간 표시 — Minor"""
        page = ProfileEditWebPage(page_logged_in_profile)
        try:
            page.navigate_profile_edit()
            sample = "test"  # 4자
            page.clear_nickname()
            page.fill_nickname(sample)
            page_logged_in_profile.wait_for_timeout(200)
            counter_text = page.get_nickname_counter_text()
            assert (
                str(len(sample)) in counter_text
                and str(ProfileEditWebPage.NICKNAME_MAX_LENGTH) in counter_text
            ), (
                f"[FAIL] FULLTC-400: 닉네임 카운터 실시간 표시 불일치. "
                f"기대 '{len(sample)}/{ProfileEditWebPage.NICKNAME_MAX_LENGTH}', 실제: '{counter_text}'"
            )
        except Exception as e:
            page.take_screenshot("FULLTC-400_failure")
            raise e