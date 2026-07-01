from tkinter import N
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.review_service import (
    check_review_exists,
    create_review,
    delete_review,
    get_reviews_by_user
)


class ReviewSaveRequest(BaseModel):
    user_id: Optional[int] = None
    movie_id: int
    content: str
    sentiment: str
    positive_prob: Optional[float] = None
    expected_rating: Optional[float] = None
    keywords: Optional[list[str]] = None


class ReviewDeleteRequest(BaseModel):
    user_id: int


router = APIRouter()


@router.post("/reviews")
def save_review(request: ReviewSaveRequest):
    return create_review(
        user_id=request.user_id,
        movie_id=request.movie_id,
        content=request.content,
        sentiment=request.sentiment,
        positive_prob=request.positive_prob,
        expected_rating=request.expected_rating,
        keywords=request.keywords
    )


@router.get("/users/{user_id}/reviews")
def user_reviews(user_id: int):
    return get_reviews_by_user(user_id=user_id)
    

@router.delete("/reviews/{review_id}")
def delete_review_api(review_id: int, request: ReviewDeleteRequest):
    return delete_review(
        review_id=review_id,
        user_id=request.user_id
    )


@router.get("/reviews/check")
def check_review(user_id: int, movie_id: int):
    return check_review_exists(
        user_id=user_id,
        movie_id=movie_id
    )