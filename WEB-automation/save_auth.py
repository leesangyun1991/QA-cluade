"""
save_auth.py — 로그인 세션 저장 스크립트
실행: python save_auth.py
결과: auth.json (동일 디렉토리에 저장)
"""
import os
from playwright.sync_api import sync_playwright

SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth.json")
LOGIN_URL  = "https://web-stg.bloomingbit.io"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False, slow_mo=300)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="ko-KR",
        )
        page = context.new_page()
        page.goto(LOGIN_URL, wait_until="domcontentloaded")

        print("\n" + "="*60)
        print("  브라우저가 열렸습니다.")
        print("  STG 사이트에서 직접 로그인하세요.")
        print("  로그인 완료 후 이 터미널에서 Enter를 누르세요.")
        print("="*60 + "\n")
        input("  로그인 완료 후 Enter ▶ ")

        context.storage_state(path=SAVE_PATH)
        print(f"\n✅ auth.json 저장 완료: {SAVE_PATH}")
        browser.close()

if __name__ == "__main__":
    main()