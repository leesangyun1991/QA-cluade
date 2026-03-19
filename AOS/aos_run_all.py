from appium import webdriver
from appium.options.android import UiAutomator2Options # 안드로이드 옵션으로 변경
import time
import requests
import json
import importlib

# 1. 안드로이드 모듈 임포트 (파일명이 1_aos_header.py 등이라고 가정)
try:
    aos_header = importlib.import_module("1_aos_header")
    aos_news = importlib.import_module("2_aos_news")
    aos_comment = importlib.import_module("3_aos_news_comment")
    # 필요한 안드로이드 모듈들을 추가하세요
except ImportError as e:
    print(f"🚨 모듈 임포트 실패: {e}")

# 슬랙 웹훅 함수 (AOS 버전)
def send_slack_report(status, message, final_stats, detail_results, app_version):
    webhook_url = "https://hooks.slack.com/services/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"
    
    emoji = "✅" if status == "Success" else "🚨"
    
    # 📝 안드로이드 앱 버전 정보 표기
    app_info = f"\n*앱 버전*: Android STG v{app_version}"
    
    detail_text = "\n\n📂 *모듈별 상세 결과*:"
    for name, stats in detail_results.items():
        detail_text += f"\n• {name} : 총 {stats['total']}개 (성공: {stats['pass']}, 실패: {stats['fail']})"
    
    summary = f"\n\n📈 *통합 통계*: 총 {final_stats['total']}개 (성공: {final_stats['pass']}, 실패: {final_stats['fail']})"
    
    payload = {
        "text": f"{emoji} *Android 통합 QA 자동화 결과 보고*\n*결과*: {status}{app_info}\n*내용*: {message}{detail_text}{summary}"
    }
    
    try:
        requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        print(f"📲 슬랙 보고 전송 완료 (v{app_version})")
    except Exception as e:
        print(f"❌ 슬랙 전송 에러: {e}")

def main():
    # --- ⚙️ 수동 설정 구역 ---
    CURRENT_APP_VERSION = "3.3.1(41)" # 안드로이드 빌드 버전으로 수정
    # -----------------------

    driver = None
    status = "Success"
    error_msg = "모든 시나리오가 정상 완료되었습니다."
    total_stats = {"pass": 0, "fail": 0, "total": 0}
    detail_results = {}

    # --- 1. Android 설정 (Capabilities) ---
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android_Device" # adb devices에서 확인되는 명칭 (보통 생략 가능)
    
    # 안드로이드 앱 패키지 및 액티비티 설정
    options.app_package = "com.hankyung.bloomingbit.staging"
    options.app_activity = "com.hankyung.bloomingbit.MainActivity" # 실제 메인 액티비티 확인 필요
    
    options.no_reset = True  # 앱 초기화 방지 (로그인 유지 시)
    # options.udid = "안드로이드_시리얼_번호" # 기기가 여러 대일 경우 필수

    try:
        # --- 2. Appium 세션 생성 ---
        print(f"🚀 [Android v{CURRENT_APP_VERSION}] 통합 자동화 테스트를 시작합니다...")
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        print("✅ Android 세션 생성 성공")
        time.sleep(2)

        # --- 3. 각 시나리오 순차 실행 ---
        scenarios = [
            ("aos_header", aos_header),
            ("aos_news", aos_news),
            ("aos_comment", aos_comment)
        ]

        for name, module in scenarios:
            print(f"\n--- [Step] {name} 테스트 시작 ---")
            try:
                module.run_scenario(driver)
            except Exception as e:
                status = "Fail"
                error_msg = f"{name} 단계에서 실패: {str(e)}"
                print(f"🚨 {error_msg}")
                break 
            finally:
                detail_results[name] = {
                    "pass": module.stats["pass"],
                    "fail": module.stats["fail"],
                    "total": module.stats["total"]
                }
                total_stats["pass"] += module.stats["pass"]
                total_stats["fail"] += module.stats["fail"]
                total_stats["total"] += module.stats["total"]

    except Exception as e:
        status = "Fail"
        error_msg = f"초기화 또는 드라이버 연결 실패: {str(e)}"
        print(f"🚨 {error_msg}")

    finally:
        send_slack_report(status, error_msg, total_stats, detail_results, CURRENT_APP_VERSION)
        
        if driver:
            driver.quit()
        print(f"\n🛑 [Android v{CURRENT_APP_VERSION}] 테스트 프로세스 종료")

if __name__ == "__main__":
    main()