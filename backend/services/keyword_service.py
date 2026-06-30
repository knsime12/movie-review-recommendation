import re
from pathlib import Path

import joblib
import pandas as pd

from services.common import okt, stopwords_keyword, movie_keywords

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "backend" / "models"

tfidf = joblib.load(MODEL_DIR / "tfidf_sentiment.pkl")

KEYWORD_TOP_N = 7

def preprocess_keyword(text) :

    # 결측치 방지
    if pd.isna(text) :
        return ''

    # 문자열 아닌 경우 방지
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

        # 명사만
        if pos == 'Noun' :

            # 불용어 제거
            if word not in stopwords_keyword :

                # 2글자 이상
                if len(word) > 1 :

                    words.append(word)

    return ' '.join(words)

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