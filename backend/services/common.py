from pathlib import Path
import pandas as pd
from konlpy.tag import Okt

BASE_DIR = Path(__file__).resolve().parents[2]

movie_df = pd.read_csv(BASE_DIR / "data" / "movies.csv")
movie_index = pd.Series(movie_df.index, index=movie_df["영화제목"]).drop_duplicates()

# ======================
# 형태소 분석기(공용 1개)
# ======================
okt = Okt()










