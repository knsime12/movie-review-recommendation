from fastapi import APIRouter
from pydantic import BaseModel

from services.user_service import (
    create_user,
    login_user
)

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


router = APIRouter()


@router.post("/signup")
def signup(request: SignupRequest):
    return create_user(
        username=request.username,
        email=request.email,
        password=request.password
    )


@router.post("/login")
def login(request: LoginRequest):
    return login_user(
        email=request.email,
        password=request.password
    )