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

#------------ 뉴스 메인 ------------

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(502, 401)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(498, 1591)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("자동화 스크립트 실행 전 페이지 갱신", click_article_by_coord)
        time.sleep(2)

        run_step("1번째 뉴스 클릭", lambda: driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.ImageView").instance(0)').click())
        time.sleep(2)

        run_step("뒤로가기", lambda: driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.PathView").click())
        time.sleep(2)

        run_step("2번째 뉴스 클릭", lambda: driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().className("android.widget.ImageView").instance(1)').click())
        time.sleep(2)

        run_step("뒤로가기", lambda: driver.find_element(by=AppiumBy.CLASS_NAME, value="com.horcrux.svg.PathView").click())
        time.sleep(2)        

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(518, 1175)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(PiCK뉴스)두번째 인디게이터 이동", click_article_by_coord)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(541, 1179)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(PiCK뉴스)세번째 인디게이터 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(564, 1175)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(PiCK뉴스)네번째 인디게이터 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(584, 1183)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(PiCK뉴스)다섯번째 인디게이터 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(611, 1179)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(PiCK뉴스)여섯번째 인디게이터 이동", click_article_by_coord)
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
            actions.w3c_actions.pointer_action.move_to_location(377, 331)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("[PiCK뉴스] 탭 선택", click_article_by_coord)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(140, 323)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[실시간뉴스] 탭 선택", click_article_by_coord)
        time.sleep(2)

#------------ 뉴스 상세 ------------

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(475, 572)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(실시간뉴스)첫번째 뉴스 상세", click_article_by_coord)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(70, 630)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("유저액션 위치이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(463, 545)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(447, 1930)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상단 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(226, 619)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("댓글위치 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(584, 498)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(591, 2136)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상단 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(895, 619)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[인용하기] > 게시글 에디터 진입", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(70, 175)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[인용하기] > 게시글 에디터 종료", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1008, 619)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'공유하기' 모달", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(759, 1549)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'공유하기' 모달 종료", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(89, 619)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("유저액션 위치이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(125, 490)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[좋아요] 활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(327, 502)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[슬퍼요] 활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(525, 475)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[화나요] 활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(739, 451)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[놀랐어요] 활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(969, 482)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[불안해요] 활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(518, 479)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(537, 2082)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상단 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(219, 611)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("댓글위치 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(475, 2152)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'댓글입력'인풋필드 활성화", click_article_by_coord)
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
            element.send_keys("자동화테스트중")
            time.sleep(1)

        # 실행
        run_step("테스트용 댓글입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1008, 1109)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("테스트용댓글 작성완료", click_article_by_coord)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(219, 611)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("댓글위치 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(475, 2152)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'댓글입력'인풋필드 활성화", click_article_by_coord)
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
            element.send_keys("자동화테스트중")
            time.sleep(1)

        # 실행
        run_step("테스트용 댓글입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1008, 1109)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("테스트용댓글 작성완료", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(296, 984)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'답글'바텀시트", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(475, 2152)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'답글입력'인풋필드 활성화", click_article_by_coord)
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
            element.send_keys("자동화테스트중")
            time.sleep(1)

        # 실행
        run_step("테스트용 답글입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1012, 1183)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("테스트용 답글 작성완료", click_article_by_coord)
        time.sleep(2)


        def close_bottom_sheet_by_back():
            # 안드로이드 물리 뒤로가기 키(KeyCode 4) 전송
            driver.press_keycode(4)

        run_step("'답글'바텀시트 종료(뒤로가기)", close_bottom_sheet_by_back)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(974, 329)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[최신순]필터", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(830, 323)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()


        run_step("[순공감순]필터", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(614, 733)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(604, 2174)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상단 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(226, 620)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("댓글위치 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(896, 670)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상위 댓글 [공감]선택", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(993, 661)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상위 댓글 [비공감]선택", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1015, 454)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("나의댓글 > [...]바텀시트 활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(335, 2114)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'댓글을 삭제여부 팝업' 노출", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(222, 1356)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'댓글을 삭제여부 팝업' > [취소]", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1015, 454)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("나의댓글 > [...]바텀시트 활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(391, 2123)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'댓글을 삭제여부 팝업' 노출", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(655, 1350)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'댓글을 삭제여부 팝업' > [삭제]", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(518, 479)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(537, 2082)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상단 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(219, 611)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("댓글위치 이동", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(475, 2152)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'댓글입력'인풋필드 활성화", click_article_by_coord)
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
            element.send_keys("자동화테스트중")
            time.sleep(1)

        # 실행
        run_step("테스트용 댓글입력", input_comment_reliable)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1008, 1109)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("테스트용댓글 작성완료", click_article_by_coord)
        time.sleep(2)



        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(655, 1350)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'답글'바텀시트", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(893, 658)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("메인댓글 > [공감]활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(990, 651)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("메인댓글 > [비공감]활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(874, 1015)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상단답글 > [공감]활성화", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(987, 1005)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("최상단답글 > [비공감]활성화", click_article_by_coord)
        time.sleep(2)


        def close_bottom_sheet_by_back():
            # 안드로이드 물리 뒤로가기 키(KeyCode 4) 전송
            driver.press_keycode(4)

        run_step("'답글'바텀시트 종료(뒤로가기)", close_bottom_sheet_by_back)
        time.sleep(2)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(58, 191)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("뒤로가기", close_bottom_sheet_by_back)
        time.sleep(2)

    finally:
        if driver:
            driver.quit()
        print("🛑 종료")

if __name__ == "__main__":
    main()