from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from core.domain.enums.cipher_type import CipherType
from core.domain.value_objects.url import URL
from core.domain.entities.password_entry import Category

@dataclass
class PasswordInput:
    name: str
    category: Category
    url: URL
    password: str
    cipher_type: CipherType