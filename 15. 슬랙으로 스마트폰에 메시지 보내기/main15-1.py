# Slack 웹훅을 사용하여 메시지를 보내는 코드 작성
import requests

def send_slack_message(webhook_url, message):
    payload = {
        'text': message
    }
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 200:
        print("메시지가 성공적으로 전송되었습니다.")
    else:
        print(f"메시지 전송 실패: {response.status_code}, {response.text}")

def greet_user():
    print("안녕하세요, 새로운 프로젝트를 시작합니다!")

if __name__ == "__main__":
    greet_user()
    webhook_url = 'https://hooks.slack.com/services/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'
    message = '파이썬에서 보내는 메시지입니다'
    send_slack_message(webhook_url, message)
