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

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="SmoothADA3739, sangyunlee@bloomingbit.io"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("로그인 정보", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("프로필 이미지", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="취소"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'프로필 변경하기'모달 > [취소]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("프로필 이미지", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="업로드"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'프로필 변경하기'모달 > [업로드]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '(//android.widget.ImageView[@resource-id="com.google.android.documentsui:id/icon_thumb"])[1]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("디바이스 앨범 > 첫번째 이미지 첨부", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="저장"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'프로필 변경하기'모달 > [저장]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        #3초 대기...
        time.sleep(3)

        # 실행 부분
        run_step("프로필 이미지", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[4]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 첫번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[5]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 두번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[6]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 세번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[7]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 네번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[8]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 다섯번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[9]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 여섯번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[9]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 일곱번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[11]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 여덟번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[12]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 아홉번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[13]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("기본제공이미지 > 열번째 이미지 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="저장"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'프로필 변경하기'모달 > [저장]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="탈퇴하기"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[탈퇴하기]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="유의사항을 모두 확인하였고, 동의합니다."]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(1/2) > [ ]유의사항을 모두 확인하였고, 동의합니다. 체크", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="탈퇴 이유 입력하기"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[탈퇴이유 입력하기] 선택", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="자주 사용하지 않아요."]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView[2]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(2/2) > 'O 자주 이용하지 않아요.' 체크", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="알람이 너무 자주 와요."]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView[2]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(2/2) > 'O 알람이 너무 자주 와요.' 체크", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="다른 서비스를 이용하고 있어요."]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.CircleView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(2/2) > 'O 다른 서비스를 이용하고 있어요.' 체크", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="원하는 정보가 없어요."]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView[2]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(2/2) > 'O 원하는 정보가 없어요.' 체크", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="서비스 이용이 불편해요."]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView[2]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(2/2) > 'O 서비스 이용이 불편해요.' 체크", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="직접 입력"]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.CircleView'
            
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
            actions.w3c_actions.pointer_action.move_to_location(381, 1494)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("'직접입력'인풋필드 활성화", click_article_by_coord)
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
            element.send_keys("자동화 탈퇴사유 입력")
            time.sleep(1)
        
        # 실행
        run_step("탈퇴사유 입력", input_comment_reliable)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(2/2) > 뒤로가기", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("회원탈퇴(1/2) > 뒤로가기", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("프로필 편집 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="내 활동"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("마이페이지 > [내 활동 >]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="댓글 / 답글"]'
            
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
            actions.w3c_actions.pointer_action.move_to_location(413, 523)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[댓글/답글]탭 > 최상단 목록 선택", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("게시글 상세 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="게시글"]'
            
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
            actions.w3c_actions.pointer_action.move_to_location(420, 498)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("[게시글]탭 > 최상단 목록 선택", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("게시글 상세 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("내 활동 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="공지사항"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("고객지원 > [공지사항 >]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="[공지] 이용약관 개정 안내 (AI 서비스 도입 관련)"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("공지사항 > 상단 첫번째 공지사항목록]", click_by_full_xpath)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(590, 1796)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(590, 1160)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("공지사항 상세 > 하단방향 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(516, 605)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(516, 2031)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("공지사항 상세 > 상단방향 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("공지사항 상세 > 뒤로가기]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.SvgView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("공지사항 > 뒤로가기]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="문의하기"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("고객지원 > [문의하기 >]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.ImageButton[@content-desc="탭 닫기"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("왈라폼 인웹뷰 종료", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="개인정보 처리방침"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("약관 및 정책 > [개인정보 처리방침 >]", click_by_full_xpath)

        # #3초 대기...
        time.sleep(3)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(509, 338)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("개인정보 처리방침 > '시행/변경일자' 펼침", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(448, 544)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("시행/변경일자 > 날짜 변경", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("개인정보 처리방침 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="서비스 이용약관"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("약관 및 정책 > [서비스 이용약관 >]", click_by_full_xpath)

        # #3초 대기...
        time.sleep(3)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(462, 331)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("서비스 이용약관 > '시행/변경일자' 펼침", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(459, 541)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("시행/변경 일자 > 날짜 변경", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("서비스 이용약관 > 뒤로가기", click_by_full_xpath)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(498, 1875)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(509, 697)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("내 정보 > 하단방향 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="커뮤니티 운영정책"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("약관 및 정책 > [커뮤니티 운영정책 >]", click_by_full_xpath)

        # #3초 대기...
        time.sleep(3)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(452, 331)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("서비스 이용약관 > '시행/변경일자' 펼침", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(445, 541)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("시행/변경 일자 > 날짜 변경", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("서비스 이용약관 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="윤리강령 청소년보호정책"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("약관 및 정책 > [윤리강령 청소년보호정책 >]", click_by_full_xpath)

        # #3초 대기...
        time.sleep(3)

        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(455, 324)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("윤리강령 청소년보호정책 > '시행/변경일자' 펼침", click_article_by_coord)
        time.sleep(2)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(448, 541)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("시행/변경 일자 > 날짜 변경", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("서비스 이용약관 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="알림설정"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("앱설정 > [알림설정 >]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 푸시알림받기 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 푸시알림받기 Toggle : on", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 추천뉴스 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 추천뉴스 Toggle : on", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)
        
        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[4]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 시세 급변동 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[4]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 시세 급변동 Toggle : on", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[5]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 거래소 상폐관리 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[5]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 거래소 상폐관리 Toggle : on", click_by_full_xpath)
        
        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[6]/android.view.ViewGroup/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 댓글/답글 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[6]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 댓글/답글 Toggle : on", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[7]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 입출금 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[7]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 입출금 Toggle : on", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="약관 보기"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 마케팅 수신 동의사항 > [약관 보기]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="약관 보기"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > '마케팅 수신 동의사항'모달 > [확인]", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[9]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 마케팅 수신 동의사항 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[9]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 마케팅 수신 동의사항 Toggle : on", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[10]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 야간 수신 동의 Toggle : off", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[10]/android.view.ViewGroup'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 야간 수신 동의 Toggle : on", click_by_full_xpath)

        #2초 대기...
        time.sleep(2)

        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//com.horcrux.svg.PathView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("푸시알림 설정 > 뒤로가기", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="언어"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("앱설정 > [언어 >]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="English"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("언어 설정 > [English]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="취소"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'언어를 변경하시겠습니까?'모달 > [취소]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="English"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("언어 설정 > [English]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="언어 변경"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'언어를 변경하시겠습니까?'모달 > [언어변경]", click_by_full_xpath)

        #5초 대기...
        time.sleep(5)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.View[@content-desc="My Page"]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("Nav > [(en)내 정보]", click_by_full_xpath)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(544, 1843)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(544, 822)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(en)내 정보 > 하단방향 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="Language"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[(en)내 정보] > [(en)언어 >]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="日本語"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("(en)언어 설정 > [日本語]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="Cancel"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'(en)언어를 변경하시겠습니까?'모달 > [취소]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="日本語"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("(en)언어 설정 > [日本語]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="Change Language"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'(en)언어를 변경하시겠습니까?'모달 > [언어변경]", click_by_full_xpath)

        #5초 대기...
        time.sleep(5)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.View[@content-desc="マイページ"]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("Nav > [(ja)내 정보]", click_by_full_xpath)


        def click_article_by_coord():
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(544, 1843)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(544, 822)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        run_step("(ja)내 정보 > 하단방향 스크롤", click_article_by_coord)
        time.sleep(2)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="言語"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("[(en)내 정보] > [(ja)언어 >]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="한국어"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("(ja)언어 설정 > [한국어]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="キャンセル"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'(ja)언어를 변경하시겠습니까?'모달 > [취소]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.view.ViewGroup[@content-desc="한국어"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("(ja)언어 설정 > [한국어]", click_by_full_xpath)


        def click_by_full_xpath():
            # 제공해주신 긴 XPath 값
            xpath = '//android.widget.TextView[@text="言語変更"]'
            
            # 10초 대기 후 요소가 발견되면 즉시 클릭
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click()

        # 실행 부분
        run_step("'(ja)언어를 변경하시겠습니까?'모달 > [언어변경]", click_by_full_xpath)

        #5초 대기...
        time.sleep(5)

    finally:
        if driver:
            driver.quit()
        print("🛑 종료")

if __name__ == "__main__":
    main()