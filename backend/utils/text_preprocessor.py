import re

import pandas as pd

from nlp.resources import (
    okt,
    stopwords_sentiment,
    stopwords_keyword,
    stopwords_recommend
)

def clean_korean_text(text):
    if pd.isna(text):
        return ""
    
    if not isinstance(text, str):
        return ""
    
    text = re.sub(r"[^가-힣\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_korean_english_text(text):
    if pd.isna(text):
        return ""
    
    if not isinstance(text, str):
        return ""
    
    text = re.sub(r"[^가-힣a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def _is_valid_word(word, stopwords):
    return word not in stopwords and len(word) > 1


def preprocess_sentiment(text):
    text = clean_korean_text(text)

    tokens = okt.pos(text, stem=True)

    words = []

    for word, pos in tokens:
        if pos in ["Noun", "Adjective"] and _is_valid_word(word, stopwords_sentiment):
            words.append(word)

    return " ".join(words)


def preprocess_keyword(text):
    text = clean_korean_text(text)

    tokens = okt.pos(text, stem=True)

    words = []

    for word, pos in tokens:
        if pos == "Noun" and _is_valid_word(word, stopwords_keyword):
            words.append(word)

    return " ".join(words)


def preprocess_recommend(text):
    text = clean_korean_english_text(text)

    # 형태소 분석 - 명사
    tokens = okt.nouns(text)

    # 불용어 제거
    words = [
        word for word in tokens
        if _is_valid_word(word, stopwords_recommend)
    ]

    return " ".join(words)