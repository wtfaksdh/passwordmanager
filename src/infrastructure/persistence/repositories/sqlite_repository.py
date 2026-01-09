import sqlite3
from typing import List
from core.domain import PasswordEntry, User, EncryptedPassword, CipherType, Email, URL, Category, UserPolicy
from core.ports import PasswordRepository, UserRepository
from core.ports import EncryptionService, KeyDerivationService, KeyStoreService

class SQLitePasswordRepository(PasswordRepository):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
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
        self.conn.commit()

    def add_password(self, entry: PasswordEntry) -> None:
        cursor = self.conn.cursor()
        data = entry.encrypted_password.serialize()
        cursor.execute(
            "INSERT INTO passwords (user_id, name, category, url, password, cipher_type) VALUES (?, ?, ?, ?, ?, ?)",
            (entry.user_id, entry.name, entry.category.value, entry.url.value, data, entry.encrypted_password.cipher_type.value)
        )
        entry.id = cursor.lastrowid
        self.conn.commit()

    def get_password(self, entry_id: int) -> PasswordEntry:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, user_id, name, category, url, password, cipher_type FROM passwords WHERE id = ?", (entry_id,))
        row = cursor.fetchone()
        if not row:
            return None
        id_, user_id, name, category, url, data, cipher_type = row
        cipher_enum = CipherType(cipher_type)
        encrypted = EncryptedPassword.deserialize(data, cipher_enum)
        return PasswordEntry(id=id_, user_id=user_id, name=name, category=Category(category), url=URL(url), encrypted_password=encrypted)

    def update_password(self, entry: PasswordEntry) -> None:
        cursor = self.conn.cursor()
        data = entry.encrypted_password.serialize()
        cursor.execute(
            "UPDATE passwords SET name = ?, category = ?, url = ?, password = ?, cipher_type = ? WHERE id = ?",
            (entry.name, entry.category.value, entry.url.value, data, entry.encrypted_password.cipher_type.value, entry.id)
        )
        self.conn.commit()

    def delete_password(self, entry_id: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        self.conn.commit()

    def list_passwords(self, user_id: int) -> List[PasswordEntry]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, user_id, name, category, url, password, cipher_type FROM passwords WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        entries: List[PasswordEntry] = []
        for row in rows:
            id_, user_id, name, category, url, data, cipher_type = row
            cipher_enum = CipherType(cipher_type)
            encrypted = EncryptedPassword.deserialize(data, cipher_enum)
            entries.append(PasswordEntry(id=id_, user_id=user_id, name=name, category=Category(category), url=URL(url), encrypted_password=encrypted))
        return entries

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            salt BLOB NOT NULL
        );
        """)
        self.conn.commit()

    def get_user(self, user_id: int) -> User:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, email, password_hash, salt FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        id_, username, email, password_hash, salt = row
        return User(id=id_, username=username, email=Email(email), password_hash=password_hash, salt=salt)

    def find_by_username(self, username: str) -> User | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, email, password_hash, salt FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row:
            return None
        id_, username, email, password_hash, salt = row
        return User(id=id_, username=username, email=Email(email), password_hash=password_hash, salt=salt)

    def create_user(self, user: User) -> None:
        UserPolicy.validate(user)
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
            (user.username, user.email.address, user.password_hash, user.salt)
        )
        user.id = cursor.lastrowid
        self.conn.commit()