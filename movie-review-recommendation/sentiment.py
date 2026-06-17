import re
from common import okt, stopwords_sentiment, stopwords_keyword, movie_keywords
import numpy as np
import pandas as pd

# ===== 외부 주입 =====
tfidf_sentiment = None
lr_model = None

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
# 키워드 추출 전처리
# ======================
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

# ======================
# 키워드 추출 함수
# ======================
def extract_keyword(review, top_n = 7) :

    # 전처리
    review_p = preprocess_keyword(review)

    # 벡터화
    vec = tfidf_sentiment.transform([review_p])

    # 점수
    scores = vec.toarray()[0]

    # 단어 목록
    features = tfidf_sentiment.get_feature_names_out()

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

# ======================
# 감정예측 함수
# ======================
def predict_sentiment(review) :

    # 전처리
    review_p = preprocess_sentiment(review)

    # 벡터화
    vec = tfidf_sentiment.transform([review_p])

    # 예측
    pred = lr_model.predict(vec)[0]

    # 긍정확률
    positive_prob = lr_model.predict_proba(vec)[0][1]

    # 평점
    rating = round(1 + positive_prob * 4, 0)

    # 예측결과
    sentiment = "긍정" if pred == 1 else "부정"

    # 키워드 추출
    keywords = extract_keyword(review)

    return {
        "리뷰": review,
        "감정": sentiment,
        "긍정확률": positive_prob,
        "예측평점": rating,
        "키워드": keywords
    }