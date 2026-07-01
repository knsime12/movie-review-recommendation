from fastapi import APIRouter

from services.movie_service import (
    get_movie_detail,
    get_movies,
    get_popular_movies,
)


router = APIRouter()


@router.get("/movies")
def movies(keyword: str = "", page: int = 1, size: int = 12):
    return get_movies(
        keyword=keyword,
        page=page,
        size=size
    )


@router.get("/movies/popular")
def popular_movies(limit: int = 6):
    return get_popular_movies(limit=limit)


@router.get("/movies/{movie_id}")
def movie_detail(movie_id: int):
    return get_movie_detail(movie_id=movie_id)