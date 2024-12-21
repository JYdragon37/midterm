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

if __name__ == "__main__":
    print("모듈 설치 상태를 확인합니다...")
    check_modules()
    print("마우스 좌표를 추적하려면 Ctrl+C로 종료하세요.")
    print_mouse_coordinates()
