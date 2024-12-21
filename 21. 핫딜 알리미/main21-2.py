from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import telegram
from telegram import Bot
import asyncio
import schedule

# 크롬 드라이버 설정 및 브라우저 실행 함수 정의
def get_ppomppu_posts():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 브라우저가 열리지 않도록 설정 (옵션)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 크롬 드라이버 자동 설치 및 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 웹사이트 접속
        url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
        driver.get(url)

        # 페이지 로딩 시간 대기
        time.sleep(3)  # 페이지 로딩 시간을 충분히 기다려줍니다.

        # 게시물 제목과 링크 및 추천 수 추출
        titles = driver.find_elements(By.CSS_SELECTOR, "tr.baseList")

        # 텔레그램 메시지 내용 구성
        message = "📌 <b>추천 3개 이상인 게시물 목록</b>:\n"

        # 게시물 제목과 링크 출력 (추천이 3개 이상인 것만)
        if titles:
            for row in titles:
                try:
                    recommendation_text = row.find_element(By.CSS_SELECTOR, "td.baseList-space.baseList-rec").text.strip()
                    recommendation_upvotes = int(recommendation_text.split(" - ")[0])
                    if recommendation_upvotes >= 3:
                        post_title_element = row.find_element(By.CSS_SELECTOR, ".baseList-title span")
                        post_title = post_title_element.text.strip()
                        post_link = post_title_element.find_element(By.XPATH, "..")  # 부모 <a> 태그를 찾음
                        post_link_url = post_link.get_attribute("href")
                        message += f"🔗 <b>{post_title}</b>\n추천수: {recommendation_upvotes}\n<a href=\"https://www.ppomppu.co.kr/zboard/{post_link_url}\">게시물 링크</a>\n\n"
                except Exception as e:
                    # 추천 수가 없는 경우도 있으므로 예외 처리
                    print(f"[Error] 게시물 처리 중 오류 발생: {e}")
                    continue
        else:
            print("게시물을 찾을 수 없습니다. CSS 셀렉터를 확인해주세요.")

    except Exception as e:
        print(f"[Error] 웹페이지 접속 중 오류 발생: {e}")
    finally:
        # 브라우저 종료
        driver.quit()

    return message

# 텔레그램 메시지 전송 함수
async def send_message(api_token, chat_id, message):
    bot = Bot(token=api_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 메시지가 성공적으로 전송되었습니다.")
    except telegram.error.TelegramError as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 메시지 전송 실패: {e}")

# 텔레그램 설정
API_TOKEN = '7936899167:AAFl_3jTqQ-B2b4CUPaKnf_4tWgoY1FI_os'
CHAT_ID = '1059657134'

# 주기적으로 실행하는 작업 함수
def job():
    message = get_ppomppu_posts()
    if len(message) > len("📌 <b>추천 3개 이상인 게시물 목록</b>:\n"):
        asyncio.run(send_message(API_TOKEN, CHAT_ID, message))

# 스케줄 설정 - 테스트를 위해 1분마다 실행
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 스케줄 확인

