from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain.entities.password_entry import Category
from core.domain.value_objects.url import URL

@dataclass
class PasswordOutput:
    id: int
    name: str
    category: Category
    url: URL
    password: str  # расшифрованный пароль (при выводе)