import sqlite3

# DB 파일 경로
DB_PATH = r"C:\Users\highk\pypy50\lotto_stats.db"

def validate_stats_tab():
    """stats 탭의 데이터와 직접 계산된 번호별 등장 횟수를 비교합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # stats 테이블 데이터 가져오기
    cursor.execute("SELECT 번호, 당첨횟수 FROM lotto_number_stats ORDER BY 번호")
    stats_tab = cursor.fetchall()
    
    # 직접 계산한 번호별 등장 횟수 가져오기
    query = """
    SELECT 번호, COUNT(번호) AS 등장횟수
    FROM (
        SELECT 번호1 AS 번호 FROM lotto_round_data
        UNION ALL
        SELECT 번호2 FROM lotto_round_data
        UNION ALL
        SELECT 번호3 FROM lotto_round_data
        UNION ALL
        SELECT 번호4 FROM lotto_round_data
        UNION ALL
        SELECT 번호5 FROM lotto_round_data
        UNION ALL
        SELECT 번호6 FROM lotto_round_data
    ) 번호_집합
    GROUP BY 번호
    ORDER BY 번호;
    """
    cursor.execute(query)
    calculated_stats = cursor.fetchall()
    
    conn.close()

    # 비교
    is_valid = True
    for (num1, count1), (num2, count2) in zip(stats_tab, calculated_stats):
        if num1 != num2 or count1 != count2:
            print(f"불일치 발견: 번호 {num1} (stats 탭: {count1}, 계산된 값: {count2})")
            is_valid = False
    
    if is_valid:
        print("검증 성공: stats 탭의 데이터가 정확합니다.")
    else:
        print("검증 실패: stats 탭의 데이터와 계산된 값이 다릅니다.")

# 실행
validate_stats_tab()
