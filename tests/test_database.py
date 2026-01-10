"""Tests for database operations"""
import pytest
import sqlite3
import tempfile
from pathlib import Path

from src.database.db import Database, DatabaseInitializer
from src.database.crud import UserRepository, PasswordRepository
from src.database.models import User, Password


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        DatabaseInitializer.init_db(db_path)
        yield db_path
        if db_path.exists():
            db_path.unlink()


@pytest.fixture
def db_connection(temp_db):
    """Create database connection"""
    db = Database(temp_db)
    db.connect()
    yield db
    db.disconnect()


class TestUserRepository:
    """Test User CRUD operations"""

    def test_create_user(self, db_connection):
        """Test user creation"""
        user = User(username="testuser", password_hash="hashed_password123")
        user_id = UserRepository.create(db_connection, user)

        assert user_id is not None
        assert isinstance(user_id, int)

    def test_duplicate_username(self, db_connection):
        """Test duplicate username"""
        user1 = User(username="testuser", password_hash="hashed_password123")
        user2 = User(username="testuser", password_hash="hashed_password456")

        UserRepository.create(db_connection, user1)
        user_id_2 = UserRepository.create(db_connection, user2)

        assert user_id_2 is None

    def test_get_user_by_username(self, db_connection):
        """Test get user by username"""
        user = User(username="testuser", password_hash="hashed_password123")
        UserRepository.create(db_connection, user)

        retrieved_user = UserRepository.get_by_username(db_connection, "testuser")
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"

    def test_get_user_not_found(self, db_connection):
        """Test get non-existent user"""
        user = UserRepository.get_by_username(db_connection, "nonexistent")
        assert user is None

    def test_get_user_by_id(self, db_connection):
        """Test get user by ID"""
        user = User(username="testuser", password_hash="hashed_password123")
        user_id = UserRepository.create(db_connection, user)

        retrieved_user = UserRepository.get_by_id(db_connection, user_id)
        assert retrieved_user is not None
        assert retrieved_user.id == user_id
        assert retrieved_user.username == "testuser"

    def test_delete_user(self, db_connection):
        """Test user deletion"""
        user = User(username="testuser", password_hash="hashed_password123")
        user_id = UserRepository.create(db_connection, user)

        success = UserRepository.delete(db_connection, user_id)
        assert success is True

        deleted_user = UserRepository.get_by_id(db_connection, user_id)
        assert deleted_user is None


class TestPasswordRepository:
    """Test Password CRUD operations"""

    @pytest.fixture
    def user_id(self, db_connection):
        """Create user for password tests"""
        user = User(username="testuser", password_hash="hashed_password123")
        return UserRepository.create(db_connection, user)

    def test_create_password(self, db_connection, user_id):
        """Test password creation"""
        password = Password(
            user_id=user_id,
            service="Gmail",
            login="user@gmail.com",
            password="secret123"
        )
        pwd_id = PasswordRepository.create(db_connection, password)

        assert pwd_id is not None
        assert isinstance(pwd_id, int)

    def test_get_password_by_id(self, db_connection, user_id):
        """Test get password by id"""
        password = Password(
            user_id=user_id,
            service="Gmail",
            login="user@gmail.com",
            password="secret123"
        )
        pwd_id = PasswordRepository.create(db_connection, password)

        retrieved = PasswordRepository.get_by_id(db_connection, pwd_id)
        assert retrieved is not None
        assert retrieved.service == "Gmail"
        assert retrieved.login == "user@gmail.com"

    def test_get_passwords_by_user_id(self, db_connection, user_id):
        """Test get all passwords for user"""
        pwd1 = Password(
            user_id=user_id,
            service="Gmail",
            login="user@gmail.com",
            password="secret123"
        )
        pwd2 = Password(
            user_id=user_id,
            service="GitHub",
            login="username",
            password="secret456"
        )

        PasswordRepository.create(db_connection, pwd1)
        PasswordRepository.create(db_connection, pwd2)

        passwords = PasswordRepository.get_by_user(db_connection, user_id)
        assert len(passwords) == 2
        assert passwords[0].service in ["Gmail", "GitHub"]

    def test_update_password(self, db_connection, user_id):
        """Test password update"""
        password = Password(
            user_id=user_id,
            service="Gmail",
            login="user@gmail.com",
            password="secret123"
        )
        pwd_id = PasswordRepository.create(db_connection, password)

        # Update password
        updated_password = Password(
            id=pwd_id,
            user_id=user_id,
            service="Gmail",
            login="user@gmail.com",
            password="newsecret456"
        )
        success = PasswordRepository.update(db_connection, updated_password)
        assert success is True

        updated = PasswordRepository.get_by_id(db_connection, pwd_id)
        assert updated.password == "newsecret456"

    def test_delete_password(self, db_connection, user_id):
        """Test password deletion"""
        password = Password(
            user_id=user_id,
            service="Gmail",
            login="user@gmail.com",
            password="secret123"
        )
        pwd_id = PasswordRepository.create(db_connection, password)

        success = PasswordRepository.delete(db_connection, pwd_id)
        assert success is True

        deleted = PasswordRepository.get_by_id(db_connection, pwd_id)
        assert deleted is None

    def test_delete_all_for_user(self, db_connection, user_id):
        """Test delete all passwords for user"""
        pwd1 = Password(
            user_id=user_id,
            service="Gmail",
            login="user@gmail.com",
            password="secret123"
        )
        pwd2 = Password(
            user_id=user_id,
            service="GitHub",
            login="username",
            password="secret456"
        )

        PasswordRepository.create(db_connection, pwd1)
        PasswordRepository.create(db_connection, pwd2)

        success = PasswordRepository.delete_all_for_user(db_connection, user_id)
        assert success is True

        passwords = PasswordRepository.get_by_user(db_connection, user_id)
        assert len(passwords) == 0
