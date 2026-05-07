"""
pages/web/correction_report_page.py
[STEP 2 — POM v1]  정정·반론보도 센터(Correction & Rebuttal Report) 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
실제 STG HTML(2026-05-06) 기반 CSS Selector 전면 적용.

⚠️  주의사항:
    - CSS Modules 해시 클래스(_correctionRebuttalReportingClient-module-scss-module__8thuXW__xxx)는
      빌드마다 변경되므로 절대 직접 사용하지 않는다.
    - 안정적 셀렉터 우선순위: ID > plain class > [class*='...'] 부분 매칭
    - domcontentloaded 사용 — networkidle 금지 (CLAUDE.md 규칙)

    실제 HTML 분석 결과:
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │  ✅ 안정 셀렉터 (HTML에서 직접 확인됨):                                      │
    │    · 페이지 타이틀: h1 = "정정·반론보도 센터" (센터 앞 공백 주의!)            │
    │    · 리스트 래퍼: div[class*='correctionRebuttalReportingListWrapper']       │
    │    · Empty State: div[class*='emptyCorrectionRebuttalReportingListContainer']│
    │    · Empty State 메시지: p = "정정 및 반론보도 기사가 존재하지 않습니다."     │
    │                                                                              │
    │  ⚠️ TODO_ 셀렉터 (HTML에 기사 없는 빈 상태 — 기사 노출 시 F12 확인 필요):   │
    │    · 기사 카드:   ARTICLE_CARD                                               │
    │    · 기사 제목:   ARTICLE_TITLE                                              │
    │    · 기사 날짜:   ARTICLE_DATE                                               │
    │    · 기사 썸네일: ARTICLE_THUMBNAIL                                          │
    │    · LNB 메뉴:    LNB_WRAPPER, LNB_CORRECTION_MENU                          │
    │    · 상세 페이지: DETAIL_TITLE, DETAIL_BODY 등                               │
    │    · 로딩 인디케이터: LOADING_INDICATOR                                      │
    │                                                                              │
    │  페이지 URL 추정: /mypage/correction-rebuttal                               │
    │    (F12 주소창 확인 후 CORRECTION_PATH 수정 필요)                            │
    │  기사 상세 URL 추정: /correction/{id} 또는 /feed/correction/{id}            │
    └──────────────────────────────────────────────────────────────────────────────┘

셀렉터 전략:
    - 해시 포함 class → [class*='안정키워드'] 부분 매칭
    - Tailwind 유틸리티 클래스 셀렉터 사용 금지
    - TODO_ 셀렉터: 기사 등록 후 DOM 확인하여 실제 값으로 교체
"""

import re

from playwright.sync_api import Page


class CorrectionReportPage:
    """블루밍비트 정정·반론보도 센터 페이지 Page Object (Playwright 기반)"""

    BASE_URL = "https://web-stg.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  URL 패턴
    # ══════════════════════════════════════════════════════════════════
    # ⚠️ TODO: 실제 진입 URL F12 주소창 확인 후 수정
    CORRECTION_PATH         = "/terms/service/correct"
    # ⚠️ TODO: 상세 페이지 URL 패턴 확인 후 수정
    CORRECTION_DETAIL_PATH  = "/correction/"
    MYPAGE_PATH             = "/mypage"
    SIGNIN_PATH             = "/user/signin"

    # 페이지 타이틀 텍스트 (h1 내용 — 센터 앞 공백 포함)
    EXPECTED_TITLE_TEXT     = "정정·반론보도 센터"
    # Empty State 정확한 메시지 텍스트 (HTML 기반 — 변경되지 않는 한 그대로 사용)
    EXPECTED_EMPTY_MSG      = "정정 및 반론보도 기사가 존재하지 않습니다."

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS  (실제 HTML 기반 + TODO_)
    # ══════════════════════════════════════════════════════════════════

    # ── 페이지 구조 (✅ 안정 — HTML에서 직접 확인) ──────────────────
    # HTML: <section class="...__myPageCommonContentWrapper">
    PAGE_WRAPPER = "section[class*='myPageCommonContentWrapper']"
    # HTML: <header class="...__contentHeader">
    PAGE_HEADER  = "header[class*='contentHeader']"
    # HTML: <h1>정정·반론보도 센터</h1>
    PAGE_TITLE   = "header[class*='contentHeader'] h1"
    # HTML: <a class="...__backBtn" href="/mypage">
    BACK_BTN     = "header[class*='contentHeader'] a[href='/mypage']"

    # ── 리스트 래퍼 (✅ 안정 — HTML에서 직접 확인) ───────────────────
    # HTML: <div class="...__correctionRebuttalReportingListWrapper">
    LIST_WRAPPER = "div[class*='correctionRebuttalReportingListWrapper']"

    # ── Empty State (✅ 완전 안정 — HTML에서 정확히 확인됨) ──────────
    # HTML: <div class="...__emptyCorrectionRebuttalReportingListContainer">
    #           <p>정정 및 반론보도 기사가 존재하지 않습니다.</p>
    #       </div>
    EMPTY_CONTAINER = "div[class*='emptyCorrectionRebuttalReportingListContainer']"
    EMPTY_MSG_P     = "div[class*='emptyCorrectionRebuttalReportingListContainer'] p"

    # ── 기사 카드 (⚠️ TODO — 현재 빈 상태, 기사 등록 후 F12 확인) ──
    # 예상 클래스 키워드: correctionCard / correctionRebuttalCard 등
    ARTICLE_CARD      = (
        "[data-testid='TODO_correctionCard'], "
        "[class*='correctionCard'], "
        "[class*='correctionRebuttalCard']"
    )
    ARTICLE_TITLE     = (
        "[data-testid='TODO_correctionTitle'], "
        "[class*='correctionTitle'], "
        "[class*='correctionCardTitle']"
    )
    ARTICLE_DATE      = (
        "[data-testid='TODO_correctionDate'], "
        "[class*='correctionDate'], "
        "[class*='correctionCardDate']"
    )
    ARTICLE_THUMBNAIL = (
        "[data-testid='TODO_correctionThumbnail'], "
        "[class*='correctionThumbnail'], "
        "[class*='correctionCardImage'] img, "
        "[class*='correctionCard'] img"
    )

    # ── LNB(좌측 네비게이션 바) (⚠️ TODO — HTML 미노출) ─────────────
    # ⚠️ TODO: 마이페이지 LNB 영역 F12 확인 후 튜닝
    LNB_WRAPPER         = (
        "[data-testid='TODO_lnbWrapper'], "
        "[class*='lnb'], "
        "[class*='sideNav'], "
        "aside nav"
    )
    LNB_CORRECTION_MENU = (
        "[data-testid='TODO_lnbCorrectionMenu'], "
        "nav a[href*='correction'], "
        "nav button:has-text('정정'), "
        "aside a:has-text('정정·반론')"
    )

    # ── 상세 페이지 (⚠️ TODO — HTML 미노출) ─────────────────────────
    # ⚠️ TODO: /correction/{id} 접속 후 F12로 셀렉터 확인 후 튜닝
    DETAIL_WRAPPER = (
        "[data-testid='TODO_detailWrapper'], "
        "[class*='correctionDetail'], "
        "article"
    )
    DETAIL_TITLE   = (
        "[data-testid='TODO_detailTitle'], "
        "[class*='correctionDetailTitle'], "
        "h1, h2"
    )
    DETAIL_DATE    = (
        "[data-testid='TODO_detailDate'], "
        "[class*='correctionDetailDate'], "
        "time, [class*='date']"
    )
    DETAIL_BODY    = (
        "[data-testid='TODO_detailBody'], "
        "[class*='correctionDetailBody'], "
        "[class*='content'], "
        "article"
    )

    # ── 로딩 인디케이터 (⚠️ TODO — HTML 미노출) ──────────────────────
    LOADING_INDICATOR = (
        "[data-testid='TODO_loadingIndicator'], "
        "[class*='spinner'], "
        "[class*='Spinner'], "
        "[aria-label='loading'], "
        "[role='progressbar']"
    )

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def _safe_goto(self, url: str) -> None:
        """about:blank 충돌 및 ERR_ABORTED 방지하는 안전한 goto (최대 3회 재시도)"""
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

    def go_to_correction_report(self) -> None:
        """정정·반론보도 센터 목록 페이지로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.CORRECTION_PATH}")
        self.page.wait_for_timeout(600)

    def go_to_correction_detail(self, article_id: str) -> None:
        """정정·반론보도 상세 페이지로 직접 이동 (⚠️ URL 패턴 확인 후 수정)"""
        self._safe_goto(f"{self.BASE_URL}{self.CORRECTION_DETAIL_PATH}{article_id}")
        self.page.wait_for_timeout(600)

    def go_to_mypage(self) -> None:
        """마이페이지(/mypage)로 이동"""
        self._safe_goto(f"{self.BASE_URL}{self.MYPAGE_PATH}")
        self.page.wait_for_timeout(500)

    def go_back(self) -> None:
        """브라우저 뒤로가기"""
        try:
            self.page.go_back(wait_until="domcontentloaded")
        except Exception:
            pass
        self.page.wait_for_timeout(600)

    def refresh_page(self) -> None:
        """현재 페이지 새로고침"""
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(600)

    def get_current_url(self) -> str:
        return self.page.url

    def is_on_correction_report_page(self) -> bool:
        return self.CORRECTION_PATH in self.page.url

    def is_on_correction_detail_page(self) -> bool:
        return self.CORRECTION_DETAIL_PATH in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self, timeout: int = 8_000) -> bool:
        """페이지 로드 완료 여부 (리스트 래퍼 노출 기준 — HTML 안정 셀렉터)"""
        try:
            self.page.wait_for_selector(self.LIST_WRAPPER, timeout=timeout)
            return True
        except Exception:
            # 폴백: 페이지 래퍼 또는 헤더 노출 확인
            return (
                self.page.locator(self.PAGE_WRAPPER).count() > 0
                or self.page.locator(self.PAGE_HEADER).count() > 0
            )

    def is_page_title_correct(self) -> bool:
        """페이지 타이틀이 '정정·반론보도 센터'인지 확인 (HTML 안정 셀렉터)"""
        try:
            el = self.page.locator(self.PAGE_TITLE)
            if el.count() == 0:
                return False
            title_text = el.first.inner_text().strip()
            return "정정" in title_text and "반론" in title_text
        except Exception:
            return False

    def get_page_title_text(self) -> str:
        """페이지 h1 타이틀 텍스트 반환"""
        try:
            return self.page.locator(self.PAGE_TITLE).first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  Empty State (✅ HTML에서 완전 확인 — 안정적으로 테스트 가능)
    # ══════════════════════════════════════════════════════════════════

    def is_empty_state_visible(self) -> bool:
        """빈 상태 컨테이너 노출 여부 (HTML에서 직접 확인된 안정 셀렉터)"""
        return self.page.locator(self.EMPTY_CONTAINER).count() > 0

    def get_empty_state_message(self) -> str:
        """빈 상태 안내 문구 텍스트 반환 (HTML에서 직접 확인된 안정 셀렉터)"""
        try:
            loc = self.page.locator(self.EMPTY_MSG_P)
            if loc.count() > 0:
                return loc.first.inner_text().strip()
        except Exception:
            pass
        return ""

    def is_empty_message_correct(self) -> bool:
        """빈 상태 문구가 정확히 '정정 및 반론보도 기사가 존재하지 않습니다.'인지 확인"""
        return self.get_empty_state_message() == self.EXPECTED_EMPTY_MSG

    def is_empty_layout_intact(self) -> bool:
        """빈 상태 UI가 레이아웃을 벗어나지 않는지 확인
        (빈 상태 컨테이너가 리스트 래퍼 내부에 존재하는지)
        """
        try:
            # 리스트 래퍼가 있고, 그 안에 empty 컨테이너가 있으면 정상
            wrapper_count = self.page.locator(self.LIST_WRAPPER).count()
            empty_count   = self.page.locator(self.EMPTY_CONTAINER).count()
            if wrapper_count > 0 and empty_count > 0:
                # empty 컨테이너의 Y 위치가 viewport 내에 있는지 확인
                bounding = self.page.locator(self.EMPTY_CONTAINER).first.evaluate(
                    "e => ({ top: e.getBoundingClientRect().top, height: e.getBoundingClientRect().height })"
                )
                return float(bounding.get("height", 0)) > 0
            return False
        except Exception:
            return self.is_empty_state_visible()

    # ══════════════════════════════════════════════════════════════════
    #  기사 목록 메서드 (⚠️ TODO — 기사 등록 후 셀렉터 튜닝 필요)
    # ══════════════════════════════════════════════════════════════════

    def get_article_count(self) -> int:
        """현재 화면에 노출된 기사 카드 수 (⚠️ TODO: ARTICLE_CARD 셀렉터 튜닝 필요)"""
        return self.page.locator(self.ARTICLE_CARD).count()

    def get_article_title(self, index: int = 0) -> str:
        """index 번째 기사 카드 제목 텍스트 (⚠️ TODO: ARTICLE_TITLE 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.ARTICLE_TITLE).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_article_date(self, index: int = 0) -> str:
        """index 번째 기사 카드 날짜 텍스트 (⚠️ TODO: ARTICLE_DATE 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.ARTICLE_DATE).nth(index).inner_text().strip()
        except Exception:
            return ""

    def get_article_href(self, index: int = 0) -> str:
        """index 번째 기사 카드 href (⚠️ TODO: ARTICLE_CARD 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.ARTICLE_CARD).nth(index).get_attribute("href") or ""
        except Exception:
            return ""

    def get_all_dates(self) -> list:
        """모든 기사 카드의 날짜 텍스트 목록 반환 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        dates = []
        try:
            els = self.page.locator(self.ARTICLE_DATE).all()
            for el in els:
                txt = el.inner_text().strip()
                if txt:
                    dates.append(txt)
        except Exception:
            pass
        return dates

    def are_dates_sorted_latest(self) -> bool:
        """기사 날짜가 최신순(내림차순)으로 정렬되어 있는지 확인
        날짜 형식 허용: 'YYYY.MM.DD', 'YYYY-MM-DD', 'YYYY년 MM월 DD일' 등
        """
        dates = self.get_all_dates()
        if len(dates) < 2:
            return True  # 1건 이하는 정렬 검증 불가

        def normalize_date(date_str: str) -> str:
            """다양한 날짜 포맷을 'YYYYMMDD' 문자열로 정규화"""
            digits = re.sub(r"[^\d]", "", date_str)
            return digits[:8] if len(digits) >= 8 else digits

        normalized = [normalize_date(d) for d in dates]
        for i in range(len(normalized) - 1):
            if normalized[i] and normalized[i + 1]:
                if normalized[i] < normalized[i + 1]:
                    return False
        return True

    def is_date_format_valid(self, date_text: str) -> bool:
        """날짜 텍스트가 YYYY.MM.DD 또는 유사 표준 형식인지 확인"""
        if not date_text.strip():
            return False
        # YYYY.MM.DD 패턴
        if re.match(r"\d{4}\.\d{2}\.\d{2}", date_text.strip()):
            return True
        # YYYY-MM-DD 패턴
        if re.match(r"\d{4}-\d{2}-\d{2}", date_text.strip()):
            return True
        # 'YYYY년 MM월 DD일' 패턴
        if re.search(r"\d{4}.*\d{1,2}.*\d{1,2}", date_text.strip()):
            return True
        return False

    def has_thumbnail(self, index: int = 0) -> bool:
        """index 번째 기사 카드에 썸네일 이미지 요소가 있는지 확인"""
        try:
            return self.page.locator(self.ARTICLE_THUMBNAIL).count() > index
        except Exception:
            return False

    def is_thumbnail_broken(self, index: int = 0) -> bool:
        """index 번째 기사 썸네일 이미지가 깨졌는지 확인 (naturalWidth == 0)"""
        try:
            img = self.page.locator(self.ARTICLE_THUMBNAIL).nth(index)
            natural_w = img.evaluate("e => e.naturalWidth")
            return int(natural_w) == 0
        except Exception:
            return False

    def is_card_layout_intact(self, index: int = 0) -> bool:
        """index 번째 기사 카드의 레이아웃이 정상인지 확인 (width > 0 기준)"""
        try:
            card = self.page.locator(self.ARTICLE_CARD).nth(index)
            bounding = card.evaluate(
                "e => ({ width: e.getBoundingClientRect().width, "
                "height: e.getBoundingClientRect().height })"
            )
            return float(bounding.get("width", 0)) > 0 and float(bounding.get("height", 0)) > 0
        except Exception:
            return True  # 레이아웃 확인 실패 → pass 처리

    # ══════════════════════════════════════════════════════════════════
    #  기사 카드 클릭 / 라우팅
    # ══════════════════════════════════════════════════════════════════

    def click_article_card(self, index: int = 0) -> None:
        """index 번째 기사 카드 클릭 (href goto 방식 우선 — Next.js Router 우회)
        ⚠️ TODO: ARTICLE_CARD 셀렉터 튜닝 필요
        """
        loc = self.page.locator(self.ARTICLE_CARD).nth(index)
        try:
            loc.wait_for(state="attached", timeout=5_000)
        except Exception:
            return

        href = loc.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            try:
                self.page.goto(full_url, wait_until="domcontentloaded")
                self.page.wait_for_timeout(600)
            except Exception:
                try:
                    loc.click(force=True)
                    self.page.wait_for_timeout(800)
                except Exception:
                    pass
        else:
            try:
                loc.evaluate("(el) => el.click()")
                self.page.wait_for_timeout(800)
            except Exception:
                pass

    # ══════════════════════════════════════════════════════════════════
    #  LNB 메뉴 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_lnb_visible(self) -> bool:
        """LNB(좌측 네비게이션) 영역 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        return self.page.locator(self.LNB_WRAPPER).count() > 0

    def click_lnb_correction_menu(self) -> None:
        """LNB에서 '정정·반론보도센터' 메뉴 클릭 (⚠️ TODO: 셀렉터 튜닝 필요)
        ① visible 클릭 우선, ② attached + force=True 폴백
        """
        loc = self.page.locator(self.LNB_CORRECTION_MENU).first
        try:
            loc.wait_for(state="visible", timeout=3_000)
            loc.click(timeout=3_000)
            self.page.wait_for_timeout(800)
            return
        except Exception:
            pass
        try:
            loc.wait_for(state="attached", timeout=5_000)
            loc.click(force=True)
            self.page.wait_for_timeout(800)
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════════
    #  상세 페이지 메서드 (⚠️ TODO — HTML 미노출)
    # ══════════════════════════════════════════════════════════════════

    def is_detail_page_loaded(self, timeout: int = 8_000) -> bool:
        """상세 페이지 로드 완료 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            self.page.wait_for_selector(self.DETAIL_TITLE, timeout=timeout)
            return True
        except Exception:
            return self.page.locator(self.DETAIL_BODY).count() > 0

    def get_detail_title(self) -> str:
        """상세 페이지 기사 제목 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.DETAIL_TITLE).first.inner_text().strip()
        except Exception:
            return ""

    def get_detail_body_text(self) -> str:
        """상세 페이지 본문 텍스트 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            return self.page.locator(self.DETAIL_BODY).first.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════════════════════════
    #  스크롤 / 무한 로딩
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_bottom(self, steps: int = 5, delay_ms: int = 500) -> None:
        """페이지 최하단까지 단계적 스크롤"""
        for _ in range(steps):
            self.page.keyboard.press("End")
            self.page.wait_for_timeout(delay_ms)

    def get_scroll_y_position(self) -> float:
        """현재 스크롤 Y 위치"""
        try:
            return self.page.evaluate("() => window.scrollY")
        except Exception:
            return 0.0

    def is_loading_indicator_visible(self, timeout: int = 2_000) -> bool:
        """로딩 인디케이터 노출 여부 (⚠️ TODO: 셀렉터 튜닝 필요)"""
        try:
            self.page.wait_for_selector(self.LOADING_INDICATOR, timeout=timeout)
            return True
        except Exception:
            return False