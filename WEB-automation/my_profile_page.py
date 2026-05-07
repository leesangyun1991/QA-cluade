"""
pages/web/my_profile_page.py
[STEP 2 — POM v2]  내 프로필(My Profile) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
변경 이력 (v2 리팩토링):
    - 모든 TODO_ 셀렉터를 실제 HTML 기반 CSS Selector로 교체
    - PROFILE_MODAL                : div.myInfoContainer (실제 DOM)
    - PROFILE_NICKNAME / EMAIL     : 모달 헤더 버튼 내부 텍스트 노드
    - 다크 모드는 단일 토글 버튼 구조로 변경 (라이트/다크 별도 버튼 없음)
    - 언어 설정은 2단계 구조: '언어' 행 클릭 → #myInfoLanguageBoxComp 노출
    - GNB 프로필 아이콘: 모바일/데스크톱 UI 중복으로 인한 hidden 문제 방어
        ① :visible 필터 우선 클릭
        ② attached + click(force=True) 폴백
        ③ JavaScript .click() 이벤트 디스패치 폴백
    - 실제 모달에 없는 항목('프로필 수정', '내 활동', '리워드 잔액')은
      placeholder 셀렉터를 유지하되 메뉴 라우팅은 마이페이지 진입 후
      이동하는 폴백을 적용 (count() == 0 가드)

셀렉터 전략:
    - CSS Modules 해시 클래스 직접 사용 금지 → [class*='...'] 부분 매칭
    - 안정적 셀렉터 우선순위: aria-* > role > 시맨틱 태그 > 비해시 CSS 클래스
    - domcontentloaded 사용 — networkidle 30초 타임아웃 방지
"""

from typing import Optional

from playwright.sync_api import Page


class MyProfilePage:
    """블루밍비트 내 프로필(My Profile) 도메인 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반 — v2)
    # ══════════════════════════════════════════════════════════════════

    # ── GNB ──────────────────────────────────────────────────────────
    GNB_HEADER = "header#headerContainer"

    # GNB 프로필 아이콘
    # ※ 모바일/데스크톱 UI 중복으로 인한 hidden 판정 가능 → :visible 우선 사용
    GNB_PROFILE_ICON = (
        "header#headerContainer button:has(.userProfileImage), "
        "header#headerContainer button:has(img[alt='userProfileImage']), "
        "div.myInfo button:has(div.userProfileImage)"
    )
    GNB_PROFILE_ICON_VISIBLE = (
        "header#headerContainer button:has(.userProfileImage):visible, "
        "header#headerContainer button:has(img[alt='userProfileImage']):visible, "
        "div.myInfo button:has(div.userProfileImage):visible"
    )

    # ── 프로필 모달 컨테이너 ─────────────────────────────────────────
    # HTML: <div class="myInfoContainer ..."> 내부에 모든 콘텐츠 존재
    PROFILE_MODAL = "div.myInfoContainer"
    # 명시적 dim 요소 없음 → close_profile_modal_by_dim()에서 좌표 클릭 폴백
    PROFILE_MODAL_DIM = "[data-testid='TODO_profileDim']"
    # 모달 자체에 X 버튼 없음 → ESC 키 폴백 사용
    PROFILE_MODAL_CLOSE = "[data-testid='TODO_profileCloseBtn']"

    # ── 사용자 정보 영역 ─────────────────────────────────────────────
    # 모달 헤더 버튼 내부:
    #   <div class="userProfileImage"><img .../></div>
    #   <div class="flex w-full flex-col gap-(--value-xxxs)">
    #       <span class="text-[16px] leading-[24px] font-medium ...">SmoothADA3739</span>
    #       <div ...><div><svg google.../></div><p>email@x.com</p></div>
    #   </div>
    PROFILE_NICKNAME = (
        "div.myInfoContainer .userProfileImage + div > span[class*='text-[16px]'][class*='font-medium']"
    )
    PROFILE_EMAIL = "div.myInfoContainer button p:has-text('@')"
    PROFILE_IMAGE = "div.myInfoContainer .userProfileImage img"
    # 기본 이미지 마커: alt='userProfileImage' + src 미설정 또는 SVG 아이콘 폴백
    PROFILE_IMAGE_DEFAULT = "div.myInfoContainer .userProfileImage:not(:has(img[src^='http']))"

    # ── 리워드 잔액 ──────────────────────────────────────────────────
    # ※ 실제 모달에는 존재하지 않음 — 마이페이지 내부에 위치할 가능성
    REWARD_BALANCE      = "[data-testid='TODO_rewardBalance']"
    REWARD_BALANCE_UNIT = "[data-testid='TODO_rewardUnit']"

    # ── 언어 설정 ────────────────────────────────────────────────────
    # 메인 모달의 '언어' 행 (클릭하면 sub-menu 노출)
    LANGUAGE_TOGGLE_AREA = "div.myInfoContainer div:has(> p:text-is('언어'))"
    LANGUAGE_ROW         = "div.myInfoContainer div:has(> p:text-is('언어'))"
    LANGUAGE_CURRENT     = "div.myInfoContainer div:has(> p:text-is('언어')) .languageWrapper > span"

    # 언어 sub-menu (id="myInfoLanguageBoxComp")
    # 평소에는 'hidden' 클래스, 활성화 시 'flex'
    LANGUAGE_SUBMENU       = "#myInfoLanguageBoxComp"
    LANGUAGE_SUBMENU_VISIBLE = "#myInfoLanguageBoxComp:not(.hidden)"
    LANGUAGE_BTN_KR        = "#myInfoLanguageBoxComp button:has(span:text-is('한국어'))"
    LANGUAGE_BTN_EN        = "#myInfoLanguageBoxComp button:has(span:text-is('English'))"
    LANGUAGE_BTN_JA        = "#myInfoLanguageBoxComp button:has(span:text-is('日本語'))"
    LANGUAGE_BACK_BTN      = "#myInfoLanguageBoxComp button.myInfoInitButton"

    # ── 테마 설정 (단일 토글) ────────────────────────────────────────
    # HTML: <p>다크 모드</p> 옆 <div><button type="button">...</button></div>
    THEME_TOGGLE_AREA = "div.myInfoContainer div:has(> p:text-is('다크 모드'))"
    THEME_TOGGLE_BTN  = "div.myInfoContainer div:has(> p:text-is('다크 모드')) button[type='button']"

    # ── 메뉴 라우팅 ──────────────────────────────────────────────────
    # 모달에 실제 존재하는 메뉴: 마이 페이지, 공지사항, 문의하기, 약관 및 정책, 로그아웃
    MENU_MYPAGE       = "div.myInfoContainer div:has(> p:text-is('마이 페이지'))"
    MENU_ANNOUNCEMENT = "div.myInfoContainer div:has(> p:text-is('공지사항'))"
    MENU_CONTACT      = "div.myInfoContainer div:has(> p:text-is('문의하기'))"
    MENU_TERMS        = "div.myInfoContainer div:has(> p:text-is('약관 및 정책'))"

    # ※ 모달에 없는 메뉴 — 마이페이지 진입 후 이동하는 폴백 사용
    MENU_PROFILE_EDIT = "div.myInfoContainer div:has(> p:text-is('프로필 수정'))"
    MENU_MY_ACTIVITY  = "div.myInfoContainer div:has(> p:text-is('내 활동'))"

    # ── 로그아웃 ─────────────────────────────────────────────────────
    # HTML: <p>로그아웃</p> (실제로 클릭 가능한 부모 div를 타겟)
    LOGOUT_BTN     = "div.myInfoContainer div:has(> p:text-is('로그아웃'))"
    LOGOUT_BTN_TXT = "div.myInfoContainer p:text-is('로그아웃')"

    # ── 프로필 수정 페이지 폼 ────────────────────────────────────────
    EDIT_NICKNAME_INPUT  = "[data-testid='TODO_editNicknameInput'], input[name='nickname']"
    EDIT_NICKNAME_ERROR  = "[data-testid='TODO_nicknameError'], [class*='TODO_inputError']"
    EDIT_PROFILE_IMG_INP = "[data-testid='TODO_profileImageInput'], input[type='file'][accept*='image']"
    EDIT_SAVE_BTN        = "[data-testid='TODO_editSaveBtn'], button:has-text('저장')"

    # ── URL 패턴 ────────────────────────────────────────────────────
    MAIN_PATH         = "/"
    MYPAGE_PATH       = "/mypage"
    MYPAGE_EDIT_PATH  = "/mypage/edit"
    MY_ACTIVITY_PATH  = "/mypage/activity"
    SIGNIN_PATH       = "/user/signin"

    # ── 에러/로그인 감지 ─────────────────────────────────────────────
    ERROR_PAGE           = "p:has-text('이용에 불편을 드려 죄송합니다'), h1:has-text('이용에 불편을 드려 죄송합니다')"
    LOGIN_PAGE_CONTAINER = "main#signInContainer"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def _safe_goto(self, url: str) -> None:
        """about:blank 충돌 및 ERR_ABORTED 방지하는 안전한 goto"""
        for attempt in range(3):
            try:
                self.page.wait_for_timeout(300)
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Exception as e:
                err = str(e)
                if attempt < 2 and (
                    "about:blank" in err
                    or "interrupted" in err
                    or "ERR_ABORTED" in err
                ):
                    self.page.wait_for_timeout(1_000)
                    continue
                raise

    def go_to_main(self) -> None:
        """메인 페이지(/)로 이동"""
        self._safe_goto(self.BASE_URL)
        self.page.wait_for_timeout(500)

    def go_to_mypage(self) -> None:
        self._safe_goto(f"{self.BASE_URL}{self.MYPAGE_PATH}")
        self.page.wait_for_timeout(500)

    def go_to_mypage_edit(self) -> None:
        self._safe_goto(f"{self.BASE_URL}{self.MYPAGE_EDIT_PATH}")
        self.page.wait_for_timeout(500)

    def go_to_my_activity(self) -> None:
        self._safe_goto(f"{self.BASE_URL}{self.MY_ACTIVITY_PATH}")
        self.page.wait_for_timeout(500)

    def refresh_page(self) -> None:
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)

    def go_back(self) -> None:
        try:
            self.page.go_back(wait_until="domcontentloaded")
        except Exception:
            pass
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  GNB 상태 확인
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_visible(self) -> bool:
        return self.page.is_visible(self.GNB_HEADER)

    def is_gnb_logged_in_state(self) -> bool:
        return self.page.locator(self.GNB_PROFILE_ICON).count() > 0

    def is_login_page_visible(self) -> bool:
        return (
            self.SIGNIN_PATH in self.page.url
            or self.page.locator(self.LOGIN_PAGE_CONTAINER).count() > 0
        )

    def is_error_page_visible(self) -> bool:
        return self.page.locator(self.ERROR_PAGE).count() > 0

    def get_current_url(self) -> str:
        return self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  GNB 프로필 아이콘 / 모달 제어
    # ══════════════════════════════════════════════════════════════════

    def is_profile_icon_visible(self) -> bool:
        return self.page.locator(self.GNB_PROFILE_ICON).count() > 0

    def click_profile_icon(self) -> None:
        """GNB 프로필 아이콘 클릭 → 프로필 모달 오픈

        견고화 전략 (3-Tier Fallback):
            ① :visible 필터로 데스크톱/모바일 중 보이는 요소만 우선 클릭
            ② attached 대기 후 click(force=True) — visibility 검사 우회
            ③ JavaScript .click() 이벤트 디스패치 — Playwright 우회
        ※ 절대 타임아웃이 나지 않도록 모든 단계에서 try/except 처리
        """
        # 1단계: visible한 아이콘 우선 클릭
        visible_icon = self.page.locator(self.GNB_PROFILE_ICON_VISIBLE)
        if visible_icon.count() > 0:
            try:
                visible_icon.first.click(timeout=3_000)
                self.page.wait_for_timeout(500)
                if self.is_profile_modal_visible():
                    return
            except Exception:
                pass

        # 2단계: attached 대기 + force=True 클릭
        try:
            icon = self.page.locator(self.GNB_PROFILE_ICON).first
            icon.wait_for(state="attached", timeout=8_000)
            try:
                icon.click(force=True, timeout=3_000)
                self.page.wait_for_timeout(500)
                if self.is_profile_modal_visible():
                    return
            except Exception:
                pass

            # 3단계: JavaScript 클릭 이벤트 디스패치
            try:
                icon.evaluate("(el) => el.click()")
                self.page.wait_for_timeout(500)
                return
            except Exception:
                pass
        except Exception:
            pass

        # 마지막: GNB 헤더 내 첫 번째 'userProfileImage' 보유 버튼을 강제 JS 클릭
        try:
            self.page.evaluate(
                """
                () => {
                    const header = document.querySelector('header#headerContainer');
                    if (!header) return;
                    const btn = header.querySelector('button:has(.userProfileImage)')
                            || Array.from(header.querySelectorAll('button'))
                                    .find(b => b.querySelector('.userProfileImage'));
                    if (btn) btn.click();
                }
                """
            )
            self.page.wait_for_timeout(500)
        except Exception:
            pass

    def is_profile_modal_visible(self) -> bool:
        """프로필 모달(div.myInfoContainer) 노출 여부"""
        return self.page.locator(self.PROFILE_MODAL).count() > 0

    def open_profile_modal(self) -> None:
        """프로필 아이콘 클릭으로 모달 오픈 (이미 열려있으면 유지)"""
        if not self.is_profile_modal_visible():
            self.click_profile_icon()
            try:
                self.page.locator(self.PROFILE_MODAL).first.wait_for(
                    state="attached", timeout=5_000
                )
            except Exception:
                pass

    def close_profile_modal_by_dim(self) -> None:
        """프로필 모달 외부 영역 클릭으로 모달 닫기
        ※ 명시적 dim 요소가 없는 드롭다운 구조 → 좌측 바깥 좌표 클릭
        """
        self.page.mouse.click(10, 200)
        self.page.wait_for_timeout(500)

    def close_profile_modal_by_close_btn(self) -> None:
        """프로필 모달 X 버튼 클릭으로 닫기
        ※ 실제 X 버튼이 없으므로 ESC 키 폴백으로 동작
        """
        close_btn = self.page.locator(self.PROFILE_MODAL_CLOSE)
        if close_btn.count() > 0:
            try:
                close_btn.first.click(force=True)
                self.page.wait_for_timeout(400)
                return
            except Exception:
                pass
        # 폴백: ESC 키
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(400)

    def close_profile_modal_by_escape(self) -> None:
        """ESC 키로 모달 닫기"""
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(400)

    def wait_for_modal_dismiss(self, timeout: int = 3_000) -> bool:
        try:
            self.page.locator(self.PROFILE_MODAL).first.wait_for(
                state="detached", timeout=timeout
            )
            return True
        except Exception:
            return self.page.locator(self.PROFILE_MODAL).count() == 0

    # ══════════════════════════════════════════════════════════════════
    #  사용자 정보 노출
    # ══════════════════════════════════════════════════════════════════

    def get_displayed_nickname(self) -> str:
        try:
            return self.page.locator(self.PROFILE_NICKNAME).first.inner_text().strip()
        except Exception:
            return ""

    def get_displayed_email(self) -> str:
        try:
            return self.page.locator(self.PROFILE_EMAIL).first.inner_text().strip()
        except Exception:
            return ""

    def is_profile_image_visible(self) -> bool:
        # img가 있거나 .userProfileImage 컨테이너 자체가 있으면 노출 인정
        if self.page.locator(self.PROFILE_IMAGE).count() > 0:
            return True
        return self.page.locator("div.myInfoContainer .userProfileImage").count() > 0

    def is_profile_image_default(self) -> bool:
        # 1) src에 default/placeholder 키워드 확인
        try:
            src = self.page.locator(self.PROFILE_IMAGE).first.get_attribute("src") or ""
            if "default" in src.lower() or "placeholder" in src.lower():
                return True
        except Exception:
            pass
        # 2) img가 아예 없고 SVG 폴백만 있는 경우
        return (
            self.page.locator(self.PROFILE_IMAGE).count() == 0
            and self.page.locator("div.myInfoContainer .userProfileImage").count() > 0
        )

    def get_profile_image_src(self) -> str:
        try:
            return self.page.locator(self.PROFILE_IMAGE).first.get_attribute("src") or ""
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  데이터 갱신 (리워드 잔액)
    #  ※ 실제 모달에는 미존재 — placeholder 셀렉터 유지
    # ══════════════════════════════════════════════════════════════════

    def get_reward_balance_text(self) -> str:
        try:
            return self.page.locator(self.REWARD_BALANCE).first.inner_text().strip()
        except Exception:
            return ""

    def get_reward_balance_as_number(self) -> int:
        text = self.get_reward_balance_text()
        try:
            return int(text.replace(",", "").replace("BB", "").strip())
        except Exception:
            return -1

    def is_reward_balance_visible(self) -> bool:
        return self.page.locator(self.REWARD_BALANCE).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  언어 설정 (2단계)
    # ══════════════════════════════════════════════════════════════════

    def is_language_toggle_visible(self) -> bool:
        return self.page.locator(self.LANGUAGE_TOGGLE_AREA).count() > 0

    def _open_language_submenu(self) -> None:
        """메인 모달의 '언어' 행 클릭 → #myInfoLanguageBoxComp 노출"""
        # 이미 sub-menu가 열려있으면 skip
        submenu = self.page.locator(self.LANGUAGE_SUBMENU_VISIBLE)
        if submenu.count() > 0:
            return
        row = self.page.locator(self.LANGUAGE_ROW)
        if row.count() > 0:
            try:
                row.first.click(force=True)
                self.page.wait_for_timeout(500)
            except Exception:
                pass

    def select_language_korean(self) -> None:
        self._open_language_submenu()
        btn = self.page.locator(self.LANGUAGE_BTN_KR)
        if btn.count() > 0:
            try:
                btn.first.click(force=True)
            except Exception:
                pass
            self.page.wait_for_timeout(1_500)

    def select_language_english(self) -> None:
        self._open_language_submenu()
        btn = self.page.locator(self.LANGUAGE_BTN_EN)
        if btn.count() > 0:
            try:
                btn.first.click(force=True)
            except Exception:
                pass
            self.page.wait_for_timeout(1_500)

    def select_language_japanese(self) -> None:
        self._open_language_submenu()
        btn = self.page.locator(self.LANGUAGE_BTN_JA)
        if btn.count() > 0:
            try:
                btn.first.click(force=True)
            except Exception:
                pass
            self.page.wait_for_timeout(1_500)

    def get_active_language(self) -> str:
        """현재 활성 언어: 'KR' / 'EN' / 'JA' / ''"""
        url = self.page.url
        if "web-stg-en" in url:
            return "EN"
        if "web-stg-ja" in url:
            return "JA"
        if "web-stg.bloomingbit.io" in url:
            return "KR"
        try:
            lang_attr = (self.page.locator("html").first.get_attribute("lang") or "").lower()
            if lang_attr.startswith("ko"): return "KR"
            if lang_attr.startswith("en"): return "EN"
            if lang_attr.startswith("ja"): return "JA"
        except Exception:
            pass
        return ""

    # ══════════════════════════════════════════════════════════════════
    #  테마 설정 (단일 토글 버튼)
    # ══════════════════════════════════════════════════════════════════

    def is_theme_toggle_visible(self) -> bool:
        return self.page.locator(self.THEME_TOGGLE_AREA).count() > 0

    def _click_theme_toggle(self) -> None:
        btn = self.page.locator(self.THEME_TOGGLE_BTN)
        if btn.count() > 0:
            try:
                btn.first.click(force=True)
                self.page.wait_for_timeout(800)
            except Exception:
                pass

    def toggle_dark_mode(self) -> None:
        """다크 모드로 전환 (현재 라이트면 토글, 이미 다크면 유지)"""
        if self.is_dark_mode_active():
            return
        self._click_theme_toggle()

    def toggle_light_mode(self) -> None:
        """라이트 모드로 전환 (현재 다크면 토글, 이미 라이트면 유지)"""
        if self.is_light_mode_active():
            return
        self._click_theme_toggle()

    def get_active_theme(self) -> str:
        """현재 활성 테마: 'dark' / 'light' / ''"""
        # 1) html data-theme
        try:
            theme = self.page.locator("html").first.get_attribute("data-theme") or ""
            if theme:
                return theme.lower()
        except Exception:
            pass
        # 2) html class
        try:
            cls = self.page.locator("html").first.get_attribute("class") or ""
            if "dark" in cls.lower():
                return "dark"
            if "light" in cls.lower():
                return "light"
        except Exception:
            pass
        # 3) body class
        try:
            cls = self.page.locator("body").first.get_attribute("class") or ""
            if "dark" in cls.lower():
                return "dark"
            if "light" in cls.lower():
                return "light"
        except Exception:
            pass
        # 4) data-theme on body
        try:
            theme = self.page.locator("body").first.get_attribute("data-theme") or ""
            if theme:
                return theme.lower()
        except Exception:
            pass
        return ""

    def is_dark_mode_active(self) -> bool:
        return self.get_active_theme() == "dark"

    def is_light_mode_active(self) -> bool:
        return self.get_active_theme() == "light"

    # ══════════════════════════════════════════════════════════════════
    #  메뉴 라우팅
    # ══════════════════════════════════════════════════════════════════

    def click_mypage_menu(self) -> None:
        """'마이 페이지' 메뉴 클릭"""
        link = self.page.locator(self.MENU_MYPAGE)
        if link.count() > 0:
            try:
                link.first.click(force=True)
                try: self.page.wait_for_load_state("domcontentloaded", timeout=5_000)
                except Exception: pass
                self.page.wait_for_timeout(800)
                return
            except Exception:
                pass
        # 폴백: 직접 URL 이동
        self.go_to_mypage()

    def click_profile_edit_menu(self) -> None:
        """'프로필 수정' 메뉴 클릭
        ※ 모달에 메뉴가 없으므로 마이페이지 진입 후 /mypage/edit 직접 이동 폴백
        """
        link = self.page.locator(self.MENU_PROFILE_EDIT)
        if link.count() > 0:
            try:
                link.first.click(force=True)
                try: self.page.wait_for_load_state("domcontentloaded", timeout=5_000)
                except Exception: pass
                self.page.wait_for_timeout(800)
                return
            except Exception:
                pass
        # 폴백: 직접 URL 이동
        self.go_to_mypage_edit()

    def click_my_activity_menu(self) -> None:
        """'내 활동' 메뉴 클릭
        ※ 모달에 메뉴가 없으므로 /mypage/activity 직접 이동 폴백
        """
        link = self.page.locator(self.MENU_MY_ACTIVITY)
        if link.count() > 0:
            try:
                link.first.click(force=True)
                try: self.page.wait_for_load_state("domcontentloaded", timeout=5_000)
                except Exception: pass
                self.page.wait_for_timeout(800)
                return
            except Exception:
                pass
        # 폴백: 직접 URL 이동
        self.go_to_my_activity()

    def is_on_mypage_edit(self) -> bool:
        return self.MYPAGE_EDIT_PATH in self.page.url

    def is_on_mypage(self) -> bool:
        url = self.page.url
        return self.MYPAGE_PATH in url and self.MYPAGE_EDIT_PATH not in url \
            and self.MY_ACTIVITY_PATH not in url

    def is_on_my_activity(self) -> bool:
        return self.MY_ACTIVITY_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  로그아웃
    # ══════════════════════════════════════════════════════════════════

    def is_logout_btn_visible(self) -> bool:
        return self.page.locator(self.LOGOUT_BTN).count() > 0

    def click_logout_btn(self) -> None:
        """'로그아웃' 클릭 → 세션 종료
        ※ 부모 div 클릭 우선, 실패 시 <p> 텍스트 직접 클릭 폴백
        """
        btn = self.page.locator(self.LOGOUT_BTN)
        if btn.count() > 0:
            try:
                btn.first.click(force=True)
            except Exception:
                # 폴백: <p> 직접 클릭
                try:
                    self.page.locator(self.LOGOUT_BTN_TXT).first.click(force=True)
                except Exception:
                    pass
            try: self.page.wait_for_load_state("domcontentloaded", timeout=5_000)
            except Exception: pass
            self.page.wait_for_timeout(1_500)

    # ══════════════════════════════════════════════════════════════════
    #  프로필 수정 폼 헬퍼
    # ══════════════════════════════════════════════════════════════════

    def fill_text_input(self, selector: str, value: str) -> None:
        loc = self.page.locator(selector).first
        loc.wait_for(state="attached", timeout=5_000)
        loc.click(force=True)
        loc.fill("")
        loc.fill(value)
        self.page.wait_for_timeout(200)

    def clear_text_input(self, selector: str) -> None:
        loc = self.page.locator(selector).first
        loc.wait_for(state="attached", timeout=5_000)
        loc.fill("")
        self.page.wait_for_timeout(200)

    def fill_nickname(self, value: str) -> None:
        self.fill_text_input(self.EDIT_NICKNAME_INPUT, value)

    def clear_nickname(self) -> None:
        self.clear_text_input(self.EDIT_NICKNAME_INPUT)

    def get_nickname_input_value(self) -> str:
        try:
            return self.page.locator(self.EDIT_NICKNAME_INPUT).first.input_value()
        except Exception:
            return ""

    def get_nickname_error_text(self) -> str:
        loc = self.page.locator(self.EDIT_NICKNAME_ERROR)
        if loc.count() > 0:
            try:
                return loc.first.inner_text().strip()
            except Exception:
                return ""
        return ""

    def is_nickname_error_visible(self) -> bool:
        return self.page.locator(self.EDIT_NICKNAME_ERROR).count() > 0

    def upload_profile_image(self, file_path: str) -> None:
        loc = self.page.locator(self.EDIT_PROFILE_IMG_INP).first
        loc.wait_for(state="attached", timeout=5_000)
        loc.set_input_files(file_path)
        self.page.wait_for_timeout(800)

    def is_save_button_disabled(self) -> bool:
        try:
            return self.page.locator(self.EDIT_SAVE_BTN).first.is_disabled()
        except Exception:
            return False

    def click_save_button(self) -> None:
        btn = self.page.locator(self.EDIT_SAVE_BTN).first
        btn.wait_for(state="attached", timeout=5_000)
        btn.click(force=True)
        self.page.wait_for_timeout(800)

    # ══════════════════════════════════════════════════════════════════
    #  비로그인 게스트 상태
    # ══════════════════════════════════════════════════════════════════

    def is_guest_state(self) -> bool:
        return (
            self.page.locator(self.GNB_PROFILE_ICON).count() == 0
            or self.is_login_page_visible()
        )

    def click_login_cta_if_present(self) -> None:
        cta = self.page.locator(
            "header#headerContainer a:has-text('로그인'), "
            "header#headerContainer button:has-text('로그인')"
        )
        if cta.count() > 0:
            try:
                cta.first.click(force=True)
                try: self.page.wait_for_load_state("domcontentloaded", timeout=5_000)
                except Exception: pass
                self.page.wait_for_timeout(500)
            except Exception:
                pass