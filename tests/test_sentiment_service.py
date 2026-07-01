import numpy as np

from services import sentiment_service


class FakeTfidf:
    def __init__(self):
        self.transform_calls = []

    def transform(self, texts):
        self.transform_calls.append(texts)
        return "vectorized-review"


class FakeSentimentModel:
    def __init__(self, pred, positive_prob):
        self.pred = pred
        self.positive_prob = positive_prob

    def predict(self, vec):
        return np.array([self.pred])

    def predict_proba(self, vec):
        return np.array([[1 - self.positive_prob, self.positive_prob]])


def test_predict_sentiment_positive(monkeypatch):
    fake_tfidf = FakeTfidf()
    fake_model = FakeSentimentModel(pred=1, positive_prob=0.8)

    monkeypatch.setattr(sentiment_service, "tfidf_sentiment", fake_tfidf)
    monkeypatch.setattr(sentiment_service, "sentiment_model", fake_model)
    monkeypatch.setattr(sentiment_service, "preprocess_sentiment", lambda review: "clean review")
    monkeypatch.setattr(sentiment_service, "extract_keywords", lambda review: ["연기", "스토리"])

    result = sentiment_service.predict_sentiment("영화가 정말 좋았다")

    assert result == {
        "review": "영화가 정말 좋았다",
        "sentiment": "긍정",
        "positive_prob": 0.8,
        "expected_rating": 4.0,
        "keywords": ["연기", "스토리"],
    }
    assert fake_tfidf.transform_calls == [["clean review"]]


def test_predict_sentiment_negative(monkeypatch):
    fake_tfidf = FakeTfidf()
    fake_model = FakeSentimentModel(pred=0, positive_prob=0.25)

    monkeypatch.setattr(sentiment_service, "tfidf_sentiment", fake_tfidf)
    monkeypatch.setattr(sentiment_service, "sentiment_model", fake_model)
    monkeypatch.setattr(sentiment_service, "preprocess_sentiment", lambda review: "clean review")
    monkeypatch.setattr(sentiment_service, "extract_keywords", lambda review: ["전개"])

    result = sentiment_service.predict_sentiment("영화가 지루했다")

    assert result["review"] == "영화가 지루했다"
    assert result["sentiment"] == "부정"
    assert result["positive_prob"] == 0.25
    assert result["expected_rating"] == 2.0
    assert result["keywords"] == ["전개"]