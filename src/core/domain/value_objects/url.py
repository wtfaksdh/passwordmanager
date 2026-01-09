from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

@dataclass(frozen=True)
class URL:
    value: str

    def __post_init__(self):
        # Базовая проверка URL
        url_pattern = re.compile(
            r'^(https?|ftp)://'  # протокол
            r'(\w+(\-\w+)*\.)*(\w+)(:\d+)?'  # домен и порт
            r'(\/.*)?$'  # путь
        )
        if not url_pattern.match(self.value):
            raise ValueError(f"Invalid URL: {self.value}")