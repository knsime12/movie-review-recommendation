from fastapi import APIRouter
from fastapi.responses import FileResponse

from core.paths import BASE_DIR


FRONTEND_DIR = BASE_DIR / "frontend"


router = APIRouter()


@router.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "html" / "index.html")


@router.get("/api")
def api_home():
    return {"message": "CineFeel API is running"}