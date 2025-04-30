import psutil

def get_computer_info():
    try:
        # CPU 정보
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_cores = psutil.cpu_count(logical=True)
        print(f"CPU 사용률: {cpu_percent}%")
        print(f"CPU 코어 수: {cpu_cores}")

        # 메모리 정보
        virtual_memory = psutil.virtual_memory()
        total_memory = virtual_memory.total / (1024 ** 3)  # GB 단위로 변환
        available_memory = virtual_memory.available / (1024 ** 3)
        print(f"전체 메모리: {total_memory:.2f} GB")
        print(f"사용 가능한 메모리: {available_memory:.2f} GB")

        # 디스크 정보
        disk_usage = psutil.disk_usage('/')
        total_disk = disk_usage.total / (1024 ** 3)  # GB 단위로 변환
        used_disk = disk_usage.used / (1024 ** 3)
        free_disk = disk_usage.free / (1024 ** 3)
        print(f"전체 디스크 용량: {total_disk:.2f} GB")
        print(f"사용된 디스크 용량: {used_disk:.2f} GB")
        print(f"사용 가능한 디스크 용량: {free_disk:.2f} GB")

        # 네트워크 정보
        net_io = psutil.net_io_counters()
        sent_data = net_io.bytes_sent / (1024 ** 2)  # MB 단위로 변환
        recv_data = net_io.bytes_recv / (1024 ** 2)
        print(f"송신된 데이터: {sent_data:.2f} MB")
        print(f"수신된 데이터: {recv_data:.2f} MB")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    get_computer_info()

    #기초
