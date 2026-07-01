from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pydantic import BaseModel
from routers import (
    movie_router, 
    sentiment_router,
    recommendation_router,
    user_router,
    review_router
)

from services.recommendation_history_service import (
    create_recommendation_history,
    get_recommendations_by_user
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


app.include_router(movie_router.router)
app.include_router(sentiment_router.router)
app.include_router(recommendation_router.router)
app.include_router(user_router.router)
app.include_router(review_router.router)


# ======================
# 정적 파일 서비스
# ======================
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/html", StaticFiles(directory=FRONTEND_DIR / "html"), name="html")


# ======================
# 요청 모델
# ======================
class RecommendationHistoryRequest(BaseModel):
    user_id: int
    base_movie_id: int
    recommended_movie_id: int
    similarity: float


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