from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from core.domain import PasswordEntry, User, EncryptedPassword, CipherType

class KeyDerivationService(ABC):
    @abstractmethod
    def derive_key(self, password: str, salt: bytes) -> bytes:
        raise NotImplementedError