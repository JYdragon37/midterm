import sqlite3
import requests
import random
import time

# DB 경로 및 API URL
DB_PATH = r"C:\Users\highk\pypy50\lotto_stats.db"
BASE_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

### 1. 데이터베이스 초기화 ###
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

### 2. 최신 데이터 가져오기 ###
def get_latest_round():
    """DB에 저장된 가장 최신 회차를 반환합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(회차) FROM lotto_round_data")
    latest_round = cursor.fetchone()[0]
    conn.close()
    return latest_round or 0  # 저장된 데이터가 없으면 0 반환

def fetch_lotto_data(draw_no):
    """API에서 특정 회차 데이터를 가져옵니다."""
    response = requests.get(BASE_URL + str(draw_no))
    if response.status_code == 200:
        lotto_data = response.json()
        if lotto_data['returnValue'] == 'success':
            return {
                "회차": lotto_data['drwNo'],
                "번호1": int(lotto_data['drwtNo1']),
                "번호2": int(lotto_data['drwtNo2']),
                "번호3": int(lotto_data['drwtNo3']),
                "번호4": int(lotto_data['drwtNo4']),
                "번호5": int(lotto_data['drwtNo5']),
                "번호6": int(lotto_data['drwtNo6']),
            }
    return None

def update_database(end_round, batch_size=50):
    """최신 데이터를 DB에 추가하고, 번호별 당첨 횟수를 업데이트합니다."""
    start_round = get_latest_round() + 1  # 가장 최신 회차 이후부터 시작
    if start_round > end_round:
        print("모든 데이터가 최신 상태입니다.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for batch_start in range(start_round, end_round + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_round)
        print(f"{batch_start}회차부터 {batch_end}회차까지 데이터를 가져오는 중...")
        
        for draw_no in range(batch_start, batch_end + 1):
            lotto_data = fetch_lotto_data(draw_no)
            if not lotto_data:
                print(f"{draw_no}회차 데이터를 가져오지 못했습니다.")
                continue
            
            # 데이터 추가
            cursor.execute("""
            INSERT INTO lotto_round_data (회차, 번호1, 번호2, 번호3, 번호4, 번호5, 번호6)
            VALUES (:회차, :번호1, :번호2, :번호3, :번호4, :번호5, :번호6)
            """, lotto_data)
        
        conn.commit()
        print(f"{batch_start}회차부터 {batch_end}회차까지 데이터 저장 완료.")
        time.sleep(1)  # API 과부하 방지
    
    conn.close()
    recalculate_stats()

def recalculate_stats():
    """모든 데이터를 기반으로 번호별 당첨 횟수를 재계산합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE lotto_number_stats SET 당첨횟수 = 0")
    cursor.execute("""
    SELECT 번호1, 번호2, 번호3, 번호4, 번호5, 번호6 FROM lotto_round_data
    """)
    all_data = cursor.fetchall()
    
    for row in all_data:
        for number in row:
            cursor.execute("""
            UPDATE lotto_number_stats
            SET 당첨횟수 = 당첨횟수 + 1
            WHERE 번호 = ?
            """, (number,))
    
    conn.commit()
    conn.close()
    print("번호별 당첨 횟수 재계산 완료.")

### 3. 번호 추천 로직 ###
def get_recent_8_rounds():
    """최근 8회차 데이터를 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 번호1, 번호2, 번호3, 번호4, 번호5, 번호6
    FROM lotto_round_data
    ORDER BY 회차 DESC
    LIMIT 8
    """)
    recent_data = cursor.fetchall()
    conn.close()
    return [num for row in recent_data for num in row]

def get_number_stats():
    """번호별 누적 횟수를 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 번호, 당첨횟수 FROM lotto_number_stats ORDER BY 당첨횟수")
    stats = cursor.fetchall()
    conn.close()
    return stats

def generate_lotto_set():
    """정교한 로직에 따라 번호 세트를 생성합니다."""
    recent_numbers = get_recent_8_rounds()
    stats = get_number_stats()
    
    # 조건 1: 가장 적은 5개 중 2개
    least_common = [num for num, _ in stats[:5]]
    selected = random.sample(least_common, min(2, len(least_common)))

    # 조건 2: 최근 8회에서 가장 자주 나온 번호 중 1개
    recent_frequency = {num: recent_numbers.count(num) for num in set(recent_numbers)}
    most_frequent = max(recent_frequency, key=recent_frequency.get, default=None)
    if most_frequent and most_frequent not in selected:
        selected.append(most_frequent)

    # 조건 3: 최근 8회 동안 한 번도 나오지 않은 번호 중 1개
    all_numbers = set(range(1, 46))
    never_in_recent = list(all_numbers - set(recent_numbers))
    never_in_recent = [num for num in never_in_recent if num not in selected]
    if never_in_recent:
        selected.append(random.choice(never_in_recent))
    
    # 조건 4: 누적 등장 횟수 기준 중간 분포에서 1개
    total_numbers = len(stats)
    lower_bound = total_numbers // 5  # 하위 20%
    upper_bound = total_numbers - lower_bound  # 상위 20%
    middle_numbers = [
        num for num, _ in stats[lower_bound:upper_bound] if num not in selected
    ]
    if middle_numbers:
        selected.append(random.choice(middle_numbers))
    
    # 조건 5: 위에서 선택되지 않은 번호 중 랜덤으로 1개
    remaining_numbers = list(all_numbers - set(selected))
    if remaining_numbers:
        selected.append(random.choice(remaining_numbers))
    
    # 선택된 번호를 정렬하여 반환
    return sorted(selected)

def generate_exclusive_set(existing_sets):
    """기존 세트에 포함되지 않은 번호로 새로운 세트를 생성."""
    all_numbers = set(range(1, 46))
    used_numbers = set(num for s in existing_sets for num in s)
    unused_numbers = list(all_numbers - used_numbers)
    
    if len(unused_numbers) < 6:
        print("사용 가능한 번호가 6개 미만입니다. 모든 번호를 섞어서 새로운 세트를 생성합니다.")
        unused_numbers = list(all_numbers)
    
    return sorted(random.sample(unused_numbers, 6))

def generate_multiple_sets(count=4):
    """여러 세트를 생성합니다."""
    sets = [generate_lotto_set() for _ in range(count)]
    
    # 마지막 세트 추가 (기존 세트에 없는 번호들로 구성)
    exclusive_set = generate_exclusive_set(sets)
    sets.append(exclusive_set)
    
    return sets

# 실행
lotto_sets = generate_multiple_sets(4)
print("추천 번호 세트:")
for i, lotto_set in enumerate(lotto_sets, 1):
    print(f"세트 {i}: {lotto_set}")