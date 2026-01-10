"""Utility functions for Password Manager"""
from typing import Optional
import re


def is_valid_username(username: str) -> bool:
    """Validate username format"""
    if not username or len(username) < 3 or len(username) > 30:
        return False
    # Allow letters, numbers, underscores
    return bool(re.match(r"^[a-zA-Z0-9_]+$", username))


def is_valid_password(password: str) -> bool:
    """Validate password strength"""
    if not password or len(password) < 4:
        return False
    return True


def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def format_password_display(service: str, login: str, password: str) -> str:
    """Format password for display"""
    return f"🔹 <b>{service}</b>\n   Логин: <code>{login}</code>\n   Пароль: <code>{password}</code>\n"
