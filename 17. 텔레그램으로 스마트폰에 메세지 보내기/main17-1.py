import requests

def get_bot_id(api_token):
    url = f'https://api.telegram.org/bot{api_token}/getMe'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['ok']:
            bot_id = data['result']['id']
            print(f"Bot ID: {bot_id}")
        else:
            print("API 응답이 성공하지 않았습니다.")
    else:
        print(f"HTTP 요청 실패: {response.status_code}")

if __name__ == "__main__":
    api_token = input("Telegram Bot API 토큰을 입력하세요: ")
    get_bot_id(api_token)
