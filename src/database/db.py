"""Database connection and initialization"""
import sqlite3
from pathlib import Path
from typing import Optional


class Database:
    """SQLite3 Database manager"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Connect to database"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row

    def disconnect(self) -> None:
        """Disconnect from database"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute query"""
        if not self.connection:
            self.connect()
        return self.connection.execute(query, params)

    def commit(self) -> None:
        """Commit changes"""
        if self.connection:
            self.connection.commit()

    def rollback(self) -> None:
        """Rollback changes"""
        if self.connection:
            self.connection.rollback()

    def close(self) -> None:
        """Close connection"""
        self.disconnect()


class DatabaseInitializer:
    """Database initialization utility"""
    
    @staticmethod
    def init_db(db_path: Path) -> None:
        """
        Initialize database with tables.
        
        Args:
            db_path: Path to database file
        """
        db = Database(db_path)
        db.connect()

        try:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            db.execute(
                """
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    service TEXT NOT NULL,
                    login TEXT NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
                """
            )

            db.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)
                """
            )

            db.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_passwords_user_id ON passwords(user_id)
                """
            )

            db.commit()
            print(f"✓ Database initialized at {db_path}")

        except sqlite3.Error as e:
            db.rollback()
            print(f"✗ Database initialization error: {e}")
            raise
        finally:
            db.close()
