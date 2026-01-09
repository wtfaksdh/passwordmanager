from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from entities.user import User


class UserPolicy:
    @staticmethod
    def validate(user: User) -> None:
        """
        Проверка свойств пользователя. Бросает ValueError при нарушении.
        """
        if not user.username or user.username.strip() == "":
            raise ValueError("Username cannot be empty.")
        # Email валидируется в объекте Email
        if user.id is not None and user.id < 0:
            raise ValueError("User ID must be positive.")