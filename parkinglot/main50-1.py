# 필요한 패키지 설치
import sys
import subprocess

# 패키지 설치 (Replit의 requirements.txt와 별개로 코드 내에서 설치)
subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "pandas", "flask"])

import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template
import threading
import time
from zoneinfo import ZoneInfo  # 한국 시간대 설정을 위해 추가
import os
import random
from bs4 import BeautifulSoup

# Signal.bz 뉴스 페이지 URL
URL = "https://signal.bz/news"

# 네이버 날씨 페이지 URL
WEATHER_URL = "https://weather.naver.com/today/02281576"

# Flask 앱 초기화
app = Flask(__name__)

# 전역 변수로 데이터 캐싱 및 타임스탬프 저장
cached_terms = []
cached_popular_news = []
cached_timestamp = ""
cached_weather_screenshot = None  # 스크린샷 파일명 저장

# 실시간 검색어 가져오기 함수
def get_realtime_search_terms(url):
    try:
        options = Options()
        options.add_argument("--headless")  # 헤드리스 모드 설정
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.rank-text")))

        search_elements = driver.find_elements(By.CSS_SELECTOR, "span.rank-text")
        terms = [element.text.strip() for element in search_elements[:10]]

        # 이모지 리스트
        emoji_list = ["🌟", "🔥", "✨", "💥", "🌈", "⚡", "💡", "⭐", "🎯", "📈"]
        terms_with_emojis = [f"{random.choice(emoji_list)} {term}" for term in terms]

        driver.quit()
        return terms_with_emojis
    except Exception as e:
        print(f"[ERROR] 실시간 검색어 수집 중 오류 발생: {e}")
        return []

# 인기 뉴스 가져오기 함수
def get_popular_news(url=None):
    try:
        today = datetime.datetime.now(ZoneInfo('Asia/Seoul')).strftime("%Y%m%d")
        nate_url = f"https://news.nate.com/rank/interest?sc=all&p=day&date={today}"
        
        print(f"[DEBUG] 접속 URL: {nate_url}")
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--lang=ko_KR")
        options.add_argument("--encoding=euc-kr")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd('Network.setBypassServiceWorker', {'bypass': True})
        
        print("[DEBUG] 브라우저 시작")
        
        driver.get(nate_url)
        time.sleep(3)  # 초기 로딩 대기
        
        print("[DEBUG] 페이지 로드 완료")
        
        try:
            # BeautifulSoup으로 파싱
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            news_items = []
            emoji_list = ['🖼', '📌', '📢', '🧠', '📖', '🎧', '✍️', '🔔', '💡']
            
            # 모스 항목 찾기
            news_list = soup.select('div.mduList ul > li')
            print(f"[DEBUG] 찾은 뉴스 항목 수: {len(news_list)}")
            
            for idx, item in enumerate(news_list[:10], 1):
                try:
                    # 순위 찾기
                    rank_elem = item.select_one('dl.mduRank dt em')
                    rank = rank_elem.text if rank_elem else str(idx)
                    
                    # 제목과 링크 찾기
                    link_elem = item.select_one('a.lt1')
                    title_elem = item.select_one('h2.tit')
                    
                    if link_elem and title_elem:
                        link = link_elem.get('href', '#')
                        if not link.startswith('http'):
                            link = 'https://news.nate.com' + link
                        
                        title = title_elem.text.strip()
                        
                        news_item = f"{random.choice(emoji_list)} {rank}위 - <a href='{link}' target='_blank'>{title}</a>"
                        news_items.append(news_item)
                        print(f"[DEBUG] 뉴스 항목 추가: {rank}위 - {title}")
                    
                except Exception as e:
                    print(f"[ERROR] {idx}위 뉴스 처리 중 상세 오류: {str(e)}")
                    continue
            
            driver.quit()
            return news_items
            
        except Exception as e:
            print(f"[ERROR] 뉴스 항목 처리 중 오류: {str(e)}")
            print("[DEBUG] 페이지 소스:", driver.page_source[:1000])
            if 'driver' in locals():
                driver.quit()
            return []
            
    except Exception as e:
        print(f"[ERROR] 인기 뉴스 수집 중 오류: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return []

# 검색어 출력 및 저장 함수 (선택 사항)
def save_search_terms(terms, popular_news):
    current_date = datetime.datetime.now(ZoneInfo('Asia/Seoul')).strftime("%Y%m%d_%H%M%S")

    # 저장할 폴더 이름
    save_folder = "news_data"

    # 폴더가 없으면 생성
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    if terms:
        df = pd.DataFrame(terms, columns=['실시간 검색어'])
        filename = os.path.join(save_folder, f"실검top10_{current_date}.csv")
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    if popular_news:
        df_popular = pd.DataFrame(popular_news, columns=['인기 뉴스'])
        filename_popular = os.path.join(save_folder, f"인기뉴스_{current_date}.csv")
        df_popular.to_csv(filename_popular, index=False, encoding='utf-8-sig')

# 네이버 날씨 페이지 스크린샷 가져오기 함수
def get_weather_screenshot(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")  # 창 크기 설정

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # 페이지가 완전히 로드될 때까지 대기
        time.sleep(5)

        # 날씨 정보 영역 찾기
        weather_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.weather_area"))
        )

        # 스크린샷 저장
        if not os.path.exists('static'):
            os.makedirs('static')
        screenshot_path = "static/weather.png"
        weather_element.screenshot(screenshot_path)

        driver.quit()
        return screenshot_path
    except Exception as e:
        print(f"[ERROR] 날씨 페이지 스크린샷 중 오류 발생: {e}")
        return None

# 데이터 업데이트 함수
def update_data():
    global cached_terms, cached_popular_news, cached_timestamp, cached_weather_screenshot

    # 최초 실행 시 즉시 업데이트
    now = datetime.datetime.now(ZoneInfo("Asia/Seoul"))
    cached_terms = get_realtime_search_terms(URL)
    cached_popular_news = get_popular_news(URL)
    save_search_terms(cached_terms, cached_popular_news)
    day_of_week = now.strftime("%A")  # 영어 요일
    korean_days = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }
    korean_day = korean_days.get(day_of_week, day_of_week)
    am_pm = "오전" if now.hour < 12 else "오후"
    hour = now.hour % 12
    hour = 12 if hour == 0 else hour
    minute = now.minute
    cached_timestamp = f"{now.year}년 {now.month}월 {now.day}일 {korean_day} {am_pm}{hour}시 {minute}분 기준"
    cached_weather_screenshot = get_weather_screenshot(WEATHER_URL)

    # 이후부터는 매 정시에만 업데이트
    while True:
        now = datetime.datetime.now(ZoneInfo("Asia/Seoul"))

        # 00시 ~ 06시는 업데이트 중단
        if 0 <= now.hour < 6:
            time.sleep(3600)  # 1시간 대기 후 다시 체크
            continue

        # 정각 체크
        if now.minute == 0:
            # 실시간 검색어와 인기 뉴스 업데이트
            cached_terms = get_realtime_search_terms(URL)
            cached_popular_news = get_popular_news(URL)
            save_search_terms(cached_terms, cached_popular_news)

            # 현재 날짜와 시간 저장
            day_of_week = now.strftime("%A")  # 영어 요일
            korean_day = korean_days.get(day_of_week, day_of_week)
            am_pm = "오전" if now.hour < 12 else "오후"
            hour = now.hour % 12
            hour = 12 if hour == 0 else hour
            minute = now.minute
            cached_timestamp = f"{now.year}년 {now.month}월 {now.day}일 {korean_day} {am_pm}{hour}시 {minute}분 기준"

            # 네이버 날씨 페이지 스크린샷 가져오기
            cached_weather_screenshot = get_weather_screenshot(WEATHER_URL)

        # 다음 체크까지 10분 대기
        time.sleep(600)

# 백그라운드 스레드 시작
thread = threading.Thread(target=update_data)
thread.daemon = True
thread.start()

# Flask 라우트 설정
@app.route('/')
def index():
    # 캐시된 데이터를 사용
    terms = cached_terms
    popular_news = cached_popular_news
    timestamp = cached_timestamp
    weather_screenshot = cached_weather_screenshot  # 스크린샷 파일명

    return render_template('index.html', terms=terms, popular_news=popular_news, timestamp=timestamp, weather_screenshot=weather_screenshot)

# Flask 앱 실행
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
