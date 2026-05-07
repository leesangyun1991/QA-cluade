from playwright.sync_api import sync_playwright

def do_login():
    with sync_playwright() as p:
        # 녹화기 없이 순수 크롬 브라우저만 실행
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./temp_profile", # 임시 프로필 사용
            channel="chrome",               # 진짜 구글 크롬 사용
            headless=False,                 # 화면 보이게
            args=["--disable-blink-features=AutomationControlled"] # 봇 탐지 방어막
        )
        page = browser.pages[0]
        page.goto("https://web-stg.bloomingbit.io/")
        
        print("\n" + "="*50)
        print("🚀 브라우저가 열렸습니다! 직접 구글 로그인을 진행해 주세요.")
        print("🚀 로그인이 완전히 끝나고 메인 화면이 보이면,")
        print("🚀 이 터미널 창으로 돌아와서 [Enter] 키를 누르세요!")
        print("="*50 + "\n")
        
        # 사용자가 엔터를 칠 때까지 대기
        input("✅ 로그인 완료 후 엔터를 눌러주세요... ")
        
        # 세션을 auth.json으로 저장
        browser.storage_state(path="auth.json")
        print("🎉 auth.json 세션 저장 완료! 창을 닫습니다.")
        browser.close()

if __name__ == "__main__":
    do_login()