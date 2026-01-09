from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re
from core.domain.enums.category import Category
from core.domain.value_objects.url import URL
from core.domain.value_objects.encrypted_password import EncryptedPassword


@dataclass
class PasswordEntry:
    id: int | None
    user_id: int
    name: str
    category: Category
    url: URL
    encrypted_password: EncryptedPassword
