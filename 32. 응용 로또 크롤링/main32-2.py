import requests
import csv
import os

# API URL
BASE_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

# 파일 경로 설정
FILE_PATH = r"C:\Users\highk\pypy50\32. 응용 로또 크롤링\lotto_data_1_to_current.csv"

def fetch_lotto_data(draw_no):
    """특정 회차의 데이터를 API로 가져옵니다."""
    response = requests.get(BASE_URL + str(draw_no))
    if response.status_code == 200:
        lotto_data = response.json()
        if lotto_data['returnValue'] == 'success':
            return {
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
    return None

def load_last_saved_round(file_path):
    """CSV 파일에서 마지막 저장된 회차를 읽어옵니다."""
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) > 1:  # 헤더 제외한 데이터가 있는 경우
                return int(rows[-1][0])  # 마지막 행의 "회차" 값
    return 0  # 파일이 없거나 데이터가 없는 경우

def save_to_csv(data, file_path):
    """CSV 파일에 데이터를 저장합니다."""
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["회차", "추첨일", "1등 당첨금액", "1등 당첨자수", "1등 번호"])
        for entry in data:
            writer.writerow([entry["회차"], entry["추첨일"], entry["1등 당첨금액"], entry["1등 당첨자수"], ', '.join(map(str, entry["1등 번호"]))])

def update_lotto_data(file_path):
    """로또 데이터를 업데이트합니다."""
    last_saved_round = load_last_saved_round(file_path)
    current_round = last_saved_round + 1
    new_data = []

    while True:
        lotto_data = fetch_lotto_data(current_round)
        if lotto_data is None:  # 더 이상 유효한 데이터가 없으면 종료
            print(f"최신 데이터까지 업데이트 완료. 마지막 회차: {current_round - 1}")
            break
        new_data.append(lotto_data)
        print(f"{current_round}회차 데이터를 가져왔습니다.")
        current_round += 1

    if new_data:
        save_to_csv(new_data, file_path)
        print(f"총 {len(new_data)}건의 데이터가 추가되었습니다.")
    else:
        print("추가할 데이터가 없습니다.")

# 실행
update_lotto_data(FILE_PATH)
