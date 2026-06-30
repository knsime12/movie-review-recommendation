from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from pydantic import BaseModel

from services.sentiment_service import predict_sentiment
from services.recommendation_service import recommend_movies
from services.movie_service import (
    get_movie_detail,
    get_movies,
    get_popular_movies,
)
from services.user_service import create_user, login_user
from services.review_service import (
    create_review,
    get_reviews_by_user,
    create_recommendation_history,
    get_recommendations_by_user,
    delete_review,
    check_review_exists
)


BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="CineFeel API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================
# 정적 파일 서비스
# ======================
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/html", StaticFiles(directory=FRONTEND_DIR / "html"), name="html")


# ======================
# 요청 모델
# ======================
class ReviewRequest(BaseModel) :
    content: str


class RecommendRequest(BaseModel) :
    movie_title: str
    top_n: int = 5
    
    
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str
    
class ReviewSaveRequest(BaseModel):
    user_id: Optional[int] = None
    movie_id: int
    content: str
    sentiment: str
    positive_prob: Optional[float] = None
    expected_rating: Optional[float] = None
    keywords: Optional[list[str]] = None
    

class RecommendationHistoryRequest(BaseModel):
    user_id: int
    base_movie_id: int
    recommended_movie_id: int
    similarity: float


class ReviewDeleteRequest(BaseModel):
    user_id: int

# ======================
# 페이지 라우팅
# ======================
@app.get("/")
def home() :
    return FileResponse(FRONTEND_DIR / "html" / "index.html")


# ======================
# API
# ======================
@app.get("/api")
def api_home():
    return {"message": "CineFeel API is running"}


@app.get("/movies")
def movies(keyword: str = "", page: int = 1, size: int = 12):
    return get_movies(
        keyword=keyword, 
        page=page,
        size=size
    )


@app.get("/movies/popular")
def popular_movies(limit: int = 6):
    return get_popular_movies(limit=limit)


@app.get("/movies/{movie_id}")
def movie_detail(movie_id: int):
    return get_movie_detail(movie_id=movie_id)


@app.post("/analyze")
def analyze(request: ReviewRequest) :
    return predict_sentiment(review=request.content)


@app.post("/recommend")
def recommend(request: RecommendRequest) :
    return recommend_movies(
        title=request.movie_title,
        top_n=request.top_n
    )


@app.post("/signup")
def signup(request: SignupRequest):
    return create_user(
        username=request.username,
        email=request.email, 
        password=request.password    
    )


@app.post("/login")
def login(request: LoginRequest):
    return login_user(
        email=request.email,
        password=request.password
    )

@app.post("/reviews")
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
    
@app.get("/users/{user_id}/reviews")
def user_reviews(user_id: int):
    return get_reviews_by_user(user_id=user_id)

@app.get("/users/{user_id}/recommendations")
def user_recommendations(user_id: int):
    return get_recommendations_by_user(user_id=user_id)


@app.post("/recommendation-history")
def save_recommendation_history(request: RecommendationHistoryRequest):
    return create_recommendation_history(
        user_id=request.user_id,
        base_movie_id=request.base_movie_id,
        recommended_movie_id=request.recommended_movie_id,
        similarity=request.similarity
    )

@app.delete("/reviews/{review_id}")
def delete_review_api(review_id: int, request: ReviewDeleteRequest):
    return delete_review(
        review_id=review_id,
        user_id=request.user_id
    )

@app.get("/reviews/check")
def check_review(user_id: int, movie_id: int):
    return check_review_exists(
        user_id=user_id,
        movie_id=movie_id
    )