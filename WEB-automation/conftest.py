# conftest.py 최상단에 추가
try:
    from dotenv import load_dotenv
    load_dotenv()          # .env 파일을 자동으로 읽어 환경변수에 주입
except ImportError:
    pass                   # python-dotenv 미설치 시 조용히 무시

"""
tests/stage8_regression/web/conftest.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[기능 1]  테스트 실행 직전 한글 Docstring 터미널 출력
          → pytest_runtest_setup 훅

[기능 2]  전체 테스트 완료 후 Slack 웹훅 요약 알림 (실패 목록 포함)
          → pytest_terminal_summary 훅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[터미널 출력 예시]
  ─── 🚀 [진행중]  FULLTC-524 | 서비스 이용약관/최신 시행일자 디폴트 선택 ───

[Slack 메시지 예시 — FAIL 발생 시]
  🔴 블루밍비트 QA — 테스트 실패 발생
  ┌──────────────────────────────────┐
  │ 📋 전체TC  ✅PASS  ❌FAIL  ⏭️SKIP │
  │   25건      20건    5건     0건   │
  └──────────────────────────────────┘
  📊 통과율: 80%  (20 / 25 케이스 통과)
  ───────────────────────────────────
  🚨 실패한 케이스 상세
  • `test_regression_news.py`  ›  `test_FULLTC_001_gnb_news_tab_active`
  • `test_regression_community.py`  ›  `test_FULLTC_201_community_home`
  ...외 3건 추가 실패 (상세 로그 확인 요망)
  ───────────────────────────────────
  ⏱ 3분 45초  |  🌐 STG 환경  |  블루밍비트 QA Harness

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Slack 웹훅 설정 방법]
  방법 A (권장): 환경 변수 설정
    export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

  방법 B: 아래 상수에 직접 입력
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/..."

[의존 패키지]
  pip install requests
  (미설치 시 Slack 전송만 조용히 스킵 — 테스트 실행에 영향 없음)
"""

import os
import textwrap
import time
from typing import Optional

import pytest


# ══════════════════════════════════════════════════════════════════
#  ★ Slack 웹훅 URL 설정
#    발급받은 URL을 아래 문자열에 붙여넣거나, 환경 변수로 주입하세요.
# ══════════════════════════════════════════════════════════════════
SLACK_WEBHOOK_URL: str = os.environ.get(
    "SLACK_WEBHOOK_URL",
    "",   # ← Slack App에서 발급받은 웹훅 URL로 교체
)

# Slack Block Kit 색상 코드
_COLOR_GREEN  = "#2EB67D"   # 전체 통과 (초록)
_COLOR_RED    = "#E01E5A"   # 실패 존재 (빨강)
_COLOR_YELLOW = "#ECB22E"   # 스킵만 존재 (노랑)

# 실패 목록 최대 표시 건수
# Slack section.text 최대 3000자 제한 방어 — 초과분은 "...외 N건" 으로 축약
_MAX_FAIL_ITEMS: int = 10


# ══════════════════════════════════════════════════════════════════
#  내부 헬퍼 함수
# ══════════════════════════════════════════════════════════════════

def _get_first_meaningful_line(docstring: Optional[str]) -> str:
    """Docstring 에서 첫 번째 의미 있는 줄을 추출합니다.

    Example:
        '''
            FULLTC-524 | 서비스 이용약관/최신 시행일자 디폴트 선택 | Major
            페이지 진입 시 ...
        '''
        → 'FULLTC-524 | 서비스 이용약관/최신 시행일자 디폴트 선택 | Major'
    """
    if not docstring:
        return ""
    normalized = textwrap.dedent(docstring).strip()
    for line in normalized.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _format_duration(seconds: float) -> str:
    """초 단위를 '분 초' 또는 '초' 형식 문자열로 변환합니다."""
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins}분 {secs:.0f}초" if mins > 0 else f"{secs:.1f}초"


def _parse_nodeid(nodeid: str) -> tuple:
    """pytest nodeid에서 (파일명, 테스트 함수명)을 추출합니다.

    Input:  "tests/stage8_regression/web/test_news.py::TestClass::test_FULLTC_001"
    Output: ("test_news.py", "test_FULLTC_001")

    - 클래스명은 제거하고 테스트 함수명만 반환합니다.
    - OS 무관(Unix/Windows 경로 구분자) 처리합니다.
    """
    parts = nodeid.split("::")
    # 파일명: 경로 구분자를 통일한 뒤 마지막 세그먼트만 추출
    raw_path = parts[0].replace("\\", "/")
    filename = raw_path.split("/")[-1]
    # 테스트 함수명: 마지막 :: 구분자 항목 (클래스명은 제외)
    test_name = parts[-1] if len(parts) > 1 else filename
    return filename, test_name


def _build_failure_section_text(
    failed_reports: list,
    error_reports: list,
    max_items: int = _MAX_FAIL_ITEMS,
) -> str:
    """실패·에러 TestReport 목록으로 mrkdwn 형식의 상세 텍스트를 생성합니다.

    처리 규칙:
      1. failed(call 단계) + error(setup/teardown 단계) 통합
      2. 동일 nodeid 중복 제거
         (같은 TC가 setup + call 양쪽에서 모두 실패할 경우 1건으로 집계)
      3. max_items 초과 시 "...외 N건 추가 실패" 로 안전 축약
         → Slack section.text 최대 3000자 제한 방어

    Args:
        failed_reports: stats["failed"] 리스트 (TestReport 객체들)
        error_reports:  stats["error"]  리스트 (TestReport 객체들)
        max_items:      최대 표시 건수 (기본값: _MAX_FAIL_ITEMS = 10)

    Returns:
        mrkdwn 형식 문자열. 실패가 없으면 빈 문자열 반환.
    """
    # ── ① 중복 제거 (nodeid 기준) ─────────────────────────────────
    seen_nodeids: set = set()
    unique_reports = []
    for report in (failed_reports + error_reports):
        if report.nodeid not in seen_nodeids:
            seen_nodeids.add(report.nodeid)
            unique_reports.append(report)

    total = len(unique_reports)
    if total == 0:
        return ""

    # ── ② 최대 max_items 건만 표시 ────────────────────────────────
    lines = []
    for report in unique_reports[:max_items]:
        filename, test_name = _parse_nodeid(report.nodeid)
        lines.append(f"• `{filename}`  ›  `{test_name}`")

    text = "\n".join(lines)

    # ── ③ 초과분 축약 안내 ────────────────────────────────────────
    if total > max_items:
        remaining = total - max_items
        text += f"\n_...외 {remaining}건 추가 실패 (상세 로그 확인 요망)_"

    return text


def _build_slack_payload(
    passed: int,
    failed: int,
    skipped: int,
    errors: int,
    duration: float,
    fail_detail_text: str = "",   # ← 실패 케이스 상세 목록 (빈 문자열이면 섹션 미노출)
) -> dict:
    """Slack Block Kit (Attachments) 형식의 페이로드를 생성합니다.

    색상 테마:
      🟢 초록 (#2EB67D) — FAIL = 0  이고 SKIP = 0
      🟡 노랑 (#ECB22E) — FAIL = 0  이고 SKIP > 0
      🔴 빨강 (#E01E5A) — FAIL > 0  (Error 포함)

    실패 케이스 상세 블록:
      fail_detail_text 가 비어있지 않은 경우에만 divider + 상세 섹션을 추가합니다.
    """
    total_fail   = failed + errors
    total        = passed + total_fail + skipped
    pass_rate    = round(passed / total * 100) if total > 0 else 0
    duration_str = _format_duration(duration)

    # ── 테마 결정 ─────────────────────────────────────────────────
    if total_fail > 0:
        color        = _COLOR_RED
        header_emoji = "🔴"
        status_label = "테스트 실패 발생"
    elif skipped > 0:
        color        = _COLOR_YELLOW
        header_emoji = "🟡"
        status_label = "일부 케이스 스킵됨"
    else:
        color        = _COLOR_GREEN
        header_emoji = "🟢"
        status_label = "전체 테스트 통과"

    # ── Block Kit 구성 ─────────────────────────────────────────────
    blocks = [
        # ① 헤더
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{header_emoji}  블루밍비트 QA — {status_label}",
                "emoji": True,
            },
        },
        # ② 통계 수치 (2×2 필드 그리드)
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*📋 전체 TC*\n`{total}건`"},
                {"type": "mrkdwn", "text": f"*✅ PASS*\n`{passed}건`"},
                {"type": "mrkdwn", "text": f"*❌ FAIL*\n`{total_fail}건`"},
                {"type": "mrkdwn", "text": f"*⏭️ SKIP*\n`{skipped}건`"},
            ],
        },
        # ③ 통과율 한 줄 요약
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"📊  통과율: *{pass_rate}%*   (`{passed}` / `{total}` 케이스 통과)",
            },
        },
    ]

    # ④ 실패 케이스 상세 목록 (fail_detail_text 가 있을 때만 추가)
    #    divider → "🚨 실패한 케이스 상세" 섹션
    if fail_detail_text:
        blocks.append({"type": "divider"})
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    # 제목 + 목록을 하나의 텍스트 필드에 포함 (3000자 이내 보장)
                    "text": f"*🚨 실패한 케이스 상세*\n\n{fail_detail_text}",
                },
            }
        )

    # ⑤ 최종 구분선 + 하단 컨텍스트 (소요 시간·환경)
    blocks.append({"type": "divider"})
    blocks.append(
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": (
                        f"⏱  소요 시간: *{duration_str}*"
                        "   |   🌐  STG 환경"
                        "   |   블루밍비트 QA Harness"
                    ),
                }
            ],
        }
    )

    # Attachments 방식: 좌측 컬러 바 + 블록 본문
    return {
        "attachments": [
            {
                "color": color,
                "blocks": blocks,
            }
        ]
    }


def _post_to_slack(payload: dict) -> None:
    """완성된 페이로드를 Slack 웹훅 URL 로 POST 합니다.

    Raises:
        ImportError: requests 미설치 시
        requests.HTTPError: 웹훅 응답이 4xx/5xx 일 때
    """
    import requests  # noqa: PLC0415 — 런타임 import (미설치 시 ImportError)

    response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()


# ══════════════════════════════════════════════════════════════════
#  pytest 훅 — 기능 1: 한글 터미널 출력
# ══════════════════════════════════════════════════════════════════

def pytest_runtest_setup(item: pytest.Item) -> None:
    """각 테스트 함수 실행 직전 Docstring 첫 줄을 터미널에 출력합니다.

    출력 형식:
      ─── 🚀 [진행중]  FULLTC-XXX | 도메인/TC명 | 우선순위 ───

    오류 처리:
      출력 실패 시 테스트 실행 자체는 중단되지 않습니다.
    """
    try:
        raw_doc: str    = getattr(item.function, "__doc__", None) or ""
        first_line: str = _get_first_meaningful_line(raw_doc)
        label: str      = first_line if first_line else f"(설명 없음) → {item.name}"

        tw = item.config.get_terminal_writer()
        tw.line("")
        tw.sep("─", f"🚀 [진행중]  {label}", bold=True, cyan=True)

    except Exception:
        pass  # 출력 실패가 테스트에 영향을 주지 않도록 무시


# ══════════════════════════════════════════════════════════════════
#  pytest 훅 — 기능 2: Slack 웹훅 알림 (실패 케이스 상세 포함)
# ══════════════════════════════════════════════════════════════════

def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    """전체 테스트 세션 종료 후 Slack 으로 요약 리포트를 발송합니다.

    데이터 소스:
      terminalreporter.stats["passed"]  — 통과 TestReport 리스트
      terminalreporter.stats["failed"]  — 실패 TestReport 리스트 (call 단계)
      terminalreporter.stats["skipped"] — 스킵 TestReport 리스트
      terminalreporter.stats["error"]   — 에러 TestReport 리스트 (setup/teardown)
      terminalreporter._sessionstarttime — 세션 시작 시각 (float)

    실패 목록 처리:
      · "failed" + "error" 리스트를 합산하여 중복 제거 후 상세 텍스트 생성
      · max_items(기본 10건) 초과 시 "...외 N건 추가 실패" 로 안전 축약
        → Slack section.text 3000자 제한 방어

    스킵 조건:
      · SLACK_WEBHOOK_URL 이 https:// 로 시작하지 않으면 전송하지 않습니다.
      · requests 패키지 미설치 시 조용히 반환합니다.
      · 수집된 TC 가 0 건이면 전송하지 않습니다.

    오류 처리:
      모든 예외를 캐치합니다. Slack 전송 실패가 exitstatus 에 영향을 주지 않습니다.
    """
    # ── ① 웹훅 URL 유효성 검사 ────────────────────────────────────
    if not SLACK_WEBHOOK_URL.startswith("https://"):
        return

    try:
        # ── ② 통계 수집 ──────────────────────────────────────────
        stats          = terminalreporter.stats
        passed         = len(stats.get("passed",  []))
        failed         = len(stats.get("failed",  []))
        skipped        = len(stats.get("skipped", []))
        errors         = len(stats.get("error",   []))
        failed_reports = stats.get("failed", [])
        error_reports  = stats.get("error",  [])

        total = passed + failed + skipped + errors
        if total == 0:
            return

        # ── ③ 소요 시간 계산 ─────────────────────────────────────
        start_ts = getattr(terminalreporter, "_sessionstarttime", None)
        duration = (time.time() - start_ts) if start_ts else 0.0

        # ── ④ 실패 케이스 상세 텍스트 생성 ───────────────────────
        #    중복 제거 + max_items 제한 + 축약 처리
        fail_detail_text = _build_failure_section_text(
            failed_reports=failed_reports,
            error_reports=error_reports,
        )

        # ── ⑤ 페이로드 빌드 및 전송 ──────────────────────────────
        payload = _build_slack_payload(
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration=duration,
            fail_detail_text=fail_detail_text,
        )
        _post_to_slack(payload)

    except ImportError:
        # requests 미설치 시 조용히 무시
        pass

    except Exception:
        # 네트워크 오류, HTTP 오류 등 모든 예외 무시
        # (Slack 전송 실패가 CI/CD 파이프라인에 영향을 주지 않도록)
        pass