from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain import PasswordEntry, Category, EncryptedPassword, PasswordStrength, PasswordPolicy, UserPolicy, CipherType, Email, URL
from core.ports import PasswordRepository, EncryptionService, KeyStoreService, KeyDerivationService, UserRepository
from core.domain import PasswordNotFoundError, UnauthorizedError, WeakPasswordError
from core.application import UserContext, PasswordInput, PasswordOutput


class UpdatePassword:
    def __init__(self, password_repo: PasswordRepository, encryption_service: EncryptionService, key_store: KeyStoreService):
        self.password_repo = password_repo
        self.encryption_service = encryption_service
        self.key_store = key_store

    def execute(self, user_context: UserContext, entry_id: int, new_input: PasswordInput) -> PasswordOutput:
        entry = self.password_repo.get_password(entry_id)
        if not entry:
            raise PasswordNotFoundError(f"Password entry {entry_id} not found.")
        if entry.user_id != user_context.user_id:
            raise UnauthorizedError("Not authorized to update this password.")

        PasswordPolicy.validate(new_input.password)
        key = self.key_store.get_key(user_context.user_id)
        if key is None:
            raise UnauthorizedError("Encryption key not found for user.")

        encrypted = self.encryption_service.encrypt(new_input.password, key, new_input.cipher_type)
        entry.name = new_input.name
        entry.category = new_input.category
        entry.url = new_input.url
        entry.encrypted_password = encrypted

        self.password_repo.update_password(entry)
        return PasswordOutput(id=entry.id, name=entry.name, category=entry.category, url=entry.url, password=new_input.password)