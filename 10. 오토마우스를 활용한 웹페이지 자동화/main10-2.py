import pyautogui
import pyperclip
import time

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

def print_mouse_coordinates():
    try:
        while True:
            # 마우스의 현재 좌표 가져오기
            x, y = pyautogui.position()
            coordinates = f"X: {x}, Y: {y}"
            
            # 좌표를 클립보드에 복사
            pyperclip.copy(coordinates)
            
            # 좌표 출력
            print(coordinates, end="\r")
            
            # 0.1초 대기
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")

def click_at_coordinates(x, y):
    # 지정된 좌표에서 마우스 클릭
    pyautogui.click(x, y)
    print(f"좌표 ({x}, {y})에서 클릭했습니다.")

def search_weather():
    # 사용자가 제공한 검색창 좌표로 이동 후 클릭
    x, y = 1300, 193
    click_at_coordinates(x, y)
    time.sleep(1)  # 클릭 후 약간 대기
    
    # '서울 날씨' 텍스트 입력 (한글 입력 지원을 위해 pyperclip 사용)
    pyperclip.copy("서울 날씨")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)  # 입력 후 약간 대기
    
    # 엔터키를 눌러 검색 실행
    pyautogui.press("enter")
    print("'서울 날씨'를 검색했습니다.")

if __name__ == "__main__":
    print("모듈 설치 상태를 확인합니다...")
    check_modules()
    
    # 네이버에서 '서울 날씨' 검색하기
    print("네이버에서 '서울 날씨'를 검색합니다...")
    search_weather()
