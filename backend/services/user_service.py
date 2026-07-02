from utils.db_utils import get_db_cursor

from core.security import hash_password, is_password_hashed, verify_password


def get_user_by_email(email):
    
    query = """
    SELECT id, username, email, password, created_at
    FROM users
    WHERE email = %s
    """
        
    with get_db_cursor() as (_, cursor):
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
    return user
    

def update_user_password(user_id, password):
    query = """
    UPDATE users
    SET password = %s
    WHERE id = %s
    """

    with get_db_cursor() as (conn, cursor):
        cursor.execute(query, (password, user_id))
        conn.commit()

        
def create_user(username, email, password):
    
    try:
        existing_user = get_user_by_email(email)
        
        if existing_user:
            return {
                "success": False,
                "message": "이미 가입된 이메일입니다."
            }
        
        hashed_password = hash_password(password)

        with get_db_cursor() as (conn, cursor):
            query = """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
            """
            
            cursor.execute(
                query, (username, email, hashed_password)
            )
            
            conn.commit()
        
        return {
            "success": True,
            "message": "회원가입이 완료되었습니다."
        }
        
    except Exception as e:
        
        return {
            "success": False,
            "message": "회원가입 중 오류가 발생했습니다.",
            "error": str(e)
        }
        
        
def login_user(email, password):
    user = get_user_by_email(email)
    
    if not user:
        
        return {
            "success": False,
            "message": "가입되지 않은 이메일입니다."
        }
        
    if not verify_password(password, user["password"]):
        
        return {
            "success": False,
            "message": "비밀번호가 올바르지 않습니다."
        }
    
    if not is_password_hashed(user["password"]):
        update_user_password(
            user_id=user["id"],
            password=hash_password(password),
        )
        
    return {
        "success": True,
        "message": "로그인 성공",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    }