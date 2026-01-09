import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    """
    Класс настроек приложения. Автоматически загружает переменные окружения и .env (через Pydantic).
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    # Конфигурация Telegram-бота. SecretStr маскирует значение в логах:contentReference[oaicite:4]{index=4}.
    telegram_token: SecretStr

    # Путь к файлу SQLite БД (по умолчанию data/passwords.db)
    db_path: str = 'data/passwords.db'

    # Имя сервиса для keyring (используется в OSKeyringStore)
    keyring_service_name: str = 'password_manager'

    # Уровень логирования (DEBUG, INFO, etc.)
    log_level: str = 'INFO'

    # (Дополнительно) AES-ключ можно хранить в keyring, поэтому здесь не задается

# Экземпляр настроек, сразу загружает значения из окружения/.env
settings = Settings()