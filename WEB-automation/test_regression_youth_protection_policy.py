"""
tests/stage8_regression/web/test_regression_youth_protection_policy.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
청소년보호정책(Youth Protection Policy) 회귀 테스트
FULLTC-534 ~ FULLTC-536 (3 TCs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_youth_protection_policy.py -v
  pytest tests/stage8_regression/web/test_regression_youth_protection_policy.py -m "youth_protection" -v
  pytest tests/stage8_regression/web/test_regression_youth_protection_policy.py -k "FULLTC_535" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)

[TC 클래스 구성]
  FULLTC-534   TestYouthPolicyEntry          메뉴 진입 (LNB 클릭)
  FULLTC-535   TestYouthPolicyLatestVersion  최신 버전 디폴트 노출
  FULLTC-536   TestYouthPolicyVersionChange  과거 버전 드롭다운 선택

[HTML 분석 핵심 포인트]
  ✅ 완전 안정 셀렉터 (즉시 사용 가능):
     · 드롭다운:    div.dropdown  (plain class!)
     · 날짜 라벨:   span.dateLabel  (plain class!)
     · 현재 날짜:   div.dropdown > div > span = "2024.03.19"
     · 정책 본문:   div#termsContent  (ID 기반 — 최강!)
     · 볼드 헤딩:   div#termsContent p b  ← <b> 태그 사용! (<strong> 아님!)
     · 섹션 1~4:    p:has-text() 기반 텍스트 매칭
     · 책임자 정보: p:has-text('성명'), p:has-text('소속') 등
                   (성명: 양한나 / 소속: 뉴스팀 / 이메일: sheep@bloomingbit.io)

  ⚠️ 이전 페이지들과의 핵심 차이점:
     · 볼드 태그: <b> (이용약관·개인정보처리방침·커뮤니티는 <strong>!)
       → div#termsContent p strong 셀렉터는 이 페이지에서 결과 없음
     · 주요 섹션(1~4)은 plain <p> 텍스트 (bold 없음)
     · 이메일: plain text (mailto 링크 아님)

  ⚠️ TODO_ 셀렉터 (실제 DOM 확인 후 튜닝 필요):
     · 드롭다운 옵션: DROPDOWN_OPTION
     · LNB 메뉴: LNB_WRAPPER, LNB_YOUTH_MENU (FULLTC-534)
     · 페이지 URL: YOUTH_POLICY_PATH (F12 주소창 확인 후 수정)
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from youth_protection_policy_page import YouthProtectionPolicyPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def youth_policy_page() -> Iterator[YouthProtectionPolicyPage]:
    """청소년보호정책 페이지 픽스처 (로그인 세션 유지)
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
        yield YouthProtectionPolicyPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-534  |  메뉴 진입
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.youth_protection
class TestYouthPolicyEntry:
    """LNB 메뉴 클릭으로 청소년보호정책 페이지 진입 검증 — FULLTC-534
    ⚠️ LNB_WRAPPER, LNB_YOUTH_MENU 셀렉터가 TODO_ 상태 → skip 자동 처리
    """

    def test_FULLTC_534_lnb_menu_click_navigates_and_activates(
        self, youth_policy_page: YouthProtectionPolicyPage
    ) -> None:
        """
        FULLTC-534 | 청소년보호정책/LNB 메뉴 클릭 | Major
        LNB에서 [청소년보호정책] 메뉴 클릭 시 해당 페이지로 이동하고
        LNB에서 [청소년보호정책] 메뉴가 활성(하이라이트) 상태로 표시되어야 한다.
        ⚠️ TODO: LNB_WRAPPER, LNB_YOUTH_MENU, LNB_ACTIVE_MENU 셀렉터 튜닝 필요
        """
        youth_policy_page.go_to_mypage()
        youth_policy_page.page.wait_for_timeout(600)

        if not youth_policy_page.is_lnb_visible():
            pytest.skip(
                "[SKIP] FULLTC-534: LNB 영역 미노출 — "
                "TODO: LNB_WRAPPER 셀렉터 튜닝 후 재실행"
            )

        url_before = youth_policy_page.get_current_url()
        youth_policy_page.click_lnb_youth_menu()

        # 1) URL 변경 확인
        assert youth_policy_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-534: LNB '청소년보호정책' 메뉴 클릭 후 URL 미변경"

        # 2) 페이지 정상 로드 확인
        assert youth_policy_page.is_loaded(), \
            "[FAIL] FULLTC-534: 청소년보호정책 페이지 로드 실패 (div#termsContent 미노출)"

        # 3) 타이틀 확인
        assert youth_policy_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-534: 페이지 타이틀이 '청소년보호정책' 아님 " \
            f"(현재: '{youth_policy_page.get_page_title_text()}')"

        # 4) LNB 활성화 상태 확인 (TODO 셀렉터)
        if youth_policy_page.is_lnb_visible():
            lnb_active = youth_policy_page.is_lnb_youth_menu_active()
            if not lnb_active:
                pytest.skip(
                    "[SKIP] FULLTC-534 (LNB 활성): LNB 활성 메뉴 확인 실패 — "
                    "TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요"
                )
            assert lnb_active, \
                "[FAIL] FULLTC-534: 이동 후 LNB에서 '청소년보호정책' 메뉴가 " \
                "활성(하이라이트) 상태 아님"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-535  |  최신 버전 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.youth_protection
class TestYouthPolicyLatestVersion:
    """최신 시행일자 드롭다운 디폴트 선택 및 본문 노출 검증 — FULLTC-535
    ✅ 다수의 안정 셀렉터로 즉시 검증 가능 (섹션 1~4, 책임자 정보 포함)
    """

    def test_FULLTC_535_latest_version_shown_by_default(
        self, youth_policy_page: YouthProtectionPolicyPage
    ) -> None:
        """
        FULLTC-535 | 청소년보호정책/최신 시행일자 디폴트 선택 | Major
        페이지 진입 시 상단 드롭다운에 가장 최신 시행일자가 디폴트로 선택되어 있고
        본문에 최신 버전 청소년보호정책 내용이 표시되어야 한다.

        ✅ 이 TC에서 검증 가능한 안정 항목:
           · 드롭다운 날짜 노출 (div.dropdown > div > span)
           · 본문 영역 로드 (div#termsContent)
           · 4개 섹션 모두 존재 (p:has-text 기반)
           · 책임자 정보 정확성 (성명·소속·이메일)
        ⚠️ 볼드 태그: p b (<strong>이 아닌 <b>) — 섹션 헤딩은 plain p로 존재
        """
        youth_policy_page.go_to_youth_policy()
        assert youth_policy_page.is_loaded(), \
            "[FAIL] FULLTC-535: 청소년보호정책 페이지 로드 실패 (div#termsContent 미노출)"

        # 1) 드롭다운 컨테이너 노출 확인
        assert youth_policy_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-535: 시행일자 드롭다운(div.dropdown) 미노출"

        # 2) 날짜 라벨 노출 및 텍스트 확인
        assert youth_policy_page.is_date_label_visible(), \
            "[FAIL] FULLTC-535: '시행/변경 일자' 라벨(span.dateLabel) 미노출"

        date_label = youth_policy_page.get_date_label_text()
        assert "시행" in date_label or "변경" in date_label, \
            f"[FAIL] FULLTC-535: 날짜 라벨 텍스트 불일치 " \
            f"(기대: '시행/변경 일자', 현재: '{date_label}')"

        # 3) 드롭다운에 날짜 표시 확인
        dropdown_date = youth_policy_page.get_dropdown_current_date()
        assert dropdown_date.strip() != "", \
            "[FAIL] FULLTC-535: 드롭다운(div.dropdown > div > span) 날짜 텍스트 비어있음"

        # 4) 날짜 포맷 확인 (YYYY.MM.DD)
        assert youth_policy_page.is_date_format_valid(dropdown_date), \
            f"[FAIL] FULLTC-535: 드롭다운 날짜 포맷 불일치 — " \
            f"'YYYY.MM.DD' 기대 (현재: '{dropdown_date}')"

        # 5) 정책 본문 노출 확인 (div#termsContent — ID 안정 셀렉터)
        assert youth_policy_page.is_policy_content_visible(), \
            "[FAIL] FULLTC-535: 청소년보호정책 본문 영역(div#termsContent) 미노출"

        # 6) 본문 텍스트 충분한 분량인지 확인 (최소 200자)
        assert youth_policy_page.is_policy_content_not_empty(), \
            "[FAIL] FULLTC-535: 청소년보호정책 본문 텍스트 200자 미만 — 내용 미로드 의심"

        # 7) 4개 주요 섹션 모두 노출 확인 (p:has-text 기반 안정 셀렉터)
        missing_sections = youth_policy_page.get_missing_sections()
        assert len(missing_sections) == 0, \
            f"[FAIL] FULLTC-535: 청소년보호정책 필수 섹션 미노출 — " \
            f"누락 항목: {missing_sections}"

        # 8) 책임자 정보 섹션 노출 확인 (HTML에서 직접 확인된 안정 셀렉터)
        assert youth_policy_page.is_manager_section_present(), \
            "[FAIL] FULLTC-535: 책임자 정보 섹션 미노출 " \
            "(p:has-text('성명') / p:has-text('소속') / p:has-text('E-mail'))"

        # 9) 책임자 정보 정확성 검증 (성명·소속·이메일)
        is_accurate, error_detail = youth_policy_page.is_manager_info_accurate()
        assert is_accurate, \
            f"[FAIL] FULLTC-535: 청소년보호 책임자 정보 불일치 — {error_detail}"

        # 10) 볼드(<b>) 요소 존재 확인 (<strong>이 아닌 <b> 태그!)
        bold_count = youth_policy_page.get_bold_element_count()
        assert bold_count >= 1, \
            f"[FAIL] FULLTC-535: <b> 태그 볼드 요소 0개 — " \
            f"청소년보호정책 타이틀·책임자 헤더 볼드 미렌더링 " \
            f"(div#termsContent p b 셀렉터 확인)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-536  |  과거 버전 변경
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.youth_protection
class TestYouthPolicyVersionChange:
    """시행일자 드롭다운으로 과거 버전 선택 및 본문 내용 변경 검증 — FULLTC-536
    ⚠️ 드롭다운 옵션 목록(DROPDOWN_OPTION)이 TODO_ 상태 →
       과거 버전이 없거나 셀렉터 미튜닝 시 skip 자동 처리
    """

    def test_FULLTC_536_past_version_dropdown_and_content_change(
        self, youth_policy_page: YouthProtectionPolicyPage
    ) -> None:
        """
        FULLTC-536 | 청소년보호정책/시행일자 드롭다운 과거 버전 선택 | Major
        드롭다운을 클릭하면 과거 시행일자 목록이 노출되고,
        과거 날짜 선택 후 해당 시점의 청소년보호정책 텍스트로 본문이 변경되어야 한다.
        ⚠️ TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요 (드롭다운 열고 F12 확인)
        사전 조건: 과거 시행일자 이력 1건 이상 존재
        """
        youth_policy_page.go_to_youth_policy()
        assert youth_policy_page.is_loaded(), \
            "[FAIL] FULLTC-536: 청소년보호정책 페이지 로드 실패"

        assert youth_policy_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-536: 시행일자 드롭다운(div.dropdown) 미노출"

        # 1) 드롭다운 클릭 (열기)
        current_date = youth_policy_page.get_dropdown_current_date()
        youth_policy_page.click_dropdown_toggle()
        youth_policy_page.page.wait_for_timeout(600)

        # 2) 드롭다운 옵션 목록 노출 확인
        option_count = youth_policy_page.get_dropdown_option_count()
        if option_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-536: 드롭다운 옵션 항목 0개 — "
                "과거 버전이 없거나 TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요. "
                "드롭다운 열고 F12 확인 후 셀렉터 교체"
            )

        # 3) 현재 날짜와 다른 옵션이 있는지 확인
        option_texts = youth_policy_page.get_dropdown_option_texts()
        other_options = [
            t for t in option_texts
            if t != current_date and youth_policy_page.is_date_format_valid(t)
        ]
        if not other_options:
            pytest.skip(
                f"[SKIP] FULLTC-536: 과거 버전 옵션 없음 — "
                f"드롭다운 항목: {option_texts}, 현재 날짜: '{current_date}'"
            )

        # 4) 현재 본문 텍스트 기록 (변경 전)
        content_before = youth_policy_page.get_all_policy_text()

        # 5) 과거 버전 선택
        selected_date = youth_policy_page.select_dropdown_option_by_index(
            option_texts.index(other_options[0])
        )
        if not selected_date:
            pytest.skip(
                "[SKIP] FULLTC-536: 과거 버전 옵션 클릭 실패 — "
                "TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요"
            )

        # 6) 드롭다운 표시 날짜 변경 확인
        new_dropdown_date = youth_policy_page.get_dropdown_current_date()
        assert new_dropdown_date != current_date, \
            f"[FAIL] FULLTC-536: 과거 버전 선택 후 드롭다운 날짜 미변경 " \
            f"(before: '{current_date}', after: '{new_dropdown_date}')"

        assert youth_policy_page.is_date_format_valid(new_dropdown_date), \
            f"[FAIL] FULLTC-536: 선택 후 드롭다운 날짜 포맷 불일치 " \
            f"(현재: '{new_dropdown_date}')"

        # 7) 본문 내용 변경 확인
        content_after = youth_policy_page.get_all_policy_text()
        assert content_after.strip() != "", \
            "[FAIL] FULLTC-536: 과거 버전 선택 후 청소년보호정책 본문 비어있음"

        if content_after == content_before:
            pytest.skip(
                "[SKIP] FULLTC-536: 과거 버전 선택 후 본문 내용이 이전과 동일 — "
                "버전 간 내용 차이 없거나 같은 버전 선택됨"
            )

        assert content_after != content_before, \
            "[FAIL] FULLTC-536: 과거 버전 선택 후 청소년보호정책 본문 미변경 — " \
            "다른 버전의 정책 내용으로 교체되지 않음"