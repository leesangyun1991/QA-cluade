"""
pages/web/community_page.py
[STEP 2 — POM 최신화 v5]  커뮤니티 도메인 Page Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
셀렉터 전략:
    - CSS Modules 해시 클래스 직접 사용 금지 → [class*='...'] 부분 매칭
    - 안정적 셀렉터 우선순위: ID > aria-* > data-* > 시맨틱 태그+구조 > 안정 CSS 클래스
    - Next.js SPA 링크: locator.get_attribute("href") + page.goto() 방식
    - 가상 스크롤: [data-testid='virtuoso-item-list'] (Virtuoso 라이브러리)
    - Portal 모달: 블루밍비트는 모달을 <div id="portal-modal"> 내부에 렌더링
      → 모든 모달 셀렉터는 반드시 #portal-modal 접두사로 스코핑
      → Quill.js 에디터가 인라인(배경)과 모달 내부 양쪽에 존재하므로 혼선 주의
    - 커뮤니티 URL 패턴:
        홈(최신)  : /community
        추천 탭   : /community?tab=rank
        예측 탭   : /community?tab=prediction
        게시글 상세: /community/post/{id}
"""

from playwright.sync_api import Page


class CommunityPage:
    """블루밍비트 커뮤니티 홈 / 상세 Page Object (Playwright 기반)"""

    BASE_URL    = "https://web-stg.bloomingbit.io"
    BASE_URL_EN = "https://web-stg-en.bloomingbit.io"
    BASE_URL_JA = "https://web-stg-ja.bloomingbit.io"

    # ══════════════════════════════════════════════════════════════════
    #  SELECTORS
    # ══════════════════════════════════════════════════════════════════

    # ── GNB (뉴스 영역과 동일한 GNB 구조 공유) ──────────────────────────
    GNB_HEADER         = "header#headerContainer"
    GNB_COMMUNITY_TAB  = "#menuWithMySettingContainer nav a[data-label='커뮤니티']"
    GNB_TAB_LIST       = "#menuWithMySettingContainer nav ul li a"
    GNB_LOGO           = "#logoWithStatLiveContainer > a[href='/']"
    GNB_SEARCH_ICON    = "#menuWithMySettingContainer a[href='/search']"

    # ── 커뮤니티 홈 — 페이지 컨테이너 ───────────────────────────────────
    COMMUNITY_HOME     = "main#communityPageContainer"

    # ── 커뮤니티 홈 — 탭 네비게이션 ─────────────────────────────────────
    # 탭 목록 전체 (feed section 내 button 요소들)
    TAB_LIST           = "#communityFeedSection button[aria-label]"
    # 최신 탭 버튼 (aria-label 기반 — 빌드 해시에 무관하게 안정적)
    TAB_LATEST         = "button[aria-label='click 최신 tab']"
    # 추천 탭 버튼 (URL: ?tab=rank)
    TAB_RECOMMENDED    = "button[aria-label='click 추천 tab']"
    # 예측 탭 버튼 (URL: ?tab=prediction)
    TAB_PREDICTION     = "button[aria-label='click 예측 tab']"
    # 현재 활성 탭 (CSS 모듈 isSelected 클래스 부분 매칭)
    TAB_ACTIVE         = "#communityFeedSection button[class*='isSelected']"

    # ── 커뮤니티 홈 — 게시글 목록 ────────────────────────────────────────
    # 가상 스크롤 아이템 컨테이너 (Virtuoso)
    POST_LIST          = "[data-testid='virtuoso-item-list']"
    # 개별 게시글 아이템 — <a class="*__postFeedItemContainer*" href="/community/post/{id}">
    POST_ITEM          = "a[class*='postFeedItemContainer']"
    # 게시글 링크 (POST_ITEM과 동일 — href 추출용)
    POST_ITEM_LINK     = "a[class*='postFeedItemContainer']"
    # 작성자명 — writerProfileInfo 내 첫 번째 <p>
    POST_AUTHOR        = "a[class*='postFeedItemContainer'] div[class*='writerProfileInfo'] p:first-child"
    # 예측률 배지 (예측 탭에서만 표시)
    POST_PREDICTION_BADGE = "span[class*='predictionBadge']"
    # 내용 미리보기 텍스트
    POST_CONTENT_PREVIEW = "div[class*='contentText']"
    # 좋아요 버튼/영역 (likeBox 클래스 부분 매칭)
    POST_LIKE_BTN      = "button[class*='likeBox']"
    # 좋아요 카운트 숫자
    POST_LIKE_COUNT    = "span[class*='likeCount']"
    # 댓글 버튼/영역
    POST_COMMENT_BTN   = "button[class*='commentBox']"
    # 댓글 카운트 숫자
    POST_COMMENT_COUNT = "span[class*='commentCount']"

    # ── 커뮤니티 홈 — 인라인 글쓰기 영역 (피드 상단, 모달 밖) ─────────────
    # Quill.js 에디터 — placeholder 속성으로 고유 식별 (인라인 에디터)
    WRITE_INLINE_AREA  = ".ql-editor[data-placeholder='지금 떠오른 생각을 남겨보세요']"
    # 활성화 후 입력 필드 (동일 엘리먼트 재사용)
    WRITE_INLINE_INPUT = ".ql-editor[data-placeholder='지금 떠오른 생각을 남겨보세요']"
    # 비로그인 시 로그인 유도 문구 영역
    WRITE_LOGIN_PROMPT = "div[class*='loginPrompt']"

    # ── 커뮤니티 홈 — 주목 인물 섹션 (우측 사이드바) ──────────────────────
    HOTPERSON_SECTION  = "section#hotPeopleEntrySection"
    HOTPERSON_VIEW_ALL = "section#hotPeopleEntrySection a[href='/people/list']"
    HOTPERSON_CARD     = "#hotPeopleEntrySection .hotPeopleEntryContainer .swiper-slide a"
    # 인물 아바타 이미지
    HOTPERSON_AVATAR   = "#hotPeopleEntrySection .swiper-slide a img"
    # 인물 이름 텍스트 — <h3> 태그 (STG HTML 확인)
    HOTPERSON_NAME     = "#hotPeopleEntrySection .swiper-slide a h3"
    # 참여 인원 수 — <span> (STG HTML 확인: "1명 참여중")
    HOTPERSON_COUNT    = "#hotPeopleEntrySection .swiper-slide a span"

    # ── 우측 사이드바 — 커뮤니티 프로필 / 글쓰기 버튼 ─────────────────────
    # 사이드바 프로필 컨테이너
    SIDEBAR_PROFILE_CONTAINER     = "section#communityProfileContainer"
    # '게시글 쓰기' 버튼 (plain class — 해시 없음)
    SIDEBAR_POST_WRITE_BTN        = "button.communityProfileEditButton"
    # '예측글 쓰기' 버튼
    SIDEBAR_PREDICTION_WRITE_BTN  = "button[class*='communityPredictionWriteButton']"
    # 예측 탭 화면 내 예측글 인라인 입력 (placeholder: '어떤 코인을 예측할까요?')
    PREDICTION_INLINE_AREA        = ".ql-editor[data-placeholder='어떤 코인을 예측할까요?']"

    # ── 게시글 작성 모달 ──────────────────────────────────────────────
    # ※ 블루밍비트는 모달을 #portal-modal 내부에 렌더링함
    #   인라인 에디터와 Quill/toolbar가 동일 셀렉터를 공유하므로
    #   모달 관련 셀렉터는 반드시 #portal-modal 접두사로 스코핑
    #
    # 모달 콘텐츠 컨테이너
    POST_MODAL             = "#portal-modal .modal-content"
    # Quill.js 텍스트 입력 영역 (portal 스코프 — 인라인 에디터 충돌 방지)
    POST_MODAL_INPUT       = "#portal-modal .ql-editor"
    # 글자수 카운터 — #customToolbar 내부 <p translate="no">0 / 3000</p> (descendant)
    # ※ HTML 확인: <p> 는 #customToolbar 의 자손(descendant), 형제(sibling)가 아님
    POST_MODAL_CHAR_COUNT  = "#customToolbar p[translate='no']"
    # 이미지 첨부 아이콘 버튼 (portal customToolbar 내 첫 번째 버튼)
    POST_MODAL_IMAGE_BTN   = "#portal-modal #customToolbar button:first-of-type"
    # 이미지 파일 input (portal 외부에서도 열릴 수 있음 — 스코프 없음)
    POST_MODAL_IMAGE_INPUT = "input[type='file'][accept*='image']"
    # 이미지 미리보기 영역 (portal 스코프)
    POST_MODAL_IMAGE_PREVIEW = "#portal-modal div[class*='previewImage'], #portal-modal img[class*='previewImg']"
    # 관련 코인 추가 버튼 — #customToolbar 내부(인라인 에디터) + portal 모달 양쪽 커버
    # ※ HTML 확인: 버튼은 #customToolbar 하위에 존재, #portal-modal 내부가 아님
    POST_MODAL_COIN_BTN    = "#customToolbar button:has(span:text-is('관련 코인')), #portal-modal button:has(span:text-is('관련 코인'))"
    # 코인 검색 드롭다운 — portal 스코프 우선, 없으면 전역 fallback
    # ※ 관련 코인 버튼 클릭 후 드롭다운이 portal 내부 또는 body 직하 별도 portal에 렌더링될 수 있음
    POST_MODAL_COIN_DROPDOWN = (
        "#portal-modal div[class*='coinSearch'], "
        "#portal-modal ul[class*='coinList'], "
        "#portal-modal input[placeholder*='코인'], "
        "div[class*='coinSearch'], "
        "ul[class*='coinList'], "
        "div[class*='coinDropdown']"
    )
    # 코인 검색 입력 (portal 스코프)
    POST_MODAL_COIN_SEARCH = "#portal-modal input[placeholder*='코인']"
    # 추가된 코인 태그 (portal 스코프)
    POST_MODAL_COIN_TAG    = "#portal-modal span[class*='coinTag'], #portal-modal button[class*='selectedCoin']"
    # '등록' 버튼 — #customToolbar 내부 descendant + portal 모달 양쪽 커버
    # ※ HTML 확인: <button><span>등록</span></button> 은 #customToolbar 의 자손
    POST_MODAL_SUBMIT_BTN  = "#customToolbar button:has(span:text-is('등록')), #portal-modal button:has(span:text-is('등록'))"
    # 모달 닫기(X) 버튼 — portal 스코프 (class*='close' 또는 aria-label 기반)
    POST_MODAL_CLOSE_BTN   = "#portal-modal button[class*='close'], #portal-modal button[aria-label*='닫기'], #portal-modal button[aria-label*='close']"
    # 파일 형식 오류 메시지 (portal 스코프)
    POST_MODAL_FILE_ERROR  = "#portal-modal p[class*='error'], #portal-modal span[class*='error']"

    # ── 예측글 작성 모달 ──────────────────────────────────────────────
    # ※ 예측 모달도 #portal-modal에 렌더링됨
    #   is_prediction_modal_visible()에서 내부 코인 검색창 유무로 게시글 모달과 구분
    PREDICTION_MODAL               = "#portal-modal .modal-content"
    # 코인 선택 검색창 (portal 스코프)
    PREDICTION_COIN_SEARCH         = "#portal-modal input[placeholder*='코인']"
    # 코인 검색 결과 목록 (portal 스코프)
    PREDICTION_COIN_RESULT         = "#portal-modal ul[class*='coinResult'], #portal-modal div[class*='searchResult']"
    # 선택된 코인 표시 영역 (portal 스코프)
    PREDICTION_SELECTED_COIN       = "#portal-modal div[class*='selectedCoin'], #portal-modal span[class*='coinName']"
    # 목표 가격 입력 필드 (portal 스코프)
    PREDICTION_TARGET_PRICE_INPUT  = "#portal-modal input[class*='priceInput'], #portal-modal input[placeholder*='가격']"
    # % 변동 표시 텍스트 (portal 스코프)
    PREDICTION_PRICE_PCT           = "#portal-modal span[class*='pricePercent'], #portal-modal p[class*='percentText']"
    # +5% / +10% / -5% / -10% 프리셋 버튼 (portal 스코프, has-text)
    PREDICTION_PRESET_PLUS5        = "#portal-modal button:has-text('+5%')"
    PREDICTION_PRESET_PLUS10       = "#portal-modal button:has-text('+10%')"
    PREDICTION_PRESET_MINUS5       = "#portal-modal button:has-text('-5%')"
    PREDICTION_PRESET_MINUS10      = "#portal-modal button:has-text('-10%')"
    # 종료일 선택 버튼 (portal 스코프, has-text 기반)
    PREDICTION_END_DATE_2DAY       = "#portal-modal button:has-text('2일')"
    PREDICTION_END_DATE_7DAY       = "#portal-modal button:has-text('7일')"
    PREDICTION_END_DATE_30DAY      = "#portal-modal button:has-text('30일')"
    # 선택된 종료일 표시 (portal 스코프) — 클래스 패턴 다수 + 시맨틱 태그 fallback
    # ※ 종료일 버튼(2일/7일/30일) 클릭 후 갱신되는 날짜 텍스트 표시 영역
    PREDICTION_END_DATE_DISPLAY    = (
        "#portal-modal span[class*='endDate'], "
        "#portal-modal p[class*='selectedDate'], "
        "#portal-modal span[class*='date'], "
        "#portal-modal p[class*='endDate'], "
        "#portal-modal div[class*='selectedDate'], "
        "#portal-modal span[class*='Date'], "
        "#portal-modal p[class*='Date'], "
        "#portal-modal div[class*='endDate'], "
        "#portal-modal time, "
        "#portal-modal span[class*='expir']"
    )
    # 예측글 '등록' 버튼 (portal 스코프, has-text)
    PREDICTION_MODAL_SUBMIT_BTN    = "#portal-modal button:has-text('등록')"
    # 모달 닫기 버튼 (portal 스코프)
    PREDICTION_MODAL_CLOSE_BTN     = "#portal-modal button[class*='close'], #portal-modal button[aria-label*='닫기']"

    # ── 게시글 상세 페이지 ──────────────────────────────────────────────
    # 상세 페이지 컨테이너
    POST_DETAIL_CONTAINER  = "main[class*='postDetail'], article[class*='postDetail']"
    # 작성자 이름 (프로필 영역 내 이름 텍스트)
    POST_DETAIL_AUTHOR     = "div[class*='writerProfileInfo'] p:first-child, a[class*='writerProfile'] p"
    # 작성 시간 — writerProfilePostTime (STG HTML 확인) 우선, fallback 다수 포함
    POST_DETAIL_DATE       = (
        "p[class*='writerProfilePostTime'], "
        "span[class*='writerProfilePostTime'], "
        "time, "
        "span[class*='date'], "
        "span[class*='createdAt'], "
        "p[class*='createdAt'], "
        "p[class*='postTime']"
    )
    # 게시글 본문 — feed HTML 확인: div[class*='contentText'] 우선 + 다양한 fallback
    # ※ 상세 페이지는 Quill 뷰 모드(.ql-editor) 또는 일반 div 둘 다 가능
    POST_DETAIL_CONTENT    = (
        "div[class*='contentText'], "
        "div[class*='postContent'], "
        "div[class*='postBody'], "
        ".ql-editor, "
        "div[class*='content']"
    )
    # 첨부 이미지
    POST_DETAIL_IMAGE      = "div[class*='imageArea'] img, img[class*='postImage']"
    # 이미지 라이트박스
    POST_DETAIL_LIGHTBOX   = "div[class*='lightbox'], div[role='dialog'][class*='image']"
    # 라이트박스 닫기 버튼
    POST_DETAIL_LIGHTBOX_CLOSE = "button[class*='lightboxClose'], div[class*='lightbox'] button[aria-label]"
    # 좋아요 버튼 — likeBtn / likeBox / likeButton 등 다양한 패턴 커버
    POST_DETAIL_LIKE_BTN   = (
        "button[class*='like'], "
        "button[class*='Like'], "
        "button[aria-label*='좋아요'], "
        "button[aria-label*='like']"
    )
    # 좋아요 카운트 숫자 — feed HTML 확인: span[class*='likeCount'] 우선
    POST_DETAIL_LIKE_COUNT = (
        "span[class*='likeCount'], "
        "button[class*='likeBox'] span, "
        "button[class*='like'] span, "
        "button[class*='Like'] span, "
        "span[class*='LikeCount'], "
        "span[class*='like_count']"
    )
    # 공유 버튼 — i18n key: community-detail-copy_link-toast → 링크 복사 버튼
    # copyLink / share / Share / 공유 aria-label 등 다양한 패턴 커버
    POST_DETAIL_SHARE_BTN  = (
        "button[class*='copyLink'], "
        "button[class*='shareBtn'], "
        "button[class*='share'], "
        "button[class*='Share'], "
        "button[aria-label*='공유'], "
        "button[aria-label*='링크'], "
        "button[aria-label*='share'], "
        "button[aria-label*='Share'], "
        "button[aria-label*='copy']"
    )
    # '...' 더보기 메뉴 버튼 — moreBtn / kebab / ellipsis / 더보기 aria-label 커버
    POST_DETAIL_MORE_BTN   = (
        "button[class*='moreBtn'], "
        "button[class*='more'], "
        "button[class*='More'], "
        "button[class*='kebab'], "
        "button[class*='ellipsis'], "
        "button[class*='dotMenu'], "
        "button[aria-label*='더보기'], "
        "button[aria-label*='more'], "
        "button[aria-label*='More'], "
        "button[aria-label*='메뉴']"
    )
    # 더보기 드롭다운 메뉴
    POST_DETAIL_MORE_MENU  = "ul[class*='moreMenu'], div[class*='dropdownMenu']"
    # '글 삭제하기' 옵션
    POST_DETAIL_DELETE_BTN = "button:has-text('삭제'), li[class*='delete'] button"
    # 삭제 확인 다이얼로그
    POST_DETAIL_DELETE_CONFIRM = "div[role='dialog'][class*='confirm'], div[class*='deleteConfirm']"
    # 신고하기 옵션 (타인 게시글)
    POST_DETAIL_REPORT_BTN = "button:has-text('신고'), li[class*='report'] button"

    # ── 댓글 섹션 ─────────────────────────────────────────────────────
    COMMENT_SECTION        = "section[class*='commentSection'], div[class*='commentArea']"
    # 댓글 수 표시 (예: '댓글 N개')
    COMMENT_COUNT_LABEL    = "h2[class*='commentCount'], span[class*='commentCount']"
    # 댓글 정렬 — 인기순 버튼
    COMMENT_SORT_POPULAR   = "button:has-text('인기순')"
    # 댓글 정렬 — 최신순 버튼
    COMMENT_SORT_LATEST    = "button:has-text('최신순')"
    # 댓글 입력 영역 — Quill.js contenteditable 우선, textarea/div fallback 포함
    # i18n key: "community-comment_after_login-placehoder" → "이 글에 대해 어떻게 생각하시나요?"
    COMMENT_INPUT_AREA     = (
        ".ql-editor[data-placeholder='이 글에 대해 어떻게 생각하시나요?'], "
        "textarea[placeholder*='생각'], "
        "textarea[placeholder*='댓글'], "
        "div[class*='commentInput'] .ql-editor, "
        "div[class*='comment'] .ql-editor"
    )
    # 댓글 텍스트 입력 필드 (동일 패턴 재사용)
    COMMENT_INPUT_FIELD    = (
        ".ql-editor[data-placeholder='이 글에 대해 어떻게 생각하시나요?'], "
        "textarea[placeholder*='생각'], "
        "textarea[placeholder*='댓글'], "
        "div[class*='commentInput'] .ql-editor, "
        "div[class*='comment'] .ql-editor"
    )
    # 댓글 전송 버튼 — commentSubmit 클래스 우선, 없으면 댓글 영역 내 '등록' 텍스트 버튼 탐색
    # ※ i18n: community-comment-write_btn → '등록'
    COMMENT_SUBMIT_BTN     = (
        "button[class*='commentSubmit'], "
        "button[aria-label*='댓글 등록'], "
        "div[class*='comment'] button:has-text('등록'), "
        "section[class*='comment'] button:has-text('등록'), "
        "div[class*='commentInput'] button, "
        "div[class*='commentWrite'] button"
    )
    # 비로그인 댓글 유도 메시지
    COMMENT_LOGIN_PROMPT   = "div[class*='commentLoginPrompt'], p[class*='loginPrompt']"
    # 댓글 아이템 (각 댓글)
    COMMENT_ITEM           = "li[class*='commentItem'], div[class*='commentItem']"
    # 댓글 좋아요 버튼
    COMMENT_LIKE_BTN       = "button[class*='commentLike'], button[aria-label*='좋아요']"
    # 댓글 좋아요 카운트
    COMMENT_LIKE_COUNT     = "span[class*='commentLikeCount']"
    # 댓글 싫어요 버튼
    COMMENT_DISLIKE_BTN    = "button[class*='commentDislike'], button[aria-label*='싫어요']"
    # 댓글 싫어요 카운트
    COMMENT_DISLIKE_COUNT  = "span[class*='commentDislikeCount']"
    # '답글 쓰기' 버튼
    COMMENT_REPLY_BTN      = "button:has-text('답글 쓰기'), button[class*='replyBtn']"
    # 답글 입력 영역
    COMMENT_REPLY_INPUT    = "div[class*='replyInput'] textarea, textarea[class*='replyInput']"
    # 답글 전송 버튼
    COMMENT_REPLY_SUBMIT   = "button[class*='replySubmit'], button[aria-label*='답글 등록']"
    # 답글 목록 (댓글 하단)
    COMMENT_REPLY_LIST     = "ul[class*='replyList'], div[class*='replyList']"
    # 댓글 '...' 더보기 메뉴
    COMMENT_MORE_BTN       = "button[class*='commentMore'], button[aria-label*='댓글 더보기']"
    # 댓글 삭제 옵션
    COMMENT_DELETE_BTN     = "button:has-text('댓글 삭제'), li[class*='deleteComment'] button"

    # ── 로그인 유도 모달 ──────────────────────────────────────────────
    LOGIN_MODAL            = "#portal-modal div[class*='loginModal'], div[role='dialog'][class*='loginModal']"
    LOGIN_MODAL_CONFIRM    = "#portal-modal button[class*='confirm'], #portal-modal button:first-of-type"
    LOGIN_MODAL_CANCEL     = "#portal-modal button[class*='cancel'], #portal-modal button:last-of-type"

    # ── URL 패턴 ────────────────────────────────────────────────────
    COMMUNITY_HOME_PATH      = "/community"
    COMMUNITY_TAB_RANK_PATH  = "/community?tab=rank"
    COMMUNITY_TAB_PRED_PATH  = "/community?tab=prediction"
    POST_DETAIL_URL_PATTERN  = "/community/post/"
    PEOPLE_LIST_URL_PATTERN  = "/people/list"
    SEARCH_URL_PATTERN       = "/search"

    # ══════════════════════════════════════════════════════════════════
    #  INIT
    # ══════════════════════════════════════════════════════════════════

    def __init__(self, page: Page) -> None:
        self.page = page

    # ══════════════════════════════════════════════════════════════════
    #  네비게이션
    # ══════════════════════════════════════════════════════════════════

    def go_to_community_home(self) -> None:
        """커뮤니티 홈(최신 탭)으로 이동
        ※ wait_until='domcontentloaded' 사용 — Next.js SPA + Clarity/Twitter Pixel 등
           서드파티 스크립트가 계속 실행되어 'networkidle' 은 30초 타임아웃 발생
        """
        self.page.goto(
            f"{self.BASE_URL}{self.COMMUNITY_HOME_PATH}", wait_until="domcontentloaded"
        )
        self.page.wait_for_timeout(500)

    def go_to_community_tab_rank(self) -> None:
        """커뮤니티 추천 탭 직접 이동 (URL: ?tab=rank)"""
        self.page.goto(
            f"{self.BASE_URL}{self.COMMUNITY_TAB_RANK_PATH}", wait_until="domcontentloaded"
        )
        self.page.wait_for_timeout(500)

    def go_to_community_tab_prediction(self) -> None:
        """커뮤니티 예측 탭 직접 이동 (URL: ?tab=prediction)"""
        self.page.goto(
            f"{self.BASE_URL}{self.COMMUNITY_TAB_PRED_PATH}", wait_until="domcontentloaded"
        )
        self.page.wait_for_timeout(500)

    def go_to_post_detail(self, post_id: str) -> None:
        """게시글 상세 직접 이동"""
        self.page.goto(
            f"{self.BASE_URL}/community/post/{post_id}", wait_until="domcontentloaded"
        )
        self.page.wait_for_timeout(500)

    def scroll_to_bottom(self, steps: int = 5) -> None:
        """페이지를 단계적으로 스크롤 다운"""
        for _ in range(steps):
            self.page.keyboard.press("PageDown")
            self.page.wait_for_timeout(400)

    def scroll_to_element(self, selector: str) -> None:
        """특정 엘리먼트까지 스크롤"""
        self.page.locator(selector).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)

    # ══════════════════════════════════════════════════════════════════
    #  페이지 로드 확인
    # ══════════════════════════════════════════════════════════════════

    def is_loaded(self) -> bool:
        """커뮤니티 홈 로드 완료 여부 (피드 섹션 or 탭 버튼 기준)"""
        try:
            self.page.wait_for_selector(self.TAB_LATEST, timeout=8_000)
            return True
        except Exception:
            try:
                self.page.wait_for_selector(self.COMMUNITY_HOME, timeout=5_000)
                return True
            except Exception:
                return False

    def is_detail_loaded(self) -> bool:
        """게시글 상세 로드 완료 여부"""
        if self.POST_DETAIL_URL_PATTERN not in self.page.url:
            return False
        try:
            self.page.wait_for_selector(self.POST_DETAIL_CONTENT, timeout=8_000)
            return True
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════════
    #  GNB 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_gnb_visible(self) -> bool:
        return self.page.is_visible(self.GNB_HEADER)

    def is_community_tab_active(self) -> bool:
        """커뮤니티 GNB 탭 활성 여부"""
        return self.page.locator(self.GNB_COMMUNITY_TAB).count() > 0

    def click_logo(self) -> None:
        """GNB 로고 클릭 — href goto 방식"""
        locator = self.page.locator(self.GNB_LOGO).first
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click(force=True)
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  커뮤니티 홈 — 탭 메서드
    # ══════════════════════════════════════════════════════════════════

    def click_tab_latest(self) -> None:
        """'최신' 탭 클릭"""
        self.page.locator(self.TAB_LATEST).first.click()
        self.page.wait_for_timeout(800)

    def click_tab_recommended(self) -> None:
        """'추천' 탭 클릭"""
        self.page.locator(self.TAB_RECOMMENDED).first.click()
        self.page.wait_for_timeout(800)

    def click_tab_prediction(self) -> None:
        """'예측' 탭 클릭"""
        self.page.locator(self.TAB_PREDICTION).first.click()
        self.page.wait_for_timeout(800)

    def get_active_tab_text(self) -> str:
        """현재 활성 탭 텍스트"""
        try:
            return self.page.locator(self.TAB_ACTIVE).first.inner_text().strip()
        except Exception:
            return ""

    def is_url_tab_rank(self) -> bool:
        """현재 URL에 ?tab=rank 포함 여부"""
        return "tab=rank" in self.page.url

    def is_url_tab_prediction(self) -> bool:
        """현재 URL에 ?tab=prediction 포함 여부"""
        return "tab=prediction" in self.page.url

    # ══════════════════════════════════════════════════════════════════
    #  커뮤니티 홈 — 게시글 목록 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_post_count(self) -> int:
        """게시글 아이템 수"""
        return self.page.locator(self.POST_ITEM).count()

    def get_first_post_author(self) -> str:
        """첫 번째 게시글 작성자명"""
        return self.page.locator(self.POST_AUTHOR).first.inner_text().strip()

    def get_first_post_content_preview(self) -> str:
        """첫 번째 게시글 내용 미리보기"""
        return self.page.locator(self.POST_CONTENT_PREVIEW).first.inner_text().strip()

    def get_first_post_like_count(self) -> str:
        """첫 번째 게시글 좋아요 수 텍스트"""
        return self.page.locator(self.POST_LIKE_COUNT).first.inner_text().strip()

    def get_first_post_comment_count(self) -> str:
        """첫 번째 게시글 댓글 수 텍스트"""
        return self.page.locator(self.POST_COMMENT_COUNT).first.inner_text().strip()

    def click_first_post(self) -> None:
        """첫 번째 게시글 클릭 → href goto 방식"""
        locator = self.page.locator(self.POST_ITEM_LINK).first
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click(force=True)
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  커뮤니티 홈 — 주목 인물 섹션 메서드
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_hotperson_section(self) -> None:
        self.page.locator(self.HOTPERSON_SECTION).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(400)

    def is_hotperson_section_visible(self) -> bool:
        return self.page.is_visible(self.HOTPERSON_SECTION)

    def is_hotperson_view_all_visible(self) -> bool:
        return self.page.is_visible(self.HOTPERSON_VIEW_ALL)

    def get_hotperson_card_count(self) -> int:
        return self.page.locator(self.HOTPERSON_CARD).count()

    def click_hotperson_view_all(self) -> None:
        """'전체 보기 >' 링크 클릭 → href goto 방식"""
        locator = self.page.locator(self.HOTPERSON_VIEW_ALL).first
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    def click_hotperson_card(self, index: int = 0) -> None:
        """인물 아바타/카드 클릭 → href goto 방식"""
        locator = self.page.locator(self.HOTPERSON_CARD).nth(index)
        locator.wait_for(state="attached", timeout=5_000)
        href = locator.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
            self.page.goto(full_url, wait_until="domcontentloaded")
            self.page.wait_for_timeout(500)
        else:
            locator.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  인라인 글쓰기 영역 메서드 (홈 피드 상단)
    # ══════════════════════════════════════════════════════════════════

    def is_inline_write_area_visible(self) -> bool:
        """인라인 글쓰기 영역 노출 여부"""
        return self.page.locator(self.WRITE_INLINE_AREA).count() > 0

    def is_login_prompt_visible(self) -> bool:
        """비로그인 시 로그인 유도 문구 노출 여부"""
        return self.page.locator(self.WRITE_LOGIN_PROMPT).count() > 0

    def click_inline_write_area(self) -> None:
        """인라인 글쓰기 영역 클릭"""
        self.page.locator(self.WRITE_INLINE_AREA).first.click()
        self.page.wait_for_timeout(500)

    def is_login_modal_visible(self) -> bool:
        """로그인 유도 모달 노출 여부"""
        return self.page.locator(self.LOGIN_MODAL).count() > 0

    def click_prediction_inline_area(self) -> None:
        """예측 탭 인라인 입력 영역 클릭"""
        self.page.locator(self.PREDICTION_INLINE_AREA).first.click()
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  사이드바 버튼 메서드
    # ══════════════════════════════════════════════════════════════════

    def click_sidebar_post_write(self) -> None:
        """사이드바 '게시글 쓰기' 버튼 클릭"""
        self.page.locator(self.SIDEBAR_POST_WRITE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def click_sidebar_prediction_write(self) -> None:
        """사이드바 '예측글 쓰기' 버튼 클릭"""
        self.page.locator(self.SIDEBAR_PREDICTION_WRITE_BTN).first.click()
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  게시글 작성 모달 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_post_modal_visible(self) -> bool:
        """게시글 작성 모달 노출 여부
        - 포털 모달(#portal-modal .modal-content) 또는
        - 인라인 에디터(#customToolbar) 중 하나라도 존재하면 True
        """
        return (
            self.page.locator(self.POST_MODAL).count() > 0
            or self.page.locator("#customToolbar").count() > 0
        )

    def wait_for_post_modal(self, timeout: int = 5_000) -> None:
        """게시글 작성 모달(또는 인라인 에디터)이 나타날 때까지 대기"""
        try:
            self.page.wait_for_selector(self.POST_MODAL, timeout=timeout)
        except Exception:
            # 인라인 에디터 fallback
            self.page.wait_for_selector("#customToolbar", timeout=timeout)

    def get_char_count_text(self) -> str:
        """글자수 카운터 텍스트 (예: '0 / 3000')"""
        return self.page.locator(self.POST_MODAL_CHAR_COUNT).first.inner_text().strip()

    def type_post_content(self, text: str) -> None:
        """게시글 내용 입력 (Quill.js contenteditable — click 후 keyboard.type 방식)
        Quill의 contenteditable div는 fill()이 동작하지 않으므로
        click() 포커스 후 keyboard.type()으로 입력해야 함
        """
        editor = self.page.locator(self.POST_MODAL_INPUT).first
        editor.wait_for(state="visible", timeout=5_000)
        editor.click()
        self.page.wait_for_timeout(200)
        self.page.keyboard.type(text)
        self.page.wait_for_timeout(300)

    def get_post_modal_input_text(self) -> str:
        """게시글 입력 필드 현재 내용"""
        return self.page.locator(self.POST_MODAL_INPUT).first.inner_text().strip()

    def is_post_submit_btn_enabled(self) -> bool:
        """'등록' 버튼 활성화 여부
        - disabled 속성 없음
        - class에 'disabled' 없음
        - class에 'pointer-events-none' 없음 (블루밍비트 비활성화 패턴)
        """
        btn = self.page.locator(self.POST_MODAL_SUBMIT_BTN).first
        disabled_attr = btn.get_attribute("disabled")
        cls = btn.get_attribute("class") or ""
        return (
            disabled_attr is None
            and "disabled" not in cls
            and "pointer-events-none" not in cls
        )

    def click_post_submit(self) -> None:
        """'등록' 버튼 클릭"""
        self.page.locator(self.POST_MODAL_SUBMIT_BTN).first.click()
        self.page.wait_for_timeout(1_000)

    def click_post_modal_image_btn(self) -> None:
        """이미지 첨부 아이콘 클릭"""
        self.page.locator(self.POST_MODAL_IMAGE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_post_modal_image_preview_visible(self) -> bool:
        """이미지 미리보기 노출 여부"""
        return self.page.locator(self.POST_MODAL_IMAGE_PREVIEW).count() > 0

    def is_post_modal_file_error_visible(self) -> bool:
        """파일 오류 메시지 노출 여부"""
        return self.page.locator(self.POST_MODAL_FILE_ERROR).count() > 0

    def click_post_modal_coin_btn(self) -> None:
        """'관련 코인' 버튼 클릭 (portal 스코프 — modal-mask 인터셉트 방지)"""
        self.page.locator(self.POST_MODAL_COIN_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_post_modal_coin_dropdown_visible(self) -> bool:
        """코인 검색 드롭다운 노출 여부"""
        return self.page.locator(self.POST_MODAL_COIN_DROPDOWN).count() > 0

    def type_coin_search(self, coin_name: str) -> None:
        """코인 검색창에 코인명 입력"""
        self.page.locator(self.POST_MODAL_COIN_SEARCH).first.fill(coin_name)
        self.page.wait_for_timeout(500)

    def select_first_coin_result(self) -> None:
        """코인 검색 결과 첫 번째 선택"""
        self.page.locator(
            "#portal-modal ul[class*='coinList'] li, #portal-modal div[class*='coinSearch'] li"
        ).first.click()
        self.page.wait_for_timeout(300)

    def get_added_coin_tag_count(self) -> int:
        """추가된 관련 코인 태그 수"""
        return self.page.locator(self.POST_MODAL_COIN_TAG).count()

    def close_post_modal(self) -> None:
        """게시글 작성 모달 닫기"""
        self.page.locator(self.POST_MODAL_CLOSE_BTN).first.click()
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  예측글 작성 모달 메서드
    # ══════════════════════════════════════════════════════════════════

    def is_prediction_modal_visible(self) -> bool:
        """예측글 작성 모달 노출 여부
        (#portal-modal .modal-content 존재 + 코인 검색창 유무로 게시글 모달과 구분)
        """
        return (
            self.page.locator(self.PREDICTION_MODAL).count() > 0
            and self.page.locator(self.PREDICTION_COIN_SEARCH).count() > 0
        )

    def wait_for_prediction_modal(self, timeout: int = 5_000) -> None:
        """예측 모달이 나타날 때까지 대기"""
        self.page.wait_for_selector(self.PREDICTION_MODAL, timeout=timeout)
        self.page.wait_for_selector(self.PREDICTION_COIN_SEARCH, timeout=timeout)

    def search_and_select_prediction_coin(self, coin_name: str) -> None:
        """예측 모달에서 코인 검색 후 첫 번째 결과 선택

        코인 검색 input이 readonly 속성 → 직접 fill() 불가.
        1) readonly trigger input 클릭 → 드롭다운 열기
        2) 드롭다운 내 실제 editable input 찾아서 타이핑
        3) 검색 결과 리스트 첫 번째 항목 클릭
        """
        # 1. readonly trigger input 클릭 → 드롭다운/검색창 열기
        trigger = self.page.locator(self.PREDICTION_COIN_SEARCH).first
        trigger.click()
        self.page.wait_for_timeout(500)

        # 2. 드롭다운 내 editable input 입력
        #    readonly가 아닌 input이 새로 렌더링됨 (드롭다운 검색창)
        editable_input = self.page.locator(
            "#portal-modal input:not([readonly])"
        ).first
        try:
            editable_input.wait_for(state="visible", timeout=3_000)
            editable_input.fill(coin_name)
        except Exception:
            # fallback: readonly trigger에 직접 타이핑 시도 (force)
            trigger.click(force=True)
            self.page.wait_for_timeout(300)
            self.page.keyboard.type(coin_name)
        self.page.wait_for_timeout(500)

        # 3. 검색 결과 첫 번째 아이템 클릭
        #    ※ 결과 li 가 #portal-modal 스코프 밖 별도 overlay에 렌더링될 수 있으므로
        #       portal 스코프 셀렉터 우선 → 전역 fallback 순으로 탐색
        result_item = self.page.locator(
            "#portal-modal ul[class*='coinResult'] li, "
            "#portal-modal div[class*='searchResult'] li, "
            "#portal-modal ul li[class*='coin'], "
            "#portal-modal li, "
            "ul[class*='coinResult'] li, "
            "ul[class*='coinList'] li, "
            "div[class*='searchResult'] li, "
            "div[class*='coinDropdown'] li"
        ).first
        result_item.wait_for(state="visible", timeout=5_000)
        result_item.click()
        self.page.wait_for_timeout(300)

    def is_prediction_coin_selected(self) -> bool:
        """코인 선택 영역에 코인이 표시되어 있는지 확인"""
        return self.page.locator(self.PREDICTION_SELECTED_COIN).count() > 0

    def is_prediction_price_input_enabled(self) -> bool:
        """목표 가격 입력 필드 활성화 여부"""
        field = self.page.locator(self.PREDICTION_TARGET_PRICE_INPUT).first
        disabled = field.get_attribute("disabled")
        return disabled is None

    def type_prediction_target_price(self, price: str) -> None:
        """목표 가격 입력"""
        self.page.locator(self.PREDICTION_TARGET_PRICE_INPUT).first.fill(price)
        self.page.wait_for_timeout(300)

    def get_prediction_price_pct_text(self) -> str:
        """% 변동 표시 텍스트"""
        return self.page.locator(self.PREDICTION_PRICE_PCT).first.inner_text().strip()

    def click_prediction_preset_plus5(self) -> None:
        """+5% 프리셋 버튼 클릭"""
        self.page.locator(self.PREDICTION_PRESET_PLUS5).first.click()
        self.page.wait_for_timeout(300)

    def click_prediction_end_date_2day(self) -> None:
        """'2일 후' 종료일 버튼 클릭"""
        self.page.locator(self.PREDICTION_END_DATE_2DAY).first.click()
        self.page.wait_for_timeout(300)

    def get_prediction_end_date_text(self) -> str:
        """선택된 종료일 텍스트"""
        return (
            self.page.locator(self.PREDICTION_END_DATE_DISPLAY).first.inner_text().strip()
        )

    def is_prediction_submit_enabled(self) -> bool:
        """예측글 '등록' 버튼 활성화 여부
        - disabled 속성 없음
        - class에 'disabled' 없음
        - class에 'pointer-events-none' 없음 (블루밍비트 비활성화 패턴)
        """
        btn = self.page.locator(self.PREDICTION_MODAL_SUBMIT_BTN).first
        disabled_attr = btn.get_attribute("disabled")
        cls = btn.get_attribute("class") or ""
        return (
            disabled_attr is None
            and "disabled" not in cls
            and "pointer-events-none" not in cls
        )

    def click_prediction_submit(self) -> None:
        """예측글 '등록' 버튼 클릭"""
        self.page.locator(self.PREDICTION_MODAL_SUBMIT_BTN).first.click()
        self.page.wait_for_timeout(1_000)

    def close_prediction_modal(self) -> None:
        """예측글 작성 모달 닫기"""
        self.page.locator(self.PREDICTION_MODAL_CLOSE_BTN).first.click()
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════
    #  게시글 상세 메서드
    # ══════════════════════════════════════════════════════════════════

    def get_post_detail_author(self) -> str:
        return self.page.locator(self.POST_DETAIL_AUTHOR).first.inner_text().strip()

    def get_post_detail_date(self) -> str:
        return self.page.locator(self.POST_DETAIL_DATE).first.inner_text().strip()

    def get_post_detail_content(self) -> str:
        return self.page.locator(self.POST_DETAIL_CONTENT).first.inner_text().strip()

    def is_post_detail_image_visible(self) -> bool:
        return self.page.locator(self.POST_DETAIL_IMAGE).first.is_visible()

    def click_post_detail_image(self) -> None:
        """게시글 이미지 클릭 → 라이트박스 열기"""
        self.page.locator(self.POST_DETAIL_IMAGE).first.click()
        self.page.wait_for_timeout(500)

    def is_lightbox_visible(self) -> bool:
        """라이트박스 노출 여부"""
        return self.page.locator(self.POST_DETAIL_LIGHTBOX).count() > 0

    def close_lightbox(self) -> None:
        """라이트박스 닫기 버튼 클릭"""
        self.page.locator(self.POST_DETAIL_LIGHTBOX_CLOSE).first.click()
        self.page.wait_for_timeout(500)

    def get_post_like_count_text(self) -> str:
        """좋아요 카운트 텍스트"""
        return self.page.locator(self.POST_DETAIL_LIKE_COUNT).first.inner_text().strip()

    def click_post_like_btn(self) -> None:
        """좋아요 버튼 클릭"""
        self.page.locator(self.POST_DETAIL_LIKE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_post_like_btn_active(self) -> bool:
        """좋아요 버튼 활성화(색상 변경) 여부"""
        btn = self.page.locator(self.POST_DETAIL_LIKE_BTN).first
        cls = btn.get_attribute("class") or ""
        aria = btn.get_attribute("aria-pressed") or ""
        return "active" in cls or aria == "true"

    def click_share_btn(self) -> None:
        """공유 버튼 클릭"""
        self.page.locator(self.POST_DETAIL_SHARE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def click_more_menu_btn(self) -> None:
        """'...' 더보기 메뉴 버튼 클릭"""
        self.page.locator(self.POST_DETAIL_MORE_BTN).first.click()
        self.page.wait_for_timeout(400)

    def is_more_menu_visible(self) -> bool:
        """더보기 드롭다운 메뉴 노출 여부"""
        return self.page.locator(self.POST_DETAIL_MORE_MENU).count() > 0

    def is_delete_option_visible(self) -> bool:
        """'글 삭제하기' 옵션 노출 여부"""
        return self.page.locator(self.POST_DETAIL_DELETE_BTN).count() > 0

    def is_report_option_visible(self) -> bool:
        """신고하기 옵션 노출 여부"""
        return self.page.locator(self.POST_DETAIL_REPORT_BTN).count() > 0

    def click_delete_option(self) -> None:
        """'글 삭제하기' 옵션 클릭"""
        self.page.locator(self.POST_DETAIL_DELETE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def is_delete_confirm_dialog_visible(self) -> bool:
        """삭제 확인 다이얼로그 노출 여부"""
        return self.page.locator(self.POST_DETAIL_DELETE_CONFIRM).count() > 0

    # ══════════════════════════════════════════════════════════════════
    #  댓글 섹션 메서드
    # ══════════════════════════════════════════════════════════════════

    def scroll_to_comment_section(self) -> None:
        """댓글 섹션까지 스크롤"""
        self.page.locator(self.COMMENT_SECTION).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(400)

    def get_comment_count(self) -> int:
        """댓글 아이템 수"""
        return self.page.locator(self.COMMENT_ITEM).count()

    def get_comment_count_label_text(self) -> str:
        """댓글 수 표시 텍스트 (예: '댓글 5개')"""
        return self.page.locator(self.COMMENT_COUNT_LABEL).first.inner_text().strip()

    def click_comment_sort_popular(self) -> None:
        """댓글 '인기순' 정렬 클릭"""
        self.page.locator(self.COMMENT_SORT_POPULAR).first.click()
        self.page.wait_for_timeout(600)

    def click_comment_sort_latest(self) -> None:
        """댓글 '최신순' 정렬 클릭"""
        self.page.locator(self.COMMENT_SORT_LATEST).first.click()
        self.page.wait_for_timeout(600)

    def click_comment_input_area(self) -> None:
        """댓글 입력 영역 클릭 (Quill contenteditable)
        modal-mask 등 클릭 인터셉터 방지를 위해 force=True 사용
        """
        self.page.locator(self.COMMENT_INPUT_AREA).first.click(force=True)
        self.page.wait_for_timeout(400)

    def is_comment_input_active(self) -> bool:
        """댓글 입력 필드 활성화 여부 (Quill editor 존재 여부)"""
        return self.page.locator(self.COMMENT_INPUT_FIELD).count() > 0

    def is_comment_login_prompt_visible(self) -> bool:
        """비로그인 댓글 유도 문구 노출 여부"""
        return self.page.locator(self.COMMENT_LOGIN_PROMPT).count() > 0

    def type_comment(self, text: str) -> None:
        """댓글 내용 입력 (Quill.js contenteditable — force click 후 keyboard.type 방식)
        modal-mask 등 클릭 인터셉터 방지를 위해 force=True 사용
        """
        editor = self.page.locator(self.COMMENT_INPUT_FIELD).first
        editor.wait_for(state="visible", timeout=5_000)
        editor.click(force=True)
        self.page.wait_for_timeout(200)
        self.page.keyboard.type(text)
        self.page.wait_for_timeout(300)

    def is_comment_submit_enabled(self) -> bool:
        """댓글 전송 버튼 활성화 여부
        - disabled 속성 없음
        - class에 'disabled' 없음
        - class에 'pointer-events-none' 없음 (블루밍비트 비활성화 패턴)
        """
        btn = self.page.locator(self.COMMENT_SUBMIT_BTN).first
        disabled_attr = btn.get_attribute("disabled")
        cls = btn.get_attribute("class") or ""
        return (
            disabled_attr is None
            and "disabled" not in cls
            and "pointer-events-none" not in cls
        )

    def click_comment_submit(self) -> None:
        """댓글 전송 버튼 클릭"""
        self.page.locator(self.COMMENT_SUBMIT_BTN).first.click()
        self.page.wait_for_timeout(800)

    def get_comment_like_count_text(self, index: int = 0) -> str:
        """index 번째 댓글 좋아요 카운트"""
        return (
            self.page.locator(self.COMMENT_LIKE_COUNT).nth(index).inner_text().strip()
        )

    def click_comment_like_btn(self, index: int = 0) -> None:
        """index 번째 댓글 좋아요 클릭"""
        self.page.locator(self.COMMENT_LIKE_BTN).nth(index).click()
        self.page.wait_for_timeout(500)

    def click_comment_dislike_btn(self, index: int = 0) -> None:
        """index 번째 댓글 싫어요 클릭"""
        self.page.locator(self.COMMENT_DISLIKE_BTN).nth(index).click()
        self.page.wait_for_timeout(500)

    def get_comment_dislike_count_text(self, index: int = 0) -> str:
        return (
            self.page.locator(self.COMMENT_DISLIKE_COUNT).nth(index).inner_text().strip()
        )

    def click_reply_btn(self, comment_index: int = 0) -> None:
        """'답글 쓰기' 버튼 클릭"""
        self.page.locator(self.COMMENT_REPLY_BTN).nth(comment_index).click()
        self.page.wait_for_timeout(400)

    def is_reply_input_visible(self) -> bool:
        """답글 입력 영역 노출 여부"""
        return self.page.locator(self.COMMENT_REPLY_INPUT).count() > 0

    def type_reply(self, text: str) -> None:
        """답글 내용 입력"""
        self.page.locator(self.COMMENT_REPLY_INPUT).first.fill(text)
        self.page.wait_for_timeout(300)

    def click_reply_submit(self) -> None:
        """답글 전송 버튼 클릭"""
        self.page.locator(self.COMMENT_REPLY_SUBMIT).first.click()
        self.page.wait_for_timeout(800)

    def get_reply_count(self, comment_index: int = 0) -> int:
        """특정 댓글의 답글 수"""
        return (
            self.page.locator(self.COMMENT_REPLY_LIST).nth(comment_index).count()
        )

    def click_comment_more_menu(self, comment_index: int = 0) -> None:
        """댓글 '...' 더보기 메뉴 클릭"""
        self.page.locator(self.COMMENT_MORE_BTN).nth(comment_index).click()
        self.page.wait_for_timeout(400)

    def is_comment_delete_option_visible(self) -> bool:
        """댓글 삭제 옵션 노출 여부"""
        return self.page.locator(self.COMMENT_DELETE_BTN).count() > 0

    def click_comment_delete_option(self) -> None:
        """댓글 삭제 옵션 클릭"""
        self.page.locator(self.COMMENT_DELETE_BTN).first.click()
        self.page.wait_for_timeout(800)