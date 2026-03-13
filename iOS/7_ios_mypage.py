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
        xpath = '//XCUIElementTypeButton[@name="내 정보, tab, 5 of 5"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("Nav > [내 정보]", click_by_full_xpath)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(169, 151)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("계정 정보", click_article_by_coord)
    time.sleep(2)


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


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(169, 151)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("계정 정보", click_article_by_coord)
    time.sleep(2)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 편집 > 프로필 이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="취소"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > [취소]", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 편집 > 프로필 이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="업로드"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > [업로드]", click_by_full_xpath)

    time.sleep(3)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(74, 249)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("디바이스 앨범 > 첫번째 이미지 파일 지정", click_article_by_coord)
    time.sleep(2)


    def click_by_full_xpath():
        xpath = '//XCUIElementTypeOther[@name="저장"]'
        
        # 1. 요소가 나타날 때까지 대기
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
        )
        
        # 2. 일반 클릭 시도
        element.click()
        time.sleep(1) # 클릭 후 반응 기다림
        
        # 3. 만약 여전히 화면이 안 넘어갔다면? (강제 터치 시도)
        # iOS에서 XCUIElementTypeOther는 일반 클릭이 잘 안 먹힐 때가 많습니다.
        try:
            driver.execute_script('mobile: tap', {'elementId': element.id})
            print("✅ [저장] 강제 탭 실행")
        except:
            pass

    run_step("프로필 변경하기 > [저장]", click_by_full_xpath)

    time.sleep(2)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 편집 > 프로필 이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[5]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '첫번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[6]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '두번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[7]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '세번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[8]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '네번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[9]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '다섯번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[10]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '여섯번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[11]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '일곱번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[12]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '여덟번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[13]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '아홉번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[14]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 변경하기 > '열번째'기본이미지", click_by_full_xpath)


    def click_by_full_xpath():
        xpath = '//XCUIElementTypeOther[@name="저장"]'
        
        # 1. 요소가 나타날 때까지 대기
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
        )
        
        # 2. 일반 클릭 시도
        element.click()
        time.sleep(1) # 클릭 후 반응 기다림
        
        # 3. 만약 여전히 화면이 안 넘어갔다면? (강제 터치 시도)
        # iOS에서 XCUIElementTypeOther는 일반 클릭이 잘 안 먹힐 때가 많습니다.
        try:
            driver.execute_script('mobile: tap', {'elementId': element.id})
            print("✅ [저장] 강제 탭 실행")
        except:
            pass

    run_step("프로필 변경하기 > [저장]", click_by_full_xpath)

    time.sleep(2)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="탈퇴하기"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("프로필 편집 > [탈퇴하기]", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="유의사항을 모두 확인하였고, 동의합니다."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(1/2) > []유의사항을 모두 확인하였고, 동의합니다. 체크활성화", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="유의사항을 모두 확인하였고, 동의합니다."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(1/2) > []유의사항을 모두 확인하였고, 동의합니다. 체크해제", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="유의사항을 모두 확인하였고, 동의합니다."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(1/2) > []유의사항을 모두 확인하였고, 동의합니다. 체크활성화", click_by_full_xpath)
    

    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="탈퇴 이유 입력하기"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(1/2) > [탈퇴이유 입력하기]", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="자주 사용하지 않아요."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(2/2) > 'O 자주 사용하지 않아요.' 체크", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="알람이 너무 자주 와요."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(2/2) > 'O 알람이 너무 자주 와요.' 체크", click_by_full_xpath) 


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="다른 서비스를 이용하고 있어요."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(2/2) > 'O 다른 서비스를 이용하고 있어요.' 체크", click_by_full_xpath) 


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="원하는 정보가 없어요."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(2/2) > 'O 원하는 정보가 없어요.' 체크", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="서비스 이용이 불편해요."]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(2/2) > 'O 서비스 이용이 불편해요.' 체크", click_by_full_xpath) 


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="직접 입력"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("회원탈퇴(2/2) > 'O 직접 입력' 체크", click_by_full_xpath)   


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(62, 568)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("회원탈퇴(2/2) > 'O 직접 입력' 체크 > '탈퇴사유'입력필드 커서 활성화", click_article_by_coord)
    time.sleep(2)


    def input_comment_reliable_ios():
                try:
                    # 1. 특정 클래스를 찾지 못할 경우를 대비해, 현재 포커스된 요소(Active Element)를 타겟팅
                    # iOS에서 클래스 탐색 실패 시 가장 확실한 대안입니다.
                    time.sleep(2.0)  # 키보드 및 입력창 활성화 대기
                    
                    # 2. 현재 화면에서 '입력 가능'해 보이는 아무 요소나 찍어서 시도
                    # (클래스 탐색 실패 시 예외처리를 통해 강제 입력 진행)
                    try:
                        xpath_input = "//XCUIElementTypeTextView | //XCUIElementTypeTextField | //*[@focusable='true']"
                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath_input)))
                        element.click()
                    except:
                        # 요소를 못 찾아도 현재 포커스된 지점에 입력 시도 (Send Keys to Active Element)
                        actions = ActionChains(driver)
                        actions.send_keys("iOS 자동화 테스트 탈퇴사유입력합니다.")
                        actions.perform()
                        return

                    # 3. 요소가 확인된 경우 일반적인 입력 진행
                    element.send_keys("iOS 자동화 테스트 탈퇴사유입력합니다.")
                    
                    # 4. 키보드 닫기 시도
                    try:
                        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Return").click()
                    except:
                        # 'Return' 대신 'Done' 또는 '완료' 버튼 대응
                        try:
                            driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Done").click()
                        except:
                            pass

                except Exception as e:
                    raise e
                
    # 실행 부분
    run_step("회원탈퇴(2/2) > 'O 직접 입력' 체크 > '탈퇴사유'입력필드 커서 활성화 > '탈퇴사유'입력", input_comment_reliable_ios)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("뒤로가기(1/2)", click_by_full_xpath)  


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeApplication[@name="stg-bloomingbit"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("뒤로가기(2/2)", click_by_full_xpath)


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


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="내 활동"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("마이페이지 > [내 활동 >]", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="댓글 / 답글"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("내 활동 > [댓글/답글]탭", click_by_full_xpath)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="게시글"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("내 활동 > [게시글]탭", click_by_full_xpath)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(62, 568)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("내 활동 > [게시글]탭 > '최상단'게시글 목록", click_article_by_coord)
    time.sleep(2)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(26, 72)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    def click_by_full_xpath():
        # 제공해주신 긴 XPath 값
        xpath = '//XCUIElementTypeOther[@name="댓글 / 답글"]'
        
        # 10초 대기 후 요소가 발견되면 즉시 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()

    # 실행 부분
    run_step("내 활동 > [댓글/답글]탭", click_by_full_xpath)


    def click_article_by_coord():
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(26, 76)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    run_step("뒤로가기", click_article_by_coord)
    time.sleep(2)


    





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