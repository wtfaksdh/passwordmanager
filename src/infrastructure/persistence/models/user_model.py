from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserModel:
    """
    Модель пользователя для БД SQLite.
    """
    id: int
    username: str
    password_hash: bytes  # захешированный пароль пользователя
    created_at: datetime