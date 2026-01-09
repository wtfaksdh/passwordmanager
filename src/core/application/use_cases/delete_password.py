from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain import PasswordEntry, Category, EncryptedPassword, PasswordStrength, PasswordPolicy, UserPolicy, CipherType, Email, URL
from core.ports import PasswordRepository, EncryptionService, KeyStoreService, KeyDerivationService, UserRepository
from core.domain import PasswordNotFoundError, UnauthorizedError, WeakPasswordError
from core.application import UserContext, PasswordInput, PasswordOutput


class DeletePassword:
    def __init__(self, password_repo: PasswordRepository):
        self.password_repo = password_repo

    def execute(self, user_context: UserContext, entry_id: int) -> None:
        entry = self.password_repo.get_password(entry_id)
        if not entry:
            raise PasswordNotFoundError(f"Password entry {entry_id} not found.")
        if entry.user_id != user_context.user_id:
            raise UnauthorizedError("Not authorized to delete this password.")
        self.password_repo.delete_password(entry_id)