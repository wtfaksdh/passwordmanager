from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

@dataclass(frozen=True)
class Email:
    address: str

    def __post_init__(self):
        # Простая проверка email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.address):
            raise ValueError(f"Invalid email address: {self.address}")