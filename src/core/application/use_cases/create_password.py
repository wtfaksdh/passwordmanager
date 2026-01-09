from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain import PasswordEntry, Category, EncryptedPassword, PasswordStrength, PasswordPolicy, UserPolicy, CipherType, Email, URL
from core.ports import PasswordRepository, EncryptionService, KeyStoreService, KeyDerivationService, UserRepository
from core.domain import PasswordNotFoundError, UnauthorizedError, WeakPasswordError
from core.application import UserContext, PasswordInput, PasswordOutput

class CreatePassword:
    def __init__(self, password_repo: PasswordRepository, user_repo: UserRepository,
                 encryption_service: EncryptionService, key_store: KeyStoreService):
        self.password_repo = password_repo
        self.user_repo = user_repo
        self.encryption_service = encryption_service
        self.key_store = key_store

    def execute(self, user_context: UserContext, pwd_input: PasswordInput) -> PasswordOutput:
        # Проверяем существование пользователя
        user = self.user_repo.get_user(user_context.user_id)
        if not user:
            raise UnauthorizedError("User not found.")

        # Проверяем сложность пароля
        PasswordPolicy.validate(pwd_input.password)

        # Получаем ключ шифрования из хранилища
        key = self.key_store.get_key(user_context.user_id)
        if key is None:
            raise UnauthorizedError("Encryption key not found for user.")

        # Шифруем пароль
        encrypted = self.encryption_service.encrypt(pwd_input.password, key, pwd_input.cipher_type)

        # Создаём запись и сохраняем
        entry = PasswordEntry(
            id=None,
            user_id=user.id,
            name=pwd_input.name,
            category=pwd_input.category,
            url=pwd_input.url,
            encrypted_password=encrypted
        )
        self.password_repo.add_password(entry)

        return PasswordOutput(
            id=entry.id, name=entry.name, category=entry.category, url=entry.url, password=pwd_input.password)