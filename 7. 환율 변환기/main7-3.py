from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

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
        else:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: 환율 데이터를 가져올 수 없습니다.")
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: 일반 오류 - {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    get_current_exchange_rate()
