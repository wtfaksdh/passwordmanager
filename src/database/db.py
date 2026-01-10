"""Database initialization and connection"""
import sqlite3
from pathlib import Path
from typing import Optional

from src.config import DB_PATH
from src.database.models import User, Password


class Database:
    """SQLite3 Database manager"""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Connect to database"""
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


def init_db(db_path: Path = DB_PATH) -> None:
    """Initialize database with tables"""
    db = Database(db_path)
    db.connect()

    try:
        # Create users table
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Create passwords table
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

        # Create index on username for faster lookups
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)
            """
        )

        # Create index on user_id for passwords table
        db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_passwords_user_id ON passwords(user_id)
            """
        )

        db.commit()
        print(f"Database initialized at {db_path}")

    except sqlite3.Error as e:
        db.rollback()
        print(f"Database initialization error: {e}")
        raise

    finally:
        db.disconnect()
