from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain.entities.password_entry import PasswordEntry
from core.domain.entities.user import User
from core.domain.value_objects.encrypted_password import EncryptedPassword
from core.ports.encryption import EncryptionService
from core.ports.key_store import KeyStoreService
from core.ports.key_derivation import KeyDerivationService
from core.ports.repositories import PasswordRepository, UserRepository
from core.domain.exceptions.password_not_found import PasswordNotFoundError
from core.domain.exceptions.unauthorized import UnauthorizedError
from core.domain.exceptions.weak_password import WeakPasswordError
from core.domain.value_objects.url import URL
from core.domain.value_objects.email import Email
from core.domain.enums.category import Category
from core.domain.enums.cipher_type import CipherType
from core.application.dto.password_input import PasswordInput
from core.application.dto.password_output import PasswordOutput
from core.application.dto.user_context import UserContext
from core.domain.policies.password_policy import PasswordPolicy
from core.domain.policies.user_policy import UserPolicy

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