import pandas as pd

# CSV 파일에서 데이터 로드
df = pd.read_csv(r"C:\Users\highk\pypy50\blog_data.csv")

# 광고 여부와 관련된 데이터 라벨링 함수가 포함되어 있는지 확인
if 'has_ad' not in df.columns:
    def label_ad(content):
        ad_keywords = ["제공", "협찬", "체험단", "광고", "이벤트"]
        for keyword in ad_keywords:
            if keyword in content:
                return 1  # 광고
        return 0  # 비광고

    # 'has_ad' 컬럼 생성
    df['has_ad'] = df['Content'].apply(label_ad)

# `word_count` 컬럼 생성 (본문 단어 수 계산)
if 'word_count' not in df.columns:
    df['word_count'] = df['Content'].apply(lambda x: len(str(x).split()))

# 데이터 로드 확인
print(df.head())

from sklearn.model_selection import train_test_split

# Feature와 Label 분리
X = df[['word_count']]  # 단어 수를 Feature로 사용
y = df['has_ad']        # 광고 여부 (Label)

# 학습 데이터와 테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 결과 확인
print("학습 데이터 크기:", X_train.shape)
print("테스트 데이터 크기:", X_test.shape)


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Logistic Regression 모델 초기화
model = LogisticRegression()

# 모델 학습
model.fit(X_train, y_train)

# 예측
y_pred = model.predict(X_test)

# 모델 평가
print("Logistic Regression 모델 성능 평가")
print(classification_report(y_test, y_pred))
