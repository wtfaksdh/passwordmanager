import logging
import os

def setup_logging():
    """
    Базовая настройка логирования. Уровень задается через переменную окружения LOG_LEVEL (по умолчанию INFO).
    """
    level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    # Не выводим в логи чувствительные данные (пароли, ключи и т.д.).
    # Pydantic SecretStr уже маскирует значения при форматировании:contentReference[oaicite:7]{index=7}.
    # Если нужны дополнительные фильтры для скрытия секретов, их можно добавить здесь.
    logging.getLogger().info(f"Logging initialized with level {level_name}")