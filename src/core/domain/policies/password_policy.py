from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re
from exceptions import WeakPasswordError

class PasswordPolicy:
    MIN_LENGTH = 8

    @staticmethod
    def validate(password: str) -> None:
        """
        Проверка сложности пароля. Бросает WeakPasswordError при слабом пароле.
        """
        if len(password) < PasswordPolicy.MIN_LENGTH:
            raise WeakPasswordError(f"Password must be at least {PasswordPolicy.MIN_LENGTH} characters long.")
        if not re.search(r"[A-Z]", password):
            raise WeakPasswordError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise WeakPasswordError("Password must include at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            raise WeakPasswordError("Password must include at least one digit.")
        if not re.search(r"[\W_]", password):
            raise WeakPasswordError("Password must include at least one special character.")