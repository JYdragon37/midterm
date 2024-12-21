import socket
import requests
from bs4 import BeautifulSoup

def get_internal_ip():
    try:
        # 기본 소켓 라이브러리를 사용하여 IP 주소 가져오기
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        internal_ip = s.getsockname()[0]
        s.close()
        print(f"컴퓨터의 내부 IP 주소는: {internal_ip}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

def get_external_ip():
    try:
        # 외부 IP 주소 가져오기
        response = requests.get('http://ipconfig.kr/')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            ip_info = soup.find('table').find_all('td')[0].text.strip()
            print(f"컴퓨터의 외부 IP 주소는: {ip_info}")
        else:
            print("외부 IP를 가져오는 데 실패했습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    get_internal_ip()
    get_external_ip()
