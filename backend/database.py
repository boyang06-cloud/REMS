import pymysql
from config import DB_CONFIG

def get_connection():
    try:
        conn=pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None #返回None表示连接失败