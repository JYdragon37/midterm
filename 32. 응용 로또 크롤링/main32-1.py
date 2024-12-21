import requests
import csv
import os
import time

def fetch_lotto_data(start_round, end_round, batch_size=50):
    base_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    data = []

    for batch_start in range(start_round, end_round + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_round)
        for drw_no in range(batch_start, batch_end + 1):
            response = requests.get(base_url + str(drw_no))
            if response.status_code == 200:
                lotto_data = response.json()
                if lotto_data['returnValue'] == 'success':
                    round_data = {
                        "회차": lotto_data['drwNo'],
                        "추첨일": lotto_data['drwNoDate'],
                        "1등 당첨금액": f"{lotto_data['firstWinamnt']:,}원",
                        "1등 당첨자수": f"{lotto_data['firstPrzwnerCo']}명",
                        "1등 번호": [
                            lotto_data['drwtNo1'], lotto_data['drwtNo2'],
                            lotto_data['drwtNo3'], lotto_data['drwtNo4'],
                            lotto_data['drwtNo5'], lotto_data['drwtNo6']
                        ]
                    }
                    data.append(round_data)
            else:
                print(f"Error fetching data for round {drw_no}")
        # 서버 과부하를 방지하기 위해 배치 단위로 잠시 대기
        time.sleep(2)
    return data

def save_to_csv(data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["회차", "추첨일", "1등 당첨금액", "1등 당첨자수", "1등 번호"])
        for entry in data:
            writer.writerow([entry["회차"], entry["추첨일"], entry["1등 당첨금액"], entry["1등 당첨자수"], ', '.join(map(str, entry["1등 번호"]))])

# Get the current draw number
current_round = 1146  # You could make this dynamic by fetching the latest available round number from an API or a reliable source

data = fetch_lotto_data(1, current_round)
file_path = r"C:\Users\highk\pypy50\32. 응용 로또 크롤링\lotto_data_1_to_current.csv"
save_to_csv(data, file_path)

print(f"Data saved to {file_path}")
