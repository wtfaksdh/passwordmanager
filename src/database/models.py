"""Database models"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User model with encrypted password"""
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""  # Encrypted password hash
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class Password:
    """Password record model with encryption"""
    id: Optional[int] = None
    user_id: int = 0
    service: str = ""
    login: str = ""
    password: str = ""  # Encrypted password
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
