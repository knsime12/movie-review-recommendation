import os
import pandas as pd
import pymysql
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
csv_path = BASE_DIR / "data" / "movies.csv"


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_NAME = os.getenv("DB_NAME", "cinefeel")
DB_PORT = int(os.getenv("DB_PORT", "3306"))


df = pd.read_csv(csv_path)


def clean(value):
    if pd.isna(value):
        return None
    return str(value).strip()


conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT,
    charset="utf8mb4"
)

query = """
INSERT INTO movies
(title, genre, director, actors, release_date, poster_url, overview)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    genre = VALUES(genre),
    director = VALUES(director),
    actors = VALUES(actors),
    release_date = VALUES(release_date),
    poster_url = VALUES(poster_url),
    overview = VALUES(overview)
"""

data = []

for _, row in df.iterrows():
    data.append((
        clean(row["영화제목"]),
        clean(row["장르"]),
        clean(row["감독"]),
        clean(row["배우"]),
        clean(row["개봉일"]),
        clean(row["포스터이미지"]),
        clean(row["영화줄거리"]),
    ))

try:
    with conn.cursor() as cursor:
        cursor.executemany(query, data)

    conn.commit()

finally:
    conn.close()

print(f"영화 데이터 {len(data)}건 저장 완료")