import sys
import types

fake_resources = types.ModuleType("nlp.resources")


class FakeOkt:
    def pos(self, text, stem=True):
        return [
            ("영화", "Noun"),
            ("스토리", "Noun"),
            ("좋다", "Adjective"),
            ("보다", "Verb"),
            ("나", "Noun"),
        ]

    def nouns(self, text):
        return ["영화", "추천", "나", "스토리"]


setattr(fake_resources, "okt", FakeOkt())
setattr(fake_resources, "stopwords_sentiment", [])
setattr(fake_resources, "stopwords_keyword", [])
setattr(fake_resources, "stopwords_recommend", [])
sys.modules["nlp.resources"] = fake_resources

from utils import text_preprocessor


def test_clean_korean_text_removes_non_korean_characters():
    result = text_preprocessor.clean_korean_text("Movie 영화!!! 123 좋다")

    assert result == "영화 좋다"


def test_clean_korean_text_returns_empty_for_invalid_input():
    assert text_preprocessor.clean_korean_text(None) == ""
    assert text_preprocessor.clean_korean_text(123) == ""


def test_clean_korean_english_text_keeps_korean_and_english():
    result = text_preprocessor.clean_korean_english_text("Movie 영화!!! 123 좋다")

    assert result == "Movie 영화 좋다"


def test_preprocess_sentiment_filters_by_pos_stopwords_and_length(monkeypatch):
    monkeypatch.setattr(text_preprocessor, "stopwords_sentiment", {"스토리"})

    result = text_preprocessor.preprocess_sentiment("영화 스토리 좋다")

    assert result == "영화 좋다"


def test_preprocess_keyword_keeps_nouns_only(monkeypatch):
    monkeypatch.setattr(text_preprocessor, "stopwords_keyword", {"영화"})

    result = text_preprocessor.preprocess_keyword("영화 스토리 좋다")

    assert result == "스토리"


def test_preprocess_recommend_filters_nouns(monkeypatch):
    monkeypatch.setattr(text_preprocessor, "stopwords_recommend", {"영화"})

    result = text_preprocessor.preprocess_recommend("영화 추천 스토리")

    assert result == "추천 스토리"