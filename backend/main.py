from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.sentiment_service import predict_sentiment 
from services.recommend_service import recommend_movies
from services.movie_service import get_movies, get_movie, get_popular_movies

app = FastAPI(title="CineFeel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel) :
    review: str

class RecommendRequest(BaseModel) :
    movie_title: str
    top_n: int = 5

@app.get("/")
def home() :
    return {"message": "CineFeel API is running"}

@app.get("/movies")
def movies():
    return get_movies()

@app.get("/movies/popular")
def popular_movies(limit: int = 6):
    return get_popular_movies(limit)

@app.get("/movies/{movie_id}")
def movie_detail(movie_id: int):
    return get_movie(movie_id)

@app.post("/analyze")
def analyze(request: ReviewRequest) :
    return predict_sentiment(request.review)

@app.post("/recommend")
def recommend(request: RecommendRequest) :
    return recommend_movies(request.movie_title, request.top_n)