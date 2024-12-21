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

def perform_initial_actions():
    # 1111, 164 위치로 마우스를 이동해서 더블클릭
    pyautogui.moveTo(1111, 164)
    pyautogui.doubleClick()
    print("좌표 (1111, 164)에서 더블클릭했습니다.")
    time.sleep(3)  # 3초 대기

    # 1026, 794 위치로 마우스를 이동 후 메시지 입력
    pyautogui.moveTo(1026, 794)
    pyautogui.click()
    print("좌표 (1026, 794)에서 클릭했습니다.")
    
    # 메시지 입력 받기
    message = '이 메시지는 파이썬 자동화 테스트입니다'
    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    print(f"메시지 '{message}'를 입력했습니다.")
    
    # 엔터키를 눌러 메시지 전송
    pyautogui.press("enter")
    print("엔터키를 눌러 메시지를 전송했습니다.")

if __name__ == "__main__":
    print("모듈 설치 상태를 확인합니다...")
    check_modules()
    
    # 초기 동작 수행하기
    perform_initial_actions()
    
    # 마우스 좌표 출력하기
    print("마우스 좌표를 추적하려면 Ctrl+C로 종료하세요.")
    print_mouse_coordinates()
