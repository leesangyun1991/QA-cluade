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

        def input_comment_reliable():
            # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
            try:
                # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            except:
                # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
                element = driver.switch_to.active_element

            # 2. 클릭하여 확실히 포커스 주기
            element.click()
            time.sleep(1)

            # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
            # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
            element.send_keys("게시글 에디터 본문 자동화테스트 입력")
            time.sleep(1)

        # 실행
        run_step("본문내용 입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(74, 167)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뒤로가기", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(216, 1348)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'! 글 작성을 취소하시겠습니까?'모달 > [닫기]", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(74, 167)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뒤로가기", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(656, 1348)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'! 글 작성을 취소하시겠습니까?'모달 > [작성취소]", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(287, 482)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("게시글 에디터", click_article_by_coord)
        time.sleep(2)


        def input_comment_reliable():
            # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
            try:
                # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            except:
                # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
                element = driver.switch_to.active_element

            # 2. 클릭하여 확실히 포커스 주기
            element.click()
            time.sleep(1)

            # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
            # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
            element.send_keys("게시글 에디터 본문 자동화테스트 입력")
            time.sleep(1)

        # 실행
        run_step("본문내용 입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1014, 170)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[등록]", click_article_by_coord)
        time.sleep(4)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(71, 170)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("게시글 상세 > 뒤로가기", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(287, 482)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("게시글 에디터", click_article_by_coord)
        time.sleep(3)


        def input_comment_reliable():
            # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
            try:
                # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            except:
                # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
                element = driver.switch_to.active_element

            # 2. 클릭하여 확실히 포커스 주기
            element.click()
            time.sleep(1)

            # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
            # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
            element.send_keys("게시글 에디터 본문 자동화테스트 입력")
            time.sleep(1)

        # 실행
        run_step("본문내용 입력", input_comment_reliable)
    

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(149, 1082)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[+ 관련코인]", click_article_by_coord)
        time.sleep(2)


        def input_comment_reliable():
            # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
            try:
                # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            except:
                # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
                element = driver.switch_to.active_element

            # 2. 클릭하여 확실히 포커스 주기
            element.click()
            time.sleep(1)

            # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
            # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
            element.send_keys("BTC")
            time.sleep(1)

        # 실행
        run_step("'코인티커' 검색어 입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(149, 1082)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'코인티커' 검색어 삭제", click_article_by_coord)
        time.sleep(2)


        def input_comment_reliable():
            # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
            try:
                # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            except:
                # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
                element = driver.switch_to.active_element

            # 2. 클릭하여 확실히 포커스 주기
            element.click()
            time.sleep(1)

            # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
            # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
            element.send_keys("BTC")
            time.sleep(1)

        # 실행
        run_step("'코인티커' 검색어 입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(199, 507)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("단말키패드 해제", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(213, 511)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("'코인티커'선택", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1014, 170)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[등록]", click_article_by_coord)
        time.sleep(4)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(71, 170)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("게시글 상세 > 뒤로가기", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(287, 482)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("게시글 에디터", click_article_by_coord)
        time.sleep(3)


        def input_comment_reliable():
            # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
            try:
                # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            except:
                # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
                element = driver.switch_to.active_element

            # 2. 클릭하여 확실히 포커스 주기
            element.click()
            time.sleep(1)

            # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
            # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
            element.send_keys("게시글 에디터 본문 자동화테스트 입력")
            time.sleep(1)

        # 실행
        run_step("본문내용 입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(149, 1082)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[+ 관련코인]", click_article_by_coord)
        time.sleep(2)


        def input_comment_reliable():
            # 1. 엘리먼트 직접 찾기 (스크린샷 기반으로 class 확인)
            try:
                # 안드로이드의 일반적인 입력창 클래스인 EditText를 찾습니다.
                element = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            except:
                # 요소를 못 찾을 경우 현재 포커스된 곳을 지정
                element = driver.switch_to.active_element

            # 2. 클릭하여 확실히 포커스 주기
            element.click()
            time.sleep(1)

            # 3. 텍스트 입력 (한글 대신 영어로 먼저 테스트 권장)
            # 팁: 기존에 써있던 글자가 있다면 clear()를 먼저 해주는 것이 좋습니다.
            element.send_keys("BTC")
            time.sleep(1)

        # 실행
        run_step("'코인티커' 검색어 입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(199, 507)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("단말키패드 해제", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(213, 511)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("'코인티커'선택", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(78, 1220)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("[앨범] 선택", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(199, 823)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("디바이스 앨범 > '첫번째' 이미지 첨부", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1014, 170)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[등록]", click_article_by_coord)
        time.sleep(4)
        

    finally:
        if driver:
            driver.quit()
        print("🛑 종료")

if __name__ == "__main__":
    main()