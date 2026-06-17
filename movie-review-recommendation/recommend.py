import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from common import okt, stopwords_recommend
import common
import re

# ===== 외부주입 ======
genre_matrix = None
overview_matrix = None
actor_matrix = None
director_matrix = None

# ======================
# 전처리
# ======================

def preprocess_recommend(text) :

    # 결측치 방지
    if pd.isna(text) :
        return ''

    # 문자열 아닌경우
    if not isinstance(text, str) :
        return ''

    # 한글 영어 공백 제외 제거
    text = re.sub(r'[^가-힣a-zA-Z\s]', '', text)

    # 공백 제거
    text = text.strip()

    # 형태소분석 - 명사
    tokens = okt.nouns(text)

    # 불용어 제거
    tokens = [
        word for word in tokens
        if word not in stopwords_recommend and len(word) > 1
    ]

    return ' '.join(tokens)

# ======================
# 추천함수
# ======================
def recommend_movies(title, top_n = 5) :

    idx = common.movie_index[title]

    #  유사도
    genre_sim = linear_kernel(genre_matrix[idx], genre_matrix).flatten()
    overview_sim = linear_kernel(overview_matrix[idx], overview_matrix).flatten()
    actor_sim = linear_kernel(actor_matrix[idx], actor_matrix).flatten()
    director_sim = linear_kernel(director_matrix[idx], director_matrix).flatten()

    # 유사도 가중합
    final_sim = (
        genre_sim * 0.35 +
        np.clip(overview_sim * 15, 0, 1) * 0.35 +
        np.clip(actor_sim * 10, 0, 1) * 0.2 +
        director_sim * 0.1
    )

    # 추천 영화 정렬 및 자신 제거
    sim_indices = final_sim.argsort()[::-1][1:top_n+1]

    # 추천
    recommendations = []

    for i in sim_indices :
        recommendations.append({
            "영화제목": common.movie_df.iloc[i]["영화제목"],
            "장르": common.movie_df.iloc[i]["장르"],
            "매칭률(%)": round(60 + final_sim[i] * 40, 1)
        })

    return {
        "리뷰작성영화": title,
        "추천영화목록": recommendations
    }