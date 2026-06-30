from nlp.stopwords import stopwords_keyword
from nlp.keyword_dictionary import movie_keywords

from utils.text_preprocessor import preprocess_keyword

from core.model_loader import tfidf_sentiment

KEYWORD_TOP_N = 7


def extract_keywords(review, top_n=KEYWORD_TOP_N) :

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