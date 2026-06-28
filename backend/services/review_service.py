from database import get_connection

def create_review(user_id, movie_id, content, sentiment, positive_prob, expected_rating):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO reviews
        (user_id, movie_id, content, sentiment, positive_prob, expected_rating)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(
            query, (user_id, movie_id, content, sentiment, positive_prob, expected_rating)
        )
        
        conn.commit()
        
        return {
            "success": True,
            "message": "리뷰가 저장되었습니다.",
            "review_id": cursor.lastrowid
        }
        
    except Exception as e:
        conn.rollback()
        print("리뷰 저장 오류:", e)
        
        return {
            "success": False,
            "message": "리뷰 저장 중 오류가 발생했습니다.",
            "error": str(e)
        }
        
    finally:
        cursor.close()
        conn.close()
        
def get_reviews_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT
            r.id AS review_id,
            r.user_id,
            r.movie_id,
            r.content,
            r.sentiment,
            r.positive_prob,
            r.expected_rating,
            r.created_at,
            m.title,
            m.genre,
            m.poster_url
        FROM reviews r
        JOIN movies m
        ON r.movie_id = m.id
        WHERE r.user_id = %s
        ORDER BY r.created_at DESC
        """
        
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        
        return {
            "success": True,
            "reviews": rows
        }
        
    except Exception as e:
        print("리뷰 조회 오류:", e)
        
        return {
            "success": False,
            "message": "리뷰 조회 중 오류가 발생했습니다.",
            "error": str(e)
        }
        
    finally:
        cursor.close()
        conn.close()