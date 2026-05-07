"""
ProfileEditWebPage — Bloomingbit STG (Final / All-merged)
STG URL: https://web-stg.bloomingbit.io
영역: 프로필 편집

[Final 병합 사항]
  1) PROFILE_EDIT_URL 수정: /mypage/profile/edit → /mypage/profile  (★ 404 원인 제거)
  2) 실 HTML 기반 셀렉터 전면 교체 (CSS Modules 해시 무관 [class*='...'] 부분 매칭)
  3) navigate_profile_edit(): #myPageProfileEditContainer 대기 제거
     → 닉네임 입력창 + 저장 버튼 visible 대기로 안전 교체
  4) is_save_btn_disabled(): 명시 class 셀렉터 + .first + visible 대기 강화

[셀렉터 전략]
  - 모호 매칭 방지: 부모 wrapper 스코프로 단일 후손 매칭
  - Playwright 빌트인 로케이터 헬퍼 제공 (get_by_placeholder / get_by_role)
  - 본 페이지 미존재 영역(소개글/이탈팝업/이미지삭제)은 [PENDING] + 사전 체크 헬퍼
"""
import os
from playwright.sync_api import Page, Locator


class ProfileEditWebPage:
    BASE_URL = "https://web-stg.bloomingbit.io"
    # ★ Final 수정: 실제 서비스 프로필 편집 화면 URL은 /mypage/profile
    PROFILE_EDIT_URL = f"{BASE_URL}/mypage/profile"

    DEFAULT_TIMEOUT_MS = 10_000

    # ════════════════════════════════════════════
    # ✔ 프로필 이미지 (실 DOM)
    # ════════════════════════════════════════════
    PROFILE_IMAGE_WRAPPER       = "button[class*='profileImageWrapper']"
    PROFILE_IMAGE_PREVIEW       = "button[class*='profileImageWrapper'] img"
    PROFILE_IMAGE_INNER         = "[class*='userProfileImg']"
    PROFILE_PHOTO_SYMBOL        = "[class*='profilePhotoSymbol']"
    IMAGE_CHANGE_BTN            = "button[class*='profileImageWrapper']"
    IMAGE_FILE_INPUT            = "input[type='file'][accept*='image']"
    PROFILE_IMAGE_DEFAULT       = "button[class*='profileImageWrapper'] img[src*='default']"
    # [PENDING - 본 페이지 미존재]
    IMAGE_DELETE_BTN            = "button[class*='imageDelete'], button:has-text('이미지 삭제'):visible"
    IMAGE_FORMAT_ERROR          = "[class*='toast']:has-text('형식'), [class*='alert']:has-text('형식')"
    IMAGE_SIZE_ERROR            = "[class*='toast']:has-text('용량'), [class*='alert']:has-text('용량')"

    # ════════════════════════════════════════════
    # ✔ 유저 아이디 (TC상 닉네임 매핑)
    # ════════════════════════════════════════════
    NICKNAME_SECTION            = "[class*='userIdEditBox']"
    NICKNAME_INPUT_WRAPPER      = "[class*='userIdInputWrapper']"
    # ★ 부모 wrapper 스코프로 단일 input 매칭 (모호 매칭 방지)
    NICKNAME_INPUT              = "[class*='userIdInputWrapper'] input"
    NICKNAME_COUNTER            = "[class*='userIdInputWrapper'] [class*='commonInputInner'] [class*='length']"
    NICKNAME_LABEL              = "[class*='userIdEditBox'] [class*='commonInputLabel']"
    # ★ 별도 중복확인 버튼 미존재 → 통합 저장 버튼이 검증 처리
    NICKNAME_DUP_CHECK_BTN      = "button[class*='userIdSaveBtn']"
    NICKNAME_VALIDATION_BOX     = "[class*='userIdValidationBox']"
    NICKNAME_VALIDATION_ITEMS   = "[class*='userIdCondition']"
    NICKNAME_VALIDATION_CHECK_OK = "[class*='userIdCondition'] svg[class*='checkSVG']"
    NICKNAME_DUP_MSG_OK         = "[class*='userIdCondition']:has-text('사용 가능'), [class*='toast']:has-text('사용 가능')"
    NICKNAME_DUP_MSG_FAIL       = "[class*='userIdCondition']:has-text('이미 사용'), [class*='toast']:has-text('이미 사용')"
    NICKNAME_MIN_LENGTH_ERROR   = "[class*='userIdCondition']:has-text('최소'), [class*='toast']:has-text('최소'), [class*='guideText']:has-text('최소')"
    NICKNAME_SPECIAL_CHAR_ERROR = "[class*='userIdCondition']:has-text('영문'), [class*='toast']:has-text('영문')"
    NICKNAME_BLANK_ERROR        = "[class*='userIdCondition']:has-text('필수'), [class*='toast']:has-text('필수'), [class*='toast']:has-text('공백')"
    NICKNAME_FORBIDDEN_ERROR    = "[class*='toast']:has-text('금칙'), [class*='toast']:has-text('사용할 수 없'), [class*='alert']:has-text('금칙')"
    NICKNAME_GUIDE_TEXT         = "[class*='idChangeGuideText']"

    # ════════════════════════════════════════════
    # ✘ 소개글 [PENDING - 본 페이지 미존재]
    # ════════════════════════════════════════════
    BIO_INPUT                   = "textarea[placeholder*='소개'], [class*='bioEditBox'] textarea"
    BIO_COUNTER                 = "[class*='bioEditBox'] [class*='length'], textarea + [class*='length']"

    # ════════════════════════════════════════════
    # ✔ 저장 / 취소
    # ════════════════════════════════════════════
    SAVE_BTN                    = "button[class*='userIdSaveBtn']"
    WITHDRAW_BTN                = "button[class*='withdrawBtn']"
    HEADER_BACK_BTN             = "header[class*='contentHeader'] a[class*='backBtn']"
    CANCEL_BTN                  = "header[class*='contentHeader'] a[class*='backBtn']"
    SAVE_SUCCESS_TOAST          = "[class*='toast']:has-text('저장'), [class*='toast']:has-text('완료'), [class*='snackbar']"
    NO_CHANGES_MSG              = "[class*='toast']:has-text('변경'), [class*='guideText']:has-text('변경')"

    # ════════════════════════════════════════════
    # ✘ 이탈 방지 팝업 [PENDING - 본 페이지 미존재]
    # ════════════════════════════════════════════
    LEAVE_WARNING_POPUP         = "[role='dialog']:has-text('변경'), [class*='confirmPopup']:has-text('변경'), [class*='modal']:has-text('변경')"
    LEAVE_POPUP_CONTINUE_BTN    = "[role='dialog'] button:has-text('계속 수정'):visible"
    LEAVE_POPUP_LEAVE_BTN       = "[role='dialog'] button:has-text('나가기'):visible"

    # ════════════════════════════════════════════
    # ✔ 기타 (참고)
    # ════════════════════════════════════════════
    COUNTRY_INPUT_PLACEHOLDER   = "국가명을 영문으로 입력해주세요"
    SOCIAL_LOGIN_TYPE           = "[class*='socialName']"
    USER_EMAIL_DISPLAY          = "[class*='userEmail']"
    PAGE_HEADER_TITLE           = "header[class*='contentHeader'] h1"

    # ════════════════════════════════════════════
    # [PENDING] 로그아웃
    # ════════════════════════════════════════════
    LOGOUT_BTN                  = "button:has-text('로그아웃'):visible, [data-testid*='logout']"

    # ════════════════════════════════════════════
    # 테스트 픽스처 파일
    # ════════════════════════════════════════════
    SAMPLE_IMAGE_VALID_JPG      = "tests/fixtures/profile/sample_valid.jpg"
    SAMPLE_IMAGE_VALID_PNG      = "tests/fixtures/profile/sample_valid.png"
    SAMPLE_IMAGE_INVALID_PDF    = "tests/fixtures/profile/sample_invalid.pdf"
    SAMPLE_IMAGE_INVALID_GIF    = "tests/fixtures/profile/sample_invalid.gif"
    SAMPLE_IMAGE_OVERSIZE       = "tests/fixtures/profile/sample_oversize.jpg"

    # ════════════════════════════════════════════
    # 정책 상수 (실 DOM minlength/maxlength 반영)
    # ════════════════════════════════════════════
    NICKNAME_MIN_LENGTH = 4    # input minlength="4"
    NICKNAME_MAX_LENGTH = 15   # input maxlength="15"
    BIO_MAX_LENGTH      = 100  # [PENDING] 본 페이지 미존재

    def __init__(self, page: Page):
        self.page = page

    # ─────────────────────────────────────────────
    # Playwright 빌트인 로케이터 헬퍼
    # ─────────────────────────────────────────────
    def nickname_input_locator(self) -> Locator:
        """userIdInputWrapper 스코프 + get_by_role(textbox) 빌트인 매칭"""
        return self.page.locator(self.NICKNAME_INPUT_WRAPPER).get_by_role("textbox")

    def country_input_locator(self) -> Locator:
        return self.page.get_by_placeholder(self.COUNTRY_INPUT_PLACEHOLDER)

    def save_btn_locator(self) -> Locator:
        """class 명시 셀렉터 + .first로 단일 매칭 보장"""
        return self.page.locator(self.SAVE_BTN).first

    def withdraw_btn_locator(self) -> Locator:
        return self.page.get_by_role("button", name="탈퇴하기")

    def back_btn_locator(self) -> Locator:
        return self.page.locator(self.HEADER_BACK_BTN)

    # ─────────────────────────────────────────────
    # 네비게이션 / 공통
    # ─────────────────────────────────────────────
    def navigate_profile_edit(self):
        """
        프로필 편집 페이지 진입 + 핵심 요소 렌더링 보장.
          - ★ URL: /mypage/profile (수정됨)
          - 무한 타임아웃 유발 원인이던 #myPageProfileEditContainer 대기 제거
          - 안전한 대기: 닉네임 입력창 + 저장 버튼 visible 으로 교체
        """
        self.page.goto(self.PROFILE_EDIT_URL)
        self.page.wait_for_load_state("networkidle")
        # 핵심 입력/버튼이 실제로 보일 때까지 대기 (실 화면 도달 보장)
        self.page.wait_for_selector(
            self.NICKNAME_INPUT,
            state="visible",
            timeout=self.DEFAULT_TIMEOUT_MS,
        )
        self.page.wait_for_selector(
            self.SAVE_BTN,
            state="visible",
            timeout=self.DEFAULT_TIMEOUT_MS,
        )

    def take_screenshot(self, name: str):
        os.makedirs("screenshots", exist_ok=True)
        self.page.screenshot(path=f"screenshots/{name}.png")

    # ─────────────────────────────────────────────
    # 이미지 액션
    # ─────────────────────────────────────────────
    def upload_profile_image(self, file_path: str):
        """
        wrapper 클릭 → file chooser 콜백 (SPA hidden input 대비).
        force=True로 hover 의존성 회피.
        """
        try:
            with self.page.expect_file_chooser(timeout=5000) as fc_info:
                self.page.click(self.IMAGE_CHANGE_BTN, force=True)
            fc_info.value.set_files(file_path)
        except Exception:
            self.page.set_input_files(self.IMAGE_FILE_INPUT, file_path)
        self.page.wait_for_timeout(500)

    def click_image_delete(self):
        """[PENDING - 본 페이지 미존재]"""
        self.page.click(self.IMAGE_DELETE_BTN, force=True)

    def get_preview_src(self) -> str:
        return self.page.get_attribute(self.PROFILE_IMAGE_PREVIEW, "src") or ""

    def is_default_image(self) -> bool:
        src = self.get_preview_src()
        return (not src) or ("default" in src.lower())

    # ─────────────────────────────────────────────
    # 닉네임(유저 아이디) 액션
    # ─────────────────────────────────────────────
    def fill_nickname(self, value: str):
        loc = self.nickname_input_locator()
        loc.click()
        loc.fill(value)

    def clear_nickname(self):
        loc = self.nickname_input_locator()
        loc.click()
        loc.fill("")

    def get_nickname_value(self) -> str:
        return self.nickname_input_locator().input_value()

    def get_nickname_counter_text(self) -> str:
        return self.page.inner_text(self.NICKNAME_COUNTER)

    def click_duplicate_check(self):
        """별도 중복확인 버튼 미존재 → 저장 버튼이 통합 검증"""
        self.save_btn_locator().click(force=True)
        self.page.wait_for_timeout(500)

    # ─────────────────────────────────────────────
    # 소개글 액션 [PENDING - 본 페이지 미존재]
    # ─────────────────────────────────────────────
    def fill_bio(self, value: str):
        self.page.fill(self.BIO_INPUT, value)

    def clear_bio(self):
        self.page.fill(self.BIO_INPUT, "")

    def get_bio_value(self) -> str:
        return self.page.input_value(self.BIO_INPUT)

    def get_bio_counter_text(self) -> str:
        return self.page.inner_text(self.BIO_COUNTER)

    def is_bio_field_present(self) -> bool:
        """본 페이지 소개글 영역 실재 여부 사전 체크 — 미존재 시 테스트 skip 가능"""
        return self.page.locator(self.BIO_INPUT).count() > 0

    # ─────────────────────────────────────────────
    # 저장 / 취소 액션
    # ─────────────────────────────────────────────
    def click_save(self):
        """일반 클릭 — 비활성 상태면 자동 대기/오류 (의도된 동작)"""
        self.save_btn_locator().click()

    def click_save_force(self):
        """비활성 검증 후 강제 클릭이 필요한 케이스 전용"""
        self.save_btn_locator().click(force=True)

    def click_cancel(self):
        """별도 취소 버튼 미존재 → 헤더 backBtn으로 대체"""
        self.back_btn_locator().click(force=True)

    def is_save_btn_disabled(self) -> bool:
        """
        저장 버튼 disabled 상태 정확 판정.
          - 명시적 class 셀렉터(button[class*='userIdSaveBtn'])
          - .first로 strict mode 안전성 확보
          - is_disabled()는 disabled 속성 + aria-disabled='true' 모두 감지
        """
        btn = self.save_btn_locator()
        btn.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT_MS)
        return btn.is_disabled()

    def is_save_btn_enabled(self) -> bool:
        btn = self.save_btn_locator()
        btn.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT_MS)
        return btn.is_enabled()

    # ─────────────────────────────────────────────
    # 이탈 방지 [PENDING - 본 페이지 미존재]
    # ─────────────────────────────────────────────
    def click_browser_back(self):
        self.page.go_back()

    def click_continue_edit(self):
        self.page.click(self.LEAVE_POPUP_CONTINUE_BTN, force=True)

    def click_leave(self):
        self.page.click(self.LEAVE_POPUP_LEAVE_BTN, force=True)

    def is_leave_popup_visible(self) -> bool:
        return (
            self.page.locator(self.LEAVE_WARNING_POPUP).count() > 0
            and self.page.is_visible(self.LEAVE_WARNING_POPUP)
        )

    def is_leave_popup_supported(self) -> bool:
        """이탈 방지 팝업 실재 여부 — 미지원 시 skip 권장"""
        return self.page.locator(self.LEAVE_WARNING_POPUP).count() > 0

    # ─────────────────────────────────────────────
    # 로그아웃 / 재로그인
    # ─────────────────────────────────────────────
    def logout(self):
        self.page.click(self.LOGOUT_BTN, force=True)
        self.page.wait_for_load_state("networkidle")

    def relogin_and_return(self, email: str, password: str):
        self.logout()
        self.page.goto(f"{self.BASE_URL}/login")
        self.page.fill("input[type='email'], input[placeholder*='이메일']", email)
        self.page.fill("input[type='password'], input[placeholder*='비밀번호']", password)
        self.page.click("button[type='submit']:has-text('로그인')")
        self.page.wait_for_load_state("networkidle")
        self.navigate_profile_edit()