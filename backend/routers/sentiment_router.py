from fastapi import APIRouter
from pydantic import BaseModel

from services.sentiment_service import predict_sentiment

class ReviewRequest(BaseModel):
    content: str


router = APIRouter()


@router.post("/analyze")
def analyze(request: ReviewRequest):
    return predict_sentiment(request.content)