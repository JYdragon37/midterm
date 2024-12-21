from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Selenium 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 창을 띄우지 않음
chrome_options.add_argument("--disable-gpu")  # GPU 비활성화
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
)

# ChromeDriver 서비스 설정
driver_service = Service("C:/Users/highk/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")

# ChromeDriver 초기화
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

# 네이버 블로그 처리 함수
def count_images_in_naver_blog(url):
    """네이버 블로그에서 iframe 내부 이미지 수를 추출"""
    try:
        driver.get(url)
        time.sleep(2)  # 페이지 로드 대기

        # iframe 탐지 및 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)  # iframe으로 전환

        # 이미지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )

        # 이미지 태그 개수 확인
        images = driver.find_elements(By.TAG_NAME, "img")
        return len(images)  # 이미지 수 반환
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return 0
    finally:
        driver.switch_to.default_content()  # 기본 컨텍스트로 복귀

# 티스토리 블로그 처리 함수
def count_images_in_tistory_blog(url):
    """티스토리 블로그에서 이미지 수를 추출"""
    try:
        driver.get(url)
        time.sleep(5)  # 페이지 로드 대기

        # 이미지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )

        # 이미지 태그 개수 확인
        images = driver.find_elements(By.TAG_NAME, "img")
        return len(images)  # 이미지 수 반환
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return 0

# 테스트용 블로그 링크
test_links = [
    "https://blog.naver.com/zpzp9285/223636147608",  # 네이버 블로그 링크
    "https://hkebi.tistory.com/3053"  # 티스토리 블로그 링크
]

# 결과 출력
for link in test_links:
    if "naver.com" in link:
        image_count = count_images_in_naver_blog(link)
    elif "tistory.com" in link:
        image_count = count_images_in_tistory_blog(link)
    else:
        image_count = 0
    print(f"URL: {link}, Image Count: {image_count}")

# Selenium 드라이버 종료
driver.quit()
