from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime, timedelta
import telegram
from telegram import Bot
import asyncio

# 크롬 드라이버 경로 설정 (사용 환경에 맞게 변경하세요)
CHROME_DRIVER_PATH = 'C:/Users/highk/.wdm/drivers/chromedriver/win64/130.0.6723.116/chromedriver.exe'  # 실제 크롬 드라이버 경로로 변경

# 네이버 서울 날씨 URL
URL = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&oquery=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%82%A0%EC%94%A8&tqi=i0anedqo15wssNoW5J8ssssssdK-395548"

# 텔레그램 봇 설정
API_TOKEN = '7936899167:AAFl_3jTqQ-B2b4CUPaKnf_4tWgoY1FI_os'  # 실제 봇 API 토큰으로 변경
CHAT_ID = '1059657134'  # 메시지를 보낼 채팅 ID

# 브라우저 옵션 설정 (헤드리스 모드)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 캡처 파일 저장 경로 설정
BASE_PATH = r"C:\Users\highk\pypy50\31. (응용) 네이버 날씨 검색후 텔레그램 전송 스케줄링"
CAPTURE_PATH = os.path.join(BASE_PATH, "weather_captures")
os.makedirs(CAPTURE_PATH, exist_ok=True)

# 날씨 정보 캡처 및 텔레그램 전송 함수
def capture_and_send_weather():
    service = Service(CHROME_DRIVER_PATH)
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 네이버 날씨 페이지 열기
        driver.get(URL)
        time.sleep(3)  # 페이지 로딩 대기 (필요 시 조정)

        # 화면 캡처하여 파일로 저장 (날짜와 시간 추가)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(CAPTURE_PATH, f"seoul_weather_{now}.png")
        driver.save_screenshot(screenshot_path)
        print(f"날씨 정보 캡처 완료: {screenshot_path}")

        # 텔레그램으로 사진 전송
        bot = Bot(token=API_TOKEN)
        asyncio.run(bot.send_photo(chat_id=CHAT_ID, photo=open(screenshot_path, 'rb')))
        print(f"사진 '{screenshot_path}'이 성공적으로 전송되었습니다.")

    finally:
        # 드라이버 종료
        if 'driver' in locals():
            driver.quit()

# 매일 1분 간격으로 실행하기 위해 스케줄링 설정
def schedule_weather_updates():
    import schedule
    import time

    schedule.every(4).hours.do(capture_and_send_weather)
    print("스케줄링이 시작되었습니다. 4시간 간격으로 날씨 정보를 전송합니다.")
    next_run_time = datetime.now().replace(microsecond=0, second=0, minute=0) + timedelta(hours=4)
    print(f"다음 전송 예정 시간: {next_run_time}")

    while True:
        schedule.run_pending()
        time.sleep(1)
        now = datetime.now().replace(microsecond=0, second=0)
        if now == next_run_time:
            next_run_time += timedelta(hours=4)
            print(f"다음 전송 예정 시간: {next_run_time}")

if __name__ == "__main__":
    # 스케줄링 시작
    schedule_weather_updates()
