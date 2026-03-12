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

######################뉴스 홈######################

    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(112, 236)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("PiCK뉴스 > (메인)첫번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(28, 87)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(291, 228)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("PiCK뉴스 > (메인)두번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(27, 87)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(199, 380)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("PiCK뉴스 > (서브)첫번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(27, 87)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(206, 427)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("PiCK뉴스 > (서브)두번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(30, 87)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("PiCK뉴스 > 두번째 인디게이터", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[5]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("PiCK뉴스 > 세번째 인디게이터", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[6]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("PiCK뉴스 > 네번째 인디게이터", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[7]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("PiCK뉴스 > 다섯번째 인디게이터", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[8]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("PiCK뉴스 > 여섯번째 인디게이터", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("PiCK뉴스 > 첫번째 인디게이터", click_by_full_xpath)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(193, 744)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(198, 159)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[실시간 뉴스][PiCK 뉴스][Only블루밍비트] 탭 영역 최상단에 걸치도록 위치 스크롤", click_article_by_coord)
    time.sleep(4)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(143, 145)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[PiCK 뉴스]탭", click_article_by_coord)
    time.sleep(5)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(254, 145)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[Only 블루밍비트]탭", click_article_by_coord)
    time.sleep(5)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(55, 145)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[실시간 뉴스]탭", click_article_by_coord)
    time.sleep(5)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(235, 241)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[실시간 뉴스]탭 > 첫번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(28, 87)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(199, 358)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[실시간 뉴스]탭 > 두번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(30, 89)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(150, 145)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[PiCK 뉴스]탭", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(187, 244)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[PiCK 뉴스]탭 > 첫번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(31, 89)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(187, 244)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[PiCK 뉴스]탭 > 두번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(28, 89)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(251, 146)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[Only 블루밍비트]탭", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(197, 250)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[Only 블루밍비트]탭 > 첫번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(27, 89)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(192, 411)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("[Only 블루밍비트]탭 > 두번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(28, 87)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(204, 650)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(201, 204)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뉴스목록 > 하단방향 스크롤(1/5)", click_article_by_coord)
    time.sleep(1)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(212, 692)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(213, 400)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뉴스목록 > 하단방향 스크롤(2/5)", click_article_by_coord)
    time.sleep(1)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(199, 640)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(199, 214)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뉴스목록 > 하단방향 스크롤(3/5)", click_article_by_coord)
    time.sleep(1)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(204, 682)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(208, 259)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뉴스목록 > 하단방향 스크롤(4/5)", click_article_by_coord)
    time.sleep(1)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(196, 683)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(197, 211)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    run_step("뉴스목록 > 하단방향 스크롤(5/5)", click_article_by_coord)
    time.sleep(1)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeButton[@name="뉴스, tab, 1 of 5"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("뉴스 홈 > 최상단 스크롤", click_by_full_xpath)

######################뉴스 상세######################

    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(112, 236)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("PiCK뉴스 > (메인)첫번째 뉴스", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(38, 292)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뉴스 상세 > '유저액션' 위치 스크롤", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(38, 292)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("유저액션 > [좋아요]", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(38, 292)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("유저액션 > [슬퍼요]", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(203, 214)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("유저액션 > [화나요]", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(291, 214)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("유저액션 > [놀랐어요]", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(385, 215)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("유저액션 > [불안해요]", click_article_by_coord)
    time.sleep(2)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(1/4)", swipe_to_top)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(2/4)", swipe_to_top)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(3/4)", swipe_to_top)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(4/4)", swipe_to_top)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(38, 292)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뉴스 상세 > '댓글' 위치 스크롤", click_article_by_coord)
    time.sleep(2)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(1/5)", swipe_to_top)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(2/5)", swipe_to_top)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(3/5)", swipe_to_top)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(4/5)", swipe_to_top)


    def swipe_to_top():
        # 'swipe'는 'scroll'보다 동작이 빠르고 가볍습니다.
        # 아래 방향(down)으로 쓸어내려야 화면이 위(top)로 올라갑니다.
        driver.execute_script('mobile: swipe', {'direction': 'down'})

    run_step("뉴스 상세 > 최상단 스와이프 이동(5/5)", swipe_to_top)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(355, 278)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뉴스 상세 > [인용하기]", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(28, 91)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(403, 279)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뉴스상세 > [공유하기]", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(268, 211)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뉴스상세 > '공유하기 모달' 해제", click_article_by_coord)
    time.sleep(2)


    def swipe_to_bottom():
        # 'up' 방향은 손가락을 위로 올리는 동작이며, 
        # 결과적으로 화면(콘텐츠)은 아래쪽(Bottom)으로 내려가게 됩니다.
        driver.execute_script('mobile: swipe', {'direction': 'up'})

    # 실행 부분 (스텝 이름도 하단 이동으로 변경)
    run_step("뉴스 상세 > 하단 방향 스크롤(1/3)", swipe_to_bottom)
    time.sleep(2)


    def swipe_to_bottom():
        # 'up' 방향은 손가락을 위로 올리는 동작이며, 
        # 결과적으로 화면(콘텐츠)은 아래쪽(Bottom)으로 내려가게 됩니다.
        driver.execute_script('mobile: swipe', {'direction': 'up'})

    # 실행 부분 (스텝 이름도 하단 이동으로 변경)
    run_step("뉴스 상세 > 하단 방향 스크롤(2/3)", swipe_to_bottom)
    time.sleep(2)


    def swipe_to_bottom():
        # 'up' 방향은 손가락을 위로 올리는 동작이며, 
        # 결과적으로 화면(콘텐츠)은 아래쪽(Bottom)으로 내려가게 됩니다.
        driver.execute_script('mobile: swipe', {'direction': 'up'})

    # 실행 부분 (스텝 이름도 하단 이동으로 변경)
    run_step("뉴스 상세 > 하단 방향 스크롤(3/3)", swipe_to_bottom)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(218, 239)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()



    run_step("뉴스상세 > '인물페이지'배너", click_article_by_coord)
    time.sleep(2)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeButton[@name="뉴스, tab, 1 of 5"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("Navigation > [뉴스]", click_by_full_xpath)


def main():
    # iOS 설정 (XCUITest)
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.device_name = "이상윤이의 iPhone"  # Xcode에서 확인된 기기 명칭
    options.udid = "00008110-001459E022D1401E"                 # 실물 기기 연결 시 auto 혹은 실제 UDID 입력
    
    # Xcode에서 설정한 본인의 Bundle ID 및 팀 정보 반영
    options.bundle_id = "com.hankyung.bloomingbit.staging" # 혹은 테스트할 앱 번들 ID
    options.xcode_org_id = "H58K49T23N"          # BLOOMINGBIT 팀 ID
    options.xcode_signing_id = "iPhone Developer"
    
    # 중요: Xcode에서 수정한 WebDriverAgentRunner의 번들 아이디와 일치해야 함
    options.set_capability("appium:updatedWdaBundleId", "com.sangyunlee.WebDriverAgentRunner.bloomingbit01")

    driver = None

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