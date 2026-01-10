from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re
from core.domain.value_objects.email import Email


@dataclass
class User:
    id: int | None
    username: str
    email: Email
    password_hash: str
    salt: bytes = field(default_factory=bytes)