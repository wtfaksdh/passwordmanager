from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re
from enums import Category
from value_objects import URL, EncryptedPassword

@dataclass
class PasswordEntry:
    id: int | None
    user_id: int
    name: str
    category: Category
    url: URL
    encrypted_password: EncryptedPassword