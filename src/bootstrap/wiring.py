from dependency_injector import containers, providers

from infrastructure.crypto.encryption.aes_gcm_service import AESGCMService
from infrastructure.crypto.key_store.os_keyring_store import OSKeyringStore
from infrastructure.config.settings import Settings

class Container(containers.DeclarativeContainer):
    """
    DI-контейнер приложения. Содержит провайдеры для сервисов шифрования, хранилища ключей и т.д.
    """
    config = providers.Configuration()

    # Провайдер сервисов шифрования AES-GCM. Ключ передается из конфигурации.
    encryption_service = providers.Singleton(
        AESGCMService,
        key=config.encryption_key  # передача ключа для AESGCMService
    )

    # Провайдер для хранилища ключей на основе системного keyring
    key_store = providers.Singleton(
        OSKeyringStore,
        service_name=config.keyring_service_name  # имя сервиса для keyring
    )

    # Здесь можно добавить другие провайдеры, например базу данных, репозитории и т.д.

# Инициализация контейнера
container = Container()
# Загрузка конфигурации из переменных окружения/файла .env
container.config.from_pydantic(Settings())

# Возможная настройка wiring для телеграм-бота (привязка зависимостей к модулям-обработчикам команд):
# container.wire(modules=[telegram_entrypoint_module])