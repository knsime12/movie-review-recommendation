import json

from services.recommendation_history_service import delete_recommendation_histories
from utils.db_utils import get_db_cursor

def _validate_review_input (user_id, movie_id, content):
    # ======================
    # 예외 처리
    # ======================
    if not user_id:
        return {
            "success": False,
            "message": "로그인이 필요합니다."
        }
    
    if not movie_id:
        return {
            "success": False,
            "message": "영화 정보가 없습니다."
        }
    
    if not content or not content.strip():
        return {
            "success": False,
            "message": "리뷰 내용을 입력해주세요."
        }
    
    if len(content.strip()) < 5:
        return {
            "success": False,
            "message": "리뷰는 5자 이상 작성해주세요."
        }
    
    if len(content.strip()) > 500:
        return {
            "success": False,
            "message": "리뷰는 500자 이하로 작성해주세요."
        }
    
    return None


# 리뷰 작성
def create_review(user_id, movie_id, content, sentiment, positive_prob, expected_rating, keywords=None):

    validation_error = _validate_review_input(user_id, movie_id, content)

    if validation_error:
        return validation_error
    
    try:
        with get_db_cursor() as (conn, cursor):
            # ======================
            # 리뷰 중복 작성 방지
            # ======================
            check_query = """
            SELECT id
            FROM reviews
            WHERE user_id = %s AND movie_id = %s
            """

            cursor.execute(check_query, (user_id, movie_id))
            existing_review = cursor.fetchone()

            if existing_review:
                return {
                    "success": False,
                    "message": "이미 이 영화에 리뷰를 작성했습니다."
                }

            # ======================
            # 리뷰 저장
            # ======================
            keyword_text = json.dumps(keywords or [], ensure_ascii = False)

            query = """
            INSERT INTO reviews
            (user_id, movie_id, content, sentiment, positive_prob, expected_rating, keywords)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(
                query, 
                (
                    user_id,
                    movie_id, 
                    content, 
                    sentiment, 
                    positive_prob, 
                    expected_rating, 
                    keyword_text
                )
            )
        
            conn.commit()
            
            return {
                "success": True,
                "message": "리뷰가 저장되었습니다.",
                "review_id": cursor.lastrowid
            }
        
    except Exception as e:
        print("리뷰 저장 오류:", e)

        return {
            "success": False,
            "message": "리뷰 저장 중 오류가 발생했습니다.",
            "error": str(e)
        }
        
# 리뷰 조회
def get_reviews_by_user(user_id):
    query = """
    SELECT
        r.id AS review_id,
        r.user_id,
        r.movie_id,
        r.content,
        r.sentiment,
        r.positive_prob,
        r.expected_rating,
        r.keywords,
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
    
    try:
        with get_db_cursor() as (_, cursor):
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


# 리뷰 삭제(추천이력 포함)
def delete_review(review_id, user_id):

    try:
        with get_db_cursor() as (conn, cursor):
            query = """
            SELECT movie_id
            FROM reviews
            WHERE id = %s AND user_id = %s
            """

            cursor.execute(query, (review_id, user_id))

            review = cursor.fetchone()

            if not review:
                return {
                    "success": False,
                    "message": "삭제할 리뷰를 찾을 수 없습니다."
                }
        
            movie_id = review["movie_id"]

            delete_recommendation_histories(user_id, movie_id)

            query = """
            DELETE FROM reviews
            WHERE id = %s AND user_id = %s
            """

            cursor.execute(query, (review_id, user_id))
            conn.commit()

            return {
                "success": True,
                "message": "리뷰와 추천 이력이 삭제되었습니다."
            }
    
    except Exception as e:
        print("리뷰 삭제 오류:", e)

        return {
            "success": False,
            "message": "리뷰 삭제 중 오류가 발생했습니다.",
            "error": str(e)
        }

# 리뷰 중복 검사
def check_review_exists(user_id, movie_id):
    
    try:
        query = """
        SELECT id
        FROM reviews
        WHERE user_id = %s AND movie_id = %s
        """

        with get_db_cursor() as (_, cursor):
            cursor.execute(query, (user_id, movie_id))
            review = cursor.fetchone()
       
        return {
            "success": True,
            "exists": review is not None,
            "message": "이미 작성한 리뷰가 있습니다." if review else "작성 가능한 영화입니다."
        }
    
    except Exception as e:
        print("리뷰 중복 확인 오류:", e)

        return {
            "success": False,
            "exists": False,
            "message": "리뷰 중복 확인 중 오류가 발생했습니다.",
            "error": str(e)
        }