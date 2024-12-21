from flask import Flask, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
from datetime import datetime
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# 크롬 드라이버 경로
CHROME_DRIVER_PATH = 'C:/Users/highk/.wdm/drivers/chromedriver/win64/130.0.6723.116/chromedriver.exe'

# 네이버 서울 날씨 URL
URL = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"

# 캡처 파일 저장 경로
BASE_PATH = r"C:\Users\highk\pypy50\31. (응용) 네이버 날씨 검색후 텔레그램 전송 스케줄링"
CAPTURE_PATH = os.path.join(BASE_PATH, "weather_captures")
os.makedirs(CAPTURE_PATH, exist_ok=True)

# 브라우저 옵션 (헤드리스 모드)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 날씨 정보 캡처 함수
def capture_weather():
    service = Service(CHROME_DRIVER_PATH)
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 네이버 날씨 페이지 열기
        driver.get(URL)
        time.sleep(3)  # 페이지 로딩 대기

        # 현재 시간 기준 파일명 생성
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(CAPTURE_PATH, f"seoul_weather_{now}.png")

        # 화면 캡처 저장
        driver.save_screenshot(screenshot_path)
        print(f"날씨 정보 캡처 완료: {screenshot_path}")
        return screenshot_path

    finally:
        driver.quit()

# API: 메인 페이지
@app.route('/')
def index():
    return "Flask Weather API is running. Use /capture_weather or /get_latest_image endpoints."

# API: 날씨 정보 캡처 및 파일 경로 반환
@app.route('/capture_weather', methods=['GET'])
def capture_weather_api():
    try:
        print("날씨 캡처 시작.")
        image_path = capture_weather()
        print(f"날씨 캡처 성공: {image_path}")
        return jsonify({'message': 'Capture completed', 'image_path': image_path}), 200
    except Exception as e:
        print(f"캡처 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500

# API: 저장된 이미지 파일 반환
@app.route('/get_latest_image', methods=['GET'])
def get_latest_image():
    try:
        # 저장된 파일 목록에서 최신 파일 찾기
        files = [f for f in os.listdir(CAPTURE_PATH) if f.endswith('.png')]
        if not files:
            return jsonify({'error': 'No images found'}), 404

        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(CAPTURE_PATH, f)))
        latest_file_path = os.path.join(CAPTURE_PATH, latest_file)

        # 파일 반환
        return send_file(latest_file_path, mimetype='image/png', as_attachment=False)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    print("Flask 서버 시작 중...")
    app.run(host='0.0.0.0', port=5000)
