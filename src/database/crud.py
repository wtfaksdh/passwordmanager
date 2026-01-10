"""CRUD operations for Password Manager"""
import sqlite3
from typing import List, Optional

from src.database.db import Database
from src.database.models import User, Password


class UserCRUD:
    """CRUD operations for User"""

    @staticmethod
    def create(db: Database, user: User) -> Optional[int]:
        """Create new user"""
        try:
            cursor = db.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (user.username, user.password),
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            db.rollback()
            return None

    @staticmethod
    def get_by_username(db: Database, username: str) -> Optional[User]:
        """Get user by username"""
        cursor = db.execute(
            "SELECT id, username, password, created_at, updated_at FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                username=row["username"],
                password=row["password"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        return None

    @staticmethod
    def get_by_id(db: Database, user_id: int) -> Optional[User]:
        """Get user by id"""
        cursor = db.execute(
            "SELECT id, username, password, created_at, updated_at FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                username=row["username"],
                password=row["password"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        return None

    @staticmethod
    def verify_password(db: Database, username: str, password: str) -> Optional[User]:
        """Verify user credentials"""
        user = UserCRUD.get_by_username(db, username)
        if user and user.password == password:
            return user
        return None

    @staticmethod
    def delete(db: Database, user_id: int) -> bool:
        """Delete user"""
        try:
            db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            db.commit()
            return True
        except sqlite3.Error:
            db.rollback()
            return False


class PasswordCRUD:
    """CRUD operations for Password records"""

    @staticmethod
    def create(db: Database, password: Password) -> Optional[int]:
        """Create new password record"""
        try:
            cursor = db.execute(
                """
                INSERT INTO passwords (user_id, service, login, password)
                VALUES (?, ?, ?, ?)
                """,
                (password.user_id, password.service, password.login, password.password),
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            db.rollback()
            return None

    @staticmethod
    def get_by_id(db: Database, password_id: int) -> Optional[Password]:
        """Get password record by id"""
        cursor = db.execute(
            """
            SELECT id, user_id, service, login, password, created_at, updated_at
            FROM passwords WHERE id = ?
            """,
            (password_id,),
        )
        row = cursor.fetchone()
        if row:
            return Password(
                id=row["id"],
                user_id=row["user_id"],
                service=row["service"],
                login=row["login"],
                password=row["password"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        return None

    @staticmethod
    def get_by_user_id(db: Database, user_id: int) -> List[Password]:
        """Get all password records for user"""
        cursor = db.execute(
            """
            SELECT id, user_id, service, login, password, created_at, updated_at
            FROM passwords WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        return [
            Password(
                id=row["id"],
                user_id=row["user_id"],
                service=row["service"],
                login=row["login"],
                password=row["password"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    @staticmethod
    def update(db: Database, password_id: int, **kwargs) -> bool:
        """Update password record"""
        try:
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ["service", "login", "password"]:
                    fields.append(f"{key} = ?")
                    values.append(value)

            if not fields:
                return False

            fields.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE passwords SET {', '.join(fields)} WHERE id = ?"
            values.append(password_id)

            db.execute(query, tuple(values))
            db.commit()
            return True

        except sqlite3.Error:
            db.rollback()
            return False

    @staticmethod
    def delete(db: Database, password_id: int) -> bool:
        """Delete password record"""
        try:
            db.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
            db.commit()
            return True
        except sqlite3.Error:
            db.rollback()
            return False

    @staticmethod
    def delete_by_user_id(db: Database, user_id: int) -> bool:
        """Delete all password records for user"""
        try:
            db.execute("DELETE FROM passwords WHERE user_id = ?", (user_id,))
            db.commit()
            return True
        except sqlite3.Error:
            db.rollback()
            return False
