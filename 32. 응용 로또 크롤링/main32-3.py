import sqlite3
import requests
import time

# API URL
BASE_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
DB_PATH = "lotto_stats.db"

def create_database():
    """SQLite 데이터베이스 생성 및 초기화."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 번호별 당첨 횟수 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lotto_number_stats (
        번호 INTEGER PRIMARY KEY,
        당첨횟수 INTEGER NOT NULL DEFAULT 0
    )
    """)
    
    # 회차별 데이터 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lotto_round_data (
        회차 INTEGER PRIMARY KEY,
        번호1 INTEGER,
        번호2 INTEGER,
        번호3 INTEGER,
        번호4 INTEGER,
        번호5 INTEGER,
        번호6 INTEGER
    )
    """)
    
    # 번호 초기화 (1~45)
    cursor.execute("SELECT COUNT(*) FROM lotto_number_stats")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO lotto_number_stats (번호, 당첨횟수) VALUES (?, ?)",
            [(i, 0) for i in range(1, 46)]
        )
        print("번호별 당첨 횟수 초기화 완료")
    
    conn.commit()
    conn.close()

def fetch_lotto_data(draw_no):
    """API에서 특정 회차 데이터를 가져옵니다."""
    response = requests.get(BASE_URL + str(draw_no))
    if response.status_code == 200:
        lotto_data = response.json()
        if lotto_data['returnValue'] == 'success':
            # 번호를 숫자로 변환
            return {
                "회차": lotto_data['drwNo'],
                "번호1": int(lotto_data['drwtNo1']),
                "번호2": int(lotto_data['drwtNo2']),
                "번호3": int(lotto_data['drwtNo3']),
                "번호4": int(lotto_data['drwtNo4']),
                "번호5": int(lotto_data['drwtNo5']),
                "번호6": int(lotto_data['drwtNo6'])
            }
    return None

def update_database(start_round, end_round, batch_size=100):
    """배치 단위로 데이터를 DB에 추가하고 번호별 당첨 횟수를 업데이트합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for batch_start in range(start_round, end_round + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_round)
        print(f"{batch_start}회차부터 {batch_end}회차까지 데이터를 가져오는 중...")
        
        for draw_no in range(batch_start, batch_end + 1):
            # 이미 존재하는 회차는 건너뜀
            cursor.execute("SELECT COUNT(*) FROM lotto_round_data WHERE 회차 = ?", (draw_no,))
            if cursor.fetchone()[0] > 0:
                print(f"{draw_no}회차 데이터는 이미 존재합니다. 건너뜁니다.")
                continue

            lotto_data = fetch_lotto_data(draw_no)
            if not lotto_data:
                print(f"{draw_no}회차 데이터를 가져오지 못했습니다.")
                continue
            
            # 회차별 데이터 추가
            cursor.execute("""
            INSERT INTO lotto_round_data (회차, 번호1, 번호2, 번호3, 번호4, 번호5, 번호6)
            VALUES (:회차, :번호1, :번호2, :번호3, :번호4, :번호5, :번호6)
            """, lotto_data)
        
        conn.commit()
        print(f"{batch_start}회차부터 {batch_end}회차까지 데이터가 DB에 저장되었습니다.")
        time.sleep(1)  # API 과부하 방지를 위해 대기

    conn.close()
    recalculate_stats()

def recalculate_stats():
    """모든 회차 데이터를 기반으로 번호별 당첨 횟수를 재계산합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 번호별 당첨 횟수 초기화
    cursor.execute("UPDATE lotto_number_stats SET 당첨횟수 = 0")
    
    # 모든 데이터를 조회
    cursor.execute("SELECT 번호1, 번호2, 번호3, 번호4, 번호5, 번호6 FROM lotto_round_data")
    all_data = cursor.fetchall()
    
    # 당첨 횟수 재계산
    for row in all_data:
        for number in row:
            cursor.execute("""
            UPDATE lotto_number_stats
            SET 당첨횟수 = 당첨횟수 + 1
            WHERE 번호 = ?
            """, (number,))
    
    conn.commit()
    conn.close()
    print("모든 데이터를 기반으로 번호별 당첨 횟수를 재계산했습니다.")

def get_stats():
    """DB에서 번호별 당첨 횟수를 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT 번호, 당첨횟수 FROM lotto_number_stats ORDER BY 당첨횟수 DESC")
    stats = cursor.fetchall()
    conn.close()
    return stats

# 실행
create_database()

# 1회부터 1147회까지 데이터를 배치 처리
update_database(1, 1147, batch_size=100)

# 통계 출력
print("번호별 당첨 횟수:")
for stat in get_stats():
    print(f"번호: {stat[0]}, 당첨횟수: {stat[1]}")
