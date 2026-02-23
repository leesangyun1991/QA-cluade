from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time


def main():
    # 1) Inspector에서 설정한 Capabilities 그대로
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "R39M209E1GF"

    # SDK 경로 (Inspector에서 넣었던 값)
    options.set_capability("appium:androidHome", "/Users/bloomingbit/Library/Android/sdk")

    # # (설정 앱 실행 예시)
    # options.app_package = "com.android.settings"
    # options.app_activity = ".Settings"

    # 2) Appium 서버 연결
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        #-------- 뉴스 홈 ------------#
        print("✅ 세션 생성 성공")
        time.sleep(2)

        el1 = driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().className("android.widget.ImageView").instance(0)'
        )
        el1.click()
        print("✅ 뉴스홈 > PiCK뉴스 > 1번째 뉴스 클릭")

        time.sleep(2)

        el2 = driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.PathView")
        el2.click()
        print("✅ 뒤로가기")

        time.sleep(2)


        el1 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(1)")
        el1.click()
        status = driver.get_status()
        driver.execute_script('mobile:getCurrentPackage')
        print("✅ 뉴스홈 > PiCK뉴스 > 2번째 뉴스 클릭")

        time.sleep(2)

        el3 = driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.SvgView")
        el3.click()
        print("✅ 뒤로가기")

        time.sleep(2)

        el2 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.ViewGroup\").instance(30)")
        el2.click()
        print("✅ PiCK뉴스 인디게이터 2페이지")

        # el3 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"2026-02-03 [자비스] 'PICK뉴스 이미지5 개인기자'\").instance(1)")
        # el3.click()
        # print("✅ 뉴스홈 > PiCK뉴스 > 3번째 뉴스 클릭")

        # time.sleep(2)

        # el4 = driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.SvgView")
        # el4.click()
        # print("✅ 뒤로가기")

        # time.sleep(2)


        # el5 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"2026-02-03 [자비스] 'PICK뉴스 이미지5 개인기자'\").instance(2)")
        # el5.click()
        # print("✅ 뉴스홈 > PiCK뉴스 > 4번째 뉴스 클릭")

        # time.sleep(2)

        # el6 = driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.PathView")
        # el6.click()
        # print("✅ 뒤로가기")


        # el3 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"com.horcrux.svg.PathView\").instance(22)")
        # el3.click()
        # print("✅ 랭킹뉴스 펼치기")

        # time.sleep(2)


        # el4 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"com.horcrux.svg.PathView\").instance(22)")
        # el4.click()
        # print("✅ 랭킹뉴스 닫기")
        
        # time.sleep(2)


        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(560, 1798)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(568, 961)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print("✅ 스크롤 다운")

        time.sleep(2)

        el1 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"PiCK 뉴스\")")
        el1.click()
        print("✅ [PiCK뉴스] 탭 선택")

        time.sleep(2)


        el2 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.ViewGroup\").instance(44)")
        el2.click()
        print("✅ [Only블루밍비트] 탭 선택")

        time.sleep(2)

        el3 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"2026-02-05 [자비스] '거래소공지 이미지1 포모봇 기자'\").instance(0)")
        el3.click()
        print("✅ [Only블루밍비트] 탭 > 1번째 뉴스 클릭")

        time.sleep(2)

        el4 = driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.SvgView")
        el4.click()
        print("✅ 뒤로가기")

        time.sleep(2)

        el5 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"BTC\").instance(0)")
        el5.click()
        print("✅ [Only블루밍비트 탭 > 1번째 뉴스 > 코인티커 클릭]")

        time.sleep(2)

        el1 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"com.horcrux.svg.SvgView\").instance(0)")
        el1.click()
        print("✅ 뒤로가기")

        time.sleep(2)

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(555, 1828)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(596, 525)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print("✅ 하단 인피니티 스크롤 (n/1)")

        time.sleep(2)

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(525, 2004)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(533, 173)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print("✅ 하단 인피니티 스크롤 (n/2)")

        time.sleep(2)

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(517, 2042)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(523, 552)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print("✅ 하단 인피니티 스크롤 (n/3)")

        time.sleep(2)

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(528, 2047)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(525, 393)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print("✅ 하단 인피니티 스크롤 (n/4)")

        time.sleep(2)

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(542, 2063)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(547, 417)
        actions.w3c_actions.pointer_action.release()
        actions.perform()        

        print("✅ 하단 인피니티 스크롤 (n/5)")

        time.sleep(2)


    #-------- 뉴스 상세 ------------#

    


    finally:
        driver.quit()
        print("🛑 종료")


if __name__ == "__main__":
    main()