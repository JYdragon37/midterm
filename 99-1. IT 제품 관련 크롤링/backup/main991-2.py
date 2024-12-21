import pandas as pd
import re
from textblob import TextBlob
from collections import Counter

# 데이터 로드
df = pd.read_csv("processed_blog_data.csv")

# 1. HTML 태그 제거 함수
def remove_html_tags(text):
    """HTML 태그를 제거하는 함수"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# HTML 태그 제거
df['Title'] = df['Title'].apply(remove_html_tags)
df['Description'] = df['Description'].apply(remove_html_tags)

# 2. 단어 수 계산 (word_count)
df['word_count'] = df['Description'].apply(lambda x: len(str(x).split()))

# 3. 광고성 키워드 등장 횟수 계산
ad_keywords = [
    "제공", "협찬", "체험단", "광고", "이벤트", "추천", "파트너스", "후원",
    "리뷰 제공", "무료 제공", "서포터즈", "후기 이벤트", "제휴", "배너"
]
df['ad_keywords_count'] = df['Description'].apply(
    lambda x: sum(1 for word in ad_keywords if word in str(x))
)

# 4. 키워드 밀도 (keyword_ratio)
df['keyword_ratio'] = df['ad_keywords_count'] / df['word_count']

# 5. 자주 사용된 표현 추출 (불필요한 단어 제외)
stop_words = {'이', '바로', '그럼', '여기에', '해야하는', '저', '그', '나', '내'}
def extract_frequent_words(text, top_n=5):
    """본문에서 자주 사용된 표현과 등장 횟수를 추출 (불필요한 단어 제외)"""
    words = [word for word in str(text).split() if word not in stop_words]
    counter = Counter(words)
    return dict(counter.most_common(top_n))

df['frequent_expressions'] = df['Description'].apply(extract_frequent_words)

# 6. 감정 분석 (Sentiment Analysis)
def analyze_sentiment(text):
    """텍스트의 감정 점수를 계산 (-1 ~ 1)"""
    blob = TextBlob(str(text))
    return blob.sentiment.polarity

df['sentiment_score'] = df['Description'].apply(analyze_sentiment)

def classify_sentiment(score):
    """감정 점수를 기반으로 감정 레이블 분류"""
    if score > 0.5:
        return "매우 긍정"
    elif 0.1 < score <= 0.5:
        return "긍정"
    elif -0.1 <= score <= 0.1:
        return "중립"
    elif -0.5 <= score < -0.1:
        return "부정"
    else:
        return "매우 부정"

df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)

# 7. 태그 수 계산 (tag_cnt, 정확성 개선)
def count_tags(description):
    """본문에서 해시태그(#)의 개수를 계산"""
    tags = re.findall(r'#\w+', str(description))
    return len(tags)

df['tag_cnt'] = df['Description'].apply(count_tags)

# 8. 이미지 수 계산 (image_cnt, 정규표현식 개선)
def count_images(description):
    """본문에서 이미지 링크(URL)의 개수를 계산"""
    images = re.findall(r'https?://\S+\.(?:png|jpg|jpeg|gif)', str(description))
    return len(images)

df['image_cnt'] = df['Description'].apply(count_images)

# 9. 광고성 여부 탐지 (유사 문구 탐지)
def detect_ad(text):
    """광고성 문구 탐지 (유사 문구 포함)"""
    ad_phrases = [
        r"제공.*작성", r"파트너스.*활동", r"무료로.*제공",
        r"리뷰.*후원", r"광고.*포함", r"이 글은 .*제공받아 작성"
    ]
    for phrase in ad_phrases:
        if re.search(phrase, str(text)):
            return 1
    return 0

df['has_ad_phrases'] = df['Description'].apply(detect_ad)
df['has_ad'] = df.apply(
    lambda row: 1 if row['ad_keywords_count'] > 0 or row['has_ad_phrases'] == 1 else 0,
    axis=1
)

# 데이터 확인
print(df.head())

# 전처리 완료된 데이터 저장
df.to_csv("processed_blog_data_complete_updated.csv", index=False, encoding="utf-8-sig")
print("완성된 데이터가 processed_blog_data_complete_updated.csv에 저장되었습니다!")
