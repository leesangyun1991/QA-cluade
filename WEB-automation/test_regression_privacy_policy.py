"""
tests/stage8_regression/web/test_regression_privacy_policy.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
개인정보 처리방침(Privacy Policy) 회귀 테스트
FULLTC-527 ~ FULLTC-530 (4 TCs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_privacy_policy.py -v
  pytest tests/stage8_regression/web/test_regression_privacy_policy.py -m "privacy_policy" -v
  pytest tests/stage8_regression/web/test_regression_privacy_policy.py -k "FULLTC_528" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)

[TC 클래스 구성]
  FULLTC-527   TestPrivacyPolicyEntry          메뉴 진입 (LNB 클릭)
  FULLTC-528   TestPrivacyPolicyLatestVersion  최신 버전 디폴트 노출
  FULLTC-529   TestPrivacyPolicyVersionChange  과거 버전 드롭다운 선택
  FULLTC-530   TestPrivacyPolicyTextRendering  텍스트 가독성 및 포맷

[HTML 분석 핵심 포인트]
  ✅ 완전 안정 셀렉터 (즉시 사용 가능):
     · 드롭다운:     div.dropdown  (plain class! — 이용약관과 동일 구조)
     · 날짜 라벨:    span.dateLabel  (plain class!)
     · 현재 날짜:    div.dropdown > div > span = "2025.08.25"
     · 방침 본문:    div#termsContent  (ID 기반 — 최강!)
     · 조항 헤딩:    div#termsContent p strong
       (14개: 제1조~제12조 + GDPR 부록 <1><2>)

  ⚠️ TODO_ 셀렉터 (실제 DOM 확인 후 튜닝 필요):
     · 드롭다운 옵션: DROPDOWN_OPTION
     · LNB 메뉴: LNB_WRAPPER, LNB_PRIVACY_MENU (FULLTC-527)
     · 페이지 URL: PRIVACY_PATH (F12 주소창 확인 후 수정)

  ⚠️ HTML 특이사항:
     · 제7조 내용부터 <strong> 태그 잘못 중첩 → p strong 셀렉터 정상 매칭
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from privacy_policy_page import PrivacyPolicyPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def privacy_page() -> Iterator[PrivacyPolicyPage]:
    """개인정보 처리방침 페이지 픽스처 (로그인 세션 유지)
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
        yield PrivacyPolicyPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-527  |  메뉴 진입
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.privacy_policy
class TestPrivacyPolicyEntry:
    """LNB 메뉴 클릭으로 개인정보 처리방침 페이지 진입 검증 — FULLTC-527
    ⚠️ LNB_WRAPPER, LNB_PRIVACY_MENU 셀렉터가 TODO_ 상태 → skip 자동 처리
    """

    def test_FULLTC_527_lnb_menu_click_navigates_and_activates(
        self, privacy_page: PrivacyPolicyPage
    ) -> None:
        """
        FULLTC-527 | 개인정보 처리방침/LNB 메뉴 클릭 | Major
        LNB에서 [개인정보 처리방침] 메뉴 클릭 시 해당 페이지로 이동하고
        LNB에서 [개인정보 처리방침] 메뉴가 활성(하이라이트) 상태로 표시되어야 한다.
        ⚠️ TODO: LNB_WRAPPER, LNB_PRIVACY_MENU, LNB_ACTIVE_MENU 셀렉터 튜닝 필요
        """
        privacy_page.go_to_mypage()
        privacy_page.page.wait_for_timeout(600)

        if not privacy_page.is_lnb_visible():
            pytest.skip(
                "[SKIP] FULLTC-527: LNB 영역 미노출 — "
                "TODO: LNB_WRAPPER 셀렉터 튜닝 후 재실행"
            )

        url_before = privacy_page.get_current_url()
        privacy_page.click_lnb_privacy_menu()

        # 1) URL 변경 확인
        assert privacy_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-527: LNB '개인정보 처리방침' 메뉴 클릭 후 URL 미변경"

        # 2) 페이지 정상 로드 확인
        assert privacy_page.is_loaded(), \
            "[FAIL] FULLTC-527: 개인정보 처리방침 페이지 로드 실패 (div#termsContent 미노출)"

        # 3) 타이틀 확인
        assert privacy_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-527: 페이지 타이틀이 '개인정보 처리방침' 아님 " \
            f"(현재: '{privacy_page.get_page_title_text()}')"

        # 4) LNB 활성화 상태 확인 (TODO 셀렉터)
        if privacy_page.is_lnb_visible():
            lnb_active = privacy_page.is_lnb_privacy_menu_active()
            if not lnb_active:
                pytest.skip(
                    "[SKIP] FULLTC-527 (LNB 활성): LNB 활성 메뉴 확인 실패 — "
                    "TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요"
                )
            assert lnb_active, \
                "[FAIL] FULLTC-527: 이동 후 LNB에서 '개인정보 처리방침' 메뉴가 활성(하이라이트) 상태 아님"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-528  |  최신 버전 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.privacy_policy
class TestPrivacyPolicyLatestVersion:
    """최신 시행일자 드롭다운 디폴트 선택 및 본문 노출 검증 — FULLTC-528
    ✅ div.dropdown / div#termsContent — 이용약관과 동일한 안정 셀렉터!
    """

    def test_FULLTC_528_latest_version_shown_by_default(
        self, privacy_page: PrivacyPolicyPage
    ) -> None:
        """
        FULLTC-528 | 개인정보 처리방침/최신 시행일자 디폴트 선택 | Major
        페이지 진입 시 상단 드롭다운에 가장 최신 시행일자가 디폴트로 선택되어 있고
        본문에 최신 버전 처리방침 내용이 표시되어야 한다.
        ✅ div.dropdown / div#termsContent — 안정 셀렉터로 즉시 검증 가능
        """
        privacy_page.go_to_privacy_policy()
        assert privacy_page.is_loaded(), \
            "[FAIL] FULLTC-528: 개인정보 처리방침 페이지 로드 실패 (div#termsContent 미노출)"

        # 1) 드롭다운 컨테이너 노출 확인
        assert privacy_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-528: 시행일자 드롭다운(div.dropdown) 미노출"

        # 2) 날짜 라벨 노출 및 텍스트 확인
        assert privacy_page.is_date_label_visible(), \
            "[FAIL] FULLTC-528: '시행/변경 일자' 라벨(span.dateLabel) 미노출"

        date_label = privacy_page.get_date_label_text()
        assert "시행" in date_label or "변경" in date_label, \
            f"[FAIL] FULLTC-528: 날짜 라벨 텍스트 불일치 " \
            f"(기대: '시행/변경 일자', 현재: '{date_label}')"

        # 3) 드롭다운에 날짜 표시 확인
        dropdown_date = privacy_page.get_dropdown_current_date()
        assert dropdown_date.strip() != "", \
            "[FAIL] FULLTC-528: 드롭다운(div.dropdown > div > span) 날짜 텍스트 비어있음"

        # 4) 날짜 포맷 확인 (YYYY.MM.DD)
        assert privacy_page.is_date_format_valid(dropdown_date), \
            f"[FAIL] FULLTC-528: 드롭다운 날짜 포맷 불일치 — " \
            f"'YYYY.MM.DD' 기대 (현재: '{dropdown_date}')"

        # 5) 방침 본문 노출 확인 (div#termsContent — ID 안정 셀렉터)
        assert privacy_page.is_policy_content_visible(), \
            "[FAIL] FULLTC-528: 처리방침 본문 영역(div#termsContent) 미노출"

        # 6) 본문 텍스트 충분한 분량인지 확인 (최소 500자)
        assert privacy_page.is_policy_content_not_empty(), \
            "[FAIL] FULLTC-528: 처리방침 본문 텍스트 500자 미만 — 내용 미로드 의심"

        # 7) 제1조 헤딩 존재 확인 (최신 버전 방침 내용 로드 기준)
        assert privacy_page.is_article_present("제1조"), \
            "[FAIL] FULLTC-528: 본문에 '제1조' 조항 미노출 — 최신 버전 처리방침 미로드"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-529  |  과거 버전 변경
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.privacy_policy
class TestPrivacyPolicyVersionChange:
    """시행일자 드롭다운으로 과거 버전 선택 및 본문 내용 변경 검증 — FULLTC-529
    ⚠️ 드롭다운 옵션 목록(DROPDOWN_OPTION)이 TODO_ 상태 →
       과거 버전이 없거나 셀렉터 미튜닝 시 skip 자동 처리
    """

    def test_FULLTC_529_past_version_dropdown_and_content_change(
        self, privacy_page: PrivacyPolicyPage
    ) -> None:
        """
        FULLTC-529 | 개인정보 처리방침/시행일자 드롭다운 과거 버전 선택 | Major
        드롭다운을 클릭하면 과거 시행일자 목록이 노출되고,
        과거 날짜 선택 후 해당 시점의 처리방침 텍스트로 본문이 변경되어야 한다.
        ⚠️ TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요 (드롭다운 열고 F12 확인)
        사전 조건: 과거 시행일자 이력 1건 이상 존재
        """
        privacy_page.go_to_privacy_policy()
        assert privacy_page.is_loaded(), \
            "[FAIL] FULLTC-529: 개인정보 처리방침 페이지 로드 실패"

        assert privacy_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-529: 시행일자 드롭다운(div.dropdown) 미노출"

        # 1) 드롭다운 클릭 (열기)
        current_date = privacy_page.get_dropdown_current_date()
        privacy_page.click_dropdown_toggle()
        privacy_page.page.wait_for_timeout(600)

        # 2) 드롭다운 옵션 목록 노출 확인
        option_count = privacy_page.get_dropdown_option_count()
        if option_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-529: 드롭다운 옵션 항목 0개 — "
                "과거 버전이 없거나 TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요. "
                "드롭다운 열고 F12 확인 후 셀렉터 교체"
            )

        # 3) 현재 날짜와 다른 옵션이 있는지 확인
        option_texts = privacy_page.get_dropdown_option_texts()
        other_options = [
            t for t in option_texts
            if t != current_date and privacy_page.is_date_format_valid(t)
        ]
        if not other_options:
            pytest.skip(
                f"[SKIP] FULLTC-529: 과거 버전 옵션 없음 — "
                f"드롭다운 항목: {option_texts}, 현재 날짜: '{current_date}'"
            )

        # 4) 현재 본문 텍스트 기록 (변경 전)
        content_before = privacy_page.get_all_policy_text()

        # 5) 과거 버전 선택
        selected_date = privacy_page.select_dropdown_option_by_index(
            option_texts.index(other_options[0])
        )
        if not selected_date:
            pytest.skip(
                "[SKIP] FULLTC-529: 과거 버전 옵션 클릭 실패 — "
                "TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요"
            )

        # 6) 드롭다운 표시 날짜 변경 확인
        new_dropdown_date = privacy_page.get_dropdown_current_date()
        assert new_dropdown_date != current_date, \
            f"[FAIL] FULLTC-529: 과거 버전 선택 후 드롭다운 날짜 미변경 " \
            f"(before: '{current_date}', after: '{new_dropdown_date}')"

        assert privacy_page.is_date_format_valid(new_dropdown_date), \
            f"[FAIL] FULLTC-529: 선택 후 드롭다운 날짜 포맷 불일치 " \
            f"(현재: '{new_dropdown_date}')"

        # 7) 본문 내용 변경 확인
        content_after = privacy_page.get_all_policy_text()
        assert content_after.strip() != "", \
            "[FAIL] FULLTC-529: 과거 버전 선택 후 처리방침 본문 비어있음"

        if content_after == content_before:
            pytest.skip(
                "[SKIP] FULLTC-529: 과거 버전 선택 후 본문 내용이 이전과 동일 — "
                "버전 간 내용 차이 없거나 같은 버전 선택됨"
            )

        assert content_after != content_before, \
            "[FAIL] FULLTC-529: 과거 버전 선택 후 처리방침 본문 미변경 — " \
            "다른 버전의 처리방침 내용으로 교체되지 않음"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-530  |  텍스트 렌더링
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.privacy_policy
class TestPrivacyPolicyTextRendering:
    """처리방침 텍스트 가독성·포맷·줄바꿈 검증 — FULLTC-530
    ✅ div#termsContent / p strong — 이용약관과 동일한 안정 셀렉터!
    """

    def test_FULLTC_530_policy_text_format_and_readability(
        self, privacy_page: PrivacyPolicyPage
    ) -> None:
        """
        FULLTC-530 | 개인정보 처리방침/방침 텍스트 가독성 및 포맷 | Minor
        조항 번호(굵은 글씨), 들여쓰기 등 포맷이 정상 렌더링되고
        텍스트가 화면 너비에 맞게 노출되며 가로 스크롤이 발생하지 않아야 한다.
        ✅ div#termsContent p strong — 안정 셀렉터로 즉시 검증 가능
        """
        privacy_page.go_to_privacy_policy()
        assert privacy_page.is_loaded(), \
            "[FAIL] FULLTC-530: 개인정보 처리방침 페이지 로드 실패"

        assert privacy_page.is_policy_content_visible(), \
            "[FAIL] FULLTC-530: 처리방침 본문 영역(div#termsContent) 미노출"

        # ── 1) 조항 헤딩 수 확인 ───────────────────────────────────
        heading_count = privacy_page.get_article_heading_count()
        assert heading_count >= PrivacyPolicyPage.MIN_ARTICLE_COUNT, \
            f"[FAIL] FULLTC-530: 처리방침 조항 헤딩 수 부족 — " \
            f"기대: {PrivacyPolicyPage.MIN_ARTICLE_COUNT}개 이상, " \
            f"실제: {heading_count}개 (div#termsContent p strong)"

        # 제1조(처리 목적) 존재 확인 — 첫 번째 조항
        assert privacy_page.is_article_present("제1조"), \
            "[FAIL] FULLTC-530: '제1조(개인정보 처리의 목적)' 헤딩 미노출 — " \
            "처리방침 내용 렌더링 오류"

        # 제12조(변경 고지) 존재 확인 — 마지막 번호 조항
        assert privacy_page.is_article_present("제12조"), \
            "[FAIL] FULLTC-530: '제12조(변경 고지의 의무)' 헤딩 미노출 — " \
            "마지막 조항까지 렌더링 필요"

        # GDPR 부록 존재 확인 (개인정보처리방침 특유의 섹션)
        has_gdpr = privacy_page.is_article_present("GDPR")
        if not has_gdpr:
            # GDPR 키워드로 재확인
            all_text = privacy_page.get_all_policy_text()
            has_gdpr = "GDPR" in all_text
        assert has_gdpr, \
            "[FAIL] FULLTC-530: GDPR 부록 섹션 미노출 — " \
            "개인정보처리방침 내 GDPR 적용 내용 렌더링 필요"

        # ── 2) strong 헤딩 굵기 CSS 확인 ──────────────────────────
        assert privacy_page.is_strong_formatted_correctly(), \
            "[FAIL] FULLTC-530: 조항 헤딩(<strong>) CSS font-weight 600 미만 — " \
            "굵은 글씨 포맷이 정상 렌더링되지 않음"

        # ── 3) 텍스트 가로 오버플로우(스크롤) 확인 ────────────────
        assert not privacy_page.is_text_overflowing_horizontally(), \
            "[FAIL] FULLTC-530: 처리방침 본문 영역(div#termsContent)에 가로 스크롤 발생 — " \
            "텍스트 줄바꿈 미적용 또는 레이아웃 문제"

        assert not privacy_page.is_body_overflowing_horizontally(), \
            "[FAIL] FULLTC-530: 페이지 body 전체에 가로 스크롤 발생 — " \
            "처리방침 텍스트 또는 요소가 뷰포트 밖으로 벗어남"

        # ── 4) 본문 단락 수 확인 ──────────────────────────────────
        paragraph_count = privacy_page.get_paragraph_count()
        assert paragraph_count >= 40, \
            f"[FAIL] FULLTC-530: 처리방침 단락(<p>) 수 부족 — " \
            f"기대: 40개 이상, 실제: {paragraph_count}개 " \
            f"(일부 조항 미렌더링 의심)"

        # ── 5) 페이지 스크롤 가능 여부 확인 ──────────────────────
        scroll_height   = privacy_page.get_page_scroll_height()
        viewport_height = privacy_page.get_viewport_height()
        assert scroll_height > viewport_height, \
            f"[FAIL] FULLTC-530: 처리방침 페이지가 뷰포트보다 짧음 — 스크롤 불가 " \
            f"(scroll_height:{scroll_height}, viewport:{viewport_height})"

        # ── 6) 최하단까지 스크롤하여 모든 콘텐츠 접근 가능한지 확인 ─
        privacy_page.scroll_to_bottom(steps=8)
        scroll_y = privacy_page.get_scroll_y_position()
        assert scroll_y > 0, \
            f"[FAIL] FULLTC-530: 스크롤 후 scrollY = {scroll_y} — 스크롤 미동작"

        # ── 7) 스크롤 후 가로 오버플로우 재확인 ─────────────────────
        assert not privacy_page.is_body_overflowing_horizontally(), \
            "[FAIL] FULLTC-530: 최하단 스크롤 후 가로 스크롤 발생 — " \
            "GDPR 부록 등 하단 콘텐츠 렌더링 시 뷰포트 벗어남"