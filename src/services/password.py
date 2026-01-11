"""Password management service"""
from typing import List

from src.database.db import Database
from src.database.models import Password
from src.database.crud import PasswordRepository
from src.security import EncryptionService


class PasswordService:
    """Service for managing encrypted passwords"""

    @staticmethod
    def create_password(
        db: Database,
        user_id: int,
        service: str,
        login: str,
        password: str,
        master_password: str,
    ) -> tuple[bool, str]:
        """
        Create new password record with encryption.
        
        Args:
            db: Database instance
            user_id: User ID
            service: Service name
            login: Login for service
            password: Plain text password
            master_password: User's master password for encryption
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:

            encrypted_password = EncryptionService.encrypt_password(
                password, master_password
            )
            

            pwd = Password(
                user_id=user_id,
                service=service,
                login=login,
                password=encrypted_password,
            )
            
            pwd_id = PasswordRepository.create(db, pwd)
            if pwd_id:
                return True, f"Пароль для {service} успешно сохранён"
            else:
                return False, "Ошибка при сохранении пароля"
        except Exception as e:
            return False, f"Ошибка при создании пароля: {str(e)}"

    @staticmethod
    def get_user_passwords(
        db: Database, user_id: int, master_password: str
    ) -> tuple[bool, List[dict], str]:
        """
        Get all passwords for user with decryption.
        
        Args:
            db: Database instance
            user_id: User ID
            master_password: User's master password for decryption
            
        Returns:
            Tuple of (success: bool, passwords_list: List[dict], message: str)
        """
        try:
            passwords = PasswordRepository.get_by_user(db, user_id)
            
            decrypted_passwords = []
            for pwd in passwords:
                try:
                    decrypted_text = EncryptionService.decrypt_password(
                        pwd.password, master_password
                    )
                    decrypted_passwords.append(
                        {
                            "id": pwd.id,
                            "service": pwd.service,
                            "login": pwd.login,
                            "password": decrypted_text,
                            "created_at": pwd.created_at,
                        }
                    )
                except Exception:

                    continue
            
            return True, decrypted_passwords, ""
        except Exception as e:
            return False, [], f"Ошибка при получении паролей: {str(e)}"

    @staticmethod
    def update_password(
        db: Database,
        password_id: int,
        service: str,
        login: str,
        new_password: str,
        master_password: str,
    ) -> tuple[bool, str]:
        """
        Update password record with encryption.
        
        Args:
            db: Database instance
            password_id: Password record ID
            service: Service name
            login: Login for service
            new_password: New plain text password
            master_password: User's master password for encryption
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Encrypt new password
            encrypted_password = EncryptionService.encrypt_password(
                new_password, master_password
            )
            
            # Update password record
            pwd = Password(
                id=password_id,
                service=service,
                login=login,
                password=encrypted_password,
            )
            
            success = PasswordRepository.update(db, pwd)
            if success:
                return True, f"Пароль для {service} успешно обновлён"
            else:
                return False, "Ошибка при обновлении пароля"
        except Exception as e:
            return False, f"Ошибка при обновлении пароля: {str(e)}"

    @staticmethod
    def delete_password(db: Database, password_id: int) -> tuple[bool, str]:
        """
        Delete password record.
        
        Args:
            db: Database instance
            password_id: Password record ID
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            success = PasswordRepository.delete(db, password_id)
            if success:
                return True, "Пароль успешно удалён"
            else:
                return False, "Ошибка при удалении пароля"
        except Exception as e:
            return False, f"Ошибка при удалении пароля: {str(e)}"
