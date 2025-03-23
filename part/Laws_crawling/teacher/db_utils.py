import pymysql

def connect_to_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="ntC1234#31#",
        db="workshop_law"
    )

def drop_and_create_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="ntC1234#31#"
    )
    cur = conn.cursor()

    cur.execute("DROP DATABASE IF EXISTS workshop_law")
    cur.execute("CREATE DATABASE workshop_law")
    conn.commit()
    conn.close()

def insert_laws(laws_data):
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
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="ntC1234#31#",
            db="workshop_law"
        )
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
        if conn:
            conn.close()