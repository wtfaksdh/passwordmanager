import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import Field
import base64

class Settings(BaseSettings):
    """
    Класс настроек приложения. Автоматически загружает переменные окружения и .env (через Pydantic).
    """
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / '.env',     # .env в корне проекта
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',                              # не ругаться на лишние переменные
        env_nested_delimiter='__'                    # полезно если будут вложенные настройки
    )

    # Основной токен бота — самый важный параметр
    telegram_token: SecretStr = Field(
        ...,
        alias='TELEGRAM_TOKEN',                      # явно говорим какое имя ищем
        description="Токен бота от @BotFather"
    )

    # Путь к файлу SQLite БД (по умолчанию data/passwords.db)
    db_path: str = 'data/passwords.db'

    # Имя сервиса для keyring (используется в OSKeyringStore)
    keyring_service_name: str = 'password_manager'

    # Уровень логирования (DEBUG, INFO, etc.)
    log_level: str = 'INFO'

    # Ключ шифрования AES (32 байта для AES-256)
    encryption_key: bytes = Field(
        default_factory=lambda: base64.b64decode(os.getenv(
            'ENCRYPTION_KEY',
            base64.b64encode(os.urandom(32)).decode()
        )),
        description="Base64-encoded AES encryption key"
    )

# Экземпляр настроек, сразу загружает значения из окружения/.env
settings = Settings()
