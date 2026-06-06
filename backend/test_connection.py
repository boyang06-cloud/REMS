from database import get_connection

conn=get_connection()
try:
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM experiment")
    print(cursor.fetchall())
    print("Connection successful")
except Exception as e:
    print(f"Error connecting to database: {e}")
finally:
    conn.close()