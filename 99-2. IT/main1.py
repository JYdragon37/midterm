import pandas as pd
import json

# 원본 CSV 파일 읽기
df_original = pd.read_csv('/Users/jeongyong/Documents/pypy50/99-2. IT/naver_blog_final_results_20241130_label.csv')

# JSON 결과 파일 읽기
with open('/Users/jeongyong/Documents/pypy50/99-2. IT/analysis_results.json', 'r', encoding='utf-8') as f:
    analysis_results = json.load(f)

# JSON 결과를 데이터프레임으로 변환
df_analysis = pd.DataFrame(analysis_results)

# 처음 5개 행에 대해서만 결과가 있으므로, 원본 데이터프레임의 처음 5개 행과 결합
df_original.loc[:4, 'text_count'] = df_analysis['text_count']
df_original.loc[:4, 'frequently_used_expressions'] = df_analysis['frequently_used_expressions']
df_original.loc[:4, 'keyword_ratio'] = df_analysis['keyword_ratio']
df_original.loc[:4, 'sentiment_distribution'] = df_analysis['sentiment_distribution'].apply(str)
df_original.loc[:4, 'tone'] = df_analysis['tone']
df_original.loc[:4, 'has_negative_content'] = df_analysis['has_negative_content']
df_original.loc[:4, 'has_ad'] = df_analysis['has_ad']
df_original.loc[:4, 'has_brand'] = df_analysis['has_brand']
df_original.loc[:4, 'has_promotion'] = df_analysis['has_promotion']
df_original.loc[:4, 'is_provided'] = df_analysis['is_provided']
df_original.loc[:4, 'overaction'] = df_analysis['overaction']
df_original.loc[:4, 'is_my_money'] = df_analysis['is_my_money']
df_original.loc[:4, 'structure'] = df_analysis['structure']
df_original.loc[:4, 'technical_details'] = df_analysis['technical_details']
df_original.loc[:4, 'price'] = df_analysis['price']
df_original.loc[:4, 'has_question'] = df_analysis['has_question']

# 결합된 데이터를 새로운 CSV 파일로 저장
df_original.to_csv('/Users/jeongyong/Documents/pypy50/99-2. IT/naver_blog_final_results_with_analysis.csv', 
                  index=False, 
                  encoding='utf-8-sig')  # utf-8-sig를 사용하여 한글이 엑셀에서도 잘 보이도록 함

print("Results merged and saved to naver_blog_final_results_with_analysis.csv")
