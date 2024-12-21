import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


# 수집된 데이터 로드
df = pd.read_csv("naver_blog_search_results.csv")

# HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# HTML 태그 제거
df['Title'] = df['Title'].apply(remove_html_tags)
df['Description'] = df['Description'].apply(remove_html_tags)

# 단어 수 계산 (word_count)
df['word_count'] = df['Description'].apply(lambda x: len(str(x).split()))

# 광고성 키워드 리스트 확장
ad_keywords = [
    "제공", "협찬", "체험단", "광고", "이벤트", "추천", "파트너스", "후원",
    "리뷰 제공", "무료 제공", "서포터즈", "후기 이벤트", "제휴", "배너"
]

# 광고성 키워드 등장 횟수 계산
df['ad_keywords_count'] = df['Description'].apply(
    lambda x: sum(1 for word in ad_keywords if word in str(x))
)

# 광고성 문구 탐지 함수
ad_phrases = [
    "이 글은 .* 제공받아 작성되었습니다",
    "쿠팡 파트너스 활동의 일환으로 수수료를 받을 수 있습니다",
    "이 제품은 협찬받았습니다",
    "무료로 제공받은 제품입니다"
]

def detect_ad_phrases(text):
    for phrase in ad_phrases:
        if re.search(phrase, str(text)):
            return 1  # 광고
    return 0  # 비광고

# 광고성 문구 탐지
df['has_ad_phrases'] = df['Description'].apply(detect_ad_phrases)

# 광고성 여부 라벨링 (키워드와 문구 탐지 조합)
df['has_ad'] = df.apply(
    lambda row: 1 if row['ad_keywords_count'] > 0 or row['has_ad_phrases'] == 1 else 0,
    axis=1
)

# 데이터 확인
print(df.head())

# 전처리 완료된 데이터를 저장
df.to_csv("processed_blog_data.csv", index=False, encoding="utf-8-sig")
print("전처리된 데이터가 processed_blog_data.csv에 저장되었습니다!")



# 데이터 로드
df = pd.read_csv("processed_blog_data.csv")

# Feature와 Label 분리
X = df[['word_count', 'ad_keywords_count']]  # 주요 Feature
y = df['has_ad']  # 광고 여부 (Label)

# 학습 데이터와 테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Logistic Regression 모델 초기화
model = LogisticRegression()

# 모델 학습
model.fit(X_train, y_train)

# 예측
y_pred = model.predict(X_test)

# 성능 평가
print("Logistic Regression 모델 성능 평가:")
print(classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Random Forest 모델 초기화
rf_model = RandomForestClassifier(random_state=42)

# 모델 학습
rf_model.fit(X_train, y_train)

# 예측
y_pred_rf = rf_model.predict(X_test)

# 성능 평가
print("Random Forest 모델 성능 평가:")
print(classification_report(y_test, y_pred_rf))


from sklearn.svm import SVC

# SVM 모델 초기화
svm_model = SVC(random_state=42)

# 모델 학습
svm_model.fit(X_train, y_train)

# 예측
y_pred_svm = svm_model.predict(X_test)

# 성능 평가
print("SVM 모델 성능 평가:")
print(classification_report(y_test, y_pred_svm))

from xgboost import XGBClassifier

# XGBoost 모델 초기화
xgb_model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')

# 모델 학습
xgb_model.fit(X_train, y_train)

# 예측
y_pred_xgb = xgb_model.predict(X_test)

# 성능 평가
print("XGBoost 모델 성능 평가:")
print(classification_report(y_test, y_pred_xgb))
