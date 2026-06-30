import pandas as pd

from core.paths import DATA_DIR

movie_df = pd.read_csv(DATA_DIR / "movies.csv")
movie_index = pd.Series(
    movie_df.index,
    index=movie_df["영화제목"]
).drop_duplicates()