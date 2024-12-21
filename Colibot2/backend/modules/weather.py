from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz
import os
import time
from PIL import Image

def capture_weather(save_dir='frontend/public/weather'):
    driver = None
    try:
        # 한국 시간대 설정
        kr_timezone = pytz.timezone('Asia/Seoul')
        now = datetime.now(kr_timezone)
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        # 저장 디렉토리 생성
        os.makedirs(save_dir, exist_ok=True)

        # 이전 스크린샷 파일들 삭제
        for old_file in os.listdir(save_dir):
            if old_file.endswith('.png'):
                os.remove(os.path.join(save_dir, old_file))

        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1024,1500')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        print("Chrome 드라이버 시작...")
        driver = webdriver.Chrome(options=chrome_options)

        print("페이지 로딩 시작...")
        driver.get("https://weather.naver.com/today")  # URL 수정

        # 페이지 로딩 대기
        time.sleep(5)  # 페이지 로딩을 위한 대기 시간 증가

        # 날씨 정보 영역 찾기 (여러 선택자 시도)
        try:
            weather_section = driver.find_element(By.CLASS_NAME, "weather_area")
        except:
            try:
                weather_section = driver.find_element(By.CLASS_NAME, "section_center")
            except:
                weather_section = driver.find_element(By.TAG_NAME, "main")

        # 스크린샷 캡처
        screenshot_path = os.path.join(save_dir, f'weather_{timestamp}.png')
        driver.save_screenshot(screenshot_path)

        # 이미지 크롭
        with Image.open(screenshot_path) as im:
            # 전체 페이지에서 상단 부분만 크롭
            width = im.size[0]
            height = 800  # 상단 800픽셀만 캡처
            im_cropped = im.crop((0, 0, width, height))
            im_cropped.save(screenshot_path)

        print("드라이버 종료...")
        driver.quit()

        return f'/weather/weather_{timestamp}.png'

    except Exception as e:
        print(f"날씨 캡처 중 오류 발생: {str(e)}")
        if driver:
            driver.quit()
        raise e