from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
# iOS 전용 옵션 클래스로 변경
from appium.options.ios import XCUITestOptions 
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json

# 글로벌 통계 변수
stats = {"pass": 0, "fail": 0, "total": 0}

#-- 슬렉 웹훅 수신 함수--

# def send_slack_report(status, message):
#     webhook_url = "https://hooks.slack.com/services/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"
    
#     emoji = "✅" if status == "Success" else "🚨"
#     # 통계 요약 추가
#     summary = f"\n📊 *통계*: 총 {stats['total']}개 (성공: {stats['pass']}, 실패: {stats['fail']})"
    
#     payload = {
#         "text": f"{emoji} *QA 자동화 결과 보고*\n*결과*: {status}\n*내용*: {message}{summary}"
#     }
    
#     try:
#         requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
#     except Exception as e:
#         print(f"❌ 슬랙 전송 에러: {e}")

#-- 슬렉 웹훅 수신 함수--

# 각 테스트 단계를 실행하고 카운트하는 래퍼 함수
def run_step(step_name, func):
    global stats
    stats["total"] += 1
    try:
        func()
        print(f"✅ {step_name} 통과")
        stats["pass"] += 1
        return True
    except Exception as e:
        print(f"❌ {step_name} 실패")
        stats["fail"] += 1
        raise Exception(f"[{step_name}] 단계에서 에러 발생")


# --- 통합 실행을 위한 시나리오 함수 (기존 로직 100% 유지) ---
def run_scenario(driver):
    """
    외부 드라이버를 전달받아 시나리오를 실행합니다. 
    기존 코드의 모든 함수와 호출 순서를 그대로 유지합니다.
    """

    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("header > [검색]", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("뒤로가기", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("header > [알림]", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("뒤로가기", click_by_full_xpath)


def main():
    # iOS 설정 (XCUITest)
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.device_name = "상윤이의 iPhone"  # Xcode에서 확인된 기기 명칭
    options.udid = "auto"                 # 실물 기기 연결 시 auto 혹은 실제 UDID 입력
    
    # Xcode에서 설정한 본인의 Bundle ID 및 팀 정보 반영
    options.bundle_id = "com.hankyung.bloomingbit.staging" # 혹은 테스트할 앱 번들 ID
    options.xcode_org_id = "H58K49T23N"          # BLOOMINGBIT 팀 ID
    options.xcode_signing_id = "iPhone Developer"
    
    # 중요: Xcode에서 수정한 WebDriverAgentRunner의 번들 아이디와 일치해야 함
    options.set_capability("appium:updatedWdaBundleId", "com.sangyunlee.WebDriverAgentRunner.bloomingbit01")

    driver = None

    status = "Success"
    error_msg = "모든 테스트 단계가 정상적으로 통과되었습니다."

    try:
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        print("✅ iOS 세션 생성 성공")
        time.sleep(2)

        # 개별 실행 시 시나리오 호출
        run_scenario(driver)

    except Exception as e:
            # 에러 발생 시 상태를 Fail로 변경하고 에러 메시지 저장
            status = "Fail"
            error_msg = str(e)
            print(f"❌ 에러 발생: {error_msg}")

    finally:
        send_slack_report(status, error_msg)

        if driver:
            driver.quit()
        print("🛑 종료")

if __name__ == "__main__":
    main()