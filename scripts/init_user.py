import sqlite3
from pathlib import Path
import keyring
from getpass import getpass
from datetime import datetime


DB_PATH = Path(__file__).parent.parent / "password_manager.db"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash BLOB NOT NULL,
    created_at TEXT NOT NULL
)
""")
conn.commit()


username = input("Введите имя пользователя для бота: ")
password = getpass("Введите мастер-пароль: ").encode()


keyring.set_password("passwordmanager", username, password.decode())


cursor.execute(
    "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
    (username, password, datetime.now().isoformat())
)
conn.commit()
conn.close()

print("Пользователь создан, база готова!")
