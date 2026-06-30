from pathlib import Path

import joblib

from services.common import stopwords_keyword, movie_keywords

from utils.text_preprocessor import preprocess_keyword

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "backend" / "models"

tfidf = joblib.load(MODEL_DIR / "tfidf_sentiment.pkl")

KEYWORD_TOP_N = 7


def extract_keywords(review, top_n=KEYWORD_TOP_N) :

    # 전처리
    review_p = preprocess_keyword(review)

    # 벡터화
    vec = tfidf.transform([review_p])

    # 점수
    scores = vec.toarray()[0]

    # 단어 목록
    features = tfidf.get_feature_names_out()

    # 저장
    keywords = []

    for idx in scores.argsort()[::-1] :

        word = features[idx]

        if scores[idx] <= 0 :
            continue

        if ' ' in word :
            continue

        if word in stopwords_keyword :
            continue

        if len(word) > 1 and word in movie_keywords :
            keywords.append(word)

        if len(keywords) >= top_n :
            break

    return keywords