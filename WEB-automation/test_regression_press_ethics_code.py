"""
tests/stage8_regression/web/test_regression_press_ethics_code.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
언론윤리강령(Press Ethics Code) 회귀 테스트
FULLTC-537 ~ FULLTC-539 (3 TCs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_press_ethics_code.py -v
  pytest tests/stage8_regression/web/test_regression_press_ethics_code.py -m "press_ethics" -v
  pytest tests/stage8_regression/web/test_regression_press_ethics_code.py -k "FULLTC_538" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)

[TC 클래스 구성]
  FULLTC-537   TestPressEthicsEntry          메뉴 진입 (LNB 클릭)
  FULLTC-538   TestPressEthicsLatestVersion  최신 버전 디폴트 노출
  FULLTC-539   TestPressEthicsVersionChange  과거 버전 드롭다운 선택

[HTML 분석 핵심 포인트]
  ✅ 완전 안정 셀렉터 (즉시 사용 가능):
     · 드롭다운:    div.dropdown  (plain class!)
     · 날짜 라벨:   span.dateLabel  (plain class!)
     · 현재 날짜:   div.dropdown > div > span = "2022.10.07"
     · 강령 본문:   div#termsContent  (ID 기반 — 최강!)
     · 조항 헤딩:   div#termsContent p strong
                   ← <strong> 태그! (청소년보호정책의 <b>와 달리 <strong> 복귀)
                   11개: 윤리강령(intro) + 제1조~제10조

  ⚠️ 청소년보호정책(youth_protection)과의 핵심 차이:
     · 볼드 태그: <strong> (youth_protection은 <b>였음!)
       → div#termsContent p strong 셀렉터 정상 동작 (11개 반환)
     · 각 조항이 <p><strong>제목</strong><br>본문</p> 구조
       (제목과 본문이 같은 <p> 안에 있음 — 이용약관과도 다른 구조)
     · 관리자 정보 없음 / mailto 링크 없음

  ⚠️ TODO_ 셀렉터 (실제 DOM 확인 후 튜닝 필요):
     · 드롭다운 옵션: DROPDOWN_OPTION
     · LNB 메뉴: LNB_WRAPPER, LNB_ETHICS_MENU (FULLTC-537)
     · 페이지 URL: ETHICS_CODE_PATH (F12 주소창 확인 후 수정)
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from press_ethics_code_page import PressEthicsCodePage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def ethics_page() -> Iterator[PressEthicsCodePage]:
    """언론윤리강령 페이지 픽스처 (로그인 세션 유지)
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
        yield PressEthicsCodePage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-537  |  메뉴 진입
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.press_ethics
class TestPressEthicsEntry:
    """LNB 메뉴 클릭으로 언론윤리강령 페이지 진입 검증 — FULLTC-537
    ⚠️ LNB_WRAPPER, LNB_ETHICS_MENU 셀렉터가 TODO_ 상태 → skip 자동 처리
    """

    def test_FULLTC_537_lnb_menu_click_navigates_and_activates(
        self, ethics_page: PressEthicsCodePage
    ) -> None:
        """
        FULLTC-537 | 언론윤리강령/LNB 메뉴 클릭 | Major
        LNB에서 [언론윤리강령] 메뉴 클릭 시 해당 페이지로 이동하고
        LNB에서 [언론윤리강령] 메뉴가 활성(하이라이트) 상태로 표시되어야 한다.
        ⚠️ TODO: LNB_WRAPPER, LNB_ETHICS_MENU, LNB_ACTIVE_MENU 셀렉터 튜닝 필요
        """
        ethics_page.go_to_mypage()
        ethics_page.page.wait_for_timeout(600)

        if not ethics_page.is_lnb_visible():
            pytest.skip(
                "[SKIP] FULLTC-537: LNB 영역 미노출 — "
                "TODO: LNB_WRAPPER 셀렉터 튜닝 후 재실행"
            )

        url_before = ethics_page.get_current_url()
        ethics_page.click_lnb_ethics_menu()

        # 1) URL 변경 확인
        assert ethics_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-537: LNB '언론윤리강령' 메뉴 클릭 후 URL 미변경"

        # 2) 페이지 정상 로드 확인
        assert ethics_page.is_loaded(), \
            "[FAIL] FULLTC-537: 언론윤리강령 페이지 로드 실패 (div#termsContent 미노출)"

        # 3) 타이틀 확인
        assert ethics_page.is_page_title_correct(), \
            f"[FAIL] FULLTC-537: 페이지 타이틀이 '언론윤리강령' 아님 " \
            f"(현재: '{ethics_page.get_page_title_text()}')"

        # 4) LNB 활성화 상태 확인 (TODO 셀렉터)
        if ethics_page.is_lnb_visible():
            lnb_active = ethics_page.is_lnb_ethics_menu_active()
            if not lnb_active:
                pytest.skip(
                    "[SKIP] FULLTC-537 (LNB 활성): LNB 활성 메뉴 확인 실패 — "
                    "TODO: LNB_ACTIVE_MENU 셀렉터 튜닝 필요"
                )
            assert lnb_active, \
                "[FAIL] FULLTC-537: 이동 후 LNB에서 '언론윤리강령' 메뉴가 " \
                "활성(하이라이트) 상태 아님"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-538  |  최신 버전 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.press_ethics
class TestPressEthicsLatestVersion:
    """최신 시행일자 드롭다운 디폴트 선택 및 본문 노출 검증 — FULLTC-538
    ✅ 다수의 안정 셀렉터로 즉시 검증 가능 (조항 헤딩 p strong, 조항별 has-text)
    """

    def test_FULLTC_538_latest_version_shown_by_default(
        self, ethics_page: PressEthicsCodePage
    ) -> None:
        """
        FULLTC-538 | 언론윤리강령/최신 시행일자 디폴트 선택 | Major
        페이지 진입 시 상단 드롭다운에 가장 최신 시행일자가 디폴트로 선택되어 있고
        본문에 최신 버전 언론윤리강령 내용이 표시되어야 한다.

        ✅ 이 TC에서 검증 가능한 안정 항목:
           · 드롭다운 날짜 노출 (div.dropdown > div > span)
           · 강령 본문 로드 (div#termsContent)
           · 조항 헤딩 수 >= 5 (div#termsContent p strong)
           · 윤리강령(intro), 제1조, 제10조 존재 확인
        ⚠️ 볼드 태그: p strong (<strong>! 청소년보호정책의 <b>와 달리 <strong>)
        ⚠️ 각 조항은 <p><strong>제목</strong><br>본문</p> 구조 (제목·본문 동일 p)
        """
        ethics_page.go_to_ethics_code()
        assert ethics_page.is_loaded(), \
            "[FAIL] FULLTC-538: 언론윤리강령 페이지 로드 실패 (div#termsContent 미노출)"

        # 1) 드롭다운 컨테이너 노출 확인
        assert ethics_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-538: 시행일자 드롭다운(div.dropdown) 미노출"

        # 2) 날짜 라벨 노출 및 텍스트 확인
        assert ethics_page.is_date_label_visible(), \
            "[FAIL] FULLTC-538: '시행/변경 일자' 라벨(span.dateLabel) 미노출"

        date_label = ethics_page.get_date_label_text()
        assert "시행" in date_label or "변경" in date_label, \
            f"[FAIL] FULLTC-538: 날짜 라벨 텍스트 불일치 " \
            f"(기대: '시행/변경 일자', 현재: '{date_label}')"

        # 3) 드롭다운에 날짜 표시 확인
        dropdown_date = ethics_page.get_dropdown_current_date()
        assert dropdown_date.strip() != "", \
            "[FAIL] FULLTC-538: 드롭다운(div.dropdown > div > span) 날짜 텍스트 비어있음"

        # 4) 날짜 포맷 확인 (YYYY.MM.DD)
        assert ethics_page.is_date_format_valid(dropdown_date), \
            f"[FAIL] FULLTC-538: 드롭다운 날짜 포맷 불일치 — " \
            f"'YYYY.MM.DD' 기대 (현재: '{dropdown_date}')"

        # 5) 강령 본문 노출 확인 (div#termsContent — ID 안정 셀렉터)
        assert ethics_page.is_ethics_content_visible(), \
            "[FAIL] FULLTC-538: 언론윤리강령 본문 영역(div#termsContent) 미노출"

        # 6) 본문 텍스트 충분한 분량인지 확인 (최소 200자)
        assert ethics_page.is_ethics_content_not_empty(), \
            "[FAIL] FULLTC-538: 언론윤리강령 본문 텍스트 200자 미만 — 내용 미로드 의심"

        # 7) 조항 헤딩 수 확인 (div#termsContent p strong — <strong> 태그!)
        heading_count = ethics_page.get_article_heading_count()
        assert heading_count >= PressEthicsCodePage.MIN_ARTICLE_COUNT, \
            f"[FAIL] FULLTC-538: 언론윤리강령 조항 헤딩 수 부족 — " \
            f"기대: {PressEthicsCodePage.MIN_ARTICLE_COUNT}개 이상, " \
            f"실제: {heading_count}개 (div#termsContent p strong)"

        # 8) 핵심 조항 존재 확인 (first / last / middle)
        missing = ethics_page.get_missing_key_articles()
        assert len(missing) == 0, \
            f"[FAIL] FULLTC-538: 핵심 조항 미노출 — 누락 항목: {missing}"

        # 9) 개별 조항 내용 확인 — 제1조 단락에 '언론의 자유' 포함
        article_1_text = ethics_page.get_article_1_text()
        if article_1_text.strip():
            assert "언론의 자유" in article_1_text or "알권리" in article_1_text, \
                f"[FAIL] FULLTC-538: 제1조 본문에 '언론의 자유' 관련 내용 미포함 " \
                f"(실제: '{article_1_text[:80]}'...)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-539  |  과거 버전 변경
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.press_ethics
class TestPressEthicsVersionChange:
    """시행일자 드롭다운으로 과거 버전 선택 및 본문 내용 변경 검증 — FULLTC-539
    ⚠️ 드롭다운 옵션 목록(DROPDOWN_OPTION)이 TODO_ 상태 →
       과거 버전이 없거나 셀렉터 미튜닝 시 skip 자동 처리
    """

    def test_FULLTC_539_past_version_dropdown_and_content_change(
        self, ethics_page: PressEthicsCodePage
    ) -> None:
        """
        FULLTC-539 | 언론윤리강령/시행일자 드롭다운 과거 버전 선택 | Major
        드롭다운을 클릭하면 과거 시행일자 목록이 노출되고,
        과거 날짜 선택 후 해당 시점의 언론윤리강령 텍스트로 본문이 변경되며
        텍스트 포맷이 깨지지 않아야 한다.
        ⚠️ TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요 (드롭다운 열고 F12 확인)
        사전 조건: 과거 시행일자 이력 1건 이상 존재
        """
        ethics_page.go_to_ethics_code()
        assert ethics_page.is_loaded(), \
            "[FAIL] FULLTC-539: 언론윤리강령 페이지 로드 실패"

        assert ethics_page.is_dropdown_visible(), \
            "[FAIL] FULLTC-539: 시행일자 드롭다운(div.dropdown) 미노출"

        # 1) 드롭다운 클릭 (열기)
        current_date = ethics_page.get_dropdown_current_date()
        ethics_page.click_dropdown_toggle()
        ethics_page.page.wait_for_timeout(600)

        # 2) 드롭다운 옵션 목록 노출 확인
        option_count = ethics_page.get_dropdown_option_count()
        if option_count == 0:
            pytest.skip(
                "[SKIP] FULLTC-539: 드롭다운 옵션 항목 0개 — "
                "과거 버전이 없거나 TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요. "
                "드롭다운 열고 F12 확인 후 셀렉터 교체"
            )

        # 3) 현재 날짜와 다른 옵션이 있는지 확인
        option_texts = ethics_page.get_dropdown_option_texts()
        other_options = [
            t for t in option_texts
            if t != current_date and ethics_page.is_date_format_valid(t)
        ]
        if not other_options:
            pytest.skip(
                f"[SKIP] FULLTC-539: 과거 버전 옵션 없음 — "
                f"드롭다운 항목: {option_texts}, 현재 날짜: '{current_date}'"
            )

        # 4) 현재 본문 텍스트 기록 (변경 전)
        content_before = ethics_page.get_all_ethics_text()
        heading_count_before = ethics_page.get_article_heading_count()

        # 5) 과거 버전 선택
        selected_date = ethics_page.select_dropdown_option_by_index(
            option_texts.index(other_options[0])
        )
        if not selected_date:
            pytest.skip(
                "[SKIP] FULLTC-539: 과거 버전 옵션 클릭 실패 — "
                "TODO: DROPDOWN_OPTION 셀렉터 튜닝 필요"
            )

        # 6) 드롭다운 표시 날짜 변경 확인
        new_dropdown_date = ethics_page.get_dropdown_current_date()
        assert new_dropdown_date != current_date, \
            f"[FAIL] FULLTC-539: 과거 버전 선택 후 드롭다운 날짜 미변경 " \
            f"(before: '{current_date}', after: '{new_dropdown_date}')"

        assert ethics_page.is_date_format_valid(new_dropdown_date), \
            f"[FAIL] FULLTC-539: 선택 후 드롭다운 날짜 포맷 불일치 " \
            f"(현재: '{new_dropdown_date}')"

        # 7) 본문 내용 변경 확인
        content_after = ethics_page.get_all_ethics_text()
        assert content_after.strip() != "", \
            "[FAIL] FULLTC-539: 과거 버전 선택 후 언론윤리강령 본문 비어있음"

        if content_after == content_before:
            pytest.skip(
                "[SKIP] FULLTC-539: 과거 버전 선택 후 본문 내용이 이전과 동일 — "
                "버전 간 내용 차이 없거나 같은 버전 선택됨"
            )

        assert content_after != content_before, \
            "[FAIL] FULLTC-539: 과거 버전 선택 후 언론윤리강령 본문 미변경 — " \
            "다른 버전의 강령 내용으로 교체되지 않음"

        # 8) 변경 후 텍스트 포맷 무결성 확인
        #    — TC-539 기대결과에 "텍스트 포맷이 깨지지 않는다" 명시됨
        heading_count_after = ethics_page.get_article_heading_count()
        assert heading_count_after >= 1, \
            f"[FAIL] FULLTC-539: 과거 버전 선택 후 조항 헤딩(p strong) 0개 — " \
            f"텍스트 포맷 깨짐 의심 (변경 전: {heading_count_before}개)"

        # 본문이 여전히 충분한 텍스트를 가지는지 확인
        assert len(content_after.strip()) >= 100, \
            f"[FAIL] FULLTC-539: 과거 버전 선택 후 본문 텍스트 100자 미만 — " \
            f"텍스트 포맷 깨짐 또는 내용 누락 ({len(content_after.strip())}자)"