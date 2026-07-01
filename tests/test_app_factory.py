import main
from fastapi import FastAPI

from main import app, create_app
from routers import (
    movie_router,
    page_router,
    recommendation_history_router,
    recommendation_router,
    review_router,
    sentiment_router,
    user_router
)


def test_create_app_returns_fastapi_instance():
    test_app = create_app()

    assert isinstance(test_app, FastAPI)


def test_app_is_created_from_factory():
    assert isinstance(app, FastAPI)


def test_create_app_registers_routes():

    test_app = create_app()
    paths = set(test_app.openapi()["paths"].keys())

    assert "/" in paths
    assert "/api" in paths
    assert "/movies" in paths
    assert "/analyze" in paths
    assert "/recommend" in paths
    assert "/signup" in paths
    assert "/login" in paths
    assert "/reviews" in paths
    assert "/recommendation-history" in paths