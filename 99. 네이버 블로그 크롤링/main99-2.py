from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 크롬 드라이버 경로 설정
driver_path = "/path/to/chromedriver"
driver = webdriver.Chrome(driver_path)

# 블로그 URL 접속
blog_url = "https://blog.naver.com/tablestorystudio/223666930153"
driver.get(blog_url)

# 페이지 로드 대기
time.sleep(5)

# 본문 크롤링 (CSS 셀렉터 활용)
try:
    content = driver.find_element(By.CSS_SELECTOR, ".se-main-container").text
    print(content)
except Exception as e:
    print("크롤링 실패:", e)

# 드라이버 종료
driver.quit()
