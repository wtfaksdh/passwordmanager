from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from core.domain.entities.password_entry import PasswordEntry
from core.domain.enums.cipher_type import CipherType
from core.domain.value_objects.encrypted_password import EncryptedPassword
from core.domain.entities.user import User

class KeyDerivationService(ABC):
    @abstractmethod
    def derive_key(self, password: str, salt: bytes) -> bytes:
        raise NotImplementedError