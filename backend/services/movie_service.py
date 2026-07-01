from utils.db_utils import get_db_cursor

def get_movies(keyword="", page=1, size=12):
    offset = (page - 1) * size
    
    with get_db_cursor() as (_, cursor):
        if keyword:
            count_query = """
            SELECT COUNT(*) AS total
            FROM movies
            WHERE title LIKE %s
            """

            cursor.execute(count_query, (f"%{keyword}%",))
            total = cursor.fetchone()["total"]

            query = """
            SELECT
                id,
                title,
                genre,
                director,
                actors,
                overview,
                release_date,
                poster_url,
                rating
            FROM movies
            WHERE title LIKE %s
            ORDER BY id ASC
            LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, (f"%{keyword}%", size, offset))
            
        else:
            count_query = """
            SELECT COUNT(*) AS total
            FROM movies
            """
            
            cursor.execute(count_query)
            total = cursor.fetchone()["total"]
            
            query = """
            SELECT
                id,
                title,
                genre,
                director,
                actors,
                overview,
                release_date,
                poster_url,
                rating
            FROM movies
            ORDER BY id ASC
            LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, (size, offset))
            
        rows = cursor.fetchall()
    
    total_pages = (total + size - 1) // size
    
    return {
        "movies": rows,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages
    }

def get_movie_detail(movie_id):

    with get_db_cursor() as (_, cursor):
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
        WHERE id=%s
        """

        cursor.execute(query, (movie_id,))

        return cursor.fetchone()

def get_movie_by_title(title):

    with get_db_cursor() as (_, cursor):
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
        WHERE title = %s
        LIMIT 1
        """

        cursor.execute(query, (title,))
        return cursor.fetchone()
        

def get_popular_movies(limit=6):

    with get_db_cursor() as (_, cursor):
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