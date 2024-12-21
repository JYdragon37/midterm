import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

def get_current_exchange_rate():
    url = "https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_USDKRW"
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않는 옵션
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        # 특정 요소가 로드될 때까지 최대 20초 대기
        wait = WebDriverWait(driver, 20)
        driver.switch_to.frame('exchangeDailyQuote')  # 프레임 전환
        date_container = wait.until(EC.presence_of_element_located((By.XPATH, '//tr[1]/td[1]')))
        rate_container = wait.until(EC.presence_of_element_located((By.XPATH, '//tr[1]/td[2]')))
        
        if date_container and rate_container:
            datetime_now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            date_text = date_container.text.strip()
            exchange_rate = rate_container.text.strip()
            real_text = f"현재시간 : {datetime_now}, 날짜 : {date_text}, USD -> KRW : {exchange_rate}"
            print(real_text)
            send_email(real_text)
        else:
            error_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: 환율 데이터를 가져올 수 없습니다."
            print(error_message)
            send_email(error_message)
    except Exception as e:
        error_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: 일반 오류 - {e}"
        print(error_message)
        send_email(error_message)
    finally:
        driver.quit()

def send_email(message):
    sender_email = "huhjungyong@gmail.com"
    receiver_email = "jeongyong@moloco.com"
    password = os.getenv("Rntqkak!200")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Daily Exchange Rate Update"

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


import threading

def schedule_task():
    while True:
        current_time = datetime.now().strftime('%H:%M')
        if current_time == '09:00':
            get_current_exchange_rate()
            time.sleep(60)  # 1분 대기 후 반복 방지
        time.sleep(1)  # 매초마다 시간 확인

if __name__ == "__main__":
    thread = threading.Thread(target=schedule_task)
    thread.daemon = True
    thread.start()
    try:
        while True:
            time.sleep(1)  # 메인 스레드를 계속 유지
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
