import pandas as pd

# 파일 경로 설정
file_path = r"C:\Users\highk\pypy50\27. 전국 대학교 위치 시각화\고등교육기관 하반기 주소록(2023).xlsx"

# Excel 파일 읽기
df = pd.read_excel(file_path)

# 데이터 확인
print(df.head())
