from appium import webdriver
from appium.options.ios import XCUITestOptions
import time
import requests
import json
import importlib

# 1. 각 모듈 임포트
# (1_ios_header.py, 2_ios_news.py, 3_ios_news_comment.py 파일이 동일 폴더에 존재해야 함)
try:
    ios_header = importlib.import_module("1_ios_header")
    ios_news = importlib.import_module("2_ios_news")
    ios_comment = importlib.import_module("3_ios_news_comment")
    ios_community = importlib.import_module("4_ios_community")
    ios_editor = importlib.import_module("5_ios_editor")
    
except ImportError as e:
    print(f"🚨 모듈 임포트 실패: {e}")

# 슬랙 웹훅 함수 (앱 버전 및 모듈별 상세 결과 포함)
def send_slack_report(status, message, final_stats, detail_results, app_version):
    webhook_url = "https://hooks.slack.com/services/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"
    
    emoji = "✅" if status == "Success" else "🚨"
    
    # 📝 앱 버전 정보 (수동 입력값 반영)
    app_info = f"\n*앱 버전*: iOS STG v{app_version}"
    
    # 📂 모듈별 상세 결과 문자열 생성
    detail_text = "\n\n📂 *모듈별 상세 결과*:"
    for name, stats in detail_results.items():
        detail_text += f"\n• {name} : 총 {stats['total']}개 (성공: {stats['pass']}, 실패: {stats['fail']})"
    
    # 📈 통합 통계 요약
    summary = f"\n\n📈 *통합 통계*: 총 {final_stats['total']}개 (성공: {final_stats['pass']}, 실패: {final_stats['fail']})"
    
    payload = {
        "text": f"{emoji} *iOS 통합 QA 자동화 결과 보고*\n*결과*: {status}{app_info}\n*내용*: {message}{detail_text}{summary}"
    }
    
    try:
        requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        print(f"📲 슬랙 보고 전송 완료 (v{app_version})")
    except Exception as e:
        print(f"❌ 슬랙 전송 에러: {e}")

def main():
    # --- ⚙️ 수동 설정 구역 ---
    # 테스트 대상 앱 버전을 직접 입력하세요.
    CURRENT_APP_VERSION = "3.3.1(47)" 
    # -----------------------

    # 변수 초기화 (UnboundLocalError 방지)
    driver = None
    status = "Success"
    error_msg = "모든 시나리오가 정상 완료되었습니다."
    total_stats = {"pass": 0, "fail": 0, "total": 0}
    detail_results = {}

    # --- 1. iOS 설정 (Capabilities) ---
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.device_name = "이상윤의 iPhone"
    options.udid = "00008110-001459E022D1401E"
    options.bundle_id = "com.hankyung.bloomingbit.staging"
    options.xcode_org_id = "H58K49T23N"
    options.xcode_signing_id = "iPhone Developer"
    options.set_capability("appium:updatedWdaBundleId", "com.sangyunlee.WebDriverAgentRunner.bloomingbit01")

    try:
        # --- 2. Appium 세션 생성 ---
        print(f"🚀 [v{CURRENT_APP_VERSION}] 통합 자동화 테스트를 시작합니다...")
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        print("✅ iOS 세션 생성 성공")
        time.sleep(2)

        # --- 3. 각 시나리오 순차 실행 ---
        scenarios = [
            ("ios_header", ios_header),
            ("ios_news", ios_news),
            ("ios_comment", ios_comment)
        ]

        for name, module in scenarios:
            print(f"\n--- [Step] {name} 테스트 시작 ---")
            try:
                # 모듈별 시나리오 실행 (드라이버 전달)
                module.run_scenario(driver)
            except Exception as e:
                status = "Fail"
                error_msg = f"{name} 단계에서 실패: {str(e)}"
                print(f"🚨 {error_msg}")
                break # 실패 시 다음 시나리오 진행 중단
            finally:
                # 실행된 시점까지의 모듈별 결과 기록
                detail_results[name] = {
                    "pass": module.stats["pass"],
                    "fail": module.stats["fail"],
                    "total": module.stats["total"]
                }
                # 통합 통계 업데이트
                total_stats["pass"] += module.stats["pass"]
                total_stats["fail"] += module.stats["fail"]
                total_stats["total"] += module.stats["total"]

    except Exception as e:
        status = "Fail"
        error_msg = f"초기화 또는 드라이버 연결 실패: {str(e)}"
        print(f"🚨 {error_msg}")

    finally:
        # --- 4. 슬랙 보고 전송 및 세션 종료 ---
        # 수동으로 설정한 CURRENT_APP_VERSION을 전달합니다.
        send_slack_report(status, error_msg, total_stats, detail_results, CURRENT_APP_VERSION)
        
        if driver:
            driver.quit()
        print(f"\n🛑 [v{CURRENT_APP_VERSION}] 테스트 프로세스 종료")

if __name__ == "__main__":
    main()