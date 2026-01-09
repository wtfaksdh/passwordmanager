from infrastructure import init_db
from infrastructure import SQLiteUserRepository, SQLitePasswordRepository, EncryptionServiceImpl, Argon2KeyDerivation, InMemoryKeyStore
from core.application import CreatePassword, GetPassword, UpdatePassword, DeletePassword, ListPasswords
from core.application import PasswordGenerator, PasswordEvaluator, PasswordMasker

# Инициализация базы данных
DB_PATH = "password_manager.db"
conn = init_db(DB_PATH)

# Контейнер зависимостей
class Container:
    # Репозитории
    user_repository = SQLiteUserRepository(DB_PATH)
    password_repository = SQLitePasswordRepository(DB_PATH)

    # Сервисы
    encryption_service = EncryptionServiceImpl()
    key_derivation_service = Argon2KeyDerivation()
    key_store_service = InMemoryKeyStore()

    # Use Cases
    create_password_use_case = CreatePassword(
        password_repository, user_repository, encryption_service, key_store_service
    )
    get_password_use_case = GetPassword(
        password_repository, key_store_service, encryption_service
    )
    update_password_use_case = UpdatePassword(
        password_repository, encryption_service, key_store_service
    )
    delete_password_use_case = DeletePassword(password_repository)
    list_passwords_use_case = ListPasswords(
        password_repository, key_store_service, encryption_service
    )

    # Утилитные сервисы
    password_generator = PasswordGenerator()
    password_evaluator = PasswordEvaluator()
    password_masker = PasswordMasker()