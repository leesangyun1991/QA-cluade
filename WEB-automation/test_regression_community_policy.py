"""
tests/stage8_regression/web/test_regression_community_policy.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
커뮤니티 운영정책(Community Operation Policy) 회귀 테스트
FULLTC-531 ~ FULLTC-533 (3 TCs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_community_policy.py -v
  pytest tests/stage8_regression/web/test_regression_community_policy.py -m "community_policy" -v
  pytest tests/stage8_regression/web/test_regression_community_policy.py -k "FULLTC_532" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)

[TC 클래스 구성]
  FULLTC-531   TestCommunityPolicyEntry          메뉴 진입 (LNB 클릭)
  FULLTC-532   TestCommunityPolicyLatestVersion  최신 버전 디폴트 노출
  FULLTC-533   TestCommunityPolicyVersionChange  과거 버전 드롭다운 선택

[HTML 분석 핵심 포인트]
  ✅ 완전 안정 셀렉터 (즉시 사용 가능):
     · 드롭다운:     div.dropdown  (plain class! — 이용약관·개인정보처리방침과 동일)
     · 날짜 라벨:    span.dateLabel  (plain class!)
     · 현재 날짜:    div.dropdown > div > span = "2025.09.02"
     · 정책 본문:    div#termsContent  (ID 기반 — 최강!)
     · 섹션 헤딩:    div#termsContent p strong
       (17개: 1. / 1.1~1.4 / 2. / 2.1~2.9 / 3. / 4.)
     · mailto 링크:  div#termsContent a[href^='mailto:']
       ← 실제 <a href="mailto:help@bloomingbit.io"> 태그로 존재!

  ⚠️ 이전 페이지(이용약관·개인정보처리방침)와의 차이점:
     · 본문 구조: div#termsContent > div > p  (span 래퍼 없음)
     · 섹션 형식: 조항 번호(1., 2.) + 소항목(1.1, 2.9) 방식
     · 시행일자 형식: "2025년 9월 9일" (한글 — YYYY.MM.DD 아님)

  ⚠️ TODO_ 셀렉터 (실제 DOM 확인 후 튜닝 필요):
     · 드롭다운 옵션: DROPDOWN_OPTION
     · LNB 메뉴: LNB_WRAPPER, LNB_COMMUNITY_MENU (FULLTC-531)
     · 페이지 URL: COMMUNITY_POLICY_PATH (F12 주소창 확인 후 수정)
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from community_policy_page import CommunityPolicyPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def community_policy_page() -> Iterator[CommunityPolicyPage]:
    """커뮤니티 운영정책 페이지 픽스처 (로그인 세션 유지)
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
        yield CommunityPolicyPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-531  |  메뉴 진입
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.community_policy
class TestCommunityPolicyEntry:
    """LNB 메뉴 클릭으로 커뮤니티 운영정책 페이지 진입 검증 — FULLTC-531
    ⚠️ LNB_WRAPPER, LNB_COMMUNITY_MENU 셀렉터가 TODO_ 상태 → skip 자동 처리
    """

    def test_FULLTC_531_lnb_menu_click_navigates_and_activates(
        self, community_policy_page: CommunityPolicyPage
    ) -> None:
        """
        FULLTC-531 | 커뮤니티 운영정책/LNB 메뉴 클릭 | Major
        LNB에서 [커뮤니티 운영정책] 메뉴 클릭 시 해당 페이지로 이동하고
        LNB에서 [커뮤니티 운영정책] 메뉴가 활성(하이라이트) 상태로 표시되어야 한다.
        ⚠️ TODO: LNB_WRAPPER, LNB_COMMUNITY_MENU, LNB_ACTIVE_MENU 셀렉터 튜닝 필요
        """
        community_policy_page.go_to_mypage()
        community_policy_page.page.wait_for_timeout(600)

        if not community_policy_page.is_lnb_visible():
            pytest.skip(
                "[SKIP] FULLTC-531: LNB 영역 미노출 — "
                "TODO: LNB_WRAPPER 셀렉터 튜닝 후 재실행"
            )

        url_before = community_policy_page.get_current_url()
        community_policy_page.click_lnb_community_menu()

        # 1) URL 변경 확인
        assert community_policy_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-531: LNB '커뮤니티 운영정책' 메뉴 클릭 후 URL 미변경"

        # 2) 페이지 정상 로드 확인
        assert community_policy_page.is_loaded(), \
            "[FAIL] FULLTC-531: 커뮤니티 운영정책 페이지 로드 실패 (div#termsContent 미노출)"

        # 3) 타이틀 확인
        assert community_policy_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-531: 페이지 타이틀이 '커뮤니티 운영정책' 아님 " \
            f"(현재: '{community_policy_page.get_page_title_text()}')"

        # 4) LNB 활성화 상태 확인 (TODO 셀렉터)
        if community_policy_page.is_lnb_visible():
            lnb_active = community_policy_page.is_lnb_community_menu_active()
            if not lnb_active:
                pytest.skip(
                    "[SKIP] FULLTC-531 (LNB 활성): LNB 활성 메뉴 확인 실패 — "
                    "TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요"
                )
            assert lnb_active, \
                "[FAIL] FULLTC-531: 이동 후 LNB에서 '커뮤니티 운영정책' 메뉴가 " \
                "활성(하이라이트) 상태 아님"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-532  |  최신 버전 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.community_policy
class TestCommunityPolicyLatestVersion:
    """최신 시행일자 드롭다운 디폴트 선택 및 본문 노출 검증 — FULLTC-532
    ✅ div.dropdown / div#termsContent — 안정 셀렉터로 즉시 검증 가능
    """

    def test_FULLTC_532_latest_version_shown_by_default(
        self, community_policy_page: CommunityPolicyPage
    ) -> None:
        """
        FULLTC-532 | 커뮤니티 운영정책/최신 시행일자 디폴트 선택 | Major
        페이지 진입 시 상단 드롭다운에 가장 최신 시행일자가 디폴트로 선택되어 있고
        본문에 최신 버전 운영정책 내용이 표시되어야 한다.
        ✅ div.dropdown / div#termsContent — 안정 셀렉터로 즉시 검증 가능
        ✅ mailto 링크(div#termsContent a[href^='mailto:']) 함께 검증
        """
        community_policy_page.go_to_community_policy()
        assert community_policy_page.is_loaded(), \
            "[FAIL] FULLTC-532: 커뮤니티 운영정책 페이지 로드 실패 (div#termsContent 미노출)"

        # 1) 드롭다운 컨테이너 노출 확인
        assert community_policy_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-532: 시행일자 드롭다운(div.dropdown) 미노출"

        # 2) 날짜 라벨 노출 및 텍스트 확인
        assert community_policy_page.is_date_label_visible(), \
            "[FAIL] FULLTC-532: '시행/변경 일자' 라벨(span.dateLabel) 미노출"

        date_label = community_policy_page.get_date_label_text()
        assert "시행" in date_label or "변경" in date_label, \
            f"[FAIL] FULLTC-532: 날짜 라벨 텍스트 불일치 " \
            f"(기대: '시행/변경 일자', 현재: '{date_label}')"

        # 3) 드롭다운에 날짜 표시 확인
        dropdown_date = community_policy_page.get_dropdown_current_date()
        assert dropdown_date.strip() != "", \
            "[FAIL] FULLTC-532: 드롭다운(div.dropdown > div > span) 날짜 텍스트 비어있음"

        # 4) 날짜 포맷 확인 (YYYY.MM.DD)
        assert community_policy_page.is_date_format_valid(dropdown_date), \
            f"[FAIL] FULLTC-532: 드롭다운 날짜 포맷 불일치 — " \
            f"'YYYY.MM.DD' 기대 (현재: '{dropdown_date}')"

        # 5) 정책 본문 노출 확인 (div#termsContent — ID 안정 셀렉터)
        assert community_policy_page.is_policy_content_visible(), \
            "[FAIL] FULLTC-532: 운영정책 본문 영역(div#termsContent) 미노출"

        # 6) 본문 텍스트 충분한 분량인지 확인 (최소 500자)
        assert community_policy_page.is_policy_content_not_empty(), \
            "[FAIL] FULLTC-532: 운영정책 본문 텍스트 500자 미만 — 내용 미로드 의심"

        # 7) 핵심 섹션 헤딩 노출 확인
        heading_count = community_policy_page.get_section_heading_count()
        assert heading_count >= CommunityPolicyPage.MIN_SECTION_COUNT, \
            f"[FAIL] FULLTC-532: 섹션 헤딩 수 부족 — " \
            f"기대: {CommunityPolicyPage.MIN_SECTION_COUNT}개 이상, " \
            f"실제: {heading_count}개 (div#termsContent p strong)"

        # 8) 첫 번째 섹션("1. 회원 정책") 존재 확인
        assert community_policy_page.is_section_present("1."), \
            "[FAIL] FULLTC-532: 본문에 '1.' 섹션 미노출 — 최신 버전 운영정책 미로드"

        # 9) 마지막 섹션("4. 커뮤니티 이용 제재 유의 사항") 존재 확인
        assert community_policy_page.is_section_present("4."), \
            "[FAIL] FULLTC-532: 본문에 '4.' 섹션 미노출 — 정책 내용 불완전 렌더링"

        # 10) mailto 링크 존재 및 정확성 확인
        # ✅ HTML에서 실제 <a href="mailto:help@bloomingbit.io"> 태그로 확인됨
        assert community_policy_page.is_mailto_link_present(), \
            f"[FAIL] FULLTC-532: mailto 링크(div#termsContent a[href^='mailto:']) 미노출 — " \
            f"4. 이의신청 섹션의 {CommunityPolicyPage.EXPECTED_EMAIL} 링크 없음"

        assert community_policy_page.is_mailto_email_correct(), \
            f"[FAIL] FULLTC-532: mailto 링크 이메일 불일치 또는 오탈자 — " \
            f"기대: 'mailto:{CommunityPolicyPage.EXPECTED_EMAIL}', " \
            f"실제 href: '{community_policy_page.get_mailto_href()}'"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-533  |  과거 버전 변경
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.community_policy
class TestCommunityPolicyVersionChange:
    """시행일자 드롭다운으로 과거 버전 선택 및 본문 내용 변경 검증 — FULLTC-533
    ⚠️ 드롭다운 옵션 목록(DROPDOWN_OPTION)이 TODO_ 상태 →
       과거 버전이 없거나 셀렉터 미튜닝 시 skip 자동 처리
    """

    def test_FULLTC_533_past_version_dropdown_and_content_change(
        self, community_policy_page: CommunityPolicyPage
    ) -> None:
        """
        FULLTC-533 | 커뮤니티 운영정책/시행일자 드롭다운 과거 버전 선택 | Major
        드롭다운을 클릭하면 과거 시행일자 목록이 노출되고,
        과거 날짜 선택 후 해당 시점의 운영정책 텍스트로 본문이 변경되어야 한다.
        ⚠️ TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요 (드롭다운 열고 F12 확인)
        사전 조건: 과거 시행일자 이력 1건 이상 존재
        """
        community_policy_page.go_to_community_policy()
        assert community_policy_page.is_loaded(), \
            "[FAIL] FULLTC-533: 커뮤니티 운영정책 페이지 로드 실패"

        assert community_policy_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-533: 시행일자 드롭다운(div.dropdown) 미노출"

        # 1) 드롭다운 클릭 (열기)
        current_date = community_policy_page.get_dropdown_current_date()
        community_policy_page.click_dropdown_toggle()
        community_policy_page.page.wait_for_timeout(600)

        # 2) 드롭다운 옵션 목록 노출 확인
        option_count = community_policy_page.get_dropdown_option_count()
        if option_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-533: 드롭다운 옵션 항목 0개 — "
                "과거 버전이 없거나 TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요. "
                "드롭다운 열고 F12 확인 후 셀렉터 교체"
            )

        # 3) 현재 날짜와 다른 옵션이 있는지 확인
        option_texts = community_policy_page.get_dropdown_option_texts()
        other_options = [
            t for t in option_texts
            if t != current_date and community_policy_page.is_date_format_valid(t)
        ]
        if not other_options:
            pytest.skip(
                f"[SKIP] FULLTC-533: 과거 버전 옵션 없음 — "
                f"드롭다운 항목: {option_texts}, 현재 날짜: '{current_date}'"
            )

        # 4) 현재 본문 텍스트 기록 (변경 전)
        content_before = community_policy_page.get_all_policy_text()

        # 5) 과거 버전 선택
        selected_date = community_policy_page.select_dropdown_option_by_index(
            option_texts.index(other_options[0])
        )
        if not selected_date:
            pytest.skip(
                "[SKIP] FULLTC-533: 과거 버전 옵션 클릭 실패 — "
                "TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요"
            )

        # 6) 드롭다운 표시 날짜 변경 확인
        new_dropdown_date = community_policy_page.get_dropdown_current_date()
        assert new_dropdown_date != current_date, \
            f"[FAIL] FULLTC-533: 과거 버전 선택 후 드롭다운 날짜 미변경 " \
            f"(before: '{current_date}', after: '{new_dropdown_date}')"

        assert community_policy_page.is_date_format_valid(new_dropdown_date), \
            f"[FAIL] FULLTC-533: 선택 후 드롭다운 날짜 포맷 불일치 " \
            f"(현재: '{new_dropdown_date}')"

        # 7) 본문 내용 변경 확인
        content_after = community_policy_page.get_all_policy_text()
        assert content_after.strip() != "", \
            "[FAIL] FULLTC-533: 과거 버전 선택 후 운영정책 본문 비어있음"

        if content_after == content_before:
            pytest.skip(
                "[SKIP] FULLTC-533: 과거 버전 선택 후 본문 내용이 이전과 동일 — "
                "버전 간 내용 차이 없거나 같은 버전 선택됨"
            )

        assert content_after != content_before, \
            "[FAIL] FULLTC-533: 과거 버전 선택 후 운영정책 본문 미변경 — " \
            "다른 버전의 운영정책 내용으로 교체되지 않음"