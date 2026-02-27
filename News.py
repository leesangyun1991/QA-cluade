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

def send_slack_report(status, message):
    webhook_url = "https://hooks.slack.com/services/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"
    
    emoji = "✅" if status == "Success" else "🚨"
    # 통계 요약 추가
    summary = f"\n📊 *통계*: 총 {stats['total']}개 (성공: {stats['pass']}, 실패: {stats['fail']})"
    
    payload = {
        "text": f"{emoji} *QA 자동화 결과 보고*\n*결과*: {status}\n*내용*: {message}{summary}"
    }
    
    try:
        requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except Exception as e:
        print(f"❌ 슬랙 전송 에러: {e}")

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
        run_step("1번째 뉴스 클릭", lambda: driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.ImageView").instance(0)').click())
        time.sleep(2)

        run_step("뒤로가기", lambda: driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.PathView").click())
        time.sleep(2)

        run_step("2번째 뉴스 클릭", lambda: driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.ImageView").instance(1)').click())
        time.sleep(2)

        run_step("뒤로가기", lambda: driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.PathView").click())
        time.sleep(2)        

        def click_article_by_coord():
            driver.execute_script('mobile:pressKey', {"keycode": 3})
            driver.execute_script('mobile:pressKey', {"keycode": 3})
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(514, 1175)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("PiCK뉴스 > 두번째 인디게이터 이동", click_article_by_coord)
        time.sleep(2)

        def scroll_down():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(560, 1798).pointer_down().move_to_location(568, 961).release()
            actions.perform()
        run_step("스크롤 다운", scroll_down)
        time.sleep(2)

        run_step("[Only블루밍비트] 탭 선택", lambda: driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Only 블루밍비트\")").click())
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(374, 346)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[PiCK뉴스] 탭 선택", click_article_by_coord)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(175, 342)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[실시간뉴스] 탭 선택", click_article_by_coord)
        time.sleep(2)

##------------ 뉴스 상세 ------------

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(475, 572)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[실시간뉴스] 탭 > 첫번째 뉴스 상세", click_article_by_coord)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(86, 728)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뉴스 상세 > 유저액션 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(463, 545)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(447, 1930)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뉴스 상세 > 유저액션 스크롤 > 상단 스크롤 (1/2)", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(498, 440)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(494, 1062)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뉴스 상세 > 유저액션 스크롤 > 상단 스크롤 (2/2)", click_article_by_coord)
        time.sleep(2)

        # 성공 리포트 전송
        send_slack_report("Success", "모든 시나리오가 정상적으로 완료되었습니다.")

    except Exception as e:
        # 실패 리포트 전송 (정확히 어느 단계에서 죽었는지 e에 포함됨)
        send_slack_report("Fail", str(e))

    finally:
        if driver:
            driver.quit()
        print("🛑 종료")

if __name__ == "__main__":
    main()