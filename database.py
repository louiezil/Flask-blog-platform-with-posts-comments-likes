

import sqlite3


def conn_cursor():
    try:
        conn = sqlite3.connect("main.db", check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        return conn, cursor
    except sqlite3.Error as e:
        print(f"error with connection :{e}")
        return None, None


def create_tables(conn, cursor):
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    email TEXT UNIQUE,
                    password TEXT,
                    bio TEXT,
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                    
                )
                """)
        
        
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT 
                
            )
            """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS posts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_id INTEGER,
                    title TEXT,
                    content TEXT,
                    image TEXT,
                    category_id INTEGER ,
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  ,
                    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE ,             
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL               
                    )
                    """)

        cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS comments
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    user_id INTEGER,
    content TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        post_id INTEGER,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE (post_id,user_id)
        
        )
        """)

      
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"error creating tables : {e}")
        return False


def close_conn(conn):
    if conn:
        conn.close()
        return True
    return False


if __name__ == "__main__":
    conn, cursor = conn_cursor()
    if create_tables(conn, cursor):
        print("tables created")

    if close_conn(conn):
        print("connection closed")
