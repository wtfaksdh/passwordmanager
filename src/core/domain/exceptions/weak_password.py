from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

class WeakPasswordError(Exception):
    """Пароль не соответствует требованиям сложности."""
    pass