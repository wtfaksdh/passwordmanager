from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from core.domain import PasswordEntry, User, EncryptedPassword, CipherType

class KeyStoreService(ABC):
    @abstractmethod
    def store_key(self, user_id: int, key: bytes) -> None:
        raise NotImplementedError
    @abstractmethod
    def get_key(self, user_id: int) -> bytes:
        raise NotImplementedError