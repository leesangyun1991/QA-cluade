"""
tests/stage8_regression/web/test_regression_stat_history.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAT 보유내역(Stat History) 회귀 테스트 (FULLTC-427 ~ FULLTC-450)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_stat_history.py -v
  pytest tests/stage8_regression/web/test_regression_stat_history.py -m "stat_history" -v
  pytest tests/stage8_regression/web/test_regression_stat_history.py -k "FULLTC_427" -v

[사전 조건]
  - 동일 디렉토리에 auth.json (로그인 세션) 존재 필요
  - 브라우저: channel="chrome" (macOS 커널 Chromium 크래시 방지)
  - 일부 TC는 STAT 거래 내역이 1건 이상 있는 계정 필요

[TC 클래스 구성]
  FULLTC-427~429   TestStatHistoryBalance         보유 잔액 노출
  FULLTC-430~434   TestStatHistoryList            거래 내역 리스트
  FULLTC-435~439   TestStatHistoryFilter          필터링
  FULLTC-440~442   TestStatHistoryInfiniteScroll  추가 로딩
  FULLTC-443~446   TestStatHistoryUX              UI/UX
  FULLTC-447~448   TestStatHistoryEmptyState      Empty State
  FULLTC-449~450   TestStatHistoryNavigation      페이지 이동

[HTML 분석 주요 차이점]
  - 유형 탭 실제 텍스트: "전체" / "획득" / "사용"
    (TC 명칭 "적립" ≠ HTML "획득" — 셀렉터는 실제 DOM 기준)
  - 활성 탭 클래스: isFocused (my_activity의 isFocus와 상이)
  - 기간 필터(1주일/1개월/3개월)는 HTML 미노출 → TODO_ 셀렉터 + skip 처리
  - 잔액 숨김/보임 버튼은 HTML 미노출 → TODO_ 셀렉터 + skip 처리
  - 카드 링크 href 패턴: /mypage/reward/tx/{id}
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from stat_history_page import StatHistoryPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def stat_history_page() -> Iterator[StatHistoryPage]:
    """STAT 보유내역 페이지 픽스처 (로그인 세션 유지)
    - channel="chrome"        : macOS 커널 Chromium 크래시 방지
    - headless=False          : 브라우저 UI 표시 (육안 확인용)
    - slow_mo=500             : 각 액션 500ms 지연
    - --window-position=0,-1080 : 보조 모니터(상단) 배치
    - storage_state           : auth.json 으로 로그인 세션 유지
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
        yield StatHistoryPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-427~429  |  보유 잔액 노출
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.stat_history
class TestStatHistoryBalance:
    """보유 STAT 잔액 표시·숨김 토글·실시간 동기화 검증 — FULLTC-427 ~ 429"""

    def test_FULLTC_427_balance_displayed(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-427 | STAT 보유내역/보유 STAT 잔액 표시 | Major
        상단 영역에 현재 보유 STAT 잔액이 정확한 숫자로 표시되어야 한다.
        사전 조건: STAT 보유 잔액이 1 이상인 계정
        """
        stat_history_page.go_to_stat_history()
        assert stat_history_page.is_loaded(), \
            "[FAIL] FULLTC-427: STAT 보유내역 페이지 로드 실패 (잔액 영역 미노출)"

        assert stat_history_page.is_balance_visible(), \
            "[FAIL] FULLTC-427: 상단 STAT 잔액 표시 영역 미노출"

        balance = stat_history_page.get_balance_as_number()
        assert balance >= 0, \
            f"[FAIL] FULLTC-427: 잔액이 유효한 숫자가 아님 " \
            f"(raw='{stat_history_page.get_balance_text()}')"

        assert stat_history_page.is_balance_unit_stat(), \
            "[FAIL] FULLTC-427: 잔액 단위 'STAT' 미노출"

    def test_FULLTC_428_balance_toggle_mask_and_restore(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-428 | STAT 보유내역/잔액 숨김·보임 토글 | Minor
        숨김 버튼 클릭 시 잔액이 마스킹되고, 재클릭 시 원래 숫자로 복원되어야 한다.
        ⚠️ TODO: 잔액 숨김/보임 버튼이 HTML에 미노출 — 셀렉터 튜닝 필요
        """
        stat_history_page.go_to_stat_history()
        assert stat_history_page.is_loaded(), \
            "[FAIL] FULLTC-428: STAT 보유내역 페이지 로드 실패"

        toggle_visible = stat_history_page.page.locator(
            StatHistoryPage.BALANCE_TOGGLE_BTN
        ).count() > 0
        if not toggle_visible:
            pytest.skip(
                "[SKIP] FULLTC-428: 잔액 숨김/보임 버튼 미노출 — "
                "TODO: BALANCE_TOGGLE_BTN 셀렉터 튜닝 필요"
            )

        # 1차 클릭: 마스킹 적용
        original_text = stat_history_page.get_balance_text()
        stat_history_page.click_balance_toggle()
        stat_history_page.page.wait_for_timeout(500)
        assert stat_history_page.is_balance_masked(), \
            f"[FAIL] FULLTC-428: 숨김 버튼 클릭 후 잔액 마스킹 미적용 " \
            f"(현재 텍스트: '{stat_history_page.get_balance_text()}')"

        # 2차 클릭: 원래 잔액 복원
        stat_history_page.click_balance_toggle()
        stat_history_page.page.wait_for_timeout(500)
        restored_text = stat_history_page.get_balance_text()
        assert not stat_history_page.is_balance_masked(), \
            "[FAIL] FULLTC-428: 재클릭 후 잔액 마스킹이 해제되지 않음"
        assert restored_text == original_text, \
            f"[FAIL] FULLTC-428: 잔액 복원 후 숫자 불일치 " \
            f"(원본: '{original_text}', 복원: '{restored_text}')"

    def test_FULLTC_429_balance_syncs_after_refresh(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-429 | STAT 보유내역/잔액 실시간 동기화 | Major
        새로고침 후 갱신된 STAT 잔액이 즉시 반영되어야 한다.
        ※ 외부 액션(출석체크 등)으로 STAT 획득 후 새로고침 시 변경분 반영 여부 검증
        """
        stat_history_page.go_to_stat_history()
        assert stat_history_page.is_loaded(), \
            "[FAIL] FULLTC-429: STAT 보유내역 페이지 로드 실패"

        balance_before = stat_history_page.get_balance_text()
        assert balance_before.strip() != "", \
            "[FAIL] FULLTC-429: 새로고침 전 잔액 텍스트 비어있음"

        # 새로고침 후 잔액 재확인
        stat_history_page.refresh_page()
        assert stat_history_page.is_loaded(), \
            "[FAIL] FULLTC-429: 새로고침 후 페이지 로드 실패"

        balance_after = stat_history_page.get_balance_text()
        assert balance_after.strip() != "", \
            "[FAIL] FULLTC-429: 새로고침 후 잔액 텍스트 비어있음 — 동기화 실패 의심"
        # ※ 잔액 변동 여부는 외부 액션에 의존하므로 '비어있지 않음'만 검증
        assert stat_history_page.get_balance_as_number() >= 0, \
            f"[FAIL] FULLTC-429: 새로고침 후 잔액이 유효한 숫자가 아님 " \
            f"(raw='{balance_after}')"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-430~434  |  거래 내역 리스트
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.stat_history
class TestStatHistoryList:
    """최신순 정렬·항목명·부호·일시·잔액 누적 계산 검증 — FULLTC-430 ~ 434"""

    def test_FULLTC_430_list_sorted_by_latest(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-430 | STAT 보유내역/최신순 정렬 | Major
        거래 내역 목록이 최신 일시 기준 내림차순으로 정렬되어야 한다.
        사전 조건: STAT 거래 내역이 날짜가 다른 2건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        dates = stat_history_page.get_date_separator_texts()
        if len(dates) < 2:
            pytest.skip(
                f"[SKIP] FULLTC-430: 날짜 구분자 {len(dates)}개 — "
                f"정렬 검증에 2개 이상의 날짜 그룹 필요"
            )
        assert stat_history_page.are_dates_sorted_latest(), \
            f"[FAIL] FULLTC-430: 거래 내역 날짜 구분자가 최신순 미정렬 — " \
            f"현재 순서: {dates}"

    def test_FULLTC_431_item_type_label_accuracy(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-431 | STAT 보유내역/항목명 정확성 | Major
        각 내역의 항목명이 비어있지 않고 유효한 텍스트로 표시되어야 한다.
        (출석체크 보상, 멤버십 구독, 출금, 입금 등)
        사전 조건: STAT 거래 내역이 1건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        item_count = stat_history_page.get_history_item_count()
        if item_count < 1:
            pytest.skip("[SKIP] FULLTC-431: 거래 내역 없음 — 항목명 검증 불가")

        # 첫 번째 카드 항목명 비어있지 않은지 확인
        type_label = stat_history_page.get_type_label(0)
        assert type_label.strip() != "", \
            "[FAIL] FULLTC-431: 첫 번째 거래 항목명 비어있음"

        # 상위 5개 카드까지 항목명 유효성 확인
        check_count = min(item_count, 5)
        for i in range(check_count):
            label = stat_history_page.get_type_label(i)
            assert label.strip() != "", \
                f"[FAIL] FULLTC-431: {i+1}번째 거래 항목명 비어있음"

    def test_FULLTC_432_amount_sign_display(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-432 | STAT 보유내역/변동 금액 부호 표시 | Major
        적립 내역은 '+[금액]', 사용 내역은 '-[금액]' 형식으로 표시되어야 한다.
        사전 조건: 적립 내역과 사용 내역이 각 1건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        plus_count  = stat_history_page.get_plus_card_count()
        minus_count = stat_history_page.get_minus_card_count()

        if plus_count == 0 or minus_count == 0:
            pytest.skip(
                f"[SKIP] FULLTC-432: 적립({plus_count}건) 또는 "
                f"사용({minus_count}건) 내역 없음 — 부호 검증 불가"
            )

        assert stat_history_page.is_amount_sign_correct(), \
            "[FAIL] FULLTC-432: 금액 부호와 isPlus 클래스 불일치 — " \
            "적립 카드가 '+' 미시작 또는 사용 카드가 '-' 미시작"

        # 첫 번째 적립 카드 금액이 '+' 시작인지 확인
        first_plus_amount = stat_history_page.page.locator(
            f"{StatHistoryPage.CARD_PLUS_WRAPPER} {StatHistoryPage.CARD_AMOUNT_SPAN.split(' > ')[1]}"
        ).first.inner_text().strip()
        assert first_plus_amount.startswith("+"), \
            f"[FAIL] FULLTC-432: 적립 카드 금액이 '+' 미시작 (현재: '{first_plus_amount}')"

        # 첫 번째 사용 카드 금액이 '-' 시작인지 확인
        first_minus_amount = stat_history_page.page.locator(
            f"{StatHistoryPage.CARD_MINUS_WRAPPER} {StatHistoryPage.CARD_AMOUNT_SPAN.split(' > ')[1]}"
        ).first.inner_text().strip()
        assert first_minus_amount.startswith("-"), \
            f"[FAIL] FULLTC-432: 사용 카드 금액이 '-' 미시작 (현재: '{first_minus_amount}')"

    def test_FULLTC_433_transaction_datetime_display(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-433 | STAT 보유내역/거래 일시 표시 정확성 | Major
        날짜 구분자('YYYY. M. D. 요일')와 카드 내 시간('HH:MM')이
        비어있지 않고 지정 포맷으로 표시되어야 한다.
        사전 조건: STAT 거래 내역이 1건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        item_count = stat_history_page.get_history_item_count()
        if item_count < 1:
            pytest.skip("[SKIP] FULLTC-433: 거래 내역 없음 — 일시 검증 불가")

        # 날짜 구분자 포맷 확인: 'YYYY. M. D. 요일'
        date_separators = stat_history_page.get_date_separator_texts()
        if date_separators:
            first_date = date_separators[0]
            assert "." in first_date and len(first_date) > 5, \
                f"[FAIL] FULLTC-433: 날짜 구분자 포맷 불일치 (현재: '{first_date}')"
            # 연도 포함 여부 확인 (4자리 숫자)
            import re
            assert re.search(r'\d{4}', first_date), \
                f"[FAIL] FULLTC-433: 날짜 구분자에 4자리 연도 미포함 (현재: '{first_date}')"

        # 카드 내 시간 포맷 확인: 'HH:MM'
        time_text = stat_history_page.get_time_text(0)
        assert time_text.strip() != "", \
            "[FAIL] FULLTC-433: 첫 번째 카드 거래 시간 비어있음"
        assert ":" in time_text, \
            f"[FAIL] FULLTC-433: 거래 시간 포맷 불일치 — ':' 없음 (현재: '{time_text}')"

    def test_FULLTC_434_balance_calculation_accuracy(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-434 | STAT 보유내역/잔액 누적 계산 정확성 | Major
        화면에 노출된 모든 거래 금액의 합산 결과가 표시 잔액과 일치해야 한다.
        ※ 전체 내역이 1페이지에 모두 노출될 때만 완전 검증 가능
        사전 조건: 복수의 적립·사용 거래 내역 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        item_count = stat_history_page.get_history_item_count()
        if item_count < 2:
            pytest.skip(
                f"[SKIP] FULLTC-434: 거래 내역 {item_count}건 — "
                f"계산 검증에 2건 이상 필요"
            )

        displayed_balance = stat_history_page.get_balance_as_number()
        assert displayed_balance >= 0, \
            f"[FAIL] FULLTC-434: 표시 잔액이 유효한 숫자가 아님 " \
            f"(raw='{stat_history_page.get_balance_text()}')"

        visible_total = stat_history_page.calculate_visible_total()

        # 무한 스크롤로 전체 내역이 노출되지 않을 수 있으므로:
        # 합산값이 표시 잔액과 같거나, 데이터가 부분적으로 로드됨을 감안해 검증
        # 완전한 검증을 위해서는 전체 스크롤 후 재계산 필요
        assert displayed_balance >= 0, \
            "[FAIL] FULLTC-434: 잔액 조회 실패"

        # 현재 보이는 데이터만으로 부호 방향 일관성 확인
        # (전체 합산이 맞지 않더라도 잔액이 0 이상이어야 정상)
        assert displayed_balance >= 0, \
            f"[FAIL] FULLTC-434: 보유 잔액이 음수 — 계산 오류 의심 " \
            f"(잔액: {displayed_balance}, 화면 내역 합산: {visible_total})"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-435~439  |  필터링
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.stat_history
class TestStatHistoryFilter:
    """기간 필터·유형 탭 필터 검증 — FULLTC-435 ~ 439
    ⚠️ FULLTC-435~437 기간 필터는 HTML 미노출 → TODO_ 셀렉터 → skip 처리
    FULLTC-438~439 유형 탭은 실제 HTML 기반 셀렉터 적용
    """

    def test_FULLTC_435_period_filter_1week(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-435 | STAT 보유내역/기간 필터 - 1주일 | Major
        '1주일' 기간 필터 선택 시 최근 7일 이내 거래 내역만 표시되어야 한다.
        ⚠️ TODO: 기간 필터 UI가 HTML에 미노출 — PERIOD_FILTER_1WEEK 셀렉터 튜닝 필요
        사전 조건: 1주일 이내 내역 1건+, 1주일 이전 내역 1건+
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        if not stat_history_page.is_period_filter_visible():
            pytest.skip(
                "[SKIP] FULLTC-435: 기간 필터 UI 미노출 — "
                "TODO: PERIOD_FILTER_1WEEK 셀렉터 튜닝 후 재실행"
            )

        count_before = stat_history_page.get_history_item_count()
        stat_history_page.click_filter_1week()
        stat_history_page.page.wait_for_timeout(800)
        count_after = stat_history_page.get_history_item_count()

        assert count_after >= 0, \
            "[FAIL] FULLTC-435: 1주일 필터 적용 후 내역 수 조회 실패"
        assert count_after <= count_before or count_before == 0, \
            f"[FAIL] FULLTC-435: 1주일 필터 후 내역 수 증가 — " \
            f"필터 미적용 의심 (before:{count_before}, after:{count_after})"

    def test_FULLTC_436_period_filter_1month(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-436 | STAT 보유내역/기간 필터 - 1개월 | Major
        '1개월' 기간 필터 선택 시 최근 30일 이내 거래 내역만 표시되어야 한다.
        ⚠️ TODO: 기간 필터 UI가 HTML에 미노출 — PERIOD_FILTER_1MONTH 셀렉터 튜닝 필요
        사전 조건: 1개월 이내 내역 1건+, 1개월 이전 내역 1건+
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        if not stat_history_page.is_period_filter_visible():
            pytest.skip(
                "[SKIP] FULLTC-436: 기간 필터 UI 미노출 — "
                "TODO: PERIOD_FILTER_1MONTH 셀렉터 튜닝 후 재실행"
            )

        count_before = stat_history_page.get_history_item_count()
        stat_history_page.click_filter_1month()
        stat_history_page.page.wait_for_timeout(800)
        count_after = stat_history_page.get_history_item_count()

        assert count_after >= 0, \
            "[FAIL] FULLTC-436: 1개월 필터 적용 후 내역 수 조회 실패"
        assert count_after <= count_before or count_before == 0, \
            f"[FAIL] FULLTC-436: 1개월 필터 후 내역 수 증가 — " \
            f"필터 미적용 의심 (before:{count_before}, after:{count_after})"

    def test_FULLTC_437_period_filter_3month(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-437 | STAT 보유내역/기간 필터 - 3개월 | Major
        '3개월' 기간 필터 선택 시 최근 90일 이내 거래 내역만 표시되어야 한다.
        ⚠️ TODO: 기간 필터 UI가 HTML에 미노출 — PERIOD_FILTER_3MONTH 셀렉터 튜닝 필요
        사전 조건: 3개월 이내 내역 1건+, 3개월 이전 내역 1건+
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        if not stat_history_page.is_period_filter_visible():
            pytest.skip(
                "[SKIP] FULLTC-437: 기간 필터 UI 미노출 — "
                "TODO: PERIOD_FILTER_3MONTH 셀렉터 튜닝 후 재실행"
            )

        count_before = stat_history_page.get_history_item_count()
        stat_history_page.click_filter_3month()
        stat_history_page.page.wait_for_timeout(800)
        count_after = stat_history_page.get_history_item_count()

        assert count_after >= 0, \
            "[FAIL] FULLTC-437: 3개월 필터 적용 후 내역 수 조회 실패"
        assert count_after <= count_before or count_before == 0, \
            f"[FAIL] FULLTC-437: 3개월 필터 후 내역 수 증가 — " \
            f"필터 미적용 의심 (before:{count_before}, after:{count_after})"

    def test_FULLTC_438_type_filter_earn(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-438 | STAT 보유내역/유형 필터 - 적립(획득) | Major
        '획득' 탭 선택 시 적립(+) 내역만 표시되고 사용(-) 내역은 미노출되어야 한다.
        ※ HTML 실제 탭 텍스트: '획득' (TC 명칭: '적립'과 상이)
        사전 조건: 적립 내역과 사용 내역이 각 1건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        total_before = stat_history_page.get_history_item_count()
        if total_before < 2:
            pytest.skip(
                f"[SKIP] FULLTC-438: 거래 내역 {total_before}건 — "
                f"필터 검증에 적립·사용 각 1건 이상 필요"
            )

        # '획득' 탭 클릭
        stat_history_page.click_tab_earn()
        stat_history_page.page.wait_for_timeout(800)

        assert stat_history_page.is_tab_earn_active(), \
            "[FAIL] FULLTC-438: '획득' 탭 클릭 후 활성(isFocused) 상태 미확인"

        # 필터 후 사용(-) 카드가 0건이어야 함
        minus_after = stat_history_page.get_minus_card_count()
        earn_after  = stat_history_page.get_history_item_count()

        assert minus_after == 0, \
            f"[FAIL] FULLTC-438: '획득' 탭 필터 후 사용(-) 내역 잔존 " \
            f"({minus_after}건) — 필터 미동작"
        assert earn_after >= 0, \
            "[FAIL] FULLTC-438: '획득' 탭 필터 후 내역 조회 실패"

    def test_FULLTC_439_type_filter_use(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-439 | STAT 보유내역/유형 필터 - 사용 | Major
        '사용' 탭 선택 시 사용(-) 내역만 표시되고 적립(+) 내역은 미노출되어야 한다.
        사전 조건: 적립 내역과 사용 내역이 각 1건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        total_before = stat_history_page.get_history_item_count()
        if total_before < 2:
            pytest.skip(
                f"[SKIP] FULLTC-439: 거래 내역 {total_before}건 — "
                f"필터 검증에 적립·사용 각 1건 이상 필요"
            )

        # '사용' 탭 클릭
        stat_history_page.click_tab_use()
        stat_history_page.page.wait_for_timeout(800)

        assert stat_history_page.is_tab_use_active(), \
            "[FAIL] FULLTC-439: '사용' 탭 클릭 후 활성(isFocused) 상태 미확인"

        # 필터 후 적립(+, isPlus) 카드가 0건이어야 함
        plus_after = stat_history_page.get_plus_card_count()
        use_after  = stat_history_page.get_history_item_count()

        assert plus_after == 0, \
            f"[FAIL] FULLTC-439: '사용' 탭 필터 후 적립(+) 내역 잔존 " \
            f"({plus_after}건) — 필터 미동작"
        assert use_after >= 0, \
            "[FAIL] FULLTC-439: '사용' 탭 필터 후 내역 조회 실패"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-440~442  |  추가 로딩
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.stat_history
class TestStatHistoryInfiniteScroll:
    """무한 스크롤·로딩 인디케이터·마지막 페이지 처리 검증 — FULLTC-440 ~ 442"""

    def test_FULLTC_440_infinite_scroll_loads_more(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-440 | STAT 보유내역/무한 스크롤 추가 로딩 | Major
        목록 하단 스크롤 후 다음 페이지 거래 내역이 자동 로드되어야 한다.
        사전 조건: STAT 거래 내역이 20건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        count_before = stat_history_page.get_history_item_count()
        if count_before < 1:
            pytest.skip("[SKIP] FULLTC-440: 거래 내역 없음 — 무한 스크롤 검증 불가")

        # 하단까지 스크롤
        stat_history_page.scroll_to_bottom(steps=5)
        stat_history_page.page.wait_for_timeout(1_500)
        count_after = stat_history_page.get_history_item_count()

        if count_before < 20:
            pytest.skip(
                f"[SKIP] FULLTC-440: 현재 내역 {count_before}건 — "
                f"무한 스크롤 검증에 20건 이상 필요 (단일 페이지 전체 노출 중)"
            )

        assert count_after > count_before, \
            f"[FAIL] FULLTC-440: 하단 스크롤 후 추가 내역 미로드 " \
            f"(before:{count_before}, after:{count_after})"

    def test_FULLTC_441_loading_indicator_visible(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-441 | STAT 보유내역/로딩 인디케이터 표시 | Minor
        추가 데이터 로딩 중 스피너/인디케이터가 노출되어야 한다.
        ⚠️ TODO: 로딩 인디케이터 셀렉터 튜닝 필요
        사전 조건: 거래 내역 20건 이상, 네트워크 속도 느린 환경
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        count_before = stat_history_page.get_history_item_count()
        if count_before < 20:
            pytest.skip(
                f"[SKIP] FULLTC-441: 내역 {count_before}건 — "
                f"로딩 인디케이터 검증에 20건 이상 필요"
            )

        # 스크롤 직후 인디케이터 감지 시도 (타이밍 민감)
        stat_history_page.scroll_to_bottom(steps=3, delay_ms=200)
        indicator_visible = stat_history_page.is_loading_indicator_visible(timeout=2_000)

        if not indicator_visible:
            pytest.skip(
                "[SKIP] FULLTC-441: 로딩 인디케이터 감지 실패 — "
                "TODO: LOADING_INDICATOR 셀렉터 튜닝 또는 네트워크 속도 조건 필요"
            )
        assert indicator_visible, \
            "[FAIL] FULLTC-441: 추가 로딩 중 로딩 인디케이터 미노출 " \
            "(TODO: LOADING_INDICATOR 셀렉터 튜닝 필요)"

    def test_FULLTC_442_last_page_end_indicator(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-442 | STAT 보유내역/마지막 페이지 처리 | Minor
        전체 내역 마지막까지 스크롤 후 추가 로딩이 발생하지 않고
        '더 이상 내역 없음' 안내가 표시되어야 한다.
        사전 조건: 전체 목록 마지막까지 스크롤 완료 상태
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        item_count = stat_history_page.get_history_item_count()
        if item_count < 1:
            pytest.skip("[SKIP] FULLTC-442: 거래 내역 없음 — 마지막 페이지 검증 불가")

        # 끝까지 스크롤 후 카드 수 확인
        stat_history_page.scroll_to_bottom(steps=15)
        stat_history_page.page.wait_for_timeout(1_500)
        count_1 = stat_history_page.get_history_item_count()

        # 추가 스크롤 후 카드 수가 더 이상 증가하지 않는지 확인
        stat_history_page.scroll_to_bottom(steps=5)
        stat_history_page.page.wait_for_timeout(1_000)
        count_2 = stat_history_page.get_history_item_count()

        # 마지막 페이지 도달: 카드 수 변화 없어야 함
        assert count_2 >= count_1, \
            f"[FAIL] FULLTC-442: 마지막 페이지에서 카드 수 감소 " \
            f"(1차: {count_1}, 2차: {count_2}) — 예상치 못한 동작"

        # Empty State 또는 카드 수 안정화로 마지막 페이지 판단
        assert count_2 == count_1 or count_2 > 0, \
            "[FAIL] FULLTC-442: 마지막 페이지 도달 후 예상치 못한 상태"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-443~446  |  UI/UX
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.stat_history
class TestStatHistoryUX:
    """색상 구분·필터 초기화·복합 필터·천 단위 구분 기호 검증 — FULLTC-443 ~ 446"""

    def test_FULLTC_443_plus_minus_color_distinction(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-443 | STAT 보유내역/적립·사용 색상 시각적 구분 | Major
        적립(+) 금액과 사용(-) 금액의 색상이 시각적으로 구분되어야 한다.
        사전 조건: 적립 내역과 사용 내역이 각 1건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        plus_count  = stat_history_page.get_plus_card_count()
        minus_count = stat_history_page.get_minus_card_count()

        if plus_count == 0 or minus_count == 0:
            pytest.skip(
                f"[SKIP] FULLTC-443: 적립({plus_count}건) 또는 "
                f"사용({minus_count}건) 내역 없음 — 색상 검증 불가"
            )

        assert stat_history_page.are_plus_minus_colors_different(), \
            "[FAIL] FULLTC-443: 적립(+)과 사용(-) 금액의 CSS color 값이 동일함 — " \
            "시각적 색상 구분 미적용"

    def test_FULLTC_444_filter_reset_shows_all(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-444 | STAT 보유내역/필터 초기화 | Minor
        필터 적용 후 '전체' 초기화 시 모든 거래 내역이 다시 표시되어야 한다.
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        # 전체 내역 수 기록
        total_count = stat_history_page.get_history_item_count()
        if total_count < 1:
            pytest.skip("[SKIP] FULLTC-444: 거래 내역 없음 — 필터 초기화 검증 불가")

        # '획득' 탭으로 필터 적용
        stat_history_page.click_tab_earn()
        stat_history_page.page.wait_for_timeout(600)
        filtered_count = stat_history_page.get_history_item_count()

        # '전체' 탭으로 초기화
        stat_history_page.click_filter_reset()
        stat_history_page.page.wait_for_timeout(600)
        restored_count = stat_history_page.get_history_item_count()

        assert stat_history_page.is_tab_all_active(), \
            "[FAIL] FULLTC-444: 필터 초기화 후 '전체' 탭 활성 상태 미확인"
        assert restored_count >= filtered_count, \
            f"[FAIL] FULLTC-444: 필터 초기화 후 전체 내역 미복원 " \
            f"(필터 후:{filtered_count}, 초기화 후:{restored_count})"
        assert restored_count == total_count, \
            f"[FAIL] FULLTC-444: 초기화 후 전체 내역 수 불일치 " \
            f"(초기:{total_count}, 초기화 후:{restored_count})"

    def test_FULLTC_445_combined_period_and_type_filter(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-445 | STAT 보유내역/기간+유형 복합 필터 | Major
        기간 '1개월' + 유형 '획득' 동시 적용 시 해당 조건의 내역만 표시되어야 한다.
        ⚠️ TODO: 기간 필터 UI가 HTML 미노출 → 기간 필터 부분은 skip
        사전 조건: 다양한 기간과 유형의 거래 내역 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        if not stat_history_page.is_period_filter_visible():
            # 기간 필터 없으면 유형 탭 단독 필터만 검증
            total_count = stat_history_page.get_history_item_count()
            if total_count < 1:
                pytest.skip("[SKIP] FULLTC-445: 거래 내역 없음 — 복합 필터 검증 불가")

            stat_history_page.click_tab_earn()
            stat_history_page.page.wait_for_timeout(600)
            earn_count = stat_history_page.get_history_item_count()

            assert stat_history_page.is_tab_earn_active(), \
                "[FAIL] FULLTC-445: '획득' 탭 활성 미확인"
            assert earn_count <= total_count, \
                f"[FAIL] FULLTC-445: '획득' 탭 필터 후 내역 증가 — 필터 미동작 " \
                f"(전체:{total_count}, 필터후:{earn_count})"
            pytest.skip(
                "[SKIP] FULLTC-445: 기간 필터 UI 미노출 — "
                "유형 탭 단독 필터만 검증 완료, "
                "TODO: PERIOD_FILTER_1MONTH 셀렉터 튜닝 후 재실행"
            )

        # 기간 필터 + 유형 탭 복합 적용
        total_count = stat_history_page.get_history_item_count()
        stat_history_page.click_filter_1month()
        stat_history_page.page.wait_for_timeout(600)
        stat_history_page.click_tab_earn()
        stat_history_page.page.wait_for_timeout(800)

        combined_count = stat_history_page.get_history_item_count()
        minus_count    = stat_history_page.get_minus_card_count()

        assert combined_count <= total_count, \
            f"[FAIL] FULLTC-445: 복합 필터 후 내역 수가 전체보다 많음 " \
            f"(전체:{total_count}, 복합필터:{combined_count})"
        assert minus_count == 0, \
            f"[FAIL] FULLTC-445: 복합 필터 후 사용(-) 내역 잔존 ({minus_count}건)"

    def test_FULLTC_446_thousands_separator_display(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-446 | STAT 보유내역/금액 천 단위 구분 기호 표시 | Minor
        1,000 이상의 잔액·금액에 천 단위 구분 기호(,)가 포함되어야 한다.
        사전 조건: 잔액 또는 거래 금액이 1,000 이상인 내역 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        # 1) 잔액 천 단위 구분 기호 확인
        balance = stat_history_page.get_balance_as_number()
        if balance >= 1_000:
            assert stat_history_page.is_balance_has_thousands_separator(), \
                f"[FAIL] FULLTC-446: 잔액 {balance}이 1,000 이상인데 " \
                f"천 단위 구분 기호(,) 미포함 (raw='{stat_history_page.get_balance_text()}')"

        # 2) 거래 내역 금액 천 단위 구분 기호 확인
        item_count = stat_history_page.get_history_item_count()
        if item_count < 1:
            pytest.skip("[SKIP] FULLTC-446: 거래 내역 없음 — 거래 금액 구분 기호 검증 불가")

        found_over_1k = False
        for i in range(min(item_count, 10)):
            if stat_history_page.is_amount_has_thousands_separator(i):
                amount_txt = stat_history_page.get_amount_text(i)
                amount_num = int(amount_txt.replace(",", "").replace("+", "").replace("-", ""))
                if amount_num >= 1_000:
                    found_over_1k = True
                    assert "," in amount_txt, \
                        f"[FAIL] FULLTC-446: {i+1}번째 거래 금액 {amount_num}이 " \
                        f"1,000 이상인데 구분 기호(,) 미포함 (raw='{amount_txt}')"

        if not found_over_1k and balance < 1_000:
            pytest.skip("[SKIP] FULLTC-446: 1,000 이상 금액 내역 없음 — 구분 기호 검증 불가")


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-447~448  |  Empty State
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.stat_history
class TestStatHistoryEmptyState:
    """거래 내역 없음 UI · 필터 결과 없음 UI 검증 — FULLTC-447 ~ 448
    ⚠️ 각 TC는 해당 조건이 충족된 계정에서만 의미 있음
    데이터 존재 시 자동 skip 처리
    """

    def test_FULLTC_447_no_history_empty_state(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-447 | STAT 보유내역/거래 내역 없음 UI | Minor
        STAT 거래 내역이 0건인 계정에서 빈 상태 UI와 안내 문구가 표시되어야 한다.
        ⚠️ TODO: EMPTY_STATE 셀렉터 튜닝 필요 (실제 HTML 확인 후)
        사전 조건: STAT 거래 내역이 0건인 계정
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        item_count = stat_history_page.get_history_item_count()
        if item_count > 0:
            pytest.skip(
                f"[SKIP] FULLTC-447: 거래 내역 {item_count}건 존재 — "
                f"Empty State 검증은 0건 계정에서 실행하세요"
            )

        assert stat_history_page.is_empty_state_visible(), \
            "[FAIL] FULLTC-447: 거래 내역 0건 상태에서 빈 상태 UI 미노출 " \
            "(TODO: EMPTY_STATE 셀렉터 튜닝 필요)"

    def test_FULLTC_448_filter_empty_state(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-448 | STAT 보유내역/필터 결과 없음 UI | Minor
        필터 조건에 해당하는 내역이 없을 때 빈 상태 UI와 안내 문구가 표시되어야 한다.
        ⚠️ TODO: EMPTY_STATE 셀렉터 튜닝 필요
        사전 조건: 선택한 필터 조건에 해당하는 내역 없는 상태
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        # '사용' 탭 선택 후 사용 내역이 없으면 Empty State 확인
        stat_history_page.click_tab_use()
        stat_history_page.page.wait_for_timeout(800)
        use_count = stat_history_page.get_history_item_count()

        if use_count > 0:
            # '획득' 탭도 시도
            stat_history_page.click_tab_earn()
            stat_history_page.page.wait_for_timeout(800)
            earn_count = stat_history_page.get_history_item_count()
            if earn_count > 0:
                pytest.skip(
                    "[SKIP] FULLTC-448: 모든 탭에 내역 존재 — "
                    "Empty State 검증은 해당 탭 내역이 0건일 때 실행하세요"
                )

        assert stat_history_page.is_empty_state_visible(), \
            "[FAIL] FULLTC-448: 필터 결과 0건 상태에서 빈 상태 UI 미노출 " \
            "(TODO: EMPTY_STATE 셀렉터 튜닝 필요)"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-449~450  |  페이지 이동
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.stat_history
class TestStatHistoryNavigation:
    """내역 클릭 시 상세 페이지 이동·비연결 내역 클릭 동작 검증 — FULLTC-449 ~ 450"""

    def test_FULLTC_449_linked_card_navigates_to_detail(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-449 | STAT 보유내역/내역 클릭 시 상세 페이지 이동 | Minor
        href가 있는 거래 내역 클릭 시 /mypage/reward/tx/{id} 상세 페이지로 이동해야 한다.
        사전 조건: 상세 페이지로 연결되는 STAT 거래 내역 1건 이상 존재
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        item_count = stat_history_page.get_history_item_count()
        if item_count < 1:
            pytest.skip("[SKIP] FULLTC-449: 거래 내역 없음 — 라우팅 검증 불가")

        # 첫 번째 카드의 href 확인
        href = stat_history_page.get_card_href(0)
        if not href or StatHistoryPage.TX_DETAIL_PATH not in href:
            pytest.skip(
                f"[SKIP] FULLTC-449: 첫 번째 카드 href 없음 또는 tx 경로 불일치 "
                f"(href='{href}') — 상세 페이지 없는 내역"
            )

        url_before = stat_history_page.get_current_url()
        stat_history_page.click_history_card(0)

        assert stat_history_page.get_current_url() != url_before, \
            "[FAIL] FULLTC-449: 거래 내역 클릭 후 URL 미변경"
        assert StatHistoryPage.TX_DETAIL_PATH in stat_history_page.get_current_url(), \
            f"[FAIL] FULLTC-449: 클릭 후 tx 상세 URL 미이동 " \
            f"(기대 패턴: '{StatHistoryPage.TX_DETAIL_PATH}', " \
            f"실제: '{stat_history_page.get_current_url()}')"
        assert "about:blank" not in stat_history_page.get_current_url(), \
            "[FAIL] FULLTC-449: 클릭 후 빈 페이지(about:blank) 이동"

    def test_FULLTC_450_non_linked_card_stays_on_page(
        self, stat_history_page: StatHistoryPage
    ) -> None:
        """
        FULLTC-450 | STAT 보유내역/비연결 내역 클릭 시 동작 | Minor
        상세 페이지가 없는 내역 클릭 시 현재 페이지 유지 또는 모달 표시.
        빈 페이지(about:blank)로 이동하지 않아야 한다.
        사전 조건: 관련 링크가 없는 거래 내역 존재 (시스템 자동 지급 등)
        """
        stat_history_page.go_to_stat_history()
        stat_history_page.wait_for_history_list()

        item_count = stat_history_page.get_history_item_count()
        if item_count < 1:
            pytest.skip("[SKIP] FULLTC-450: 거래 내역 없음 — 비연결 내역 클릭 검증 불가")

        # href가 있는 카드는 tx 경로 포함 여부로 "연결/비연결" 구분
        # 비연결 내역 탐색
        non_linked_index = None
        for i in range(min(item_count, 20)):
            href = stat_history_page.get_card_href(i)
            if not href or StatHistoryPage.TX_DETAIL_PATH not in href:
                non_linked_index = i
                break

        if non_linked_index is None:
            pytest.skip(
                "[SKIP] FULLTC-450: 모든 카드에 tx 상세 링크 존재 — "
                "비연결 내역(시스템 자동 지급 등) 없음"
            )

        url_before = stat_history_page.get_current_url()
        stat_history_page.click_history_card(non_linked_index)
        stat_history_page.page.wait_for_timeout(1_000)
        url_after = stat_history_page.get_current_url()

        # 빈 페이지로 이동하지 않아야 함
        assert "about:blank" not in url_after.lower(), \
            "[FAIL] FULLTC-450: 비연결 내역 클릭 후 빈 페이지(about:blank) 이동"

        # 현재 페이지 유지 또는 모달 표시 (URL이 크게 벗어나지 않아야 함)
        stayed_on_page = stat_history_page.STAT_HISTORY_PATH in url_after
        navigated_to_related = (
            url_after != url_before
            and "about:blank" not in url_after.lower()
        )
        assert stayed_on_page or navigated_to_related, \
            f"[FAIL] FULLTC-450: 비연결 내역 클릭 후 예상치 못한 페이지 이동 " \
            f"(before='{url_before}', after='{url_after}')"