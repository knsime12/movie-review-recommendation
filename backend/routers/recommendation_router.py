from fastapi import APIRouter
from pydantic import BaseModel

from services.recommendation_service import recommend_movies


class RecommendRequest(BaseModel):
    movie_title: str
    top_n: int = 5


router = APIRouter()


@router.post("/recommend")
def recommend(request: RecommendRequest):
    return recommend_movies(
        title=request.movie_title,
        top_n=request.top_n
    )