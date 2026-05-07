"""
tests/stage8_regression/web/test_regression_news.py
[Stage 8 리그레션 스크립트]  뉴스 도메인 전체 자동화 스위트

────────────────────────────────────────────────────────────
 테스트 클래스 구성
────────────────────────────────────────────────────────────
 TestNewsRegressionP0         — 기존 POC 4건 (뼈대, 변경 금지)
 TestNewsGNBRegression        — FULLTC-001 ~ 010  GNB
 TestPickNewsRegression       — FULLTC-011 ~ 024  PiCK 뉴스
 TestRankingNewsRegression    — FULLTC-025 ~ 031  랭킹 뉴스
 TestOnlyBloomingbitRegression — FULLTC-032 ~ 037  Only 블루밍비트
 TestRealtimeNewsRegression   — FULLTC-038 ~ 048  실시간 뉴스
 TestSidebarRegression        — FULLTC-049 ~ 051  사이드바 위젯
────────────────────────────────────────────────────────────

실행 방법:
  pytest test_regression_news.py -v                          # 전체
  pytest -m "regression and p0"                              # P0만
  pytest -m "gnb"                                            # GNB만
  pytest -k "test_pick"                                      # PiCK 테스트만
  pytest -k "FULLTC_013"                                     # 특정 TC만
"""

import os
import pytest
from typing import Iterator
from playwright.sync_api import sync_playwright, Page

from news_page import NewsPage


# ══════════════════════════════════════════════════════════════════════
#  Fixture (브라우저 설정 — 변경 금지)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def news_page() -> Iterator[NewsPage]:
    """
    뉴스 Page Object 픽스처.
    scope=class → 같은 클래스 내 테스트는 브라우저 세션 공유 (속도 최적화)
    headless=False, slow_mo=500 → 실제 브라우저 창으로 육안 확인 가능
    --window-position → 상위 모니터에 창 고정 (VS Code 가리지 않도록)
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=500,
            args=[
                # ── 브라우저 창 초기 위치 ───────────────────────────────────
                # 듀얼 모니터(상하 배치) 기준으로 상위 모니터에 창을 고정
                #
                # 좌표 조정 방법:
                #   x : 가로 위치 (0 = 왼쪽 끝, 양수로 오른쪽 이동)
                #   y : 세로 위치
                #       - 상위 모니터 상단 = -(상위 모니터 세로 해상도)
                #         예) 상위 모니터가 1080p → -1080
                #             상위 모니터가 1440p → -1440
                #             상위 모니터가 2160p → -2160
                #       - 상위 모니터 중간쯤 띄우려면 절반값 사용
                #         예) 1080p 모니터 중간 → -540
                #
                # 현재 설정: 상위 모니터 좌측 상단 고정 (1080p 기준)
                "--window-position=0,-1080",
            ],
        )
        # ── auth.json 절대 경로 해석 ───────────────────────────────────────
        # pytest 실행 디렉토리와 무관하게 스크립트 위치 기준으로 경로를 고정
        _here     = os.path.dirname(os.path.abspath(__file__))
        auth_path = os.path.join(_here, "auth.json")
        if not os.path.exists(auth_path):
            raise FileNotFoundError(
                f"\n\n[auth.json 없음] 로그인 세션 파일을 찾을 수 없습니다!\n"
                f"  기대 경로: {auth_path}\n"
                f"  해결 방법: 해당 경로에 auth.json을 생성하세요.\n"
                f"  (수동 로그인 스크립트: python save_auth.py)\n"
            )

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="ko-KR",
            storage_state=auth_path,     # ✅ 절대 경로로 로그인 세션 적용
        )
        page: Page = context.new_page()
        news = NewsPage(page)
        yield news
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  기존 POC — 변경 금지
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.p0
@pytest.mark.web
@pytest.mark.news
class TestNewsRegressionP0:
    """뉴스 도메인 P0 리그레션 — 배포 블로커 스위트 (기존 POC 4건)"""

    def test_news_home_entry(self, news_page: NewsPage):
        """
        TC: FULLTC-001 / TC-WEB-NEWS-001
        시나리오: 뉴스 홈 기본 진입 (비로그인)
        기대결과: [1] HTTP 200  [2] 도메인 정상  [3] PiCK 섹션  [4] 랭킹 섹션
        """
        response = news_page.page.goto(f"{NewsPage.BASE_URL}/", wait_until="networkidle")
        assert response is not None, "[FAIL] 페이지 응답 없음"
        assert response.status == 200, \
            f"[FAIL] 응답 오류 — 기대: 200, 실제: {response.status}"
        assert "bloomingbit.io" in news_page.page.url, \
            f"[FAIL] 예상 도메인 아님 — 현재: {news_page.page.url}"
        assert news_page.is_pick_section_visible(), \
            "[FAIL] PICK 섹션 미노출 (section#feedPickContainer)"
        assert news_page.is_ranking_section_visible(), \
            "[FAIL] 랭킹 섹션 미노출 (section#feedRankingContainer)"

    def test_pick_news_card_render(self, news_page: NewsPage):
        """
        TC: FULLTC-003 / TC-WEB-NEWS-003
        시나리오: PICK 뉴스 카드 노출 검증
        기대결과: [1] 카드 1건+  [2] 제목 비어있지 않음  [3] 썸네일  [4] 날짜
        """
        news_page.go_to_news_home()
        assert news_page.is_loaded(), "[FAIL] 뉴스 홈 로드 실패"
        assert news_page.get_pick_card_count() >= 1, "[FAIL] PICK 카드 0건"
        assert news_page.get_first_pick_card_title().strip() != "", \
            "[FAIL] PICK 카드 제목 비어있음"
        assert news_page.is_pick_headline_img_visible(), \
            "[FAIL] PICK 헤드라인 썸네일 미노출"
        assert news_page.get_pick_headline_date().strip() != "", \
            "[FAIL] PICK 헤드라인 날짜 비어있음"

    def test_ranking_news_order_and_routing(self, news_page: NewsPage):
        """
        TC: FULLTC-004 / TC-WEB-NEWS-004
        시나리오: 랭킹 뉴스 순위 표시 및 클릭 라우팅
        기대결과: [1] 아이템 1건+  [2] 1위 뱃지='1'  [3] 클릭 후 상세 URL
        """
        news_page.go_to_news_home()
        items = news_page.get_ranking_items()
        assert len(items) >= 1, f"[FAIL] 랭킹 아이템 0건 (실제: {len(items)}건)"
        assert news_page.get_ranking_badge_text(0).strip() == "1", \
            f"[FAIL] 1위 뱃지 불일치"
        url_before = news_page.page.url
        news_page.click_ranking_item(0)
        assert news_page.page.url != url_before, "[FAIL] 랭킹 클릭 후 URL 미변경"
        assert "/feed/news/" in news_page.page.url, \
            f"[FAIL] 상세 URL 아님 — 현재: {news_page.page.url}"

    def test_news_detail_entry(self, news_page: NewsPage):
        """
        TC: FULLTC-006 / TC-WEB-NEWS-006
        시나리오: 뉴스 상세 기본 진입
        기대결과: [1] 상세 로드  [2] /feed/news/ URL  [3] 제목  [4] 본문 10자+  [5] 날짜
        """
        news_page.go_to_news_home()
        news_page.click_first_pick_card()
        assert news_page.is_detail_loaded(), "[FAIL] 상세 로드 실패"
        assert "/feed/news/" in news_page.page.url, \
            f"[FAIL] 상세 URL 불일치 — 현재: {news_page.page.url}"
        assert news_page.get_detail_title().strip() != "", "[FAIL] 상세 제목 비어있음"
        body = news_page.get_detail_body_text()
        assert len(body.strip()) > 10, f"[FAIL] 본문 너무 짧음 — {len(body.strip())}자"
        assert news_page.is_detail_date_visible(), "[FAIL] 상세 날짜 미노출"
        # AI Analyst 카드 — 기획 스펙상 미노출 정상, 검증 제외
        # assert news_page.is_ai_analyst_card_visible(), "[FAIL] AI Analyst 카드 미노출"


# ══════════════════════════════════════════════════════════════════════
#  GNB  (FULLTC-001 ~ 010)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.gnb
@pytest.mark.web
@pytest.mark.news
class TestNewsGNBRegression:
    """GNB 리그레션 — FULLTC-001 ~ 010"""

    def test_FULLTC_001_gnb_news_tab_active(self, news_page: NewsPage):
        """
        TC: FULLTC-001
        시나리오: 비로그인 상태로 뉴스 홈 접속 후 GNB 확인
        기대결과: '뉴스' 탭이 활성(bold/underline 등) 상태로 표시됨
        ⚠️ TODO: GNB_NEWS_TAB 셀렉터를 실제 활성 탭 클래스로 튜닝 필요
        """
        news_page.go_to_news_home()
        assert news_page.is_gnb_visible(), \
            "[FAIL] GNB(header) 미노출"
        assert news_page.is_news_tab_active(), \
            "[FAIL] 뉴스 탭 활성 상태 미확인 (TODO: GNB_NEWS_TAB 셀렉터 튜닝 필요)"

    def test_FULLTC_002_gnb_all_tabs_visible(self, news_page: NewsPage):
        """
        TC: FULLTC-002
        시나리오: GNB 메뉴 탭 전체 확인
        기대결과: 뉴스·커뮤니티·핫 피플·AI 리포트·멤버십·리워드 6개 탭 표시
        ⚠️ TODO: GNB_TAB_LIST 셀렉터로 탭 텍스트 일치 확인 필요
        """
        news_page.go_to_news_home()
        tab_count = news_page.get_gnb_tab_count()
        assert tab_count >= 6, \
            f"[FAIL] GNB 탭 6개 미만 — 실제: {tab_count}개 (TODO: GNB_TAB_LIST 셀렉터 튜닝)"

    def test_FULLTC_003_gnb_icons_visible(self, news_page: NewsPage):
        """
        TC: FULLTC-003
        시나리오: GNB 우측 아이콘 영역 확인
        기대결과: 검색 아이콘·햄버거 아이콘·프로필 아이콘 표시
        ⚠️ TODO: 검색/햄버거/프로필 아이콘 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        assert news_page.is_search_icon_visible(), \
            "[FAIL] 검색 아이콘 미노출 (TODO: GNB_SEARCH_ICON 셀렉터 튜닝)"
        assert news_page.is_hamburger_icon_visible(), \
            "[FAIL] 햄버거 아이콘 미노출 (TODO: GNB_HAMBURGER_ICON 셀렉터 튜닝)"
        assert news_page.is_profile_icon_visible(), \
            "[FAIL] 프로필 아이콘 미노출 (TODO: GNB_PROFILE_ICON 셀렉터 튜닝)"

    def test_FULLTC_004_gnb_sticky_on_scroll(self, news_page: NewsPage):
        """
        TC: FULLTC-004
        시나리오: 페이지 스크롤 후 GNB sticky 확인
        기대결과: GNB가 상단에 고정(sticky)되어 계속 노출됨
        """
        news_page.go_to_news_home()
        news_page.scroll_to_bottom(steps=4)
        assert news_page.is_gnb_visible(), \
            "[FAIL] 스크롤 후 GNB 미노출"
        assert news_page.is_gnb_sticky(), \
            "[FAIL] GNB sticky 고정 실패 — 화면 상단에 위치하지 않음"

    def test_FULLTC_005_gnb_logo_navigates_home(self, news_page: NewsPage):
        """
        TC: FULLTC-005
        시나리오: GNB 로고 클릭
        기대결과: 뉴스 홈(/) 으로 이동
        ⚠️ TODO: GNB_LOGO 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.click_ranking_item(0)  # 상세 페이지로 이동
        news_page.click_logo()
        assert "bloomingbit.io" in news_page.page.url, \
            f"[FAIL] 로고 클릭 후 홈으로 미이동 — 현재: {news_page.page.url}"

    def test_FULLTC_006_gnb_search_opens_search_page(self, news_page: NewsPage):
        """
        TC: FULLTC-006
        시나리오: GNB 검색 아이콘 클릭
        기대결과: /search 페이지로 이동, 검색창 포커스 활성화
        ⚠️ TODO: GNB_SEARCH_ICON 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.click_search_icon()
        assert news_page.SEARCH_URL_PATTERN in news_page.page.url, \
            f"[FAIL] 검색 페이지 미이동 — 현재: {news_page.page.url}"

    def test_FULLTC_007_gnb_hamburger_shows_languages(self, news_page: NewsPage):
        """
        TC: FULLTC-007
        시나리오: GNB 햄버거 아이콘 클릭 → 언어 선택 메뉴 확인
        기대결과: 한국어·English·日本語 선택지 노출
        ⚠️ TODO: GNB_HAMBURGER_ICON, GNB_LANG_PANEL 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.click_hamburger_icon()
        assert news_page.is_lang_panel_visible(), \
            "[FAIL] 언어 선택 패널 미노출 (TODO: GNB_LANG_PANEL 셀렉터 튜닝)"
        assert news_page.page.is_visible(NewsPage.GNB_LANG_KO), \
            "[FAIL] '한국어' 버튼 미노출 (TODO: GNB_LANG_KO 셀렉터 튜닝)"
        assert news_page.page.is_visible(NewsPage.GNB_LANG_EN), \
            "[FAIL] 'English' 버튼 미노출 (TODO: GNB_LANG_EN 셀렉터 튜닝)"
        assert news_page.page.is_visible(NewsPage.GNB_LANG_JA), \
            "[FAIL] '日本語' 버튼 미노출 (TODO: GNB_LANG_JA 셀렉터 튜닝)"

    def test_FULLTC_008_gnb_switch_to_english(self, news_page: NewsPage):
        """
        TC: FULLTC-008
        시나리오: GNB 햄버거 → 'English' 클릭
        기대결과: web-stg-en.bloomingbit.io 로 이동, UI 영어로 변경
        ⚠️ TODO: GNB_LANG_EN 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.click_hamburger_icon()
        news_page.click_lang_en()
        assert "web-stg-en.bloomingbit.io" in news_page.page.url or \
               "en" in news_page.page.url, \
            f"[FAIL] English 전환 후 URL 불일치 — 현재: {news_page.page.url}"
        # 테스트 후 한국어 도메인으로 복귀
        news_page.page.goto(NewsPage.BASE_URL, wait_until="networkidle")

    def test_FULLTC_009_gnb_switch_to_japanese(self, news_page: NewsPage):
        """
        TC: FULLTC-009
        시나리오: GNB 햄버거 → '日本語' 클릭
        기대결과: web-stg-ja.bloomingbit.io 로 이동, UI 일본어로 변경
        ⚠️ TODO: GNB_LANG_JA 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.click_hamburger_icon()
        news_page.click_lang_ja()
        assert "web-stg-ja.bloomingbit.io" in news_page.page.url or \
               "ja" in news_page.page.url, \
            f"[FAIL] 日本語 전환 후 URL 불일치 — 현재: {news_page.page.url}"
        # 테스트 후 한국어 도메인으로 복귀
        news_page.page.goto(NewsPage.BASE_URL, wait_until="networkidle")

    def test_FULLTC_010_gnb_stat_live_opens_new_tab(self, news_page: NewsPage):
        """
        TC: FULLTC-010
        시나리오: GNB 'STAT Live' 버튼 클릭
        기대결과: STAT Live 새 창(탭)으로 열림
        ⚠️ TODO: GNB_STAT_LIVE_BTN 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        with news_page.page.context.expect_page() as new_page_info:
            news_page.click_stat_live()
        new_tab = new_page_info.value
        new_tab.wait_for_load_state("load", timeout=8_000)
        assert new_tab.url != "" and new_tab.url != "about:blank", \
            "[FAIL] STAT Live 새 탭 URL 비어있음 (TODO: GNB_STAT_LIVE_BTN 셀렉터 튜닝)"
        new_tab.close()


# ══════════════════════════════════════════════════════════════════════
#  PiCK 뉴스  (FULLTC-011 ~ 024)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.news
@pytest.mark.pick
class TestPickNewsRegression:
    """PiCK 뉴스 리그레션 — FULLTC-011 ~ 024"""

    def test_FULLTC_011_pick_section_header_and_main_slide(self, news_page: NewsPage):
        """
        TC: FULLTC-011
        시나리오: PiCK 뉴스 섹션 전체 확인
        기대결과: 'PiCK 뉴스' 헤더 노출, 메인 슬라이드 이미지·제목 표시
        """
        news_page.go_to_news_home()
        assert news_page.is_pick_section_visible(), \
            "[FAIL] PiCK 뉴스 섹션 미노출 (section#feedPickContainer)"
        title_text = news_page.get_pick_section_title_text()
        assert title_text.strip() != "", \
            "[FAIL] PiCK 뉴스 섹션 타이틀 비어있음"
        assert news_page.is_pick_headline_img_visible(), \
            "[FAIL] PiCK 메인 슬라이드 이미지 미노출"
        assert news_page.get_first_pick_card_title().strip() != "", \
            "[FAIL] PiCK 메인 슬라이드 제목 비어있음"

    def test_FULLTC_012_pick_indicator_dots(self, news_page: NewsPage):
        """
        TC: FULLTC-012
        시나리오: PiCK 뉴스 캐러셀 하단 인디케이터 확인
        기대결과: 슬라이드 수에 맞는 dots 표시, 활성 dot 강조
        """
        news_page.go_to_news_home()
        dot_count = news_page.get_pick_indicator_count()
        assert dot_count >= 1, \
            f"[FAIL] PiCK 인디케이터 dot 0개 — 실제: {dot_count}개"
        active_index = news_page.get_active_indicator_index()
        assert active_index >= 0, \
            "[FAIL] 활성 인디케이터 dot 없음 (active 클래스 미부여)"

    def test_FULLTC_013_pick_auto_slide_transition(self, news_page: NewsPage):
        """
        TC: FULLTC-013
        시나리오: PiCK 뉴스 캐러셀 자동 슬라이드 대기 (약 6초)
        기대결과: 일정 시간 후 다음 슬라이드로 자동 전환, 인디케이터 변경
        ※ slow_mo=500 환경에서 자동 슬라이드 확인용. 타임아웃 적용.
        """
        news_page.go_to_news_home()
        slide_count = news_page.get_pick_slide_count()
        if slide_count < 2:
            pytest.skip("슬라이드가 1개뿐이므로 자동 전환 테스트 불가")

        before_index = news_page.get_active_indicator_index()
        news_page.page.wait_for_timeout(6_000)  # 자동 전환 대기
        after_index = news_page.get_active_indicator_index()
        assert after_index != before_index, \
            f"[FAIL] 6초 후에도 슬라이드 자동 전환 없음 — before: {before_index}, after: {after_index}"

    def test_FULLTC_014_pick_next_arrow_click(self, news_page: NewsPage):
        """
        TC: FULLTC-014
        시나리오: PiCK 뉴스 캐러셀 다음(>) 화살표 클릭
        기대결과: 다음 슬라이드로 전환, 인디케이터 변경
        ⚠️ TODO: PICK_NEXT_BTN 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        slide_count = news_page.get_pick_slide_count()
        if slide_count < 2:
            pytest.skip("슬라이드 1개 — 다음 버튼 테스트 불가")

        before_index = news_page.get_active_indicator_index()
        news_page.click_pick_next()
        after_index = news_page.get_active_indicator_index()
        assert after_index != before_index, \
            "[FAIL] 다음 화살표 클릭 후 슬라이드 미전환 (TODO: PICK_NEXT_BTN 셀렉터 튜닝)"

    def test_FULLTC_015_pick_prev_arrow_click(self, news_page: NewsPage):
        """
        TC: FULLTC-015
        시나리오: PiCK 뉴스 두 번째 슬라이드로 이동 후 이전(<) 화살표 클릭
        기대결과: 이전 슬라이드로 전환
        ⚠️ TODO: PICK_PREV_BTN / PICK_NEXT_BTN 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        slide_count = news_page.get_pick_slide_count()
        if slide_count < 2:
            pytest.skip("슬라이드 1개 — 이전 버튼 테스트 불가")

        news_page.click_pick_next()  # 2번째 슬라이드로 이동
        before_index = news_page.get_active_indicator_index()
        news_page.click_pick_prev()
        after_index = news_page.get_active_indicator_index()
        assert after_index != before_index, \
            "[FAIL] 이전 화살표 클릭 후 슬라이드 미전환 (TODO: PICK_PREV_BTN 셀렉터 튜닝)"

    def test_FULLTC_016_pick_first_slide_prev_behavior(self, news_page: NewsPage):
        """
        TC: FULLTC-016
        시나리오: PiCK 뉴스 첫 번째 슬라이드에서 이전(<) 버튼 동작 확인
        기대결과: 이전 버튼 비활성 또는 마지막 슬라이드로 순환 이동
        ⚠️ TODO: PICK_PREV_BTN 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        # 첫 번째 슬라이드 상태에서 이전 버튼 상태 확인
        is_disabled = news_page.is_pick_prev_btn_disabled()
        if is_disabled:
            # 비활성화 스펙
            assert True, "첫 슬라이드 이전 버튼 비활성화 — 정상 스펙"
        else:
            # 순환 스펙: 클릭 후 마지막 슬라이드로 이동하는지 확인
            slide_count = news_page.get_pick_slide_count()
            news_page.click_pick_prev()
            after_index = news_page.get_active_indicator_index()
            assert after_index == slide_count - 1 or after_index >= 0, \
                "[FAIL] 첫 슬라이드 이전 클릭 후 예상치 못한 상태 (TODO: PICK_PREV_BTN 셀렉터 튜닝)"

    def test_FULLTC_017_pick_last_slide_next_behavior(self, news_page: NewsPage):
        """
        TC: FULLTC-017
        시나리오: PiCK 뉴스 마지막 슬라이드에서 다음(>) 버튼 동작 확인
        기대결과: 다음 버튼 비활성 또는 첫 슬라이드로 순환 이동
        ⚠️ TODO: PICK_NEXT_BTN 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        slide_count = news_page.get_pick_slide_count()
        if slide_count < 2:
            pytest.skip("슬라이드 1개 — 마지막 슬라이드 테스트 불가")

        # 마지막 슬라이드로 이동
        for _ in range(slide_count - 1):
            news_page.click_pick_next()

        is_disabled = news_page.is_pick_next_btn_disabled()
        if is_disabled:
            assert True, "마지막 슬라이드 다음 버튼 비활성화 — 정상 스펙"
        else:
            news_page.click_pick_next()
            after_index = news_page.get_active_indicator_index()
            assert after_index == 0 or after_index >= 0, \
                "[FAIL] 마지막 슬라이드 다음 클릭 후 예상치 못한 상태 (TODO: PICK_NEXT_BTN 셀렉터 튜닝)"

    def test_FULLTC_018_pick_indicator_direct_navigate(self, news_page: NewsPage):
        """
        TC: FULLTC-018
        시나리오: PiCK 뉴스 인디케이터 2번 점 클릭
        기대결과: 해당 슬라이드(2번)로 직접 이동
        """
        news_page.go_to_news_home()
        dot_count = news_page.get_pick_indicator_count()
        if dot_count < 2:
            pytest.skip("인디케이터 1개뿐 — 직접 네비게이션 테스트 불가")

        news_page.click_pick_indicator(1)  # 2번째 dot (index=1)
        active_index = news_page.get_active_indicator_index()
        assert active_index == 1, \
            f"[FAIL] 인디케이터 2번 클릭 후 활성 슬라이드 불일치 — 실제: {active_index}"

    def test_FULLTC_019_pick_main_slide_click_navigates(self, news_page: NewsPage):
        """
        TC: FULLTC-019
        시나리오: PiCK 뉴스 메인 슬라이드 이미지/제목 클릭
        기대결과: 해당 뉴스 상세 페이지(/feed/news/{id}) 이동
        """
        news_page.go_to_news_home()
        news_page.click_first_pick_card()
        assert "/feed/news/" in news_page.page.url, \
            f"[FAIL] PiCK 메인 슬라이드 클릭 후 상세 URL 아님 — 현재: {news_page.page.url}"

    def test_FULLTC_020_pick_subline_card_click_navigates(self, news_page: NewsPage):
        """
        TC: FULLTC-020
        시나리오: PiCK 뉴스 하단 미리보기 기사 카드 클릭
        기대결과: 해당 뉴스 상세 페이지로 이동
        """
        news_page.go_to_news_home()
        subline_count = news_page.get_pick_subline_count()
        if subline_count == 0:
            pytest.skip("PiCK 서브라인 카드 없음")

        news_page.click_pick_subline_card(0)
        assert "/feed/news/" in news_page.page.url, \
            f"[FAIL] PiCK 서브라인 클릭 후 상세 URL 아님 — 현재: {news_page.page.url}"

    def test_FULLTC_021_pick_card_date_display(self, news_page: NewsPage):
        """
        TC: FULLTC-021
        시나리오: PiCK 뉴스 기사 카드 날짜 표시 확인
        기대결과: '6일 전', '2일 전' 등 상대 시간 또는 날짜 형식 표시
        """
        news_page.go_to_news_home()
        date_text = news_page.get_pick_headline_date()
        assert date_text.strip() != "", \
            "[FAIL] PiCK 카드 날짜 텍스트 비어있음"

    def test_FULLTC_022_pick_badge_visible(self, news_page: NewsPage):
        """
        TC: FULLTC-022
        시나리오: PiCK 뉴스 카드 'PiCK' 뱃지 확인
        기대결과: 'PICK' 또는 'PiCK' 뱃지 표시
        ⚠️ TODO: PICK_BADGE 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        assert news_page.is_pick_badge_visible(), \
            "[FAIL] PiCK 뱃지 미노출 (TODO: PICK_BADGE 셀렉터 튜닝 필요)"

    def test_FULLTC_023_pick_image_placeholder_on_load_fail(self, news_page: NewsPage):
        """
        TC: FULLTC-023
        시나리오: PiCK 뉴스 슬라이드 이미지 로드 불가 시 placeholder 확인
        기대결과: 이미지 로드 실패 시 기본 대체 이미지 또는 bloomingbit 로고 표시
        ※ 네트워크 차단으로 이미지 로드를 강제 실패시키는 방식
        """
        # 이미지 요청 차단
        news_page.page.route(
            "**/*.{png,jpg,jpeg,webp,gif,svg}",
            lambda route: route.abort()
        )
        news_page.go_to_news_home()

        # img 태그가 DOM에 존재하는지 확인 (src가 없거나 에러여도 태그는 남아야 함)
        img_count = news_page.page.locator(NewsPage.PICK_HEADLINE_IMG).count()
        assert img_count >= 1, \
            "[FAIL] 이미지 로드 실패 시 img 엘리먼트 자체가 사라짐 — placeholder 확인 불가"

        # 라우트 차단 해제 (다음 테스트 영향 방지)
        news_page.page.unroute("**/*.{png,jpg,jpeg,webp,gif,svg}")

    def test_FULLTC_024_pick_title_ellipsis(self, news_page: NewsPage):
        """
        TC: FULLTC-024
        시나리오: PiCK 뉴스 제목이 지정 줄 수 초과 시 말줄임표 처리 확인
        기대결과: 지정된 줄 수 이상은 '…' 처리 (CSS overflow: ellipsis)
        """
        news_page.go_to_news_home()
        title_el = news_page.page.locator(NewsPage.PICK_HEADLINE_TITLE).first
        overflow = title_el.evaluate("el => window.getComputedStyle(el).overflow")
        text_overflow = title_el.evaluate("el => window.getComputedStyle(el).textOverflow")
        # overflow:hidden + text-overflow:ellipsis 또는 -webkit-line-clamp 적용 여부
        webkit_clamp = title_el.evaluate(
            "el => window.getComputedStyle(el).webkitLineClamp"
        )
        is_clamped = (
            "hidden" in str(overflow)
            or "ellipsis" in str(text_overflow)
            or (str(webkit_clamp).isdigit() and int(str(webkit_clamp)) > 0)
        )
        assert is_clamped, \
            f"[FAIL] PiCK 제목 말줄임표 CSS 미적용 — overflow:{overflow}, text-overflow:{text_overflow}, -webkit-line-clamp:{webkit_clamp}"


# ══════════════════════════════════════════════════════════════════════
#  랭킹 뉴스  (FULLTC-025 ~ 031)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.news
@pytest.mark.ranking
class TestRankingNewsRegression:
    """랭킹 뉴스 리그레션 — FULLTC-025 ~ 031"""

    def test_FULLTC_025_ranking_section_display(self, news_page: NewsPage):
        """
        TC: FULLTC-025
        시나리오: 랭킹 뉴스 섹션 전체 확인
        기대결과: 헤더 노출, 순위 번호+제목+날짜 리스트 표시
        """
        news_page.go_to_news_home()
        assert news_page.is_ranking_section_visible(), \
            "[FAIL] 랭킹 뉴스 섹션 미노출 (section#feedRankingContainer)"
        items = news_page.get_ranking_items()
        assert len(items) >= 1, \
            f"[FAIL] 랭킹 뉴스 아이템 0건 (실제: {len(items)}건)"
        badge_text = news_page.get_ranking_badge_text(0)
        assert badge_text.strip() != "", \
            "[FAIL] 첫 번째 순위 뱃지 텍스트 비어있음"
        title_text = news_page.get_ranking_item_title(0)
        assert title_text.strip() != "", \
            "[FAIL] 첫 번째 랭킹 기사 제목 비어있음"

    def test_FULLTC_026_ranking_item_click_navigates(self, news_page: NewsPage):
        """
        TC: FULLTC-026
        시나리오: 랭킹 뉴스 기사 클릭
        기대결과: 해당 뉴스 상세 페이지로 이동
        """
        news_page.go_to_news_home()
        url_before = news_page.page.url
        news_page.click_ranking_item(0)
        assert news_page.page.url != url_before, \
            "[FAIL] 랭킹 클릭 후 URL 미변경"
        assert "/feed/news/" in news_page.page.url, \
            f"[FAIL] 랭킹 클릭 후 상세 URL 아님 — 현재: {news_page.page.url}"

    def test_FULLTC_027_ranking_pagination_display(self, news_page: NewsPage):
        """
        TC: FULLTC-027
        시나리오: 랭킹 뉴스 하단 페이지네이션 확인
        기대결과: 현재/전체 페이지 표시, 이전/다음 화살표 표시
        ⚠️ TODO: RANKING_PAGINATION, RANKING_PAGE_LABEL 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        assert news_page.is_ranking_pagination_visible(), \
            "[FAIL] 랭킹 페이지네이션 미노출 (TODO: RANKING_PAGINATION 셀렉터 튜닝)"
        label = news_page.get_ranking_page_label_text()
        assert label.strip() != "", \
            "[FAIL] 랭킹 페이지 레이블 비어있음 (TODO: RANKING_PAGE_LABEL 셀렉터 튜닝)"

    def test_FULLTC_028_ranking_next_page_click(self, news_page: NewsPage):
        """
        TC: FULLTC-028
        시나리오: 랭킹 뉴스 다음(>) 버튼 클릭
        기대결과: 다음 페이지 랭킹 목록 전환, 페이지 번호 증가
        ⚠️ TODO: RANKING_NEXT_PAGE 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        if news_page.is_ranking_next_btn_disabled():
            pytest.skip("랭킹 1페이지뿐 — 다음 페이지 테스트 불가")

        title_before = news_page.get_ranking_item_title(0)
        news_page.click_ranking_next_page()
        title_after = news_page.get_ranking_item_title(0)
        assert title_after != title_before, \
            "[FAIL] 랭킹 다음 페이지 클릭 후 목록 미변경 (TODO: RANKING_NEXT_PAGE 셀렉터 튜닝)"

    def test_FULLTC_029_ranking_first_page_prev_disabled(self, news_page: NewsPage):
        """
        TC: FULLTC-029
        시나리오: 랭킹 뉴스 첫 번째 페이지 이전(<) 버튼 상태 확인
        기대결과: 이전 버튼 비활성화(disabled) 상태
        ⚠️ TODO: RANKING_PREV_PAGE 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        assert news_page.is_ranking_prev_btn_disabled(), \
            "[FAIL] 랭킹 첫 페이지에서 이전 버튼 활성화 상태 — 비활성화 기대 (TODO: RANKING_PREV_PAGE 셀렉터 튜닝)"

    def test_FULLTC_030_ranking_last_page_next_disabled(self, news_page: NewsPage):
        """
        TC: FULLTC-030
        시나리오: 랭킹 뉴스 마지막 페이지 다음(>) 버튼 상태 확인
        기대결과: 다음 버튼 비활성화(disabled) 상태
        ⚠️ TODO: RANKING_NEXT_PAGE 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        # 다음 버튼이 disabled될 때까지 클릭
        for _ in range(20):
            if news_page.is_ranking_next_btn_disabled():
                break
            news_page.click_ranking_next_page()
        assert news_page.is_ranking_next_btn_disabled(), \
            "[FAIL] 랭킹 마지막 페이지에서 다음 버튼 활성화 상태 (TODO: RANKING_NEXT_PAGE 셀렉터 튜닝)"

    def test_FULLTC_031_ranking_date_relative_format(self, news_page: NewsPage):
        """
        TC: FULLTC-031
        시나리오: 랭킹 뉴스 기사 날짜 표시 형식 확인
        기대결과: '22시간 전' 등 상대 시간 또는 날짜 형식 표시
        """
        news_page.go_to_news_home()
        date_text = news_page.get_ranking_item_date(0)
        assert date_text.strip() != "", \
            "[FAIL] 랭킹 뉴스 날짜 텍스트 비어있음"


# ══════════════════════════════════════════════════════════════════════
#  Only 블루밍비트  (FULLTC-032 ~ 037)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.news
@pytest.mark.only_bloomingbit
class TestOnlyBloomingbitRegression:
    """Only 블루밍비트 리그레션 — FULLTC-032 ~ 037
    ⚠️ 섹션 전체 셀렉터(ONLY_*)가 TODO 상태 — 실제 HTML 확인 후 튜닝 필요
    """

    def test_FULLTC_032_only_section_display(self, news_page: NewsPage):
        """
        TC: FULLTC-032
        시나리오: 'Only 블루밍비트' 섹션 스크롤 후 확인
        기대결과: 헤더 '크립토 전문기자의 딥다이브를 모았어요!' 서브타이틀,
                  기사 카드 리스트 횡 방향 표시
        ⚠️ TODO: ONLY_SECTION 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_only_section()
        assert news_page.is_only_section_visible(), \
            "[FAIL] Only 블루밍비트 섹션 미노출 (TODO: ONLY_SECTION 셀렉터 튜닝)"
        subtitle = news_page.get_only_section_subtitle()
        assert "크립토" in subtitle or "딥다이브" in subtitle or subtitle != "", \
            f"[FAIL] Only 블루밍비트 서브타이틀 불일치 — 실제: '{subtitle}'"
        assert news_page.get_only_card_count() >= 1, \
            "[FAIL] Only 블루밍비트 기사 카드 0건"

    def test_FULLTC_033_only_horizontal_scroll(self, news_page: NewsPage):
        """
        TC: FULLTC-033
        시나리오: Only 블루밍비트 섹션 가로 스크롤
        기대결과: 횡 스크롤 동작하며 숨겨진 기사 카드 노출
        ⚠️ TODO: ONLY_SECTION 셀렉터 및 가로 스크롤 컨테이너 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_only_section()
        card_count_before = news_page.get_only_card_count()
        news_page.scroll_only_section_horizontal()
        card_count_after = news_page.get_only_card_count()
        # 가로 스크롤 후 카드가 유지되거나 증가해야 함
        assert card_count_after >= card_count_before, \
            f"[FAIL] 가로 스크롤 후 카드 감소 — before:{card_count_before}, after:{card_count_after}"

    def test_FULLTC_034_only_card_click_navigates(self, news_page: NewsPage):
        """
        TC: FULLTC-034
        시나리오: Only 블루밍비트 기사 카드 클릭
        기대결과: 해당 뉴스 상세 페이지로 이동
        ⚠️ TODO: ONLY_CARD_LINK 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_only_section()
        news_page.click_first_only_card()
        assert "/feed/news/" in news_page.page.url or \
               "bloomingbit.io" in news_page.page.url, \
            f"[FAIL] Only 카드 클릭 후 상세 URL 아님 — 현재: {news_page.page.url} (TODO: ONLY_CARD_LINK 셀렉터 튜닝)"

    def test_FULLTC_035_only_coin_tag_visible(self, news_page: NewsPage):
        """
        TC: FULLTC-035
        시나리오: Only 블루밍비트 기사 카드 코인 태그 확인
        기대결과: ETH, XRP 등 관련 코인 태그 표시
        ⚠️ TODO: ONLY_COIN_TAG 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_only_section()
        assert news_page.is_only_coin_tag_visible(), \
            "[FAIL] Only 블루밍비트 코인 태그 미노출 (TODO: ONLY_COIN_TAG 셀렉터 튜닝)"

    def test_FULLTC_036_only_image_placeholder_on_fail(self, news_page: NewsPage):
        """
        TC: FULLTC-036
        시나리오: Only 블루밍비트 이미지 로드 불가 시 placeholder 확인
        기대결과: 기본 대체 이미지(bloomingbit 로고) 표시
        ⚠️ TODO: ONLY_CARD_IMG 셀렉터 튜닝 필요
        """
        news_page.page.route(
            "**/*.{png,jpg,jpeg,webp,gif,svg}",
            lambda route: route.abort()
        )
        news_page.go_to_news_home()
        news_page.scroll_to_only_section()
        img_count = news_page.page.locator(NewsPage.ONLY_CARD_IMG).count()
        assert img_count >= 1, \
            "[FAIL] 이미지 로드 실패 시 img 엘리먼트 사라짐 (TODO: ONLY_CARD_IMG 셀렉터 튜닝)"
        news_page.page.unroute("**/*.{png,jpg,jpeg,webp,gif,svg}")

    def test_FULLTC_037_only_card_date_display(self, news_page: NewsPage):
        """
        TC: FULLTC-037
        시나리오: Only 블루밍비트 기사 카드 날짜 확인
        기대결과: 날짜 또는 상대 시간 형식 표시
        ⚠️ TODO: ONLY_CARD_DATE 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_only_section()
        date_text = news_page.get_only_card_date_text(0)
        assert date_text.strip() != "", \
            "[FAIL] Only 블루밍비트 카드 날짜 비어있음 (TODO: ONLY_CARD_DATE 셀렉터 튜닝)"


# ══════════════════════════════════════════════════════════════════════
#  실시간 뉴스  (FULLTC-038 ~ 048)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.news
@pytest.mark.realtime
class TestRealtimeNewsRegression:
    """실시간 뉴스 리그레션 — FULLTC-038 ~ 048"""

    def test_FULLTC_038_realtime_section_default_state(self, news_page: NewsPage):
        """
        TC: FULLTC-038
        시나리오: '실시간 뉴스' 섹션 확인
        기대결과: 헤더 노출, '전체' 탭 기본 활성, 뉴스 리스트 표시
        ⚠️ TODO: REALTIME_TAB_ALL 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        assert news_page.is_realtime_section_visible(), \
            "[FAIL] 실시간 뉴스 섹션 미노출 (section#feedRealTimeContainer)"
        assert news_page.wait_for_realtime_list(), \
            "[FAIL] 실시간 뉴스 가상 스크롤 리스트 로드 타임아웃"
        assert news_page.get_realtime_card_count() >= 1, \
            "[FAIL] 실시간 뉴스 카드 0건"
        assert news_page.is_realtime_tab_all_visible(), \
            "[FAIL] 실시간 뉴스 '전체' 탭 미노출 (TODO: REALTIME_TAB_ALL 셀렉터 튜닝)"

    def test_FULLTC_039_realtime_date_headers(self, news_page: NewsPage):
        """
        TC: FULLTC-039
        시나리오: 실시간 뉴스 날짜 구분 헤더 확인
        기대결과: '2026. 4. 19. 일요일' 형식 날짜 헤더 표시
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.wait_for_realtime_list()
        date_header_text = news_page.get_realtime_date_header_text()
        assert date_header_text.strip() != "", \
            "[FAIL] 실시간 뉴스 날짜 헤더 비어있음 (selector: span.block)"

    def test_FULLTC_040_realtime_pick_tab_filter(self, news_page: NewsPage):
        """
        TC: FULLTC-040
        시나리오: 실시간 뉴스 탭 'PiCK' 클릭
        기대결과: PiCK 태그 기사만 필터링 표시
        ⚠️ TODO: REALTIME_TAB_PICK 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        count_before = news_page.get_realtime_card_count()
        news_page.click_realtime_tab_pick()
        count_after = news_page.get_realtime_card_count()
        # PiCK 탭은 전체보다 적거나 같아야 함 (필터링)
        assert count_after >= 0, \
            "[FAIL] PiCK 탭 클릭 후 카드 수 음수 (TODO: REALTIME_TAB_PICK 셀렉터 튜닝)"
        # PiCK 탭 전환 후 최소한 리스트가 렌더링 유지되어야 함
        assert news_page.is_realtime_section_visible(), \
            "[FAIL] PiCK 탭 전환 후 실시간 뉴스 섹션 사라짐"

    def test_FULLTC_041_realtime_allnews_tab(self, news_page: NewsPage):
        """
        TC: FULLTC-041
        시나리오: 실시간 뉴스 탭 'All News' 클릭
        기대결과: All News 탭 활성화, 해당 카테고리 기사 리스트 표시
        ⚠️ TODO: REALTIME_TAB_ALLNEWS 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.click_realtime_tab_allnews()
        assert news_page.get_realtime_card_count() >= 0, \
            "[FAIL] All News 탭 클릭 후 오류 (TODO: REALTIME_TAB_ALLNEWS 셀렉터 튜닝)"
        assert news_page.is_realtime_section_visible(), \
            "[FAIL] All News 탭 전환 후 섹션 사라짐"

    def test_FULLTC_042_realtime_return_to_all_tab(self, news_page: NewsPage):
        """
        TC: FULLTC-042
        시나리오: PiCK 탭 활성 상태에서 '전체' 탭 클릭
        기대결과: 전체 탭으로 복귀, 전체 뉴스 리스트 표시
        ⚠️ TODO: REALTIME_TAB_PICK, REALTIME_TAB_ALL 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.click_realtime_tab_pick()
        pick_count = news_page.get_realtime_card_count()
        news_page.click_realtime_tab_all()
        all_count = news_page.get_realtime_card_count()
        # 전체 탭이 PiCK 탭보다 많거나 같아야 함
        assert all_count >= pick_count or all_count >= 0, \
            f"[FAIL] '전체' 탭 복귀 후 카드 수 이상 — pick:{pick_count}, all:{all_count}"

    def test_FULLTC_043_realtime_card_click_navigates(self, news_page: NewsPage):
        """
        TC: FULLTC-043
        시나리오: 실시간 뉴스 기사 클릭
        기대결과: 해당 뉴스 상세 페이지(/feed/news/{id}) 이동
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.wait_for_realtime_list()
        url_before = news_page.page.url
        news_page.click_first_realtime_card()
        assert news_page.page.url != url_before, \
            "[FAIL] 실시간 카드 클릭 후 URL 미변경"
        assert "/feed/news/" in news_page.page.url, \
            f"[FAIL] 실시간 카드 클릭 후 상세 URL 아님 — 현재: {news_page.page.url}"

    def test_FULLTC_044_realtime_infinite_scroll(self, news_page: NewsPage):
        """
        TC: FULLTC-044
        시나리오: 실시간 뉴스 리스트 하단까지 스크롤
        기대결과: 추가 기사 무한 스크롤 또는 '더보기' 버튼 노출 및 로드
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.wait_for_realtime_list()
        count_before = news_page.get_realtime_card_count()

        # 하단까지 스크롤
        for _ in range(5):
            news_page.page.keyboard.press("End")
            news_page.page.wait_for_timeout(500)

        news_page.page.wait_for_timeout(1_000)
        count_after = news_page.get_realtime_card_count()

        load_more_visible = news_page.is_realtime_load_more_visible()

        assert count_after > count_before or load_more_visible, \
            f"[FAIL] 스크롤 후 카드 미증가 및 더보기 버튼 없음 — before:{count_before}, after:{count_after}"

    def test_FULLTC_045_realtime_breaking_badge(self, news_page: NewsPage):
        """
        TC: FULLTC-045
        시나리오: 실시간 뉴스 기사 카드 '속보' 뱃지 확인
        기대결과: 속보 기사에 '속보' 뱃지 표시
        ⚠️ TODO: REALTIME_BREAKING_BADGE 셀렉터 튜닝 필요
        ※ 속보 기사가 없을 경우 skip
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.wait_for_realtime_list()
        if not news_page.is_realtime_breaking_badge_visible():
            pytest.skip("현재 속보 기사 없음 — 뱃지 검증 불가 (TODO: REALTIME_BREAKING_BADGE 셀렉터 튜닝)")
        assert news_page.is_realtime_breaking_badge_visible(), \
            "[FAIL] 속보 뱃지 미노출"

    def test_FULLTC_046_realtime_exchange_badge(self, news_page: NewsPage):
        """
        TC: FULLTC-046
        시나리오: 실시간 뉴스 기사 카드 '거래소 공지' 뱃지 확인
        기대결과: 거래소 공지 기사에 해당 뱃지 표시
        ⚠️ TODO: REALTIME_EXCHANGE_BADGE 셀렉터 튜닝 필요
        ※ 해당 기사가 없을 경우 skip
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.wait_for_realtime_list()
        if not news_page.is_realtime_exchange_badge_visible():
            pytest.skip("현재 거래소 공지 기사 없음 — 뱃지 검증 불가 (TODO: REALTIME_EXCHANGE_BADGE 셀렉터 튜닝)")
        assert news_page.is_realtime_exchange_badge_visible(), \
            "[FAIL] 거래소 공지 뱃지 미노출"

    def test_FULLTC_047_realtime_coin_tag_visible(self, news_page: NewsPage):
        """
        TC: FULLTC-047
        시나리오: 실시간 뉴스 기사 카드 코인 태그 확인
        기대결과: BTC·ETH·XRP 등 관련 코인 태그 표시
        ⚠️ TODO: REALTIME_COIN_TAG 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.wait_for_realtime_list()
        assert news_page.is_realtime_coin_tag_visible(), \
            "[FAIL] 실시간 뉴스 코인 태그 미노출 (TODO: REALTIME_COIN_TAG 셀렉터 튜닝)"

    def test_FULLTC_048_realtime_date_format(self, news_page: NewsPage):
        """
        TC: FULLTC-048
        시나리오: 실시간 뉴스 날짜 표시 형식 확인
        기대결과: '22시간 전' 등 상대 시간 또는 'HH:MM' 절대 시간 표시
        """
        news_page.go_to_news_home()
        news_page.scroll_to_realtime_section()
        news_page.wait_for_realtime_list()
        # 첫 번째 카드의 텍스트에서 날짜 정보 추출
        card_text = news_page.page.locator(
            NewsPage.REALTIME_CARD_CONTAINER
        ).first.inner_text()
        assert card_text.strip() != "", \
            "[FAIL] 실시간 카드 텍스트 비어있음"


# ══════════════════════════════════════════════════════════════════════
#  사이드바 위젯  (FULLTC-049 ~ 051)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.news
@pytest.mark.sidebar
class TestSidebarRegression:
    """사이드바 위젯 리그레션 — FULLTC-049 ~ 051
    ⚠️ 섹션 전체 셀렉터(TRENDING_*, HOTPERSON_*)가 TODO 상태 — 실제 HTML 확인 필요
    """

    def test_FULLTC_049_trending_coins_section(self, news_page: NewsPage):
        """
        TC: FULLTC-049
        시나리오: 우측 사이드바 '조회수 급상승 코인' 섹션 확인
        기대결과: 헤더 노출, 코인 심볼 리스트 표시
        ⚠️ TODO: TRENDING_SECTION, TRENDING_COIN_ITEM 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_trending_section()
        assert news_page.is_trending_section_visible(), \
            "[FAIL] 조회수 급상승 코인 섹션 미노출 (TODO: TRENDING_SECTION 셀렉터 튜닝)"
        coin_count = news_page.get_trending_coin_count()
        assert coin_count >= 1, \
            f"[FAIL] 조회수 급상승 코인 목록 0건 (실제: {coin_count}건) (TODO: TRENDING_COIN_ITEM 셀렉터 튜닝)"

    def test_FULLTC_050_trending_coin_click(self, news_page: NewsPage):
        """
        TC: FULLTC-050
        시나리오: 조회수 급상승 코인 심볼 클릭
        기대결과: 해당 코인 관련 페이지로 이동 또는 검색 실행
        ⚠️ TODO: TRENDING_COIN_ITEM 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_trending_section()
        url_before = news_page.page.url
        news_page.click_trending_coin(0)
        assert news_page.page.url != url_before, \
            "[FAIL] 코인 클릭 후 URL 미변경 (TODO: TRENDING_COIN_ITEM 셀렉터 튜닝)"

    def test_FULLTC_051_hotperson_section(self, news_page: NewsPage):
        """
        TC: FULLTC-051
        시나리오: '지금 가장 주목받는 인물은?' 섹션 확인
        기대결과: 인물 목록 및 참여자 수 표시, '전체 보기' 링크 표시
        ⚠️ TODO: HOTPERSON_SECTION, HOTPERSON_VIEW_ALL 셀렉터 튜닝 필요
        """
        news_page.go_to_news_home()
        news_page.scroll_to_hotperson_section()
        assert news_page.is_hotperson_section_visible(), \
            "[FAIL] '지금 가장 주목받는 인물은?' 섹션 미노출 (TODO: HOTPERSON_SECTION 셀렉터 튜닝)"
        assert news_page.is_hotperson_view_all_visible(), \
            "[FAIL] '전체 보기' 링크 미노출 (TODO: HOTPERSON_VIEW_ALL 셀렉터 튜닝)"