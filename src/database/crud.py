"""CRUD operations for User and Password records"""
import sqlite3
from typing import List, Optional

from src.database.db import Database
from src.database.models import User, Password


class UserRepository:
    """Repository for User CRUD operations"""

    @staticmethod
    def create(db: Database, user: User) -> Optional[int]:
        """
        Create new user.
        
        Args:
            db: Database instance
            user: User object with username and password_hash
            
        Returns:
            User ID if successful, None otherwise
        """
        try:
            cursor = db.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (user.username, user.password_hash),
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            db.rollback()
            return None
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error creating user: {e}")
            return None

    @staticmethod
    def get_by_username(db: Database, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            db: Database instance
            username: Username to search
            
        Returns:
            User object if found, None otherwise
        """
        try:
            cursor = db.execute(
                "SELECT id, username, password_hash, created_at, updated_at FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            if row:
                return User(
                    id=row["id"],
                    username=row["username"],
                    password_hash=row["password_hash"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
            return None
        except sqlite3.Error as e:
            print(f"Database error getting user: {e}")
            return None

    @staticmethod
    def get_by_id(db: Database, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database instance
            user_id: User ID to search
            
        Returns:
            User object if found, None otherwise
        """
        try:
            cursor = db.execute(
                "SELECT id, username, password_hash, created_at, updated_at FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            if row:
                return User(
                    id=row["id"],
                    username=row["username"],
                    password_hash=row["password_hash"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
            return None
        except sqlite3.Error as e:
            print(f"Database error getting user by id: {e}")
            return None

    @staticmethod
    def delete(db: Database, user_id: int) -> bool:
        """
        Delete user.
        
        Args:
            db: Database instance
            user_id: User ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            db.commit()
            return True
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error deleting user: {e}")
            return False


class PasswordRepository:
    """Repository for Password record CRUD operations"""

    @staticmethod
    def create(db: Database, password: Password) -> Optional[int]:
        """
        Create new password record.
        
        Args:
            db: Database instance
            password: Password object
            
        Returns:
            Password ID if successful, None otherwise
        """
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
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error creating password: {e}")
            return None

    @staticmethod
    def get_by_id(db: Database, password_id: int) -> Optional[Password]:
        """
        Get password record by ID.
        
        Args:
            db: Database instance
            password_id: Password ID to search
            
        Returns:
            Password object if found, None otherwise
        """
        try:
            cursor = db.execute(
                "SELECT id, user_id, service, login, password, created_at, updated_at FROM passwords WHERE id = ?",
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
        except sqlite3.Error as e:
            print(f"Database error getting password: {e}")
            return None

    @staticmethod
    def get_by_user(db: Database, user_id: int) -> List[Password]:
        """
        Get all passwords for a user.
        
        Args:
            db: Database instance
            user_id: User ID to search
            
        Returns:
            List of Password objects
        """
        try:
            cursor = db.execute(
                "SELECT id, user_id, service, login, password, created_at, updated_at FROM passwords WHERE user_id = ? ORDER BY service",
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
        except sqlite3.Error as e:
            print(f"Database error getting user passwords: {e}")
            return []

    @staticmethod
    def update(db: Database, password: Password) -> bool:
        """
        Update password record.
        
        Args:
            db: Database instance
            password: Password object with updated values
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db.execute(
                """
                UPDATE passwords 
                SET service = ?, login = ?, password = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
                """,
                (password.service, password.login, password.password, password.id),
            )
            db.commit()
            return True
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error updating password: {e}")
            return False

    @staticmethod
    def delete(db: Database, password_id: int) -> bool:
        """
        Delete password record.
        
        Args:
            db: Database instance
            password_id: Password ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
            db.commit()
            return True
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error deleting password: {e}")
            return False

    @staticmethod
    def delete_all_for_user(db: Database, user_id: int) -> bool:
        """
        Delete all passwords for a user.
        
        Args:
            db: Database instance
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db.execute("DELETE FROM passwords WHERE user_id = ?", (user_id,))
            db.commit()
            return True
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error deleting user passwords: {e}")
            return False
