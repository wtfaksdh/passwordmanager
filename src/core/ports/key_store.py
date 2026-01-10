from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from core.domain.entities.password_entry import PasswordEntry
from core.domain.enums.cipher_type import CipherType
from core.domain.entities.user import User
from core.domain.value_objects.encrypted_password import EncryptedPassword

class KeyStoreService(ABC):
    @abstractmethod
    def store_key(self, user_id: int, key: bytes) -> None:
        raise NotImplementedError
    @abstractmethod
    def get_key(self, user_id: int) -> bytes:
        raise NotImplementedError