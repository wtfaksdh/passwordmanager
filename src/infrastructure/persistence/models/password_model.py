from dataclasses import dataclass
from datetime import datetime

@dataclass
class PasswordModel:
    """
    Модель записи пароля для БД SQLite.
    """
    id: int
    user_id: int           # внешний ключ на пользователя
    service: str           # имя сервиса/сайта
    login: str             # логин/имя пользователя для сервиса
    password: bytes        # зашифрованный пароль (AES-GCM ciphertext + тег)
    nonce: bytes           # nonce/IV, использованный при шифровании
    created_at: datetime