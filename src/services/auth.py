"""User authentication service"""
from src.database.db import Database
from src.database.models import User
from src.database.crud import UserRepository
from src.security import EncryptionService


class AuthenticationService:
    """Service for user authentication with encrypted passwords"""

    @staticmethod
    def register_user(db: Database, username: str, password: str) -> tuple[bool, str]:
        """
        Register new user with encrypted password.
        
        Args:
            db: Database instance
            username: Username
            password: Plain text password
            
        Returns:
            Tuple of (success: bool, message: str)
        """
      
        existing_user = UserRepository.get_by_username(db, username)
        if existing_user:
            return False, "Пользователь с таким именем уже существует"
        
       
        try:
            password_hash = EncryptionService.encrypt_password(password, username)
        except Exception as e:
            return False, f"Ошибка при шифровании пароля: {str(e)}"
        
       
        user = User(username=username, password_hash=password_hash)
        user_id = UserRepository.create(db, user)
        
        if user_id:
            return True, f"Пользователь {username} успешно зарегистрирован"
        else:
            return False, "Ошибка при создании пользователя"

    @staticmethod
    def authenticate_user(db: Database, username: str, password: str) -> tuple[bool, str, int]:
        """
        Authenticate user with username and password.
        
        Args:
            db: Database instance
            username: Username
            password: Plain text password
            
        Returns:
            Tuple of (success: bool, message: str, user_id: int)
        """
      
        user = UserRepository.get_by_username(db, username)
        if not user:
            return False, "Пользователь не найден", 0
        
       
        try:
            decrypted_password = EncryptionService.decrypt_password(
                user.password_hash, username
            )
            if decrypted_password == password:
                return True, "Успешная аутентификация", user.id
            else:
                return False, "Неверный пароль", 0
        except Exception as e:
            return False, f"Ошибка при проверке пароля: {str(e)}", 0
