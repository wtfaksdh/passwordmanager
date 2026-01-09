from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

class PasswordNotFoundError(Exception):
    """Запись пароля не найдена."""
    pass