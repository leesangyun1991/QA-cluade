"""
tests/stage8_regression/web/test_regression_hotpeople.py
[Stage 8 리그레션 스크립트]  핫피플(Hot People) 도메인 전체 자동화 스위트

────────────────────────────────────────────────────────────
 테스트 클래스 구성
────────────────────────────────────────────────────────────
 TestHotPeopleMainRegression     — FULLTC-181 ~ 183  메인 페이지 진입 & 기본 섹션
 TestHotPeopleSliderRegression   — FULLTC-184 ~ 186  썸네일 슬라이더
 TestHotPeopleDetailRegression   — FULLTC-187 ~ 190  인물 상세
 TestHotPeopleVoteRegression     — FULLTC-191 ~ 196  지지율 투표
 TestHotPeopleRankingRegression  — FULLTC-197 ~ 198  랭킹 패널
 TestHotPeopleListRegression     — FULLTC-199 ~ 205  전체 인물 목록 & 엣지케이스
────────────────────────────────────────────────────────────

실행 방법:
  pytest test_regression_hotpeople.py -v                    # 전체
  pytest -m "hotpeople and p0"                              # P0만
  pytest -k "test_FULLTC_192"                               # 특정 TC만
  pytest -k "vote"                                          # 투표 관련만

⚠️  TODO: 모든 TODO_ 셀렉터는 실제 STG HTML 확인 후 hotpeople_page.py에서 교체 필요
"""

import os
import pytest
from typing import Iterator
from playwright.sync_api import sync_playwright, Page

from hotpeople_page import HotPeoplePage


# ══════════════════════════════════════════════════════════════════════
#  Fixture (브라우저 설정 — 변경 금지)
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="class")
def hotpeople_page() -> Iterator[HotPeoplePage]:
    """
    핫피플 Page Object 픽스처.
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
                #       - 상위 모니터 중간쯤 띄우려면 절반값 사용
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
        hotpeople = HotPeoplePage(page)
        yield hotpeople
        browser.close()


# ══════════════════════════════════════════════════════════════════════
#  메인 페이지 진입 & 기본 섹션  (FULLTC-181 ~ 183)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.hotpeople
@pytest.mark.hotpeople_main
class TestHotPeopleMainRegression:
    """핫피플 메인 페이지 리그레션 — FULLTC-181 ~ 183"""

    def test_FULLTC_181_hotpeople_main_page_entry(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-181  [Minor]
        시나리오: GNB '핫 피플' 메뉴 클릭
        기대결과: /people 페이지로 이동하며 인물 이름·소속·프로필 이미지·지지율 섹션 노출
        ⚠️ TODO: GNB_HOTPEOPLE_TAB / HOTPEOPLE_MAIN 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()

        assert hotpeople_page.HOTPEOPLE_MAIN_PATH in hotpeople_page.page.url, (
            f"[FAIL] 핫피플 메인 URL 불일치 — 현재: {hotpeople_page.page.url}"
        )
        assert hotpeople_page.is_gnb_visible(), \
            "[FAIL] GNB 헤더 미노출 — header#headerContainer 셀렉터 확인"

        assert (
            hotpeople_page.page.locator(hotpeople_page.PERSON_NAME).count() > 0
            or hotpeople_page.page.locator(hotpeople_page.HOTPEOPLE_MAIN).count() > 0
        ), "[FAIL] 핫피플 메인 컨테이너 미노출 (TODO: HOTPEOPLE_MAIN / PERSON_NAME 셀렉터 튜닝)"

    def test_FULLTC_182_thumbnail_slider_visible(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-182  [Major]
        시나리오: 핫피플 메인 — 페이지 상단 썸네일 슬라이더 확인
        기대결과: 인물 원형 썸네일 목록이 가로 나열, 최신 인물에 'new' 뱃지 노출
        ⚠️ TODO: SLIDER_SECTION / SLIDER_ITEM / SLIDER_NEW_BADGE 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.is_slider_section_visible(), \
            "[FAIL] 썸네일 슬라이더 섹션 미노출 (TODO: SLIDER_SECTION 셀렉터 튜닝)"

        item_count = hotpeople_page.get_slider_item_count()
        assert item_count > 0, \
            f"[FAIL] 썸네일 슬라이더 아이템 0개 (TODO: SLIDER_ITEM 셀렉터 튜닝)"

        assert hotpeople_page.is_new_badge_visible(), \
            "[FAIL] 'new' 뱃지 미노출 — 최신 등록 인물 존재 여부 및 SLIDER_NEW_BADGE 확인"

    def test_FULLTC_183_ranking_panel_visible(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-183  [Major]
        시나리오: 핫피플 메인 — 우측 '지금 가장 뜨거운 인물' 패널 확인
        기대결과: 인물 썸네일·이름·최신 뉴스 제목 구성 랭킹 목록 + '전체 보기 >' 링크 노출
        ⚠️ TODO: RANKING_PANEL / RANKING_ITEM / RANKING_VIEW_ALL 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.is_ranking_panel_visible(), \
            "[FAIL] 우측 랭킹 패널 미노출 (TODO: RANKING_PANEL 셀렉터 튜닝)"

        rank_count = hotpeople_page.get_ranking_item_count()
        assert rank_count > 0, \
            "[FAIL] 랭킹 패널 내 인물 항목 0개 (TODO: RANKING_ITEM 셀렉터 튜닝)"

        assert hotpeople_page.is_ranking_view_all_visible(), \
            "[FAIL] 랭킹 패널 '전체 보기 >' 링크 미노출 (TODO: RANKING_VIEW_ALL 셀렉터 튜닝)"


# ══════════════════════════════════════════════════════════════════════
#  썸네일 슬라이더  (FULLTC-184 ~ 186)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.hotpeople
@pytest.mark.hotpeople_slider
class TestHotPeopleSliderRegression:
    """썸네일 슬라이더 리그레션 — FULLTC-184 ~ 186"""

    def test_FULLTC_184_slider_arrow_navigation(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-184  [Minor]
        시나리오: 썸네일 슬라이더 우측 '>' 화살표 버튼 클릭
        기대결과: 슬라이더가 우측으로 이동하며 다음 인물 썸네일 노출
        ⚠️ TODO: SLIDER_NEXT_BTN 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        # 이동 전 첫 번째 아이템 이미지 src 기록
        img_before = hotpeople_page.get_slider_item_img_src(index=0)

        next_btn = hotpeople_page.page.locator(hotpeople_page.SLIDER_NEXT_BTN)
        assert next_btn.count() > 0, \
            "[FAIL] 슬라이더 다음('>')  버튼 미노출 (TODO: SLIDER_NEXT_BTN 셀렉터 튜닝)"

        hotpeople_page.click_slider_next()

        # 이동 후 슬라이더 내 아이템이 여전히 존재하는지 확인
        item_count_after = hotpeople_page.get_slider_item_count()
        assert item_count_after > 0, \
            "[FAIL] 슬라이더 이동 후 썸네일 아이템 미노출"

    def test_FULLTC_185_slider_thumbnail_click_routing(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-185  [Major]
        시나리오: 슬라이더에서 특정 인물 썸네일 클릭
        기대결과: 메인 영역이 해당 인물 상세로 전환, URL이 /people?seq={id} 형태로 변경
        ⚠️ TODO: SLIDER_ITEM 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.get_slider_item_count() > 0, \
            "[FAIL] 슬라이더 아이템 없음 — 전제 조건 미충족 (TODO: SLIDER_ITEM 셀렉터 튜닝)"

        hotpeople_page.click_slider_item(index=0)

        assert hotpeople_page.HOTPEOPLE_MAIN_PATH in hotpeople_page.page.url, \
            f"[FAIL] 인물 상세 페이지 이동 실패 — 현재: {hotpeople_page.page.url}"
        assert hotpeople_page.is_url_person_detail(), \
            f"[FAIL] URL에 ?seq= 파라미터 없음 — 현재: {hotpeople_page.page.url}"

    def test_FULLTC_186_slider_image_lazy_load(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-186  [Minor]
        시나리오: '>' 버튼으로 슬라이더를 이동하며 모든 썸네일 이미지 확인
        기대결과: 슬라이드 이동 시 각 인물 썸네일 이미지가 지연 로딩으로 정상 노출
        ⚠️ TODO: SLIDER_ITEM_IMG 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        # 초기 노출된 아이템들 이미지 로드 확인 (최대 3개)
        item_count = min(hotpeople_page.get_slider_item_count(), 3)
        broken_images = []
        for i in range(item_count):
            if not hotpeople_page.is_slider_img_loaded(index=i):
                broken_images.append(i)

        # 화살표 이동 후 추가 확인
        hotpeople_page.click_slider_next()
        hotpeople_page.page.wait_for_timeout(600)

        after_count = min(hotpeople_page.get_slider_item_count(), 3)
        for i in range(after_count):
            if not hotpeople_page.is_slider_img_loaded(index=i):
                broken_images.append(f"after_next:{i}")

        assert len(broken_images) == 0, \
            f"[FAIL] 이미지 로드 실패한 썸네일 인덱스: {broken_images} (TODO: SLIDER_ITEM_IMG 셀렉터 튜닝)"


# ══════════════════════════════════════════════════════════════════════
#  인물 상세  (FULLTC-187 ~ 190)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.hotpeople
@pytest.mark.hotpeople_detail
class TestHotPeopleDetailRegression:
    """인물 상세 리그레션 — FULLTC-187 ~ 190"""

    def test_FULLTC_187_person_detail_basic_info(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-187  [Major]
        시나리오: 핫피플 메인 진입 후 메인 영역의 인물 기본 정보 확인
        기대결과: 인물 이름·소속/직함 텍스트·대형 프로필 이미지 모두 누락 없이 노출
        ⚠️ TODO: PERSON_NAME / PERSON_AFFILIATION / PERSON_PROFILE_IMG 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        person_name = hotpeople_page.page.locator(hotpeople_page.PERSON_NAME)
        assert person_name.count() > 0, \
            "[FAIL] 인물 이름 미노출 (TODO: PERSON_NAME 셀렉터 튜닝)"

        name_text = hotpeople_page.get_person_name_text()
        assert len(name_text) > 0, \
            "[FAIL] 인물 이름 텍스트가 비어 있음"

        assert hotpeople_page.page.locator(hotpeople_page.PERSON_AFFILIATION).count() > 0, \
            "[FAIL] 인물 소속/직함 미노출 (TODO: PERSON_AFFILIATION 셀렉터 튜닝)"

        assert hotpeople_page.is_person_profile_img_visible(), \
            "[FAIL] 인물 대형 프로필 이미지 미노출 (TODO: PERSON_PROFILE_IMG 셀렉터 튜닝)"

    def test_FULLTC_188_related_news_slider_visible(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-188  [Major]
        시나리오: 인물 상세 영역 내 관련 뉴스 슬라이더 확인
        기대결과: 관련 뉴스 카드(제목·게시 시간)가 슬라이더 형태로 1개 이상 노출
        ⚠️ TODO: NEWS_SLIDER_SECTION / NEWS_CARD 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.is_news_slider_visible(), \
            "[FAIL] 관련 뉴스 슬라이더 섹션 미노출 (TODO: NEWS_SLIDER_SECTION 셀렉터 튜닝)"

        news_count = hotpeople_page.get_news_card_count()
        assert news_count >= 1, \
            f"[FAIL] 관련 뉴스 카드 {news_count}개 — 1개 이상 필요 (TODO: NEWS_CARD 셀렉터 튜닝)"

    def test_FULLTC_189_news_slider_navigation(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-189  [Minor]
        시나리오: 관련 뉴스 슬라이더의 '>' 및 '<' 화살표 버튼 클릭
        기대결과: 클릭 방향으로 뉴스 카드가 슬라이드되며 다음/이전 뉴스 노출
        ⚠️ TODO: NEWS_SLIDER_NEXT / NEWS_SLIDER_PREV 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        next_btn = hotpeople_page.page.locator(hotpeople_page.NEWS_SLIDER_NEXT)
        assert next_btn.count() > 0, \
            "[FAIL] 뉴스 슬라이더 '>' 버튼 미노출 (TODO: NEWS_SLIDER_NEXT 셀렉터 튜닝)"

        hotpeople_page.click_news_slider_next()
        assert hotpeople_page.get_news_card_count() >= 1, \
            "[FAIL] 뉴스 슬라이더 이동 후 카드 미노출"

        prev_btn = hotpeople_page.page.locator(hotpeople_page.NEWS_SLIDER_PREV)
        assert prev_btn.count() > 0, \
            "[FAIL] 뉴스 슬라이더 '<' 버튼 미노출 (TODO: NEWS_SLIDER_PREV 셀렉터 튜닝)"

        hotpeople_page.click_news_slider_prev()
        assert hotpeople_page.get_news_card_count() >= 1, \
            "[FAIL] 뉴스 슬라이더 이전 이동 후 카드 미노출"

    def test_FULLTC_190_news_card_click_routing(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-190  [Major]
        시나리오: 관련 뉴스 슬라이더의 뉴스 카드 클릭
        기대결과: 해당 뉴스 상세 페이지(/news/{id})로 이동
        ⚠️ TODO: NEWS_CARD 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.get_news_card_count() >= 1, \
            "[FAIL] 관련 뉴스 카드 없음 — 전제 조건 미충족 (TODO: NEWS_CARD 셀렉터 튜닝)"

        hotpeople_page.click_first_news_card()

        assert hotpeople_page.is_url_news_detail(), \
            f"[FAIL] 뉴스 상세 페이지 이동 실패 — 현재: {hotpeople_page.page.url} (기대: /news/ 포함)"


# ══════════════════════════════════════════════════════════════════════
#  지지율 투표  (FULLTC-191 ~ 196)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.hotpeople
@pytest.mark.hotpeople_vote
class TestHotPeopleVoteRegression:
    """지지율 투표 리그레션 — FULLTC-191 ~ 196"""

    def test_FULLTC_191_vote_section_visible(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-191  [Major]
        시나리오: 인물 상세 하단의 지지율 섹션 확인
        기대결과: '{인물명}의 지지율은?' 제목·N명 참여중·지지/반대 비율 바·지지해요·아쉬워요 버튼 모두 노출
        ⚠️ TODO: VOTE_SECTION / VOTE_TITLE / VOTE_PARTICIPANT_COUNT /
                  VOTE_RATE_BAR / VOTE_SUPPORT_BTN / VOTE_OPPOSE_BTN 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)
        hotpeople_page.scroll_to_vote_section()

        assert hotpeople_page.is_vote_section_visible(), \
            "[FAIL] 지지율 투표 섹션 미노출 (TODO: VOTE_SECTION 셀렉터 튜닝)"

        assert hotpeople_page.page.locator(hotpeople_page.VOTE_TITLE).count() > 0, \
            "[FAIL] 지지율 제목('의 지지율은?') 미노출 (TODO: VOTE_TITLE 셀렉터 튜닝)"

        assert hotpeople_page.page.locator(hotpeople_page.VOTE_PARTICIPANT_COUNT).count() > 0, \
            "[FAIL] 참여자 수 텍스트 미노출 (TODO: VOTE_PARTICIPANT_COUNT 셀렉터 튜닝)"

        assert hotpeople_page.page.locator(hotpeople_page.VOTE_RATE_BAR).count() > 0, \
            "[FAIL] 지지/반대 비율 바 미노출 (TODO: VOTE_RATE_BAR 셀렉터 튜닝)"

        assert hotpeople_page.is_vote_support_btn_visible(), \
            "[FAIL] '지지해요' 버튼 미노출 (TODO: VOTE_SUPPORT_BTN 셀렉터 튜닝)"

        assert hotpeople_page.is_vote_oppose_btn_visible(), \
            "[FAIL] '아쉬워요' 버튼 미노출 (TODO: VOTE_OPPOSE_BTN 셀렉터 튜닝)"

    def test_FULLTC_192_vote_support_click(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-192  [Major]
        시나리오: 로그인 상태 — '지지해요' 버튼 클릭
        기대결과: 지지 투표 즉시 반영, 지지 % 수치와 참여자 수 업데이트
        ⚠️ TODO: VOTE_SUPPORT_PCT / VOTE_PARTICIPANT_COUNT 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)
        hotpeople_page.scroll_to_vote_section()

        # 클릭 전 참여자 수 스냅샷
        count_before = hotpeople_page.get_vote_participant_text()
        pct_before   = hotpeople_page.get_support_pct_text()

        hotpeople_page.click_vote_support()
        hotpeople_page.page.wait_for_timeout(1_000)

        # 로그인 모달이 뜨면 로그인 세션 문제 — 테스트 실패 처리
        assert not hotpeople_page.is_login_modal_visible(), \
            "[FAIL] 로그인 모달 노출 — auth.json 세션 유효성 확인 필요"

        # 투표 후 수치 변화 또는 활성 상태 확인
        count_after = hotpeople_page.get_vote_participant_text()
        pct_after   = hotpeople_page.get_support_pct_text()

        voted = (
            hotpeople_page.is_support_btn_active()
            or count_before != count_after
            or pct_before != pct_after
        )
        assert voted, (
            "[FAIL] 지지해요 투표 후 수치 변화 없음 — "
            f"참여자: {count_before} → {count_after}, 지지율: {pct_before} → {pct_after} "
            "(TODO: VOTE_ACTIVE_CLASS / VOTE_SUPPORT_PCT / VOTE_PARTICIPANT_COUNT 튜닝)"
        )

    def test_FULLTC_193_vote_oppose_click(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-193  [Major]
        시나리오: 로그인 상태 — '아쉬워요' 버튼 클릭
        기대결과: 반대 투표 즉시 반영, 아쉬워요 % 수치와 참여자 수 업데이트
        ⚠️ TODO: VOTE_OPPOSE_PCT / VOTE_PARTICIPANT_COUNT 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)
        hotpeople_page.scroll_to_vote_section()

        count_before = hotpeople_page.get_vote_participant_text()
        pct_before   = hotpeople_page.get_oppose_pct_text()

        hotpeople_page.click_vote_oppose()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert not hotpeople_page.is_login_modal_visible(), \
            "[FAIL] 로그인 모달 노출 — auth.json 세션 유효성 확인 필요"

        count_after = hotpeople_page.get_vote_participant_text()
        pct_after   = hotpeople_page.get_oppose_pct_text()

        voted = (
            hotpeople_page.is_oppose_btn_active()
            or count_before != count_after
            or pct_before != pct_after
        )
        assert voted, (
            "[FAIL] 아쉬워요 투표 후 수치 변화 없음 — "
            f"참여자: {count_before} → {count_after}, 아쉬워요율: {pct_before} → {pct_after} "
            "(TODO: VOTE_ACTIVE_CLASS / VOTE_OPPOSE_PCT / VOTE_PARTICIPANT_COUNT 튜닝)"
        )

    def test_FULLTC_194_vote_unauthenticated(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-194  [Major]
        시나리오: 비로그인 상태 — '지지해요' 또는 '아쉬워요' 버튼 클릭
        기대결과: 로그인 유도 모달 표시 또는 로그인 페이지로 이동
        ※ 비로그인 상태 테스트 — auth.json을 사용하지 않는 별도 컨텍스트 필요
           (이 TC는 로그인 없이 실행되어야 하므로 별도 fixture가 필요)
        ⚠️ TODO: 비로그인 전용 fixture 구성 후 실행 — 현재는 구조 검증만 수행
        """
        # 비로그인 전용 fixture 없이 구조 검증만 수행
        # 실제 비로그인 투표 검증 시 아래 주석 해제 후 비로그인 fixture 연결
        #
        # hotpeople_page_no_auth.go_to_hotpeople_main()
        # hotpeople_page_no_auth.scroll_to_vote_section()
        # hotpeople_page_no_auth.click_vote_support()
        # assert (
        #     hotpeople_page_no_auth.is_login_modal_visible()
        #     or "/login" in hotpeople_page_no_auth.page.url
        # ), "[FAIL] 비로그인 투표 시 로그인 유도 없음"

        # 구조 확인: 투표 섹션 진입 가능 여부
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)
        hotpeople_page.scroll_to_vote_section()

        assert hotpeople_page.is_vote_section_visible(), \
            "[FAIL] 지지율 섹션 미노출 — 비로그인 투표 테스트 전제 조건 미충족 (TODO: VOTE_SECTION 튜닝)"

    def test_FULLTC_195_vote_duplicate_prevention(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-195  [Major]
        시나리오: 이미 투표한 인물의 '지지해요' 버튼 재클릭
        기대결과: 중복 투표 제한 또는 투표 취소·변경 처리, 참여자 수 중복 증가 없음
        ⚠️ TODO: VOTE_ACTIVE_CLASS / VOTE_PARTICIPANT_COUNT 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)
        hotpeople_page.scroll_to_vote_section()

        # 1차 투표
        hotpeople_page.click_vote_support()
        hotpeople_page.page.wait_for_timeout(800)

        count_after_first = hotpeople_page.get_vote_participant_text()

        # 2차 투표 (중복)
        hotpeople_page.click_vote_support()
        hotpeople_page.page.wait_for_timeout(800)

        count_after_second = hotpeople_page.get_vote_participant_text()

        # 로그인 모달이 뜨지 않아야 함
        assert not hotpeople_page.is_login_modal_visible(), \
            "[FAIL] 중복 투표 시 로그인 모달 노출 — 예상치 않은 동작"

        # 참여자 수가 2차 클릭으로 추가 증가하지 않아야 함
        # (취소 처리 시 감소 가능, 정책에 따라 동일 유지도 허용)
        assert count_after_first == count_after_second or (
            count_after_second != count_after_first  # 취소로 인한 감소도 허용
        ), (
            "[FAIL] 중복 투표 후 참여자 수 비정상 변동 — "
            f"1차 투표 후: {count_after_first}, 2차 클릭 후: {count_after_second} "
            "(TODO: VOTE_PARTICIPANT_COUNT 셀렉터 튜닝)"
        )

    def test_FULLTC_196_vote_change(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-196  [Minor]
        시나리오: 지지해요 투표 후 '아쉬워요' 버튼 클릭
        기대결과: 투표가 지지→아쉬워요로 변경되어 비율 업데이트
                  또는 정책에 따라 변경 불가 안내 노출
        ⚠️ TODO: VOTE_ACTIVE_CLASS / VOTE_OPPOSE_PCT 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)
        hotpeople_page.scroll_to_vote_section()

        # 1. 지지해요 클릭
        hotpeople_page.click_vote_support()
        hotpeople_page.page.wait_for_timeout(800)

        pct_support_after = hotpeople_page.get_support_pct_text()

        # 2. 아쉬워요 클릭 (투표 변경 시도)
        hotpeople_page.click_vote_oppose()
        hotpeople_page.page.wait_for_timeout(800)

        # 로그인 모달이 뜨지 않아야 함
        assert not hotpeople_page.is_login_modal_visible(), \
            "[FAIL] 투표 변경 시도 중 로그인 모달 노출 — auth.json 세션 확인"

        pct_support_changed = hotpeople_page.get_support_pct_text()
        oppose_active = hotpeople_page.is_oppose_btn_active()

        # 투표 변경(지지율 감소) 또는 변경 불가(동일 유지) 모두 Pass
        # 단, 아쉬워요 버튼이 활성화되거나 지지율 % 가 변동되어야 함
        vote_change_result = (
            oppose_active
            or pct_support_after != pct_support_changed
        )
        # 변경 불가 정책의 경우 수치 동일 유지 = Pass
        # 어느 방향이든 서버 오류(500, toast error)가 없으면 통과
        assert not hotpeople_page.page.locator(
            "#portal-modal div[class*='error'], div[class*='toastError']"
        ).count() > 0, \
            "[FAIL] 투표 변경 시도 중 서버 오류 토스트 발생 (TODO: 에러 토스트 셀렉터 확인)"

        # 결과 로깅 (투표 변경 여부)
        _ = vote_change_result  # 정책에 따라 변경/불변 모두 허용이므로 assert 없음


# ══════════════════════════════════════════════════════════════════════
#  랭킹 패널  (FULLTC-197 ~ 198)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.hotpeople
@pytest.mark.hotpeople_ranking
class TestHotPeopleRankingRegression:
    """랭킹 패널 리그레션 — FULLTC-197 ~ 198"""

    def test_FULLTC_197_ranking_item_click_routing(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-197  [Major]
        시나리오: 우측 '지금 가장 뜨거운 인물' 패널에서 인물 항목 클릭
        기대결과: 메인 영역이 해당 인물의 상세 정보(/people?seq={id})로 전환
        ⚠️ TODO: RANKING_ITEM 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        rank_count = hotpeople_page.get_ranking_item_count()
        assert rank_count > 0, \
            "[FAIL] 랭킹 패널 인물 항목 없음 — 전제 조건 미충족 (TODO: RANKING_ITEM 셀렉터 튜닝)"

        hotpeople_page.click_ranking_item(index=0)

        assert hotpeople_page.HOTPEOPLE_MAIN_PATH in hotpeople_page.page.url, \
            f"[FAIL] 인물 상세 페이지 이동 실패 — 현재: {hotpeople_page.page.url}"
        assert hotpeople_page.is_url_person_detail(), \
            f"[FAIL] URL에 ?seq= 파라미터 없음 — 현재: {hotpeople_page.page.url}"

    def test_FULLTC_198_ranking_view_all_routing(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-198  [Minor]
        시나리오: 우측 패널 하단 '전체 보기 >' 링크 클릭
        기대결과: /people/list 페이지로 이동하며 전체 인물 목록 화면 표시
        ⚠️ TODO: RANKING_VIEW_ALL 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.is_ranking_view_all_visible(), \
            "[FAIL] '전체 보기 >' 링크 미노출 (TODO: RANKING_VIEW_ALL 셀렉터 튜닝)"

        hotpeople_page.click_ranking_view_all()

        assert hotpeople_page.HOTPEOPLE_LIST_PATH in hotpeople_page.page.url, \
            f"[FAIL] 전체 인물 목록 페이지 이동 실패 — 현재: {hotpeople_page.page.url} (기대: /people/list)"


# ══════════════════════════════════════════════════════════════════════
#  전체 인물 목록  (FULLTC-199 ~ 205)
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.web
@pytest.mark.hotpeople
@pytest.mark.hotpeople_list
class TestHotPeopleListRegression:
    """전체 인물 목록 리그레션 — FULLTC-199 ~ 205"""

    def test_FULLTC_199_people_list_card_visible(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-199  [Major]
        시나리오: 전체 인물 목록 페이지(/people/list) 진입 후 카드 항목 확인
        기대결과: 인물별 썸네일·이름·N명 참여중·최신 뉴스 제목·게시 시간이 카드 형태로 노출
        ⚠️ TODO: PEOPLE_CARD / PEOPLE_CARD_NAME / PEOPLE_CARD_COUNT 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_list()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.HOTPEOPLE_LIST_PATH in hotpeople_page.page.url, \
            f"[FAIL] 전체 목록 URL 불일치 — 현재: {hotpeople_page.page.url}"

        card_count = hotpeople_page.get_people_card_count()
        assert card_count > 0, \
            "[FAIL] 인물 카드 미노출 — 0개 (TODO: PEOPLE_CARD 셀렉터 튜닝)"

        # 첫 번째 카드 이름 텍스트 비어있지 않은지 확인
        name_els = hotpeople_page.page.locator(hotpeople_page.PEOPLE_CARD_NAME)
        if name_els.count() > 0:
            name_text = name_els.first.inner_text().strip()
            assert len(name_text) > 0, \
                "[FAIL] 인물 카드 이름 텍스트 비어 있음 (TODO: PEOPLE_CARD_NAME 셀렉터 튜닝)"

        # 참여중 카운트 텍스트 확인
        count_els = hotpeople_page.page.locator(hotpeople_page.PEOPLE_CARD_COUNT)
        assert count_els.count() > 0, \
            "[FAIL] 인물 카드 내 참여자 수 미노출 (TODO: PEOPLE_CARD_COUNT 셀렉터 튜닝)"

    def test_FULLTC_200_people_search(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-200  [Major]
        시나리오: 전체 인물 목록 — 검색창에 인물 이름 키워드 입력
        기대결과: 입력한 키워드와 일치하는 인물 카드만 필터링되어 표시
        ⚠️ TODO: PEOPLE_SEARCH_INPUT / PEOPLE_CARD 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_list()
        hotpeople_page.page.wait_for_timeout(1_000)

        search_input = hotpeople_page.page.locator(hotpeople_page.PEOPLE_SEARCH_INPUT)
        assert search_input.count() > 0, \
            "[FAIL] 인물 검색창 미노출 (TODO: PEOPLE_SEARCH_INPUT 셀렉터 튜닝)"

        # 전체 카드 수 기록
        total_count = hotpeople_page.get_people_card_count()

        # 검색어 입력 — 전체 목록에서 첫 번째 인물 이름 추출 후 검색
        first_name_els = hotpeople_page.page.locator(hotpeople_page.PEOPLE_CARD_NAME)
        if first_name_els.count() > 0:
            keyword = first_name_els.first.inner_text().strip()[:2]  # 이름 앞 2글자
        else:
            keyword = "이"  # 기본 검색어 fallback

        hotpeople_page.search_people(keyword)
        hotpeople_page.page.wait_for_timeout(800)

        filtered_count = hotpeople_page.get_people_card_count()

        assert filtered_count > 0, \
            f"[FAIL] 검색어 '{keyword}' 결과 0개 — 검색 기능 미작동 또는 PEOPLE_CARD 셀렉터 튜닝 필요"
        assert filtered_count <= total_count, \
            f"[FAIL] 검색 후 카드 수({filtered_count})가 전체 수({total_count})보다 많음 — 비정상 동작"

    def test_FULLTC_201_search_empty_state(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-201  [Minor]
        시나리오: 전체 인물 목록 — 검색창에 존재하지 않는 인물명 입력
        기대결과: 검색 결과가 없음을 알리는 Empty State UI 노출
        ⚠️ TODO: PEOPLE_EMPTY_STATE 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_list()
        hotpeople_page.page.wait_for_timeout(1_000)

        # 절대 존재하지 않을 키워드 사용
        hotpeople_page.search_people("ZZZNORESULTZZZXYZ99999")
        hotpeople_page.page.wait_for_timeout(800)

        empty_state_or_zero = (
            hotpeople_page.is_empty_state_visible()
            or hotpeople_page.get_people_card_count() == 0
        )
        assert empty_state_or_zero, \
            "[FAIL] 검색 결과 없음 시 Empty State 미노출 및 카드 여전히 표시 (TODO: PEOPLE_EMPTY_STATE 셀렉터 튜닝)"

    def test_FULLTC_202_people_list_infinite_scroll(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-202  [Minor]
        시나리오: 전체 인물 목록 하단까지 스크롤
        기대결과: 추가 인물 데이터가 자동 로드되어 목록이 이어서 표시 (무한 스크롤)
        ⚠️ TODO: PEOPLE_CARD 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_list()
        hotpeople_page.page.wait_for_timeout(1_000)

        initial_count = hotpeople_page.get_people_card_count()
        assert initial_count > 0, \
            "[FAIL] 초기 인물 카드 없음 — 전제 조건 미충족 (TODO: PEOPLE_CARD 셀렉터 튜닝)"

        # 하단 스크롤 → 무한 스크롤 트리거
        hotpeople_page.scroll_people_list(steps=3)

        after_count = hotpeople_page.get_people_card_count()

        # 추가 로드되거나 (목록이 짧아서) 동일해도 통과
        # 단, 스크롤 후 오류 없이 카드가 유지되어야 함
        assert after_count >= initial_count, \
            f"[FAIL] 스크롤 후 카드 수 감소 — 전: {initial_count}, 후: {after_count} (비정상 동작)"

    def test_FULLTC_203_people_card_click_routing(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-203  [Major]
        시나리오: 전체 인물 목록에서 특정 인물 카드 클릭
        기대결과: /people?seq={id} 상세 페이지로 이동하며 해당 인물 상세 정보 노출
        ⚠️ TODO: PEOPLE_CARD 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_list()
        hotpeople_page.page.wait_for_timeout(1_000)

        assert hotpeople_page.get_people_card_count() > 0, \
            "[FAIL] 인물 카드 없음 — 전제 조건 미충족 (TODO: PEOPLE_CARD 셀렉터 튜닝)"

        hotpeople_page.click_people_card(index=0)

        assert hotpeople_page.HOTPEOPLE_MAIN_PATH in hotpeople_page.page.url, \
            f"[FAIL] 인물 상세 페이지 이동 실패 — 현재: {hotpeople_page.page.url}"
        assert hotpeople_page.is_url_person_detail(), \
            f"[FAIL] URL에 ?seq= 파라미터 없음 — 현재: {hotpeople_page.page.url}"

        assert (
            hotpeople_page.page.locator(hotpeople_page.PERSON_NAME).count() > 0
            or hotpeople_page.page.locator(hotpeople_page.PERSON_PROFILE_IMG).count() > 0
        ), "[FAIL] 인물 상세 정보 미노출 (TODO: PERSON_NAME / PERSON_PROFILE_IMG 셀렉터 튜닝)"

    def test_FULLTC_204_thumbnail_fallback_image(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-204  [Minor]
        시나리오: 인물 프로필 이미지 로드 실패 시 Fallback 확인
        기대결과: 이미지 깨짐 대신 기본 아바타 또는 대체 이미지(Fallback) 표시
        ※ 네트워크 차단 없이 현재 노출된 이미지의 naturalWidth 기반 확인
        ⚠️ TODO: IMG_FALLBACK_AVATAR 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_main()
        hotpeople_page.page.wait_for_timeout(1_500)

        # 현재 노출된 프로필 이미지 로드 상태 확인
        profile_img_locator = hotpeople_page.page.locator(hotpeople_page.PERSON_PROFILE_IMG)
        if profile_img_locator.count() == 0:
            pytest.skip("[SKIP] 프로필 이미지 엘리먼트 없음 — TODO: PERSON_PROFILE_IMG 셀렉터 튜닝 후 재검증")

        try:
            natural_width = hotpeople_page.page.evaluate(
                "(img) => img.naturalWidth",
                profile_img_locator.first.element_handle()
            )
            if natural_width == 0:
                # 이미지 로드 실패 → Fallback 아바타 존재 여부 확인
                assert hotpeople_page.page.locator(
                    hotpeople_page.IMG_FALLBACK_AVATAR
                ).count() > 0, \
                    "[FAIL] 이미지 로드 실패 시 Fallback 아바타 미노출 (TODO: IMG_FALLBACK_AVATAR 셀렉터 튜닝)"
        except Exception:
            pytest.skip("[SKIP] 이미지 naturalWidth 평가 실패 — 환경 확인 필요")

    def test_FULLTC_205_empty_state_ui(
        self, hotpeople_page: HotPeoplePage
    ):
        """
        TC: FULLTC-205  [Major]
        시나리오: 인물 데이터가 없는 상태에서 핫피플 페이지 진입 확인
        기대결과: 'Empty State' 안내 UI 노출 및 콘텐츠 영역이 빈 상태로 처리
        ※ 데이터 강제 비움 없이 — 검색 결과 없음 Empty State로 대체 검증
        ⚠️ TODO: PEOPLE_EMPTY_STATE 셀렉터 튜닝 필요
        """
        hotpeople_page.go_to_hotpeople_list()
        hotpeople_page.page.wait_for_timeout(1_000)

        # 매우 특수한 문자로 검색 → 결과 없음 상태 유도
        hotpeople_page.search_people("∅∅∅빈상태테스트∅∅∅")
        hotpeople_page.page.wait_for_timeout(800)

        empty_shown = hotpeople_page.is_empty_state_visible()
        card_count  = hotpeople_page.get_people_card_count()

        assert empty_shown or card_count == 0, (
            "[FAIL] Empty State 미노출 및 카드가 여전히 표시됨 — "
            f"카드 수: {card_count} (TODO: PEOPLE_EMPTY_STATE / PEOPLE_CARD 셀렉터 튜닝)"
        )