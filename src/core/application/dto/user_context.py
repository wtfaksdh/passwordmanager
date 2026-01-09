from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain import PasswordEntry, Category, EncryptedPassword, PasswordStrength, PasswordPolicy, UserPolicy, CipherType, Email, URL
from core.ports import PasswordRepository, EncryptionService, KeyStoreService, KeyDerivationService, UserRepository
from core.domain import PasswordNotFoundError, UnauthorizedError, WeakPasswordError

@dataclass
class UserContext:
    user_id: int