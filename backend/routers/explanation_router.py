from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.llm_explanation_service import generate_recommendation_explanation


class RecommendationItem(BaseModel):
    title: str
    genre: Optional[str] = None
    match_score: Optional[float] = None
    
    
class ExplanationRequest(BaseModel):
    review: str
    sentiment: str
    positive_prob: float
    expected_rating: float
    keywords: List[str]
    base_movie_title: str
    recommendations: List[RecommendationItem]
    
    
router = APIRouter()


@router.post("/recommendation-explanation")
def explain_recommendation(request: ExplanationRequest):
    if hasattr(request, "model_dump"):
        request_data = request.model_dump()
    else:
        request_data = request.dict()
        
    return generate_recommendation_explanation(request_data)