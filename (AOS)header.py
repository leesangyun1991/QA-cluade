from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
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

def main():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "R39M209E1GF"
    options.set_capability("appium:androidHome", "/Users/bloomingbit/Library/Android/sdk")

    driver = None
    try:
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        print("✅ 세션 생성 성공")
        time.sleep(2)

        # 각 시나리오 단계를 run_step으로 감싸서 통계를 냅니다.

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(899, 183)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("검색", click_article_by_coord)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(78, 218)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뒤로가기", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1019, 171)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("알림센터", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(74, 171)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뒤로가기", click_article_by_coord)
        time.sleep(2)


    finally:
        if driver:
            driver.quit()
        print("🛑 종료")

if __name__ == "__main__":
    main()