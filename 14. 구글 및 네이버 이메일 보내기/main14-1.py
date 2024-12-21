# 새로운 프로젝트를 위한 초기 코드 작성
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def greet_user():
    print("안녕하세요, 새로운 프로젝트를 시작합니다!")

def send_gmail(sender_email, sender_password, receiver_email, subject, body):
    # SMTP 서버 설정
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # 이메일 메시지 설정
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # SMTP 서버 연결 및 로그인
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # 이메일 전송
        server.send_message(msg)
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    greet_user()
    
    sender_email = 'huhjungyong@gmail.com'
    sender_password = 'iqji ztbi omer qndn'  # 실제 비밀번호로 변경하세요
    receiver_email = 'huhjungyong@naver.com'
    subject = '테스트 이메일'
    body = '안녕하세요, 이 메일은 파이썬을 사용해 보낸 테스트 메일입니다.'
    
    send_gmail(sender_email, sender_password, receiver_email, subject, body)
