from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ChromeDriver 경로 설정
driver_path = "C:/Users/highk/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)

# Selenium WebDriver 실행
driver = webdriver.Chrome(service=service)

# 크롤링할 블로그 URL 리스트
blog_urls = [
    "https://blog.naver.com/tablestorystudio/223666930153",
    "https://blog.naver.com/art2000umin",
    "https://blog.naver.com/tablestorystudio/222286293862",
    "https://blog.naver.com/tablestorystudio/222300131723"

]

# 크롤링 결과 저장 리스트
results = []

# 블로그 크롤링
for url in blog_urls:
    driver.get(url)
    
    try:
        # iframe으로 전환
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mainFrame"))
        )
        driver.switch_to.frame("mainFrame")

        # 블로그 제목
        title = driver.find_element(By.CSS_SELECTOR, ".pcol1").text

        # 블로그 본문 내용
        content = driver.find_element(By.CSS_SELECTOR, ".se-main-container").text

        # 이미지 URL 수집
        images = driver.find_elements(By.CSS_SELECTOR, ".se-image-resource")
        image_urls = [img.get_attribute("src") for img in images]

        # 태그 수집
        tags = driver.find_elements(By.CSS_SELECTOR, ".se-module-tag .se-tag")
        tag_list = [tag.text for tag in tags]

        # 댓글 수집
        comments = driver.find_elements(By.CSS_SELECTOR, ".u_cbox_contents")
        comment_list = [comment.text for comment in comments]

        # 결과 저장
        results.append({
            "URL": url,
            "Title": title,
            "Content": content,
            "Image URLs": ", ".join(image_urls),
            "Tags": ", ".join(tag_list),
            "Comments": ", ".join(comment_list)
        })

    except Exception as e:
        print(f"오류 발생 ({url}): {e}")
    
    finally:
        # iframe 전환 해제
        driver.switch_to.default_content()

    # 요청 간 대기 시간 추가
    time.sleep(2)

# 브라우저 종료
driver.quit()

# 크롤링 결과를 DataFrame으로 저장
df = pd.DataFrame(results)

# CSV 파일로 저장
df.to_csv("blog_data.csv", index=False, encoding="utf-8-sig")
print("크롤링 데이터가 blog_data.csv에 저장되었습니다!")
