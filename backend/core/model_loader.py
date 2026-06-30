import joblib

from core.paths import MODEL_DIR

def load_model(filename):
    return joblib.load(MODEL_DIR / filename)

tfidf_sentiment = load_model("tfidf_sentiment.pkl")
sentiment_model = load_model("lr_model.pkl")

genre_matrix = load_model("genre_matrix.pkl")
overview_matrix = load_model("overview_matrix.pkl")
actor_matrix = load_model("actor_matrix.pkl")
director_matrix = load_model("director_matrix.pkl")