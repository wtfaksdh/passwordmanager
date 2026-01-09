from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

@dataclass(frozen=True)
class PasswordStrength:
    score: int
    message: str