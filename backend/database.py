import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="cinefeel",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )