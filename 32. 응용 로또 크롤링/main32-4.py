import sqlite3
import random

# DB 파일 경로
DB_PATH = r"C:\Users\highk\pypy50\lotto_stats.db"

def get_recent_8_rounds():
    """최근 8회차의 번호를 가져옵니다."""
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
    
    # 데이터를 평탄화하여 리스트로 반환
    recent_numbers = [num for row in recent_data for num in row]
    return recent_numbers

def get_number_stats():
    """번호별 누적 등장 횟수를 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 번호, 당첨횟수
    FROM lotto_number_stats
    ORDER BY 당첨횟수
    """)
    stats = cursor.fetchall()
    
    conn.close()
    return stats

def generate_lotto_set():
    """요청 조건에 따라 번호 세트를 생성합니다."""
    recent_numbers = get_recent_8_rounds()
    stats = get_number_stats()
    
    # 조건 1: 1등 당첨 횟수가 가장 적은 5개 중에서 2개 선택
    least_common = [num for num, _ in stats[:5]]
    selected_numbers = random.sample(least_common, 2)
    
    # 조건 2: 최근 8회 동안 가장 자주 나온 번호 중 1개 선택
    most_frequent_recent = max(set(recent_numbers), key=recent_numbers.count)
    if most_frequent_recent not in selected_numbers:
        selected_numbers.append(most_frequent_recent)
    
    # 조건 3: 최근 8회 동안 한 번도 나오지 않은 번호 중 1개 선택
    all_numbers = set(range(1, 46))
    never_in_recent = list(all_numbers - set(recent_numbers))
    never_in_recent = [num for num in never_in_recent if num not in selected_numbers]
    if never_in_recent:
        selected_numbers.append(random.choice(never_in_recent))
    
    # 조건 4: 누적 횟수가 중간 분포인 번호 중 1개 선택
    total_count = len(stats)
    lower_bound = total_count // 5  # 하위 20%
    upper_bound = total_count - lower_bound  # 상위 20%
    middle_numbers = [num for num, _ in stats[lower_bound:upper_bound] if num not in selected_numbers]
    if middle_numbers:
        selected_numbers.append(random.choice(middle_numbers))
    
    # 조건 5: 위에서 선택되지 않은 번호 중 랜덤으로 1개 선택
    remaining_numbers = list(all_numbers - set(selected_numbers))
    if remaining_numbers:
        selected_numbers.append(random.choice(remaining_numbers))
    
    # 결과 반환
    return sorted(selected_numbers)

def generate_multiple_sets(count=4):
    """여러 개의 번호 세트를 생성합니다."""
    sets = []
    for _ in range(count):
        lotto_set = generate_lotto_set()
        sets.append(lotto_set)
    return sets

# 실행
lotto_sets = generate_multiple_sets(4)
print("생성된 번호 세트:")
for i, lotto_set in enumerate(lotto_sets, 1):
    print(f"세트 {i}: {lotto_set}")
