from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from core.domain import PasswordEntry, User, EncryptedPassword, CipherType

class EncryptionService(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str, key: bytes, cipher_type: CipherType) -> EncryptedPassword:
        raise NotImplementedError
    @abstractmethod
    def decrypt(self, encrypted: EncryptedPassword, key: bytes) -> str:
        raise NotImplementedError