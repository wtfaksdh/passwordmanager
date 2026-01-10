from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from core.domain.entities.password_entry import PasswordEntry
from core.domain.entities.user import User
from core.domain.value_objects.encrypted_password import EncryptedPassword
from core.domain.enums.cipher_type import CipherType

class PasswordRepository(ABC):
    @abstractmethod
    def add_password(self, entry: PasswordEntry) -> None:
        raise NotImplementedError
    @abstractmethod
    def get_password(self, entry_id: int) -> PasswordEntry:
        raise NotImplementedError
    @abstractmethod
    def update_password(self, entry: PasswordEntry) -> None:
        raise NotImplementedError
    @abstractmethod
    def delete_password(self, entry_id: int) -> None:
        raise NotImplementedError
    @abstractmethod
    def list_passwords(self, user_id: int) -> List[PasswordEntry]:
        raise NotImplementedError

class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> User:
        raise NotImplementedError
    @abstractmethod
    def find_by_username(self, username: str) -> User | None:
        raise NotImplementedError
    @abstractmethod
    def create_user(self, user: User) -> None:
        raise NotImplementedError    @abstractmethod
    def exists(self, user_id: int) -> bool:
        raise NotImplementedError