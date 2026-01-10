from dependency_injector import containers, providers

from core.application.use_cases.create_password import CreatePassword
from core.application.use_cases.list_passwords import ListPasswords
from core.domain.entities.password_entry import PasswordEntry

from core.ports.repositories import PasswordRepository, UserRepository
from infrastructure.crypto.encryption.aes_gcm_service import AESGCMService
from infrastructure.crypto.key_store.os_keyring_store import OSKeyringStore
from infrastructure.persistence.repositories.sqlite_repository import SQLitePasswordRepository, SQLiteUserRepository
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
    password_repository = providers.Singleton(
        SQLitePasswordRepository,
        db_path=config.db_path
    )

    user_repository = providers.Singleton(
        SQLiteUserRepository,
        db_path=config.db_path
    )

    # Use cases
    create_password_use_case = providers.Factory(
        CreatePassword,
        password_repo=password_repository,
        user_repo=user_repository,
        encryption_service=encryption_service,
        key_store=key_store
    )

    list_passwords_use_case = providers.Factory(
        ListPasswords,
        password_repo=password_repository,
        key_store=key_store,
        encryption_service=encryption_service
    )

# Инициализация контейнера
container = Container()
container.config.from_pydantic(Settings())
