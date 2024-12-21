# chat_id = 1059657134
# api_token = 7936899167:AAFl_3jTqQ-B2b4CUPaKnf_4tWgoY1FI_os

import telegram
from telegram import Bot

def send_message(api_token, chat_id, message):
    bot = Bot(token=api_token)
    try:
        import asyncio

        asyncio.run(bot.send_message(chat_id=chat_id, text=message))
        print("메시지가 성공적으로 전송되었습니다.")
    except telegram.error.TelegramError as e:
        print(f"메시지 전송 실패: {e}")

if __name__ == "__main__":
    api_token = '7936899167:AAFl_3jTqQ-B2b4CUPaKnf_4tWgoY1FI_os'  # 실제 봇 API 토큰으로 변경하세요
    chat_id = '1059657134'  # 메시지를 보낼 사용자 또는 그룹의 Chat ID로 변경하세요
    message = '안녕 나는 파이썬 자동 메시지야'  # 보낼 메시지
    
    send_message(api_token, chat_id, message)
