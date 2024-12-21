import pandas as pd
from collections import Counter

# 크롤링한 데이터 로드
df = pd.read_csv(r"C:\Users\highk\pypy50\blog_data.csv")

# 자주 사용된 표현 추출
def extract_frequent_words(content, top_n=10):
    words = content.split()
    counter = Counter(words)
    return dict(counter.most_common(top_n))

df['frequent_words'] = df['Content'].apply(extract_frequent_words)
df['word_count'] = df['Content'].apply(lambda x: len(x.split()))

# 결과 확인
print(df[['frequent_words', 'word_count']])

df.to_csv("frequent_words_output.csv", index=False, encoding="utf-8-sig")
print("결과가 frequent_words_output.csv에 저장되었습니다!")
