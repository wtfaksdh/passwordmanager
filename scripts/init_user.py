import sqlite3
from pathlib import Path
import keyring
from getpass import getpass
from datetime import datetime

# Путь к базе
DB_PATH = Path(__file__).parent.parent / "password_manager.db"

# Создаём базу и таблицу пользователей, если не существует
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

# Запрашиваем данные пользователя
username = input("Введите имя пользователя для бота: ")
password = getpass("Введите мастер-пароль: ").encode()

# Сохраняем пароль в keyring
keyring.set_password("passwordmanager", username, password.decode())

# Вставляем пользователя в базу
cursor.execute(
    "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
    (username, password, datetime.now().isoformat())
)
conn.commit()
conn.close()

print("Пользователь создан, база готова!")
