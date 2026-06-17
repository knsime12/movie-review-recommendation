import joblib
import sentiment
import recommend
import common

from sentiment import predict_sentiment
from recommend import recommend_movies

import pandas as pd

# ======================
# 모델 로딩
# ======================
sentiment.tfidf_sentiment = joblib.load("models/tfidf_sentiment.pkl")
sentiment.lr_model = joblib.load("models/lr_model.pkl")

recommend.genre_matrix = joblib.load("models/genre_matrix.pkl")
recommend.overview_matrix = joblib.load("models/overview_matrix.pkl")
recommend.actor_matrix = joblib.load("models/actor_matrix.pkl")
recommend.director_matrix = joblib.load("models/director_matrix.pkl")

common.movie_df = pd.read_csv("movie_database_unique.csv")
common.movie_index = pd.Series(
    common.movie_df.index,
    index = common.movie_df["영화제목"]
).drop_duplicates()

# 리뷰 저장
review_history = []

# ======================
# 통합 함수
# ======================
def analyze(title, review) :
    sentiment_result = predict_sentiment(review)
    recommend_result = recommend_movies(title)

    # 리뷰 저장
    review_history.append(sentiment_result)

    # 리뷰 누적
    positive_count = sum(
        1 for r in review_history if r["감정"] == "긍정"
    )
    negative_count = sum(
        1 for r in review_history if r["감정"] == "부정"
    )

    # 출력
    print("\n====================")
    print("리뷰 분석 결과")
    print("====================")

    print("리뷰: ", sentiment_result["리뷰"])
    print("감정: ", sentiment_result["감정"])
    print("예측평점: ", sentiment_result["예측평점"])

    print("\n키워드: ", ",".join(sentiment_result["키워드"]))

    if sentiment_result["예측평점"] >= 4.0 :
        print("\n추천 영화 :")
        for i in recommend_result["추천영화목록"] :
            print(f"영화제목: {i['영화제목']}, 매칭률: {i['매칭률(%)']}%")

    return {
        "sentiment": sentiment_result,
        "recommend": recommend_result,
        "positive_count": positive_count,
        "negative_count": negative_count
    }

if __name__ == "__main__":
    print("실행 시작")
    analyze(
        "인터스텔라",
        """
        영상미와 음악이 정말 뛰어나고
        몰입감이 엄청났다.
        엔딩의 여운도 강했다.
        """
    )
