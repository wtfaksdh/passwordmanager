"""Validators for user input"""
import re
from typing import Tuple


class Validators:
    """Input validation utilities"""
    
    MIN_USERNAME_LENGTH = 3
    MIN_PASSWORD_LENGTH = 4
    MIN_SERVICE_LENGTH = 2
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username.
        
        Args:
            username: Username to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        username = username.strip()
        
        if len(username) < Validators.MIN_USERNAME_LENGTH:
            return False, f"Имя пользователя должно содержать минимум {Validators.MIN_USERNAME_LENGTH} символа"
        
        if len(username) > 50:
            return False, "Имя пользователя не может быть длиннее 50 символов"
        
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            return False, "Имя пользователя может содержать только буквы, цифры, - и _"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        password = password.strip()
        
        if len(password) < Validators.MIN_PASSWORD_LENGTH:
            return False, f"Пароль должен содержать минимум {Validators.MIN_PASSWORD_LENGTH} символа"
        
        if len(password) > 255:
            return False, "Пароль не может быть длиннее 255 символов"
        
        return True, ""
    
    @staticmethod
    def validate_service(service: str) -> Tuple[bool, str]:
        """
        Validate service name.
        
        Args:
            service: Service name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        service = service.strip()
        
        if len(service) < Validators.MIN_SERVICE_LENGTH:
            return False, f"Название сервиса должно содержать минимум {Validators.MIN_SERVICE_LENGTH} символа"
        
        if len(service) > 100:
            return False, "Название сервиса не может быть длиннее 100 символов"
        
        return True, ""
    
    @staticmethod
    def validate_login(login: str) -> Tuple[bool, str]:
        """
        Validate login.
        
        Args:
            login: Login to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        login = login.strip()
        
        if len(login) < 1:
            return False, "Логин не может быть пустым"
        
        if len(login) > 100:
            return False, "Логин не может быть длиннее 100 символов"
        
        return True, ""
