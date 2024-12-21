from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
from datetime import datetime
import time

def get_trending(filename='latest_trends.csv'):
    url = "https://signal.bz/news"
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(3)

        search_elements = driver.find_elements(
            By.XPATH, 
            "//div[@class='rank-column']//span[@class='rank-text']"
        )

        trends = [element.text.strip() for element in search_elements[:10]]

        # CSV 파일로 저장 (고정된 파일명 사용)
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Rank', 'Keyword'])
            for idx, trend in enumerate(trends, 1):
                writer.writerow([idx, trend])

        driver.quit()
        return trends

    except Exception as e:
        print(f"트렌드를 가져오는데 실패했습니다: {str(e)}")
        return []