from fastapi import APIRouter
from pydantic import BaseModel

from services.recommendation_history_service import (
    create_recommendation_history,
    get_recommendations_by_user
)


class RecommendationHistoryRequest(BaseModel):
    user_id: int
    base_movie_id: int
    recommended_movie_id: int
    similarity: float


router = APIRouter()


@router.get("/users/{user_id}/recommendations")
def user_recommendations(user_id: int):
    return get_recommendations_by_user(user_id=user_id)


@router.post("/recommendation-history")
def save_recommendation_history(request: RecommendationHistoryRequest):
    return create_recommendation_history(
        user_id=request.user_id,
        base_movie_id=request.base_movie_id,
        recommended_movie_id=request.recommended_movie_id,
        similarity=request.similarity
    )