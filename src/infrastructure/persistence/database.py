import sqlite3

def init_db(db_path: str) -> sqlite3.Connection:
    """
    Инициализация SQLite БД и создание таблиц.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Таблица пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        salt BLOB NOT NULL
    );
    """)
    # Таблица паролей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        url TEXT NOT NULL,
        password BLOB NOT NULL,
        cipher_type TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    return conn