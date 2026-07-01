import numpy as np

from sklearn.metrics.pairwise import linear_kernel

from data.movie_loader import movie_df, movie_index

from services.movie_service import get_movie_by_title

from core.model_loader import (
    genre_matrix,
    overview_matrix,
    actor_matrix,
    director_matrix
)

GENRE_WEIGHT = 0.35
OVERVIEW_WEIGHT = 0.35
ACTOR_WEIGHT = 0.2
DIRECTOR_WEIGHT = 0.1

OVERVIEW_SCALE = 15
ACTOR_SCALE = 10

MATCH_SCORE_BASE = 60
MATCH_SCORE_RANGE = 40


def _calculate_final_similarity(idx):
    genre_sim = linear_kernel(genre_matrix[idx], genre_matrix).flatten()
    overview_sim = linear_kernel(overview_matrix[idx], overview_matrix).flatten()
    actor_sim = linear_kernel(actor_matrix[idx], actor_matrix).flatten()
    director_sim = linear_kernel(director_matrix[idx], director_matrix).flatten()

    return (
        genre_sim * GENRE_WEIGHT +
        np.clip(overview_sim * OVERVIEW_SCALE, 0, 1) * OVERVIEW_WEIGHT +
        np.clip(actor_sim * ACTOR_SCALE, 0, 1) * ACTOR_WEIGHT +
        director_sim * DIRECTOR_WEIGHT
    )


def _calculate_match_score(similarity):
    return round(
        float(MATCH_SCORE_BASE + similarity * MATCH_SCORE_RANGE),
        1
    )


def _build_recommendation_item(
        movie_id,
        movie,
        movie_title,
        similarity
):
    return {
        "id": movie_id,
        "title": movie_title,
        "genre": movie["장르"],
        "poster_url": movie["포스터이미지"],
        "match_score": _calculate_match_score(similarity)
    }


# ======================
# 추천함수
# ======================
def recommend_movies(title, top_n=5) :

    if title not in movie_index:
        return {
            "success": False,
            "message": "기준 영화를 찾을 수 없습니다.",
            "title": title,
            "recommendations": []
        }

    idx = movie_index[title]

    final_sim = _calculate_final_similarity(idx)

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
        
        movie = movie_df.iloc[i]

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

        recommendations.append(
            _build_recommendation_item(
                movie_id=movie_id,
                movie=movie,
                movie_title=movie_title,
                similarity=final_sim[i],
            )
        )

        recommended_ids.add(movie_id)
        recommended_titles.add(movie_title)

        if len(recommendations) >= top_n:
            break

    return {
        "success": True,
        "title": title,
        "recommendations": recommendations
    }