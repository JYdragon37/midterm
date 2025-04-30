# 쓰레드의 개념
# 쓰레드(Thread)는 프로그램에서 동시에 여러 작업을 수행할 수 있도록 해주는 실행 단위입니다.
# 멀티쓰레딩(Multi-threading)은 CPU의 여러 코어를 효율적으로 사용하거나, 네트워크나 I/O 작업과 같이 시간이 오래 걸리는 작업을 비동기적으로 처리할 때 유용합니다.

# 예를 들어, 파일 다운로드와 동시에 사용자에게 다른 작업을 수행하도록 허용하는 기능은 쓰레드를 이용해 구현할 수 있습니다.
# 이렇게 하면 사용자 경험이 크게 향상됩니다.

# 간단한 예시 코드 - 두 개의 쓰레드를 사용하여 동시에 다른 작업을 수행
import threading
import time

# 첫 번째 쓰레드 함수
def print_numbers():
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)  # 1초 대기

# 두 번째 쓰레드 함수
def print_letters():
    for letter in ['A', 'B', 'C', 'D', 'E']:
        print(f"Letter: {letter}")
        time.sleep(1)  # 1초 대기

# 메인 함수
if __name__ == "__main__":
    # 두 개의 쓰레드를 생성합니다.
    thread1 = threading.Thread(target=print_numbers)
    thread2 = threading.Thread(target=print_letters)
    
    # 쓰레드를 시작합니다.
    thread1.start()
    thread2.start()
    
    # 모든 쓰레드가 종료될 때까지 대기합니다.
    thread1.join()
    thread2.join()
    
    print("모든 작업이 완료되었습니다.")

#기초