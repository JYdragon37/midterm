import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('/Users/jeongyong/Documents/pypy50/99-2. IT/naver_blog_final_results_with_analysis.csv')

# 첫 3개 행 출력
print(df.head(3))

# 첫 3개 행을 엑셀 파일로 저장
df.head(3).to_excel('/Users/jeongyong/Documents/pypy50/99-2. IT/first_3_rows.xlsx', index=False)

print("First 3 rows saved to first_3_rows.xlsx")
