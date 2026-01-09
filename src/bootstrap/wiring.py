from dependency_injector import containers, providers

from infrastructure.crypto.encryption.aes_gcm_service import AESGCMService
from infrastructure.crypto.key_store.os_keyring_store import OSKeyringStore
from infrastructure.persistence.repositories.sqlite_repository import SQLitePasswordRepository
from core.application.use_cases.create_password import CreatePasswordUseCase
from core.application.use_cases.list_passwords import ListPasswordsUseCase
from infrastructure.config.settings import Settings

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Шифрование
    encryption_service = providers.Singleton(
        AESGCMService,
        key=config.encryption_key
    )

    # Хранилище ключей
    key_store = providers.Singleton(
        OSKeyringStore,
        service_name=config.keyring_service_name
    )

    # Репозитории
    password_repository = providers.Singleton(SQLitePasswordRepository)

    # Use cases
    create_password_use_case = providers.Factory(
        CreatePasswordUseCase,
        password_repository=password_repository,
        encryption_service=encryption_service
    )

    list_passwords_use_case = providers.Factory(
        ListPasswordsUseCase,
        password_repository=password_repository,
        encryption_service=encryption_service
    )

# Инициализация контейнера
container = Container()
container.config.from_pydantic(Settings())
