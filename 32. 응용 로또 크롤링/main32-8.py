from flask import Flask, render_template, jsonify
import random
import sqlite3

app = Flask(__name__)

# DB 경로
DB_PATH = r"C:\Users\highk\pypy50\lotto_stats.db"

def get_next_round():
    """DB에서 다음 회차 번호를 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(회차) FROM lotto_round_data")
    latest_round = cursor.fetchone()[0]
    conn.close()
    return (latest_round or 0) + 1  # 마지막 회차 + 1 반환

def generate_lotto_set():
    """정교한 로직에 따라 번호 세트를 생성합니다."""
    all_numbers = list(range(1, 46))
    return sorted(random.sample(all_numbers, 6))

def generate_multiple_sets():
    """5개의 추천 번호 세트를 생성합니다."""
    sets = [generate_lotto_set() for _ in range(5)]
    return sets

@app.route("/")
def home():
    """메인 페이지."""
    next_round = get_next_round()
    return render_template("index.html", next_round=next_round)

@app.route("/generate")
def generate():
    """추천 번호 세트를 생성하여 JSON으로 반환."""
    lotto_sets = generate_multiple_sets()
    return jsonify(lotto_sets)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
