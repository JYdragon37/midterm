import telegram
from telegram import Bot
import pyautogui
import pyperclip
import time
import os
from datetime import datetime
import asyncio

def check_modules():
    try:
        import pyautogui
        print("pyautogui 모듈이 설치되어 있습니다.")
    except ModuleNotFoundError:
        print("pyautogui 모듈이 설치되어 있지 않습니다.")
    
    try:
        import pyperclip
        print("pyperclip 모듈이 설치되어 있습니다.")
    except ModuleNotFoundError:
        print("pyperclip 모듈이 설치되어 있지 않습니다.")

def search_weather(location):
    # 사용자가 제공한 검색창 좌표로 이동 후 클릭
    x, y = 1300, 193
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(3)  # 클릭 후 약간 대기
    
    # 해당 지역의 날씨 텍스트 입력 (한글 입력 지원을 위해 pyperclip 사용)
    pyperclip.copy(location)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)  # 입력 후 약간 대기
    
    # 엔터키를 눌러 검색 실행
    pyautogui.press("enter")
    print(f"'{location}'를 검색했습니다.")

def capture_screen(location):
    # 캡처할 영역의 좌표 설정 (좌측 상단과 우측 하단 좌표)
    top_left_x, top_left_y = 937, 128
    bottom_right_x, bottom_right_y = 1684, 994

    # 화면 캡처 수행
    screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))

    # 파일 이름 설정 (지역날씨_실제날짜)
    current_date = datetime.now().strftime("%Y%m%d")
    file_index = 1
    base_path = r"C:\Users\highk\pypy50\10. 오토마우스를 활용한 웹페이지 자동화"
    file_name = os.path.join(base_path, f"{location}_{current_date}.png")

    # 파일이 이미 존재하면 번호를 붙여서 저장
    while os.path.exists(file_name):
        file_name = os.path.join(base_path, f"{location}_{current_date}_{file_index}.png")
        file_index += 1

    # 캡처한 이미지를 파일로 저장
    screenshot.save(file_name)
    print(f"화면을 캡처하여 '{file_name}'로 저장했습니다.")
    return file_name

def send_message(api_token, chat_id, message):
    bot = Bot(token=api_token)
    try:
        asyncio.run(bot.send_message(chat_id=chat_id, text=message))
        print("메시지가 성공적으로 전송되었습니다.")
    except telegram.error.TelegramError as e:
        print(f"메시지 전송 실패: {e}")

def send_photo(api_token, chat_id, photo_path):
    bot = Bot(token=api_token)
    try:
        asyncio.run(bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb')))
        print(f"사진 '{photo_path}'이 성공적으로 전송되었습니다.")
    except telegram.error.TelegramError as e:
        print(f"사진 전송 실패: {e}")

if __name__ == "__main__":
    api_token = '7936899167:AAFl_3jTqQ-B2b4CUPaKnf_4tWgoY1FI_os'  # 실제 봇 API 토큰으로 변경하세요
    chat_id = '1059657134'  # 메시지를 보낼 채팅 ID를 입력하세요
    
    # 모듈 설치 상태 확인
    check_modules()
    
    # 여러 지역의 날씨 검색 및 캡처하기
    locations = ["서울 날씨", "일산 날씨", "강남 날씨"]
    captured_files = []
    for location in locations:
        print(f"네이버에서 '{location}'를 검색합니다...")
        search_weather(location)
        time.sleep(5)  # 검색 결과 로드 대기 시간을 늘림
        
        # 화면 캡처하기
        print(f"{location}의 검색 결과를 캡처합니다...")
        captured_file = capture_screen(location)
        captured_files.append(captured_file)

    # 캡처된 파일들을 텔레그램으로 전송하기
    message = '안녕하세요! 오늘의 날씨 정보입니다.'
    send_message(api_token, chat_id, message)
    
    for file_path in captured_files:
        send_photo(api_token, chat_id, file_path)
