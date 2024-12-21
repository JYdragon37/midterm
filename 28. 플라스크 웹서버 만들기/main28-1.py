from flask import Flask

# Flask 애플리케이션 생성
app = Flask(__name__)

# 루트 경로 설정
@app.route('/')
def home():
    return "Hello, World!"

# 메인 실행
if __name__ == '__main__':
    app.run(debug=True)
