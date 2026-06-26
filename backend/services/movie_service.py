from database import get_connection

def get_movies():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT
                id,
                title,
                genre,
                director,
                actors,
                release_date,
                poster_url,
                overview
            FROM movies
            ORDER BY id DESC
            """

            cursor.execute(sql)
            movies = cursor.fetchall()

            return movies
        
    finally:
        conn.close()

def get_movie(movie_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            sql = """
            SELECT
                id,
                title,
                genre,
                director,
                actors,
                release_date,
                poster_url,
                overview
            FROM movies
            WHERE id=%s
            """

            cursor.execute(sql, (movie_id,))

            return cursor.fetchone()
        
    finally:
        conn.close()

def get_movie_by_title(title):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT
                id,
                title,
                genre,
                director,
                actors,
                release_date,
                poster_url,
                overview
            FROM movies
            WHERE title = %s
            LIMIT 1
            """

            cursor.execute(sql, (title,))
            return cursor.fetchone()
        
    finally:
        conn.close()

def get_popular_movies(limit=6):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        title,
        genre,
        director,
        actors,
        release_date,
        poster_url,
        overview
    FROM movies
    ORDER BY id ASC
    LIMIT %s
    """

    cursor.execute(query, (limit,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    movies = []

    for row in rows:
        movies.append({
            "id": row["id"],
            "title": row["title"],
            "genre": row["genre"],
            "director": row["director"],
            "actors": row["actors"],
            "release_date": row["release_date"],
            "poster_url": row["poster_url"],
            "overview": row["overview"],
            "rating": 4.5
        })

    return movies