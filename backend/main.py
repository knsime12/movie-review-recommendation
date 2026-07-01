from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import (
    movie_router, 
    sentiment_router,
    recommendation_router,
    user_router,
    review_router,
    recommendation_history_router
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
app.include_router(recommendation_history_router.router)


# ======================
# 정적 파일 서비스
# ======================
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/html", StaticFiles(directory=FRONTEND_DIR / "html"), name="html")


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