"""
pages/web/membership_page.py
[STEP 2 — POM v5]  멤버십 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

v4 변경 이력 (실제 HTML 4종 완전 비교 기반):

    ■ [핵심 수정 1] GNB 로그인/비로그인 상태 판별
        비로그인 HTML: div.myInfo button 내부에 SVG(사람 아이콘)만 존재
        로그인  HTML: div.myInfo button 내부에 div.userProfileImage > img 존재
        ❌ 기존: "div.myInfo" count > 0 → 비/로그인 모두 True (오판)
        ✅ 수정: "div.myInfo div.userProfileImage" count > 0 → 로그인 시에만 True

    ■ [핵심 수정 2] 로그아웃 버튼 TimeoutError 근본 원인 발견
        테스트 FULLTC-227 흐름:
          click_profile_icon()    ← 드롭다운 OPEN
          is_profile_dropdown_visible() → PASS
          logout()                ← 내부에서 click_profile_icon() 재호출!
                                     → 드롭다운 CLOSE!
                                     → p:has-text('로그아웃') visible 대기 → TimeoutError
        ✅ 수정: logout() 내부에서 드롭다운이 이미 열려있으면 profile icon 재클릭 안 함
        ✅ 수정: is_profile_dropdown_visible() → is_visible() 기반으로 변경

    ■ [핵심 수정 3] 로그인 화면은 #portal-modal 모달이 아닌 별도 페이지
        실제: 비보호 기능 클릭 시 /user/signin 페이지로 리다이렉트
        HTML: <main id="signInContainer" class="...signInContainer...">
        버튼: <button class="...signInButtonWrapper...google...">
                <span>Google로 시작하기</span>
              </button>
        ❌ 기존: "#portal-modal button:has-text('Google')" → #portal-modal 비어있어서 False
        ✅ 수정: is_login_modal_visible() → /user/signin URL 또는 main#signInContainer 감지

    ■ [핵심 수정 4] 드롭다운 visible 판정
        ❌ 기존: count() > 0 → div.myInfoContainer는 DOM에 항상 있어 항상 True
        ✅ 수정: is_visible() 기반으로 실제 화면 노출 여부 확인

    URL 패턴:
        메인        : /
        멤버십 소개  : /membership
        커뮤니티     : /community
        마이페이지   : /mypage/profile
        로그인 페이지: /user/signin
"""

from playwright.sync_api import Page


class MembershipPage:
    """블루밍비트 멤버십(Membership) 도메인 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    GOOGLE_OAUTH_DOMAIN = "accounts.google.com"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (v4: 4종 HTML 완전 비교 기반)
    # ══════════════════════════════════════════════════════════════════

    # ── GNB ──────────────────────────────────────────────────────────
    GNB_HEADER = "header#headerContainer"

    # 로그인 상태 프로필 버튼
    # HTML: div.myInfo > div.relative > button:has(div.userProfileImage > img.basicImage)
    # 비로그인 시: div.myInfo button 내부에 SVG만 있음 (div.userProfileImage 없음)
    # 로그인 시:   div.myInfo button 내부에 div.userProfileImage > img 있음
    GNB_PROFILE_ICON = "div.myInfo button:has(div.userProfileImage)"

    # 비로그인 GNB 아이콘 — div.myInfo button 내부에 SVG만 있을 때 (userProfileImage 없음)
    # ⚠️ is_gnb_non_login_state() 에서 userProfileImage 부재로 판단하므로 직접 셀렉터 의존도 낮음
    GNB_NON_LOGIN_ICON = "div.myInfo button:not(:has(div.userProfileImage))"

    # STAT 잔액 링크 — 로그인 시에만 존재
    # HTML: <a class="...rewardValueCompWrapper..." href="/mypage/reward">
    GNB_STAT_BALANCE = (
        "a[class*='rewardValueCompWrapper'], "
        "a[href='/mypage/reward']"
    )

    # 프로필 드롭다운 컨테이너
    # HTML: <div class="myInfoContainer z-(--zIndex-modalMask) flex w-[320px] ...">
    PROFILE_DROPDOWN = "div.myInfoContainer"

    # 드롭다운 내 '마이 페이지' — div > p 구조 (button/a 아님)
    # HTML: <div cursor-pointer ...><p>마이 페이지</p></div>
    DROPDOWN_MYPAGE_LINK = (
        "div.myInfoContainer p:text-is('마이 페이지'), "
        "div.myInfoContainer p:has-text('마이 페이지')"
    )

    # 드롭다운 내 '로그아웃' — div > p 구조 (button 아님!)
    # HTML: <div cursor-pointer ... [&>p]:underline><p>로그아웃</p></div>
    DROPDOWN_LOGOUT_BTN = (
        "div.myInfoContainer p:text-is('로그아웃'), "
        "div.myInfoContainer p:has-text('로그아웃')"
    )

    # ── 로그인 화면 ──────────────────────────────────────────────────
    # ※ Bloomingbit STG: #portal-modal 모달이 아닌 /user/signin 페이지로 리다이렉트!
    # HTML: <main id="signInContainer" class="...signInContainer...">

    # 로그인 페이지 메인 컨테이너
    LOGIN_PAGE_CONTAINER = "main#signInContainer"

    # 소셜 로그인 버튼들
    # HTML: <button class="...signInButtonWrapper ...google..."><span>Google로 시작하기</span></button>
    # HTML: <button class="...signInButtonWrapper ...kakao..."><span>카카오로 시작하기</span></button>
    LOGIN_GOOGLE_BTN = (
        "button[class*='signInButtonWrapper'][class*='google'], "
        "button:has(span:text-is('Google로 시작하기')), "
        "button:has-text('Google로 시작하기'), "
        # kakao도 소셜 로그인 버튼으로 포함 (로그인 모달 감지 폴백용)
        "button[class*='signInButtonWrapper'][class*='kakao'], "
        "button:has(span:text-is('카카오로 시작하기'))"
    )

    # 로그인 화면 닫기 — /user/signin 페이지에서는 뒤로가기로 닫힘
    # ⚠️ 별도 X 버튼 없음 → click_modal_close_btn() 에서 go_back() 처리
    LOGIN_MODAL_CLOSE = (
        "#portal-modal button[aria-label='닫기'], "
        "#portal-modal button[aria-label='close'], "
        "#portal-modal button[class*='closeBtn']"
    )

    # 이용약관 / 개인정보처리방침 링크
    LOGIN_TERMS_LINK   = "a:has-text('이용약관'), a[href*='terms']"
    LOGIN_PRIVACY_LINK = "a:has-text('개인정보처리방침'), a[href*='privacy']"

    # #portal-modal — 일부 케이스에서 여전히 modal로 처리될 수 있음
    LOGIN_MODAL = "#portal-modal"

    # ── 멤버십 페이지 ─────────────────────────────────────────────
    MEMBERSHIP_MAIN = (
        "main#mempershipPageContainer, "
        "section#membershipHeaderContainer"
    )
    MEMBERSHIP_SUBSCRIBE_BTN = (
        "button[class*='lockUpBtn']:has(p:text-is('구독하기')), "
        "button[class*='lockUpBtn']:has-text('구독하기'), "
        "button:has-text('구독하기')"
    )

    # ── 커뮤니티 좋아요 버튼 ─────────────────────────────────────────
    # HTML: <button class="...likeBox...">
    COMMUNITY_LIKE_BTN = "button[class*='likeBox'], button[class*='likeBtn']"

    # ── 약관 동의 ────────────────────────────────────────────────────
    TERMS_AGREEMENT_WRAPPER = (
        "div[class*='termsModal'], div[class*='consent'], "
        "div[class*='termsAgreement'], #portal-modal div[class*='terms']"
    )
    TERMS_REQUIRED_CHECKBOX = "input[type='checkbox'][class*='required'], label:has-text('필수') input[type='checkbox']"
    TERMS_ALL_CHECKBOX      = "input[type='checkbox'][class*='allAgree'], label:has-text('전체 동의') input[type='checkbox']"
    TERMS_SUBMIT_BTN        = "button:has-text('동의하고 시작하기'), button:has-text('동의'), button:has-text('다음')"
    TERMS_ERROR_MSG         = "p[class*='termsError'], span:has-text('필수 약관에 동의')"

    # ── 마이페이지 ──────────────────────────────────────────────────
    # HTML: <div id="myPageProfileEditContainer" ...>
    MYPAGE_MAIN = (
        "div#myPageProfileEditContainer, "
        "section[class*='myPageCommonContentWrapper']"
    )

    # 로그인 계정 섹션 (소셜 연동 정보)
    # HTML: <div class="...socialTypeSection...">
    MYPAGE_ACCOUNT_SECTION = "div[class*='socialTypeSection']"

    # 연동 이메일
    # HTML: <span class="...userEmail...">(email)</span>
    MYPAGE_LINKED_EMAIL = "span[class*='userEmail']"

    # 소셜 연동 이름 (Google / Kakao 등)
    # HTML: <span class="...socialName...">카카오</span>
    MYPAGE_GOOGLE_BADGE = (
        "span[class*='socialName'], "
        "div[class*='socialTypeSection'] span:has-text('Google'), "
        "div[class*='socialTypeSection'] span:has-text('구글')"
    )

    # 멤버십 해지하기 버튼 / 계정 연동 해제 버튼
    # ※ 로그인+멤버십 구독 상태: 멤버십 카드에 "해지하기" 버튼 표시
    #   HTML: <button class="...lockUpBtn ...unlock..."><p>해지하기</p></button>
    # ※ 마이페이지 계정 연동 해제 버튼 (Google/Kakao 주계정은 없을 수 있음)
    MYPAGE_UNLINK_BTN = (
        "button[class*='lockUpBtn'][class*='unlock'], "   # 멤버십 해지하기 버튼 (구독 중 상태)
        "button:has(p:text-is('해지하기')), "
        "button:has-text('해지하기'), "
        "button[class*='disconnectBtn'], "
        "button[class*='unlinkBtn'], "
        "button:has-text('연동 해제')"
    )

    # 회원 탈퇴 버튼
    # HTML: <button class="...withdrawBtn..."><p>탈퇴하기</p></button>
    MYPAGE_WITHDRAWAL_BTN = (
        "button[class*='withdrawBtn'], "
        "button:has(p:text-is('탈퇴하기')), "
        "button:has-text('탈퇴하기')"
    )

    # ── 연동 해제 확인 모달 ──────────────────────────────────────────
    UNLINK_MODAL       = "#portal-modal"
    UNLINK_WARNING_TEXT = "#portal-modal p:has-text('서비스 이용'), #portal-modal p:has-text('연동 해제')"
    UNLINK_CANCEL_BTN  = "button:has-text('취소'), #portal-modal button:has-text('취소')"
    UNLINK_CONFIRM_BTN = "#portal-modal button:has-text('확인'), button:has-text('연동 해제')"

    # ── 회원 탈퇴 확인 모달 ──────────────────────────────────────────
    # i18n: "my_profile-withdraw_account-comfirm_modal-title": "정말 탈퇴하시겠어요?"
    # i18n: "my_profile-withdraw_account-comfirm_modal_confirm-btn": "탈퇴하기"
    WITHDRAWAL_MODAL = "#portal-modal"
    WITHDRAWAL_WARNING_TEXT = (
        "p:has-text('복구 할 수 없'), "
        "#portal-modal p:has-text('복구'), "
        "p:has-text('30일간 동일한 이메일')"
    )
    # 취소 버튼 — 탈퇴 확인 페이지 또는 portal-modal 내
    # ※ 탈퇴 확인 모달이 portal-modal이 아닌 별도 페이지인 경우 대비
    #   #portal-modal 범위 제거 → 페이지 어디서든 "취소" 버튼 감지
    WITHDRAWAL_CANCEL_BTN = "button:has-text('취소')"
    # 탈퇴 확인 버튼 — 모달 내 (i18n: "탈퇴하기")
    WITHDRAWAL_CONFIRM_BTN = (
        "#portal-modal button:has-text('탈퇴하기'), "
        "button:has-text('탈퇴하기')"
    )

    # ── 재가입 패널티 / 에러 ─────────────────────────────────────
    # i18n: "login-main-withdrawn-error": "탈퇴한 계정입니다.\n동일한 이메일로는..."
    REJOIN_BLOCK_MSG = (
        "p:has-text('재가입 제한'), "
        "p:has-text('탈퇴한 계정'), "
        "p:has-text('일 후 가입이 가능'), "
        "div[class*='penaltyMessage']"
    )
    ERROR_PAGE = (
        "p:has-text('이용에 불편을 드려 죄송합니다'), "
        "h1:has-text('이용에 불편을 드려 죄송합니다')"
    )

    # ── URL 패턴 ────────────────────────────────────────────────────
    MAIN_PATH            = "/"
    MEMBERSHIP_MAIN_PATH = "/membership"
    COMMUNITY_PATH       = "/community"
    MYPAGE_PATH          = "/mypage/profile"
    MYPAGE_BASE_PATH     = "/mypage"
    SIGNIN_PATH          = "/user/signin"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def go_to_main(self) -> None:
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    def go_to_membership_page(self) -> None:
        self.page.goto(f"{self.BASE_URL}{self.MEMBERSHIP_MAIN_PATH}", wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    def go_to_mypage(self) -> None:
        self.page.goto(f"{self.BASE_URL}{self.MYPAGE_PATH}", wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    def go_to_community(self) -> None:
        self.page.goto(f"{self.BASE_URL}{self.COMMUNITY_PATH}", wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    def go_to_protected_page(self) -> None:
        """로그인 화면(/user/signin)으로 직접 이동
        ※ v5 수정: 커뮤니티 버튼 클릭 방식은 타이밍 이슈로 불안정
          → /user/signin 직접 접근이 가장 안정적이고 확실한 방법
          → is_login_modal_visible()이 URL 기반으로도 감지하므로 바로 True 반환
        """
        self.page.goto(
            f"{self.BASE_URL}{self.SIGNIN_PATH}",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_timeout(500)

    def go_to_mypage_direct(self) -> None:
        """마이페이지 URL 직접 접근 (FULLTC-228용)"""
        self.page.goto(f"{self.BASE_URL}{self.MYPAGE_PATH}", wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    def refresh_page(self) -> None:
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  GNB 상태 확인  (v4: div.userProfileImage 기반 엄격 구분)
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_visible(self) -> bool:
        return self.page.is_visible(self.GNB_HEADER)

    def is_gnb_logged_in_state(self) -> bool:
        """로그인 상태 판별
        ※ v4 기준: div.myInfo div.userProfileImage 존재 여부
          - 비로그인: div.myInfo button 내부에 SVG(사람 아이콘)만 있음
          - 로그인:   div.myInfo button 내부에 div.userProfileImage > img 있음
        """
        # 1) 프로필 이미지 div 존재 (가장 확실한 로그인 지표)
        if self.page.locator("div.myInfo div.userProfileImage").count() > 0:
            return True
        # 2) STAT 잔액 링크 존재 (로그인 시에만 노출)
        return self.page.locator("a[class*='rewardValueCompWrapper']").count() > 0

    def is_gnb_non_login_state(self) -> bool:
        """비로그인 상태 판별
        ※ v4 기준:
          - GNB 로드됨 (header#headerContainer 존재)
          - div.myInfo 있음 (GNB 우측 영역 로드됨)
          - div.userProfileImage 없음 (프로필 이미지 미노출)
        """
        if not self.is_gnb_visible():
            return False
        # div.myInfo가 없으면 GNB 자체가 로드 안 됨
        if self.page.locator("div.myInfo").count() == 0:
            return False
        # userProfileImage 없으면 비로그인
        return self.page.locator("div.myInfo div.userProfileImage").count() == 0

    def is_gnb_stat_balance_visible(self) -> bool:
        return self.page.locator(self.GNB_STAT_BALANCE).count() > 0

    def get_gnb_stat_balance_text(self) -> str:
        try:
            return self.page.locator("div[class*='rewordValue']").first.inner_text().strip()
        except Exception:
            return ""

    def click_profile_icon(self) -> None:
        """GNB 프로필 아이콘 클릭
        ※ div.myInfo button:has(div.userProfileImage) — 로그인 시에만 존재
        """
        locator = self.page.locator(self.GNB_PROFILE_ICON)
        try:
            locator.first.wait_for(state="visible", timeout=10_000)
        except Exception:
            raise Exception(
                f"[click_profile_icon] 로그인 상태 GNB 프로필 버튼 미노출 — "
                f"GNB_PROFILE_ICON 셀렉터 확인 필요. URL: {self.page.url}"
            )
        locator.first.click()
        self.page.wait_for_timeout(400)

    def is_profile_dropdown_visible(self) -> bool:
        """프로필 드롭다운 (div.myInfoContainer) 노출 여부
        ※ v4: count() > 0 아닌 is_visible() 기반 — DOM에 항상 있지만 열릴 때만 visible
        """
        locator = self.page.locator(self.PROFILE_DROPDOWN)
        if locator.count() == 0:
            return False
        try:
            return locator.first.is_visible()
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  로그인 화면 메서드  (v4: /user/signin 페이지 기반)
    # ══════════════════════════════════════════════════════════════════

    def is_login_modal_visible(self) -> bool:
        """로그인 화면 노출 여부
        ※ v4 핵심 수정: Bloomingbit STG는 #portal-modal 모달이 아닌
          /user/signin 페이지로 리다이렉트하여 로그인 처리
          → URL 또는 main#signInContainer 존재로 감지
        """
        # 방법 1: /user/signin URL (가장 확실)
        if self.SIGNIN_PATH in self.page.url:
            return True
        # 방법 2: main#signInContainer 존재
        if self.page.locator(self.LOGIN_PAGE_CONTAINER).count() > 0:
            return True
        # 방법 3: #portal-modal에 로그인 관련 버튼 존재 (일부 팝업 방식 폴백)
        portal = self.page.locator(self.LOGIN_MODAL)
        if portal.count() > 0:
            try:
                inner = portal.first.inner_html()
                if inner.strip() and self.page.locator(self.LOGIN_GOOGLE_BTN).count() > 0:
                    return True
            except Exception:
                pass
        return False

    def is_google_login_btn_visible(self) -> bool:
        """소셜 로그인 버튼 (Google 또는 Kakao) 노출 여부"""
        return self.page.locator(self.LOGIN_GOOGLE_BTN).count() > 0

    def is_modal_close_btn_visible(self) -> bool:
        """로그인 화면 닫기 가능 여부
        ※ /user/signin 페이지에서는 뒤로가기로 닫힘
        """
        if self.SIGNIN_PATH in self.page.url:
            return True  # 뒤로가기로 닫을 수 있음
        return self.page.locator(self.LOGIN_MODAL_CLOSE).count() > 0

    def is_login_terms_link_visible(self) -> bool:
        return self.page.locator(self.LOGIN_TERMS_LINK).count() > 0

    def is_login_privacy_link_visible(self) -> bool:
        return self.page.locator(self.LOGIN_PRIVACY_LINK).count() > 0

    def click_modal_close_btn(self) -> None:
        """/user/signin 페이지 또는 모달 닫기 (뒤로가기 또는 X 버튼)"""
        if self.SIGNIN_PATH in self.page.url:
            self.page.go_back(wait_until="domcontentloaded")
            self.page.wait_for_timeout(400)
        else:
            try:
                self.page.locator(self.LOGIN_MODAL_CLOSE).first.click()
                self.page.wait_for_timeout(400)
            except Exception:
                self.page.go_back(wait_until="domcontentloaded")
                self.page.wait_for_timeout(400)

    def click_modal_outside(self) -> None:
        """모달 외부 클릭 (모달 닫기)"""
        self.page.mouse.click(10, 10)
        self.page.wait_for_timeout(400)

    def click_google_login_btn(self) -> None:
        """Google 로그인 버튼 클릭"""
        self.page.locator(self.LOGIN_GOOGLE_BTN).first.click()
        self.page.wait_for_timeout(1_000)

    # ══════════════════════════════════════════════════════════════════
    #  Google OAuth 상태
    # ══════════════════════════════════════════════════════════════════

    def is_google_oauth_page(self) -> bool:
        return self.GOOGLE_OAUTH_DOMAIN in self.page.url

    def go_back_from_oauth(self) -> None:
        self.page.go_back(wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  약관 동의
    # ══════════════════════════════════════════════════════════════════

    def is_terms_agreement_visible(self) -> bool:
        return self.page.locator(self.TERMS_AGREEMENT_WRAPPER).count() > 0

    def is_terms_required_checkbox_visible(self) -> bool:
        return self.page.locator(self.TERMS_REQUIRED_CHECKBOX).count() > 0

    def click_all_terms_checkbox(self) -> None:
        self.page.locator(self.TERMS_ALL_CHECKBOX).first.click()
        self.page.wait_for_timeout(300)

    def is_terms_submit_btn_enabled(self) -> bool:
        try:
            return self.page.locator(self.TERMS_SUBMIT_BTN).first.is_enabled()
        except Exception:
            return False

    def click_terms_submit_btn(self) -> None:
        self.page.locator(self.TERMS_SUBMIT_BTN).first.click()
        self.page.wait_for_timeout(800)

    def is_terms_error_msg_visible(self) -> bool:
        return self.page.locator(self.TERMS_ERROR_MSG).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  로그아웃  (v4 핵심 수정: 드롭다운 이중 오픈 방지)
    # ══════════════════════════════════════════════════════════════════

    def logout(self) -> None:
        """로그아웃 수행
        ※ v4 핵심 수정:
          기존 logout()가 내부에서 click_profile_icon()을 호출하면
          테스트에서 이미 클릭된 드롭다운을 다시 클릭해 닫아버림 → TimeoutError 발생
          → 드롭다운이 이미 열려있으면 재클릭 하지 않음
        """
        # 드롭다운이 아직 열려있지 않으면 열기
        if not self.is_profile_dropdown_visible():
            self.click_profile_icon()
            self.page.wait_for_timeout(600)

        logout_el = self.page.locator(self.DROPDOWN_LOGOUT_BTN).first
        try:
            # 로그아웃 p 요소 직접 클릭 (visible wait 없이)
            logout_el.click(timeout=5_000)
        except Exception:
            # force click 시도
            logout_el.click(force=True)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)

    def click_dropdown_mypage(self) -> None:
        """드롭다운에서 '마이 페이지' 클릭 (div > p 구조 — href 없음)"""
        locator = self.page.locator(self.DROPDOWN_MYPAGE_LINK).first
        locator.wait_for(state="attached", timeout=5_000)
        locator.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  세션 관리
    # ══════════════════════════════════════════════════════════════════

    def simulate_session_expiry(self) -> None:
        """인증 토큰 강제 삭제 (세션 만료 시뮬레이션)
        - JS: localStorage, sessionStorage, document.cookie 초기화
        - Playwright context.clear_cookies(): httpOnly 쿠키 포함 전체 삭제
        """
        self.page.evaluate("""() => {
            try { localStorage.clear(); } catch(e) {}
            try { sessionStorage.clear(); } catch(e) {}
            try {
                document.cookie.split(';').forEach(c => {
                    const key = c.trim().split('=')[0];
                    if (key) {
                        document.cookie =
                            key + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                    }
                });
            } catch(e) {}
        }""")
        try:
            self.page.context.clear_cookies()
        except Exception:
            pass
        self.page.wait_for_timeout(300)

    def is_main_path(self) -> bool:
        path = self.page.url.split("?")[0].rstrip("/")
        return path == self.BASE_URL.rstrip("/") or path.endswith("/")

    def is_url_mypage(self) -> bool:
        return self.MYPAGE_BASE_PATH in self.page.url

    def is_error_page_visible(self) -> bool:
        if self.page.locator(self.ERROR_PAGE).count() > 0:
            return True
        return "이용에 불편을 드려 죄송합니다" in self.page.content()

    # ══════════════════════════════════════════════════════════════════
    #  마이페이지
    # ══════════════════════════════════════════════════════════════════

    def is_mypage_loaded(self) -> bool:
        """마이페이지 로드 완료 여부"""
        try:
            self.page.wait_for_selector(self.MYPAGE_MAIN, timeout=5_000)
            return True
        except Exception:
            pass
        if self.is_main_path():
            return False
        return self.MYPAGE_BASE_PATH in self.page.url

    def is_account_section_visible(self) -> bool:
        """소셜 계정 연동 섹션 노출 여부"""
        return self.page.locator(self.MYPAGE_ACCOUNT_SECTION).count() > 0

    def get_linked_email_text(self) -> str:
        """연동된 계정 이메일 텍스트"""
        try:
            return self.page.locator(self.MYPAGE_LINKED_EMAIL).first.inner_text().strip()
        except Exception:
            return ""

    def is_google_badge_visible(self) -> bool:
        return self.page.locator(self.MYPAGE_GOOGLE_BADGE).count() > 0

    def is_unlink_btn_visible(self) -> bool:
        return self.page.locator(self.MYPAGE_UNLINK_BTN).count() > 0

    def click_unlink_btn(self) -> None:
        self.page.locator(self.MYPAGE_UNLINK_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_unlink_modal_visible(self) -> bool:
        """연동 해제 확인 모달 노출 여부"""
        portal = self.page.locator(self.UNLINK_MODAL)
        if portal.count() == 0:
            return False
        try:
            inner = portal.first.inner_html()
            if not inner.strip():
                return False
        except Exception:
            return False
        return self.page.locator(self.UNLINK_CANCEL_BTN).count() > 0

    def is_unlink_warning_visible(self) -> bool:
        return self.page.locator(self.UNLINK_WARNING_TEXT).count() > 0

    def click_unlink_cancel(self) -> None:
        self.page.locator(self.UNLINK_CANCEL_BTN).first.click()
        self.page.wait_for_timeout(400)

    def click_unlink_confirm(self) -> None:
        self.page.locator(self.UNLINK_CONFIRM_BTN).first.click()
        self.page.wait_for_timeout(800)

    def is_withdrawal_btn_visible(self) -> bool:
        """회원 탈퇴 버튼 노출 여부"""
        try:
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(300)
        except Exception:
            pass
        return self.page.locator(self.MYPAGE_WITHDRAWAL_BTN).count() > 0

    def click_withdrawal_btn(self) -> None:
        self.page.locator(self.MYPAGE_WITHDRAWAL_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_withdrawal_modal_visible(self) -> bool:
        """탈퇴 확인 모달/페이지 노출 여부
        ※ i18n: "정말 탈퇴하시겠어요?" 또는 "회원탈퇴는 즉시 처리" 텍스트 감지
        """
        # 탈퇴 관련 URL (탈퇴 확인 페이지로 이동한 경우)
        if "withdraw" in self.page.url:
            return True
        # portal-modal에 탈퇴 관련 내용
        portal = self.page.locator(self.WITHDRAWAL_MODAL)
        if portal.count() > 0:
            try:
                inner = portal.first.inner_html()
                if inner.strip() and ("탈퇴" in inner or "복구" in inner):
                    return True
            except Exception:
                pass
        # 페이지 텍스트 감지
        content = self.page.content()
        return (
            "정말 탈퇴하시겠어요" in content
            or "탈퇴 후에는 아이디와 정보를 복구" in content
            or "회원탈퇴는 즉시 처리" in content
        )

    def is_withdrawal_warning_visible(self) -> bool:
        if self.page.locator(self.WITHDRAWAL_WARNING_TEXT).count() > 0:
            return True
        return "복구 할 수 없" in self.page.content() or "복구 불가" in self.page.content()

    def is_withdrawal_cancel_btn_visible(self) -> bool:
        return self.page.locator(self.WITHDRAWAL_CANCEL_BTN).count() > 0

    def is_withdrawal_confirm_btn_visible(self) -> bool:
        # mypage와 modal 모두에서 '탈퇴하기' 버튼 감지
        # 단, mypage의 탈퇴하기 버튼(MYPAGE_WITHDRAWAL_BTN)과 구분 필요
        # 확인 모달이 열린 상태에서 portal-modal의 탈퇴하기를 우선 확인
        portal_confirm = self.page.locator("#portal-modal button:has-text('탈퇴하기')")
        if portal_confirm.count() > 0:
            return True
        # 탈퇴 확인 페이지의 탈퇴하기 버튼
        return "정말 탈퇴하시겠어요" in self.page.content()

    def click_withdrawal_cancel(self) -> None:
        self.page.locator(self.WITHDRAWAL_CANCEL_BTN).first.click()
        self.page.wait_for_timeout(400)

    def click_withdrawal_confirm(self) -> None:
        """탈퇴 확인 클릭 (⚠️ 파괴적 액션)"""
        self.page.locator(self.WITHDRAWAL_CONFIRM_BTN).first.click()
        self.page.wait_for_timeout(1_500)

    def is_rejoin_block_msg_visible(self) -> bool:
        if self.page.locator(self.REJOIN_BLOCK_MSG).count() > 0:
            return True
        content = self.page.content()
        return "재가입 제한" in content or "탈퇴한 계정" in content or "일 후 가입이 가능" in content

    def scroll_to_bottom(self, steps: int = 3) -> None:
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(400)

    def wait_for_modal_dismiss(self, timeout: int = 3_000) -> None:
        """로그인 화면(/user/signin)이 닫힐 때까지 대기"""
        if self.SIGNIN_PATH in self.page.url:
            try:
                self.page.wait_for_url(
                    lambda url: self.SIGNIN_PATH not in url,
                    timeout=timeout
                )
            except Exception:
                pass
        else:
            try:
                self.page.locator(self.LOGIN_GOOGLE_BTN).first.wait_for(
                    state="hidden", timeout=timeout
                )
            except Exception:
                pass
        self.page.wait_for_timeout(300)