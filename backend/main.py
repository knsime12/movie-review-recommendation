from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.sentiment_service import predict_sentiment
from services.recommend_service import recommend_movies
from services.movie_service import (
    get_movie_detail,
    get_movies,
    get_popular_movies,
)
from services.user_service import create_user, login_user


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
    review: str


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
    return get_movies(keyword=keyword, page=page, size=size)


@app.get("/movies/popular")
def popular_movies(limit: int = 6):
    return get_popular_movies(limit)


@app.get("/movies/{movie_id}")
def movie_detail(movie_id: int):
    return get_movie_detail(movie_id)


@app.post("/analyze")
def analyze(request: ReviewRequest) :
    return predict_sentiment(request.review)


@app.post("/recommend")
def recommend(request: RecommendRequest) :
    return recommend_movies(request.movie_title, request.top_n)


@app.post("/signup")
def signup(request: SignupRequest):
    return create_user(request.username, request.email, request.password)


@app.post("/login")
def login(request: LoginRequest):
    return login_user(request.email, request.password)