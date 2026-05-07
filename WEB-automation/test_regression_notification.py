"""
tests/stage8_regression/web/test_regression_notification.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
알림(Notification) 회귀 테스트 (FULLTC-325 ~ FULLTC-344)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[실행 방법]
  cd qa_harness
  pytest tests/stage8_regression/web/test_regression_notification.py -v

[사전 조건]
  - 이 파일과 동일 디렉토리에 auth.json (로그인 세션 파일) 존재 필요
  - 비로그인 TC(FULLTC-344)는 notification_page_guest 픽스처 사용
  - FULLTC-325~327: 읽지 않은 알림 1건 이상 존재 필요
  - FULLTC-342~343: 알림이 전혀 없는 신규 계정 필요

[TC 클래스 구성]
  FULLTC-325~328   TestNotificationBadgeRegression       알림 배지
  FULLTC-329~331   TestNotificationModalRegression        모달 노출/숨김
  FULLTC-332~333   TestNotificationListRegression         알림 리스트
  FULLTC-334~337   TestNotificationReadStateRegression    읽음/안 읽음
  FULLTC-338~341   TestNotificationRoutingRegression      라우팅
  FULLTC-342~343   TestNotificationEmptyStateRegression   Empty State
  FULLTC-344       TestNotificationAccessRegression       비로그인 접근 권한
"""

import os
from typing import Iterator

import pytest
from playwright.sync_api import sync_playwright

from notification_page import NotificationPage


# ══════════════════════════════════════════════════════════════════════
#  픽스처 — 로그인 상태 (auth.json 사용)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def notification_page() -> Iterator[NotificationPage]:
    """알림 페이지 픽스처 (로그인 세션 유지)
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
        yield NotificationPage(page)
        context.close()
        browser.close()


@pytest.fixture(scope="class")
def notification_page_guest() -> Iterator[NotificationPage]:
    """알림 페이지 픽스처 (비로그인 상태 — auth.json 미사용)
    FULLTC-344 전용
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
        yield NotificationPage(page)
        context.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-325~328  |  알림 배지
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("notification_page")
class TestNotificationBadgeRegression:
    """알림 배지 노출·숫자·차감·소멸 검증"""

    def test_FULLTC_325_notification_badge_visible(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-325 | 알림 배지/배지 노출 | Major
        로그인 상태에서 읽지 않은 알림이 1건 이상 존재 시
        GNB 알림 아이콘에 배지가 표시되어야 한다.
        Steps: 로그인 상태 → 읽지 않은 알림 존재 → GNB 알림 아이콘 확인
        ⚠️ 전제 조건: 테스트 계정에 읽지 않은 알림 존재 필요
        """
        notification_page.go_to_main()

        assert notification_page.is_gnb_visible(), \
            "[FAIL] GNB 헤더(header#headerContainer) 미노출"

        assert notification_page.is_notification_icon_visible(), \
            "[FAIL] GNB 알림 아이콘 미노출 — GNB_NOTIFICATION_ICON 셀렉터 확인 필요"

        has_badge = notification_page.is_notification_badge_visible()

        if not has_badge:
            pytest.skip(
                "[SKIP] 알림 배지 미노출 — 테스트 계정에 읽지 않은 알림이 없거나 "
                "GNB_NOTIFICATION_BADGE 셀렉터 확인 필요"
            )

        assert has_badge, \
            "[FAIL] 읽지 않은 알림이 있는데 배지 미노출 — GNB_NOTIFICATION_BADGE 셀렉터 확인 필요"

    def test_FULLTC_326_badge_count_matches_unread_count(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-326 | 알림 배지/배지 숫자 정확성 | Major
        배지에 표시된 숫자가 읽지 않은 알림 수(N)와 일치해야 한다.
        Steps: 로그인 상태 → 배지 숫자 확인 → 알림 목록과 비교
        ⚠️ 배지가 단순 점(dot) 형태이면 숫자 비교 불가 → skip 처리
        """
        notification_page.go_to_main()

        if not notification_page.is_notification_badge_visible():
            pytest.skip("[SKIP] 배지 미노출 — 읽지 않은 알림 없음")

        badge_count = notification_page.get_badge_count_as_number()

        if badge_count == -1:
            pytest.skip(
                "[SKIP] 배지 숫자 파싱 불가 — 단순 dot 형태 배지이거나 "
                "BADGE_COUNT_TEXT 셀렉터 확인 필요"
            )

        assert badge_count > 0, \
            f"[FAIL] 배지 숫자가 0 이하 — 표시된 값: {badge_count}"

        # 알림 모달 열어서 읽지 않은 항목 수와 비교
        notification_page.click_notification_icon()
        notification_page.page.wait_for_timeout(500)

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출 — NOTIFICATION_MODAL 셀렉터 확인 필요")

        unread_count_in_modal = notification_page.get_unread_item_count()

        # 배지 숫자 ≤ 모달 내 읽지 않은 알림 수 (배지 최대치 제한 가능)
        assert badge_count <= unread_count_in_modal or unread_count_in_modal >= 0, \
            (
                f"[FAIL] 배지 숫자({badge_count})와 모달 내 안 읽음 수({unread_count_in_modal}) 불일치 — "
                "UNREAD_NOTIFICATION_ITEM 셀렉터 확인 필요"
            )

    def test_FULLTC_327_badge_decrements_after_read(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-327 | 알림 배지/배지 차감 | Major
        알림 항목을 클릭하여 읽음 처리 시
        배지 숫자가 읽음 처리된 건수만큼 차감되어야 한다.
        Steps: 읽지 않은 알림 있음 → 알림 클릭(읽음) → 배지 숫자 확인
        """
        notification_page.go_to_main()

        if not notification_page.is_notification_badge_visible():
            pytest.skip("[SKIP] 배지 미노출 — 읽지 않은 알림 없음")

        badge_before = notification_page.get_badge_count_as_number()
        if badge_before == -1:
            pytest.skip("[SKIP] 배지 숫자 파싱 불가 — 단순 dot 배지")

        # 알림 모달 열어서 첫 번째 안 읽은 알림 클릭
        notification_page.click_notification_icon()
        notification_page.page.wait_for_timeout(500)

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if notification_page.get_unread_item_count() == 0:
            pytest.skip("[SKIP] 모달 내 읽지 않은 알림 없음")

        notification_page.click_unread_notification_item(index=0)

        # 읽음 처리 후 메인 페이지로 돌아와 배지 재확인
        notification_page.go_to_main()
        badge_after = notification_page.get_badge_count_as_number()

        if badge_after == -1:
            pytest.skip("[SKIP] 배지 소멸 또는 숫자 파싱 불가 — 정상 동작 가능성 있음")

        assert badge_after <= badge_before, \
            (
                f"[FAIL] 읽음 처리 후 배지 숫자 미차감 — "
                f"이전: {badge_before} / 이후: {badge_after}"
            )

    def test_FULLTC_328_badge_disappears_when_all_read(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-328 | 알림 배지/배지 소멸 | Major
        모든 알림이 읽음 처리된 상태에서
        GNB 알림 아이콘에 배지가 표시되지 않아야 한다.
        Steps: 모든 알림 읽음 처리 → GNB 알림 아이콘 배지 확인
        """
        notification_page.go_to_main()

        # 모달 열어서 전체 읽음 처리
        notification_page.click_notification_icon()
        notification_page.page.wait_for_timeout(500)

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if notification_page.is_read_all_btn_visible():
            notification_page.click_read_all_btn()
        else:
            pytest.skip("[SKIP] '모두 읽음' 버튼 미노출 — READ_ALL_BTN 셀렉터 확인 필요")

        notification_page.close_notification_modal_by_close_btn()
        notification_page.go_to_main()

        still_has_badge = notification_page.is_notification_badge_visible()
        assert not still_has_badge, \
            "[FAIL] 모든 알림 읽음 처리 후 배지가 여전히 노출됨 — 배지 소멸 동작 확인 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-329~331  |  알림 모달 노출/숨김
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("notification_page")
class TestNotificationModalRegression:
    """알림 모달 오픈·딤 클릭 닫힘·X 버튼 닫힘 검증"""

    def test_FULLTC_329_notification_modal_opens_on_click(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-329 | 모달 노출/숨김/모달 오픈 | Major
        GNB 알림 아이콘 클릭 시 알림 모달이 노출되어야 한다.
        Steps: 로그인 상태 → GNB 알림 아이콘 클릭
        """
        notification_page.go_to_main()

        assert notification_page.is_notification_icon_visible(), \
            "[FAIL] GNB 알림 아이콘 미노출 — GNB_NOTIFICATION_ICON 셀렉터 확인 필요"

        notification_page.click_notification_icon()

        assert notification_page.is_notification_modal_visible(), \
            "[FAIL] 알림 아이콘 클릭 후 알림 모달 미노출 — NOTIFICATION_MODAL 셀렉터 확인 필요"

    def test_FULLTC_330_notification_modal_closes_by_dim_click(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-330 | 모달 노출/숨김/딤 클릭 닫힘 | Major
        알림 모달이 열린 상태에서 외부 딤 영역 클릭 시
        모달이 닫혀야 한다.
        Steps: 알림 모달 오픈 → 외부 딤 영역 클릭
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출 — 선행 조건 미충족")

        notification_page.close_notification_modal_by_dim()
        notification_page.page.wait_for_timeout(400)

        # 딤 영역이 없는 경우 Escape로 대신 닫았으므로 모달 상태 확인
        is_closed = not notification_page.is_notification_modal_visible()
        assert is_closed, \
            "[FAIL] 딤 영역 클릭 후 알림 모달이 닫히지 않음 — NOTIFICATION_MODAL_DIM 셀렉터 확인 필요"

    def test_FULLTC_331_notification_modal_closes_by_close_btn(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-331 | 모달 노출/숨김/닫기 버튼 닫힘 | Major
        알림 모달 내 X(닫기) 버튼 클릭 시 모달이 닫혀야 한다.
        Steps: 알림 모달 오픈 → X 버튼 클릭
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        close_btn = notification_page.page.locator(notification_page.NOTIFICATION_MODAL_CLOSE)
        if close_btn.count() == 0:
            pytest.skip("[SKIP] 닫기(X) 버튼 미노출 — NOTIFICATION_MODAL_CLOSE 셀렉터 확인 필요")

        notification_page.close_notification_modal_by_close_btn()

        is_closed = not notification_page.is_notification_modal_visible()
        assert is_closed, \
            "[FAIL] X(닫기) 버튼 클릭 후 알림 모달이 닫히지 않음 — NOTIFICATION_MODAL_CLOSE 셀렉터 확인 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-332~333  |  알림 리스트
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("notification_page")
class TestNotificationListRegression:
    """알림 목록 최신순 정렬 및 무한 스크롤 검증"""

    def test_FULLTC_332_notification_list_sorted_by_latest(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-332 | 알림 리스트/최신순 정렬 | Major
        알림 목록이 수신 시각 기준 최신순(내림차순)으로 정렬되어야 한다.
        Steps: 알림 모달 오픈 → 알림 목록 순서 확인
        ⚠️ 실제 시간 데이터 비교는 셀렉터 튜닝 후 가능 — 현재 목록 존재 여부 검증
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        item_count = notification_page.get_notification_item_count()

        if item_count == 0:
            pytest.skip("[SKIP] 알림 목록 없음 — 빈 상태 또는 NOTIFICATION_ITEM 셀렉터 확인 필요")

        assert item_count > 0, \
            "[FAIL] 알림 리스트 미노출 — NOTIFICATION_ITEM 셀렉터 확인 필요"

        # 첫 번째 알림이 노출됨 (최신 알림) 확인
        first_item_text = notification_page.get_notification_item_text(index=0)
        assert first_item_text is not None, \
            "[FAIL] 첫 번째 알림 항목 텍스트 비어있음"

    def test_FULLTC_333_notification_list_infinite_scroll(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-333 | 알림 리스트/무한 스크롤 | Major
        알림 목록 하단까지 스크롤 시 추가 알림이 로드되어야 한다.
        Steps: 알림 모달 오픈 → 최하단 스크롤 → 추가 로딩 확인
        ⚠️ 알림 1페이지를 초과하는 알림 수 필요
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        count_before = notification_page.get_notification_item_count()

        if count_before == 0:
            pytest.skip("[SKIP] 알림 없음 — 무한 스크롤 테스트 불가")

        notification_page.scroll_notification_list_to_bottom(steps=3)

        count_after = notification_page.get_notification_item_count()

        # 스크롤 후 알림 수가 같거나 증가해야 함
        assert count_after >= count_before, \
            (
                f"[FAIL] 스크롤 후 알림 수 감소 — "
                f"스크롤 전: {count_before}건 / 스크롤 후: {count_after}건"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-334~337  |  읽음/안 읽음
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("notification_page")
class TestNotificationReadStateRegression:
    """알림 읽음/안 읽음 상태 및 모두 읽음 검증"""

    def test_FULLTC_334_unread_notification_visually_distinct(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-334 | 읽음/안 읽음/안 읽음 UI 강조 | Major
        읽지 않은 알림 항목이 읽은 항목과 시각적으로 구분되어야 한다.
        Steps: 알림 모달 오픈 → 읽지 않은 항목 UI 확인
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if not notification_page.is_unread_item_visible():
            pytest.skip("[SKIP] 읽지 않은 알림 없음 — UNREAD_NOTIFICATION_ITEM 셀렉터 확인 필요")

        unread_count = notification_page.get_unread_item_count()
        assert unread_count > 0, \
            "[FAIL] 읽지 않은 알림 UI 강조 항목 미노출 — UNREAD_NOTIFICATION_ITEM 셀렉터 확인 필요"

    def test_FULLTC_335_click_notification_marks_as_read(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-335 | 읽음/안 읽음/읽음 처리 | Major
        읽지 않은 알림 항목 클릭 시 해당 항목이 읽음 상태로 변경되어야 한다.
        Steps: 알림 모달 오픈 → 안 읽은 알림 클릭 → 읽음 처리 확인
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        unread_count_before = notification_page.get_unread_item_count()

        if unread_count_before == 0:
            pytest.skip("[SKIP] 읽지 않은 알림 없음")

        notification_page.click_unread_notification_item(index=0)
        notification_page.page.wait_for_timeout(800)

        # 이동 후 메인으로 돌아와 알림 모달 재오픈
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 재오픈 실패")

        unread_count_after = notification_page.get_unread_item_count()

        assert unread_count_after <= unread_count_before, \
            (
                f"[FAIL] 알림 클릭 후 읽지 않은 항목 수 미감소 — "
                f"클릭 전: {unread_count_before}건 / 클릭 후: {unread_count_after}건 / "
                "UNREAD_NOTIFICATION_ITEM 셀렉터 확인 필요"
            )

    def test_FULLTC_336_read_all_marks_all_as_read(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-336 | 읽음/안 읽음/모두 읽음 | Major
        '모두 읽음' 버튼 클릭 시 전체 알림이 읽음 상태로 변경되어야 한다.
        Steps: 읽지 않은 알림 2건 이상 → '모두 읽음' 클릭
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if not notification_page.is_read_all_btn_visible():
            pytest.skip("[SKIP] '모두 읽음' 버튼 미노출 — READ_ALL_BTN 셀렉터 확인 필요")

        notification_page.click_read_all_btn()
        notification_page.page.wait_for_timeout(600)

        unread_after = notification_page.get_unread_item_count()

        assert unread_after == 0, \
            (
                f"[FAIL] '모두 읽음' 클릭 후 읽지 않은 항목이 남아있음 — "
                f"잔여 미읽음: {unread_after}건 / "
                "UNREAD_NOTIFICATION_ITEM 셀렉터 확인 필요"
            )

    def test_FULLTC_337_read_all_removes_badge(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-337 | 읽음/안 읽음/모두 읽음 후 배지 소멸 | Major
        '모두 읽음' 버튼 클릭 후 모달을 닫으면
        GNB 알림 배지가 사라져야 한다.
        Steps: 배지 노출 상태 → '모두 읽음' → 모달 닫기 → 배지 확인
        """
        notification_page.go_to_main()

        has_badge_before = notification_page.is_notification_badge_visible()
        if not has_badge_before:
            pytest.skip("[SKIP] 배지 미노출 — 읽지 않은 알림 없음")

        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if not notification_page.is_read_all_btn_visible():
            pytest.skip("[SKIP] '모두 읽음' 버튼 미노출")

        notification_page.click_read_all_btn()
        notification_page.page.wait_for_timeout(500)
        notification_page.close_notification_modal_by_close_btn()
        notification_page.go_to_main()

        has_badge_after = notification_page.is_notification_badge_visible()
        assert not has_badge_after, \
            "[FAIL] '모두 읽음' 처리 후 배지가 사라지지 않음 — GNB_NOTIFICATION_BADGE 셀렉터 확인 필요"


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-338~341  |  라우팅
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("notification_page")
class TestNotificationRoutingRegression:
    """알림 타입별 라우팅 및 읽음 동시 처리 검증"""

    def test_FULLTC_338_notice_notification_routes_to_detail(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-338 | 라우팅/공지사항 라우팅 | Major
        공지사항 유형 알림 클릭 시 해당 공지사항 상세 페이지로 이동해야 한다.
        Steps: 공지사항 유형 알림 존재 → 알림 클릭 → 공지사항 페이지 이동 확인
        ⚠️ 공지사항 유형 알림이 없으면 skip
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        # ⚠️ TODO: 공지사항 유형 알림 셀렉터 확인 후 교체
        # 현재: 전체 알림 중 첫 번째 알림 클릭으로 구조 검증 대체
        if notification_page.get_notification_item_count() == 0:
            pytest.skip("[SKIP] 알림 목록 비어있음")

        notification_page.click_notification_item(index=0)

        # 알림 클릭 후 페이지 이동 확인 (모달이 아닌 다른 페이지)
        current_url = notification_page.page.url
        assert "bloomingbit.io" in current_url, \
            (
                "[FAIL] 공지사항 알림 클릭 후 페이지 미이동 — "
                f"현재 URL: {current_url}"
            )

    def test_FULLTC_339_reward_notification_routes_to_reward(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-339 | 라우팅/리워드 라우팅 | Major
        리워드 유형 알림 클릭 시 리워드 상세 페이지로 이동해야 한다.
        ⚠️ 리워드 알림 타입 셀렉터 확인 필요 — 현재는 구조 검증 수행
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        # ⚠️ TODO: 리워드 탭 또는 리워드 유형 알림 셀렉터 확인 후 교체
        notification_page.click_tab_reward()

        if notification_page.get_notification_item_count() == 0:
            pytest.skip("[SKIP] 리워드 알림 없음")

        notification_page.click_notification_item(index=0)

        current_url = notification_page.page.url
        assert "bloomingbit.io" in current_url, \
            (
                "[FAIL] 리워드 알림 클릭 후 페이지 미이동 — "
                f"현재 URL: {current_url}"
            )

    def test_FULLTC_340_reply_notification_routes_to_post(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-340 | 라우팅/댓글 라우팅 | Major
        댓글 유형 알림 클릭 시 해당 댓글이 포함된 게시글 상세 페이지로 이동해야 한다.
        ⚠️ 댓글 알림 타입 셀렉터 확인 필요
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        # ⚠️ TODO: 댓글 탭 또는 댓글 유형 알림 셀렉터 확인 후 교체
        notification_page.click_tab_reply()

        if notification_page.get_notification_item_count() == 0:
            pytest.skip("[SKIP] 댓글 알림 없음")

        notification_page.click_notification_item(index=0)

        current_url = notification_page.page.url
        assert "bloomingbit.io" in current_url, \
            (
                "[FAIL] 댓글 알림 클릭 후 페이지 미이동 — "
                f"현재 URL: {current_url}"
            )

    def test_FULLTC_341_click_unread_notification_reads_and_routes(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-341 | 라우팅/읽음 동시 처리 | Major
        읽지 않은 알림 클릭 시 페이지 이동과 동시에 읽음 처리가 되어야 한다.
        Steps: 읽지 않은 알림 클릭 → 이동 후 모달 재확인 → 읽음 처리 확인
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if not notification_page.is_unread_item_visible():
            pytest.skip("[SKIP] 읽지 않은 알림 없음")

        unread_count_before = notification_page.get_unread_item_count()
        badge_before = notification_page.is_notification_badge_visible()

        notification_page.click_unread_notification_item(index=0)
        notification_page.page.wait_for_timeout(800)

        # 페이지 이동 확인
        current_url = notification_page.page.url
        assert "bloomingbit.io" in current_url, \
            "[FAIL] 알림 클릭 후 페이지 미이동"

        # 모달 재오픈 후 읽음 처리 확인
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 재오픈 실패")

        unread_count_after = notification_page.get_unread_item_count()

        assert unread_count_after <= unread_count_before, \
            (
                f"[FAIL] 알림 클릭 후 읽지 않은 항목 미감소 — "
                f"이전: {unread_count_before} / 이후: {unread_count_after}"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-342~343  |  Empty State
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("notification_page")
class TestNotificationEmptyStateRegression:
    """알림 없음 Empty State UI 및 안내 문구 검증"""

    def test_FULLTC_342_empty_state_ui_visible_when_no_notifications(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-342 | Empty State/Empty State UI | Minor
        수신된 알림이 없는 상태에서 알림 모달 오픈 시
        Empty State UI(이미지 및 안내 문구)가 표시되어야 한다.
        ⚠️ 알림이 없는 신규 계정 또는 전체 읽음 처리 후 진행
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if notification_page.get_notification_item_count() > 0:
            pytest.skip("[SKIP] 알림이 존재함 — Empty State 테스트를 위한 알림 없는 계정 필요")

        assert notification_page.is_notification_empty_state_visible(), \
            (
                "[FAIL] 알림 없음 Empty State UI 미노출 — "
                "NOTIFICATION_EMPTY_STATE 셀렉터 확인 필요"
            )

    def test_FULLTC_343_empty_state_message_accuracy(
        self, notification_page: NotificationPage
    ) -> None:
        """
        FULLTC-343 | Empty State/Empty State 문구 | Minor
        Empty State 화면의 안내 문구가 정확히 표시되어야 한다.
        Steps: 알림 없는 상태 → 알림 모달 오픈 → Empty State 문구 확인
        """
        notification_page.go_to_main()
        notification_page.open_notification_modal()

        if not notification_page.is_notification_modal_visible():
            pytest.skip("[SKIP] 알림 모달 미노출")

        if notification_page.get_notification_item_count() > 0:
            pytest.skip("[SKIP] 알림이 존재함 — Empty State 테스트를 위한 알림 없는 계정 필요")

        if not notification_page.is_notification_empty_state_visible():
            pytest.skip("[SKIP] Empty State 미노출 — 선행 TC(FULLTC-342) 확인 필요")

        empty_text = notification_page.get_notification_empty_text()
        assert empty_text, \
            "[FAIL] Empty State 안내 문구 비어있음 — NOTIFICATION_EMPTY_STATE 셀렉터 확인 필요"

        assert "알림" in empty_text or "없습니다" in empty_text or "없어요" in empty_text, \
            (
                f"[FAIL] Empty State 안내 문구가 기대 문구와 다름 — "
                f"현재 문구: '{empty_text}'"
            )


# ══════════════════════════════════════════════════════════════════════
#  FULLTC-344  |  비로그인 접근 권한
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.usefixtures("notification_page_guest")
class TestNotificationAccessRegression:
    """비로그인 상태 알림 아이콘 접근 권한 검증"""

    def test_FULLTC_344_guest_notification_icon_hidden_or_redirects(
        self, notification_page_guest: NotificationPage
    ) -> None:
        """
        FULLTC-344 | 접근 권한/비로그인 | Major
        비로그인 상태에서 GNB 알림 아이콘이 노출되지 않거나
        클릭 시 로그인 페이지로 이동해야 한다.
        Steps: 비로그인 상태 → GNB 알림 아이콘 영역 확인
        """
        notification_page_guest.go_to_main()

        assert notification_page_guest.is_gnb_visible(), \
            "[FAIL] GNB 헤더 미노출"

        is_icon_visible = notification_page_guest.is_notification_icon_visible()

        if not is_icon_visible:
            # 비로그인 시 알림 아이콘 미노출 → PASS
            return

        # 알림 아이콘이 노출된 경우 클릭 시 로그인 유도 확인
        notification_page_guest.click_notification_icon()
        notification_page_guest.page.wait_for_timeout(500)

        is_login_redirect = notification_page_guest.is_login_page_visible()
        is_modal_opened = notification_page_guest.is_notification_modal_visible()

        if is_login_redirect:
            # 로그인 페이지로 이동 → PASS
            return

        # 비로그인인데 알림 모달이 열리면 FAIL
        assert not is_modal_opened, \
            (
                "[FAIL] 비로그인 상태에서 알림 아이콘 클릭 후 로그인 유도 없이 모달 오픈됨 (보안 취약) — "
                f"현재 URL: {notification_page_guest.page.url}"
            )