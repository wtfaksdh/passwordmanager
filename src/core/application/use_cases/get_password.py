from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain import PasswordEntry, Category, EncryptedPassword, PasswordStrength, PasswordPolicy, UserPolicy, CipherType, Email, URL
from core.ports import PasswordRepository, EncryptionService, KeyStoreService, KeyDerivationService, UserRepository
from core.domain import PasswordNotFoundError, UnauthorizedError, WeakPasswordError
from core.application import UserContext, PasswordInput, PasswordOutput


class GetPassword:
    def __init__(self, password_repo: PasswordRepository, key_store: KeyStoreService, encryption_service: EncryptionService):
        self.password_repo = password_repo
        self.key_store = key_store
        self.encryption_service = encryption_service

    def execute(self, user_context: UserContext, entry_id: int) -> PasswordOutput:
        entry = self.password_repo.get_password(entry_id)
        if not entry:
            raise PasswordNotFoundError(f"Password entry {entry_id} not found.")
        if entry.user_id != user_context.user_id:
            raise UnauthorizedError("Not authorized to access this password.")

        key = self.key_store.get_key(user_context.user_id)
        if key is None:
            raise UnauthorizedError("Encryption key not found for user.")

        plaintext = self.encryption_service.decrypt(entry.encrypted_password, key)
        return PasswordOutput(id=entry.id, name=entry.name, category=entry.category, url=entry.url, password=plaintext)