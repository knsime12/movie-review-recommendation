from services.keyword_service import extract_keywords

from utils.text_preprocessor import preprocess_sentiment

from core.model_loader import tfidf_sentiment, sentiment_model


POSITIVE_LABEL = 1
POSITIVE_TEXT = "긍정"
NEGATIVE_TEXT = "부정"

MIN_RATING = 1
MAX_RATING = 5


def _get_sentiment_text(pred):
    return POSITIVE_TEXT if pred == POSITIVE_LABEL else NEGATIVE_TEXT


def _calculate_expected_rating(positive_prob):
    return round(
        MIN_RATING + positive_prob * (MAX_RATING - MIN_RATING),
        0
    )


# ======================
# 감정예측 함수
# ======================
def predict_sentiment(review):

    # 전처리
    review_p = preprocess_sentiment(review)

    # 벡터화
    vec = tfidf_sentiment.transform([review_p])

    # 예측
    pred = sentiment_model.predict(vec)[0]

    # 긍정확률
    positive_prob = sentiment_model.predict_proba(vec)[0][1]

    # 평점
    rating = _calculate_expected_rating(positive_prob)

    # 예측결과
    sentiment = _get_sentiment_text(pred)

    # 키워드 추출
    keywords = extract_keywords(review)

    return {
        "review": review,
        "sentiment": sentiment,
        "positive_prob": positive_prob,
        "expected_rating": rating,
        "keywords": keywords
    }