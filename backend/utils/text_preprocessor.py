import re

import pandas as pd

from nlp.tokenizer import okt
from nlp.stopwords import (
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


def preprocess_sentiment(text):
    text = clean_korean_text(text)

    tokens = okt.pos(text, stem=True)

    words = []

    for word, pos in tokens:
        if pos in ["Noun", "Adjective"]:
            if word not in stopwords_sentiment:
                if len(word) > 1:
                    words.append(word)

    return " ".join(words)


def preprocess_keyword(text):
    text = clean_korean_text(text)

    tokens = okt.pos(text, stem=True)

    words = []

    for word, pos in tokens:
        if pos == "Noun":
            if word not in stopwords_keyword:
                if len(word) > 1:
                    words.append(word)

    return " ".join(words)


def preprocess_recommend(text):
    text = clean_korean_english_text(text)

    # 형태소 분석 - 명사
    tokens = okt.nouns(text)

    # 불용어 제거
    words = [
        word for word in tokens
        if word not in stopwords_recommend and len(word) > 1
    ]

    return " ".join(words)