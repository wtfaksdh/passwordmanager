"""Password encryption and decryption module"""
import os
from typing import Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


class EncryptionService:
    """Service for encrypting and decrypting passwords"""
    
    SALT_LENGTH = 16
    
    @staticmethod
    def derive_key(master_password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from master password using PBKDF2.
        
        Args:
            master_password: The master password string
            salt: Salt bytes for key derivation
            
        Returns:
            URL-safe base64 encoded encryption key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key
    
    @staticmethod
    def encrypt_password(password: str, master_password: str) -> str:
        """
        Encrypt password with master password.
        
        Args:
            password: Password to encrypt
            master_password: Master password for encryption
            
        Returns:
            Encrypted password with salt (format: salt:encrypted)
        """

        salt = os.urandom(EncryptionService.SALT_LENGTH)
        
        key = EncryptionService.derive_key(master_password, salt)
        
        cipher = Fernet(key)
        encrypted = cipher.encrypt(password.encode())
        
        salt_b64 = base64.b64encode(salt).decode()
        encrypted_b64 = encrypted.decode()
        
        return f"{salt_b64}:{encrypted_b64}"
    
    @staticmethod
    def decrypt_password(encrypted_data: str, master_password: str) -> str:
        """
        Decrypt password with master password.
        
        Args:
            encrypted_data: Encrypted password data (format: salt:encrypted)
            master_password: Master password for decryption
            
        Returns:
            Decrypted password
            
        Raises:
            ValueError: If decryption fails or data format is invalid
        """
        try:
            
            parts = encrypted_data.split(":", 1)
            if len(parts) != 2:
                raise ValueError("Invalid encrypted data format")
            
            salt_b64, encrypted_b64 = parts
            

            salt = base64.b64decode(salt_b64)
            
   
            key = EncryptionService.derive_key(master_password, salt)
            

            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_b64.encode())
            
            return decrypted.decode()
        
        except Exception as e:
            raise ValueError(f"Failed to decrypt password: {str(e)}")
