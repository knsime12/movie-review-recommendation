import re
from services.common import okt, stopwords_sentiment
import pandas as pd
import joblib
from pathlib import Path
from services.keyword_service import extract_keywords

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "backend" / "models"

tfidf = joblib.load(MODEL_DIR / "tfidf_sentiment.pkl")
model = joblib.load(MODEL_DIR / "lr_model.pkl")

POSITIVE_LABEL = 1
POSITIVE_TEXT = "긍정"
NEGATIVE_TEXT = "부정"

MIN_RATING = 1
MAX_RATING = 5

# ======================
# 감정분석 전처리
# ======================
def preprocess_sentiment(text) :

    # 결측치 방지
    if pd.isna(text) :
        return ''

    # 문자열 아닐경우 방지
    if not isinstance(text, str) :
        return ''

    # 한글 제외 문자 제거
    text = re.sub(r'[^가-힣\s]', '', text)

    # 공백 정리
    text = re.sub(r'\s+', ' ', text)

    # 형태소 분석
    tokens = okt.pos(text, stem = True)

    words = []

    for word, pos in tokens :

        # 명사 / 형용사
        if pos in ['Noun', 'Adjective'] :

            # 불용어 제거
            if word not in stopwords_sentiment :

                # 2글자 이상
                if len(word) > 1 :

                    words.append(word)

    return ' '.join(words)

# ======================
# 감정예측 함수
# ======================
def predict_sentiment(review) :

    # 전처리
    review_p = preprocess_sentiment(review)

    # 벡터화
    vec = tfidf.transform([review_p])

    # 예측
    pred = model.predict(vec)[0]

    # 긍정확률
    positive_prob = model.predict_proba(vec)[0][1]

    # 평점
    rating = round(
        MIN_RATING + positive_prob * (MAX_RATING - MIN_RATING), 
        0
    )

    # 예측결과
    sentiment = POSITIVE_TEXT if pred == POSITIVE_LABEL else NEGATIVE_TEXT

    # 키워드 추출
    keywords = extract_keywords(review)

    return {
        "review": review,
        "sentiment": sentiment,
        "positive_prob": positive_prob,
        "expected_rating": rating,
        "keywords": keywords
    }