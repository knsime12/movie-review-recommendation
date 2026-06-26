import pandas as pd
import pymysql
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
csv_path = BASE_DIR / "data" / "movies.csv"

df = pd.read_csv(csv_path)

# NaN -> None
def clean(value):
    if pd.isna(value):
        return None
    return str(value).strip()

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="cinefeel",
    charset="utf8mb4"
)

cursor = conn.cursor()

query = """
INSERT INTO movies
(title, genre, director, actors, release_date, poster_url, overview)
VALUES (%s, %s, %s, %s, %s, %s, %s)
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

cursor.executemany(query, data)

conn.commit()
cursor.close()
conn.close()

print(f"영화 데이터 {len(data)}건 저장 완료")