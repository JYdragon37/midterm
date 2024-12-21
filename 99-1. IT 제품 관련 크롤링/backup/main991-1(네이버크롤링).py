from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import urllib.parse
import pandas as pd
import datetime
import time

# 네이버 API 키
client_id = 'Bs4d81MbFjUn7Mfc2oO5'
client_secret = 'NvF9NY3CPs'

# 키워드 리스트
keywords = ["노트북 리뷰", "노트북 추천", "태블릿 후기", "태블릿 추천"]

# 네이버 블로그 검색 함수
def search_naver_blog(keyword, display=30, start=1):
    """네이버 API를 사용하여 블로그 데이터를 수집"""
    query = urllib.parse.quote(keyword)  # 키워드 인코딩
    url = f"https://openapi.naver.com/v1/search/blog.json?query={query}&display={display}&start={start}&sort=sim"

    # 요청 헤더
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    # API 호출
    response = requests.get(url, headers=headers)

    # 결과 출력
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data['items']:
            results.append({
                "Title": item['title'],
                "Link": item['link'],
                "Description": item['description']
            })
        return results
    else:
        print(f"Error Code: {response.status_code}")
        return []

# Selenium 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 창을 띄우지 않음
chrome_options.add_argument("--disable-gpu")  # GPU 비활성화
chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 크기 제한 비활성화
chrome_options.add_argument("--disable-software-rasterizer")  # GPU 없는 환경에서 렌더링
chrome_options.add_argument("--enable-unsafe-webgl")  # WebGL 관련 경고 방지
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
)

# ChromeDriver 서비스 설정
driver_service = Service("C:/Users/highk/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

# 블로그 상세 데이터 크롤링 함수
def extract_blog_details(url):
    """블로그에서 작성자 이름, 포스팅 날짜, 이미지 수를 추출"""
    try:
        driver.get(url)
        time.sleep(2)  # 페이지 로드 대기

        # 네이버 블로그 처리
        if "naver.com" in url:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)  # iframe으로 전환

            # 작성자 이름 추출
            try:
                author = driver.find_element(By.CLASS_NAME, "nick").text
            except:
                author = "Unknown"

            # 포스팅 날짜 추출
            try:
                post_date = driver.find_element(By.CLASS_NAME, "se_publishDate").text
            except:
                post_date = "Unknown"

            # 이미지 개수 추출
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
            )
            images = driver.find_elements(By.TAG_NAME, "img")
            image_count = len(images)

        # 티스토리 블로그 처리
        elif "tistory.com" in url:
            try:
                author = driver.find_element(By.CLASS_NAME, "author").text
            except:
                author = "Unknown"

            try:
                post_date = driver.find_element(By.CLASS_NAME, "date").text
            except:
                post_date = "Unknown"

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
            )
            images = driver.find_elements(By.TAG_NAME, "img")
            image_count = len(images)

        else:
            author, post_date, image_count = "Unknown", "Unknown", 0

        return author, post_date, image_count
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return "Unknown", "Unknown", 0

# 데이터 수집
all_results = []
current_date = datetime.datetime.now().strftime("%Y%m%d")

for keyword in keywords:
    print(f"현재 키워드: {keyword}")
    keyword_results = []
    
    # 500개의 데이터를 나눠서 수집 (30개씩 요청)
    for start in range(1, 501, 30):  # 1, 31, 61, ..., 481
        results = search_naver_blog(keyword, display=30, start=start)
        keyword_results.extend(results)
        time.sleep(2)  # API 요청 간 대기

        # 중간 저장
        partial_df = pd.DataFrame(keyword_results)
        partial_file_name = f"partial_results_{keyword}_{current_date}.csv"
        partial_df.to_csv(partial_file_name, index=False, encoding="utf-8-sig")
        print(f"중간 데이터 저장: {partial_file_name}")

    # 각 키워드의 데이터 통합
    all_results.extend(keyword_results)

# 검색 결과를 데이터프레임으로 변환
df = pd.DataFrame(all_results)

# 블로그 링크별 상세 데이터 추출
print("블로그 링크에서 상세 데이터를 추출 중...")
details = df['Link'].apply(extract_blog_details)
df['Author'], df['Post_Date'], df['Image_Count'] = zip(*details)

# Selenium 드라이버 종료
driver.quit()

# 결과 저장
final_file_name = f"naver_blog_final_results_{current_date}.csv"
df.to_csv(final_file_name, index=False, encoding="utf-8-sig")
print(f"최종 데이터가 {final_file_name}에 저장되었습니다!")
