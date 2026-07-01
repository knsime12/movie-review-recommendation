import sys
import types

import numpy as np

fake_text_preprocessor = types.ModuleType("utils.text_preprocessor")
setattr(fake_text_preprocessor, "preprocess_keyword", lambda review: review)
sys.modules["utils.text_preprocessor"] = fake_text_preprocessor

from services import keyword_service


class FakeVector:
    def __init__(self, scores):
        self.scores = scores

    def toarray(self):
        return np.array([self.scores])


class FakeTfidf:
    def __init__(self, scores, features):
        self.scores = scores
        self.features = features
        self.transform_calls = []

    def transform(self, texts):
        self.transform_calls.append(texts)
        return FakeVector(self.scores)

    def get_feature_names_out(self):
        return np.array(self.features)


def test_extract_keywords_returns_filtered_keywords(monkeypatch):
    fake_tfidf = FakeTfidf(
        scores=np.array([0.9, 0.8, 0.7, 0.6, 0.0]),
        features=np.array(["연기", "스토리", "불용어", "긴 단어", "음악"]),
    )

    monkeypatch.setattr(keyword_service, "tfidf_sentiment", fake_tfidf)
    monkeypatch.setattr(keyword_service, "preprocess_keyword", lambda review: "연기 스토리 음악")
    monkeypatch.setattr(keyword_service, "stopwords_keyword", {"불용어"})
    monkeypatch.setattr(keyword_service, "movie_keywords", {"연기", "스토리", "음악"})

    result = keyword_service.extract_keywords("리뷰 내용", top_n=3)

    assert result == ["연기", "스토리"]
    assert fake_tfidf.transform_calls == [["연기 스토리 음악"]]


def test_extract_keywords_respects_top_n(monkeypatch):
    fake_tfidf = FakeTfidf(
        scores=np.array([0.9, 0.8, 0.7]),
        features=np.array(["연기", "스토리", "음악"]),
    )

    monkeypatch.setattr(keyword_service, "tfidf_sentiment", fake_tfidf)
    monkeypatch.setattr(keyword_service, "preprocess_keyword", lambda review: "연기 스토리 음악")
    monkeypatch.setattr(keyword_service, "stopwords_keyword", set())
    monkeypatch.setattr(keyword_service, "movie_keywords", {"연기", "스토리", "음악"})

    result = keyword_service.extract_keywords("리뷰 내용", top_n=2)

    assert result == ["연기", "스토리"]


def test_extract_keywords_returns_empty_when_no_keyword_matches(monkeypatch):
    fake_tfidf = FakeTfidf(
        scores=np.array([0.9, 0.8]),
        features=np.array(["하다", "그리고"]),
    )

    monkeypatch.setattr(keyword_service, "tfidf_sentiment", fake_tfidf)
    monkeypatch.setattr(keyword_service, "preprocess_keyword", lambda review: "하다 그리고")
    monkeypatch.setattr(keyword_service, "stopwords_keyword", {"하다", "그리고"})
    monkeypatch.setattr(keyword_service, "movie_keywords", {"연기", "스토리"})

    result = keyword_service.extract_keywords("리뷰 내용")

    assert result == []