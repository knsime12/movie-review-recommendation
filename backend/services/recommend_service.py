import numpy as np
import pandas as pd
import re
import joblib
from pathlib import Path
from sklearn.metrics.pairwise import linear_kernel
import services.common as common
from services.movie_service import get_movie_by_title

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "backend" / "models"

# ===== 외부주입 ======
genre_matrix = joblib.load(MODEL_DIR / "genre_matrix.pkl")
overview_matrix = joblib.load(MODEL_DIR / "overview_matrix.pkl")
actor_matrix = joblib.load(MODEL_DIR / "actor_matrix.pkl")
director_matrix = joblib.load(MODEL_DIR / "director_matrix.pkl")

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
    tokens = common.okt.nouns(text)

    # 불용어 제거
    tokens = [
        word for word in tokens
        if word not in common.stopwords_recommend and len(word) > 1
    ]

    return ' '.join(tokens)

# ======================
# 추천함수
# ======================
def recommend_movies(title, top_n = 5) :

    if title not in common.movie_index:
        return {
            "succes": False,
            "message": "기준 영화를 찾을 수 없습니다.",
            "title": title,
            "recommendations": []
        }

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
    sim_indices = final_sim.argsort()[::-1]

    # 추천
    recommendations = []
    recommended_ids = set()
    recommended_titles = set()

    for i in sim_indices:

        # 자기 자신 제외
        if i == idx:
            continue
        
        movie = common.movie_df.iloc[i]

        movie_title = movie["영화제목"]

        if movie_title == title:
            continue

        if movie_title in recommended_titles:
            continue

        # DB에서 id만 보조로 찾기
        db_movie = get_movie_by_title(movie_title)

        if not db_movie:
            continue

        movie_id = int(db_movie["id"])

        if movie_id in recommended_ids:
            continue

        recommendations.append({
            "id": movie_id,
            "title": movie_title,
            "genre": movie["장르"],
            "poster_url": movie["포스터이미지"],
            "match_score": round(60 + final_sim[i] * 40, 1)
        })

        recommended_ids.add(movie_id)
        recommended_titles.add(movie_title)

        if len(recommendations) >= top_n:
            break

    return {
        "success": True,
        "title": title,
        "recommendations": recommendations
    }