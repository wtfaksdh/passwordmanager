from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from core.domain.entities.password_entry import PasswordEntry
from core.domain.entities.user import User
from core.domain.value_objects.encrypted_password import EncryptedPassword
from core.domain.enums.cipher_type import CipherType


class EncryptionService(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str, key: bytes, cipher_type: CipherType) -> EncryptedPassword:
        raise NotImplementedError
    @abstractmethod
    def decrypt(self, encrypted: EncryptedPassword, key: bytes) -> str:
        raise NotImplementedError
