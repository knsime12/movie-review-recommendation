import logging

from utils.db_utils import get_db_cursor


logger = logging.getLogger(__name__)


def _validate_recommendation_history_input(user_id, base_movie_id, recommended_movie_id):
    # ======================
    # 예외 처리
    # ======================
    if not user_id:
        return {
            "success": False,
            "message": "로그인이 필요합니다."
        }
    
    if not base_movie_id or not recommended_movie_id:
        return {
            "success": False,
            "message": "추천 영화 정보가 없습니다."
        }
    
    if base_movie_id == recommended_movie_id:
        return {
            "success": False,
            "message": "같은 영화는 추천 이력에 저장할 수 없습니다."
        }
    
    return None


def _get_existing_recommendation_history(
        cursor,
        user_id,
        base_movie_id,
        recommended_movie_id,
):
    query = """
    SELECT id
    FROM recommendation_history
    WHERE user_id = %s
        AND base_movie_id = %s
        AND recommended_movie_id = %s
    """

    cursor.execute(
        query,
        (user_id, base_movie_id, recommended_movie_id)    
    )

    return cursor.fetchone()


# 추천 이력 저장
def create_recommendation_history(
        user_id, 
        base_movie_id, 
        recommended_movie_id, 
        similarity
):
    
    validation_error = _validate_recommendation_history_input(
        user_id,
        base_movie_id,
        recommended_movie_id,
    )

    if validation_error:
        return validation_error
    
    try:
        with get_db_cursor() as (conn, cursor):
            existing_history = _get_existing_recommendation_history(
                cursor,
                user_id,
                base_movie_id,
                recommended_movie_id,
            )

            if existing_history:
                return {
                    "success": False,
                    "message": "이미 추천된 영화입니다.",
                    "duplicated": True
                }
        
            # ======================
            # 추천 이력 저장
            # ======================
            query = """
            INSERT INTO recommendation_history
            (user_id, base_movie_id, recommended_movie_id, similarity)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query, 
                (user_id, base_movie_id, recommended_movie_id, similarity)
            )

            conn.commit()
            history_id = cursor.lastrowid

        return {
            "success": True,
            "message": "추천 이력이 저장되었습니다.",
            "history_id": history_id
        }
    
    except Exception as e:
        logger.exception("추천 이력 저장 오류")

        return {
            "success": False,
            "message": "추천 이력 저장 중 오류가 발생했습니다.",
            "error": str(e)
        }
    

# 추천 이력 조회
def get_recommendations_by_user(user_id):
    query = """
    SELECT
        rh.id,
        rh.user_id,
        rh.base_movie_id,
        rh.recommended_movie_id,
        rh.similarity AS similarity,
        rh.created_at,
        m.title,
        m.genre,
        m.poster_url
    FROM recommendation_history rh
    JOIN movies m
    ON rh.recommended_movie_id = m.id
    WHERE rh.user_id = %s
    ORDER BY rh.created_at DESC
    """

    try:
        with get_db_cursor() as (_, cursor):
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

        return {
            "success": True,
            "recommendations": rows
        }
    
    except Exception as e:
        logger.exception("추천 이력 조회 오류")

        return {
            "success": False,
            "message": "추천 이력 조회 중 오류가 발생했습니다.",
            "error": str(e)
        }


# 추천 이력 삭제
def delete_recommendation_histories(user_id, base_movie_id):

    try:
        with get_db_cursor() as (conn, cursor):
            query = """
            DELETE FROM recommendation_history
            WHERE user_id = %s AND base_movie_id = %s
            """

            cursor.execute(query, (user_id, base_movie_id))
            conn.commit()
    except Exception as e:
        logger.exception("추천 이력 삭제 오류")

        return {
            "success": False,
            "message": "추천 이력 삭제 중 오류가 발생했습니다.",
            "error": str(e)
        }