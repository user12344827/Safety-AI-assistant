import pymysql
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def connect_to_db():
    """連接到資料庫，使用環境變數中的設定"""
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )

def drop_and_create_db():
    """刪除並重新建立資料庫"""
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    
    db_name = os.getenv("DB_NAME")
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    conn.commit()
    conn.close()

def insert_laws(laws_data):
    """將法規資料插入資料庫"""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS laws (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chapter VARCHAR(255),
            article_number VARCHAR(255),
            article_link VARCHAR(255),
            content TEXT
        )
    """)

    for law in laws_data:
        sql = """
            INSERT INTO laws (chapter, article_number, article_link, content)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (
            law['chapter'],
            law['article_number'],
            law['article_link'],
            law['content']
        ))

    conn.commit()
    conn.close()

def show_laws_data():
    """顯示法規資料範例"""
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM laws LIMIT 5")
        results = cur.fetchall()

        for row in results:
            print(f"ID: {row[0]}")
            print(f"Chapter: {row[1]}")
            print(f"Article Number: {row[2]}")
            print(f"Article Link: {row[3]}")
            print(f"Content: {row[4]}")
            print("---")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()