from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.options.android import UiAutomator2Options
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

        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(794, 390)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.move_to_location(479, 390)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 우측방향 스와이프(1/2)", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(816, 383)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.move_to_location(312, 376)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 우측방향 스와이프(2/2)", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(301, 369)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.move_to_location(706, 369)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 좌측방향 스와이프(1/2)", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(252, 383)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.move_to_location(851, 383)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 좌측방향 스와이프(2/2)", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(376, 362)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 두번째 인물 선택", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(383, 376)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 세번째 인물 선택", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(379, 376)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 네번째 인물 선택", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(387, 365)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > 다섯번째 인물 선택", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(1018, 365)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > [전체]", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(74, 167)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("뒤로가기", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(1018, 365)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물 캐러셀 > [전체]", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(539, 362)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("'인물검색'인풋필드", click_article_by_coord)
        # time.sleep(2)


        # def input_comment_reliable():
        #     # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
        #     try:
        #         # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
        #         element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
        #     except:
        #         # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
        #         element = driver.switch_to.active_element

        #     # 2. 클릭하여 확실히 포커스 주기
        #     element.click()
        #     time.sleep(1)

        #     # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
        #     # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
        #     element.send_keys("비유효 검색어")
        #     time.sleep(1)

        # # 실행
        # run_step("(비유효)인물명검색어 입력", input_comment_reliable)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(979, 358)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("검색어 삭제", click_article_by_coord)
        # time.sleep(2)


        # def input_comment_reliable():
        #     # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
        #     try:
        #         # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
        #         element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
        #     except:
        #         # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
        #         element = driver.switch_to.active_element

        #     # 2. 클릭하여 확실히 포커스 주기
        #     element.click()
        #     time.sleep(1)

        #     # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
        #     # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
        #     element.send_keys("트럼프")
        #     time.sleep(1)

        # # 실행
        # run_step("(유효)인물명검색어 입력", input_comment_reliable)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(1064, 355)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("단말키패드 종료", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(135, 574)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("검색결과 > 첫번째 인물 선택", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(869, 1234)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.move_to_location(113, 1227)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물상세 > 뉴스카드 우측 1칸 스와이프", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(411, 1213)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.move_to_location(1032, 1213)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물상세 > 뉴스카드 좌측 1칸 스와이프", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(528, 1238)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("인물상세 > 중앙 뉴스카드 선택", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(71, 170)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("뒤로가기", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(312, 1993)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("$$인물명$$의 지지율은? > [지지해요]활성화", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(309, 1993)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("$$인물명$$의 지지율은? > [지지해요]활성화 해제", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(819, 2000)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("$$인물명$$의 지지율은? > [아쉬워요]활성화", click_article_by_coord)
        # time.sleep(2)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(812, 1989)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.pause(0.1)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("$$인물명$$의 지지율은? > [아쉬워요]활성화 해제", click_article_by_coord)
        # time.sleep(2)       
        

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(539, 1681)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(539, 1092)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("임의의 위치 하단방향 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_realtime_opinion():
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.widget.Button[1]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[실시간 의견 >]", click_realtime_opinion)


        def click_realtime_opinion():
            xpath = '//android.widget.Button[@text="관련 뉴스"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[관련뉴스]탭", click_realtime_opinion)


        def click_realtime_opinion():
            xpath = '//android.widget.Button[@text="실시간 의견"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[실시간 의견]탭", click_realtime_opinion)


        def click_by_full_xpath():
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("뒤로가기", click_by_full_xpath)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(532, 1723)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(535, 592)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("임의의 위치 하단방향 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.widget.Button[2]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[관련 뉴스 >]", click_by_full_xpath)


        def click_realtime_opinion():
            xpath = '//android.widget.Button[@text="실시간 의견"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[실시간 의견]탭", click_realtime_opinion)


        def click_realtime_opinion():
            xpath = '//android.widget.Button[@text="관련 뉴스"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[관련뉴스]탭", click_realtime_opinion)



        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("뒤로가기", click_by_full_xpath)


        # def click_article_by_coord():
        #     actions = ActionChains(driver)
        #     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        #     actions.w3c_actions.pointer_action.move_to_location(553, 532)
        #     actions.w3c_actions.pointer_action.pointer_down()
        #     actions.w3c_actions.pointer_action.move_to_location(557, 1667)
        #     actions.w3c_actions.pointer_action.release()
        #     actions.perform()

        # run_step("임의의 위치 상단방향 스크롤", click_article_by_coord)
        # time.sleep(2)



    finally:
        if driver:
            driver.quit()
        print("🛑 종료")

if __name__ == "__main__":
    main()