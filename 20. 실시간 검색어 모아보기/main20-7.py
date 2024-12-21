import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import telegram
from telegram import Bot
import asyncio
import schedule

# Signal.bz 뉴스 페이지에서 실시간 검색어 10가지를 가져오기
URL = "https://signal.bz/news"

# 텔레그램 설정
API_TOKEN = '7936899167:AAFl_3jTqQ-B2b4CUPaKnf_4tWgoY1FI_os'
CHAT_ID = '1059657134'

# 실시간 검색어 가져오기 함수 (Selenium 사용)
def get_realtime_search_terms(url):
    print(f"[{datetime.datetime.now()}] 실시간 검색어 수집을 시작합니다.")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        print("웹페이지에 접속했습니다.")
        
        search_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/div/section/div/section/section[1]/div[2]/div/div/div/a/span[2]")
        terms = [element.text.strip() for element in search_elements[:10]]
        
        driver.quit()
        if terms:
            print(f"[{datetime.datetime.now()}] 실시간 검색어 수집 성공: {terms}")
        else:
            print(f"[{datetime.datetime.now()}] 실시간 검색어를 수집하지 못했습니다.")
        return terms
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 실시간 검색어 수집 중 오류 발생: {e}")
        return []

# 인기 뉴스 가져오기 함수 (Selenium 사용)
def get_popular_news(url):
    print(f"[{datetime.datetime.now()}] 인기 뉴스 수집을 시작합니다.")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        print("웹페이지에 접속했습니다.")
        
        popular_news_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/div/section/div/section/section[3]/div/section/div/div/div/div[2]")
        popular_news = [element.text.strip() for element in popular_news_elements[:10]]
        
        driver.quit()
        if popular_news:
            print(f"[{datetime.datetime.now()}] 인기 뉴스 수집 성공: {popular_news}")
        else:
            print(f"[{datetime.datetime.now()}] 인기 뉴스를 수집하지 못했습니다.")
        return popular_news
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 인기 뉴스 수집 중 오류 발생: {e}")
        return []

# 검색어 출력 및 저장 함수
def save_search_terms(terms, popular_news):
    print(f"[{datetime.datetime.now()}] 검색어 및 인기 뉴스 저장을 시작합니다.")
    if terms:
        df = pd.DataFrame(terms, columns=['실시간 검색어'])
        current_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"실검top10_{current_date}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"검색어가 파일로 저장되었습니다: {filename}")
        print(df)  # 콘솔에 데이터프레임 출력
    else:
        print("검색어를 가져올 수 없습니다.")
    
    if popular_news:
        df_popular = pd.DataFrame(popular_news, columns=['인기 뉴스'])
        filename_popular = f"인기뉴스_{current_date}.csv"
        df_popular.to_csv(filename_popular, index=False, encoding='utf-8-sig')
        print(f"인기 뉴스가 파일로 저장되었습니다: {filename}")
        print(df_popular)  # 콘솔에 데이터프레임 출력
    else:
        print("인기 뉴스를 가져올 수 없습니다.")

# 텔레그램으로 메시지 전송 함수
async def send_message(api_token, chat_id, message):
    print(f"[{datetime.datetime.now()}] 텔레그램 메시지 전송을 시작합니다.")
    bot = Bot(token=api_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print(f"[{datetime.datetime.now()}] 메시지가 성공적으로 전송되었습니다.")
    except telegram.error.TelegramError as e:
        print(f"[{datetime.datetime.now()}] 메시지 전송 실패: {e}")

# 주기적으로 실행하는 함수
def job():
    print(f"[{datetime.datetime.now()}] 주기적 작업 실행 시작")
    current_hour = datetime.datetime.now().hour

    # 한국 시간 기준으로 오후 11시부터 오전 8시까지는 전송하지 않음
    if 23 <= current_hour or current_hour < 8:
        print(f"[{datetime.datetime.now()}] 현재는 메시지를 보내지 않는 시간입니다.")
        return
    
    realtime_terms = get_realtime_search_terms(URL)
    popular_news = get_popular_news(URL)
    save_search_terms(realtime_terms, popular_news)
    
    loop = asyncio.get_event_loop()
    
    if realtime_terms:
        message = "🔍 <b>실시간 검색어</b>:\n"
        for idx, term in enumerate(realtime_terms, start=1):
            message += f"{idx}. {term}\n"
        loop.run_until_complete(send_message(API_TOKEN, CHAT_ID, message))
    
    if popular_news:
        message = "📰 <b>인기 뉴스</b>:\n"
        for idx, news in enumerate(popular_news, start=1):
            message += f"{idx}. {news}\n"
        loop.run_until_complete(send_message(API_TOKEN, CHAT_ID, message))

import schedule

# 스케줄 설정 - 1시간마다 실행
schedule.every(4).hours.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(600)  # 1분마다 스케줄 확인
