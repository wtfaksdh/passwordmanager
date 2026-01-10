# Руководство по миграции на новую архитектуру

## 📋 Оглавление
1. [Обзор изменений](#обзор-изменений)
2. [Установка зависимостей](#установка-зависимостей)
3. [Обновление импортов](#обновление-импортов)
4. [Новая структура кода](#новая-структура-кода)
5. [Использование API](#использование-api)
6. [Миграция БД](#миграция-бд)
7. [Запуск и тестирование](#запуск-и-тестирование)

## 🔄 Обзор изменений

### Старая структура (v1.0):
```
src/
├── bot/handlers.py (500+ строк)
├── database/db.py
├── config.py
└── utils.py
```

### Новая структура (v2.0):
```
core/                           # Бизнес-логика и данные
├── database/                   # Работа с БД
├── security/                   # Шифрование и валидация
└── services/                   # Бизнес-сервисы

interface/                      # Интерфейсы пользователя
└── bot/                        # Telegram бот
    └── handlers/               # Разделённые обработчики

config.py                       # Централизованная конфигурация
main.py                         # Entry point
```

## 📦 Установка зависимостей

### Обновленные требования:
```bash
pip install --upgrade -r requirements.txt
pip install --upgrade -r requirements-dev.txt
```

### Новые пакеты:
- `cryptography>=41.0.0` - для шифрования AES

## 🔗 Обновление импортов

### Старый код:
```python
from src.config import TELEGRAM_BOT_TOKEN
from src.database.db import Database, init_db
from src.database.models import User, Password
from src.database.crud import UserCRUD, PasswordCRUD
from src.bot.handlers import router
```

### Новый код:
```python
from config import TELEGRAM_BOT_TOKEN
from core import Database, DatabaseInitializer
from core import User, Password
from core import UserRepository, PasswordRepository
from interface.bot.handlers import init_routers
```

## 🏗️ Новая структура кода

### Core.Database (работа с БД):
```python
from core import Database, DatabaseInitializer, User, Password
from core import UserRepository, PasswordRepository

# Инициализация БД
DatabaseInitializer.init_db(db_path)

# Создание пользователя
db = Database(db_path)
db.connect()
user = User(username="john", password_hash="encrypted_hash")
user_id = UserRepository.create(db, user)
db.close()
```

### Core.Security (шифрование):
```python
from core import EncryptionService, Validators

# Шифрование пароля
encrypted = EncryptionService.encrypt_password("my_password", "master_password")

# Дешифрование
decrypted = EncryptionService.decrypt_password(encrypted, "master_password")

# Валидация
is_valid, msg = Validators.validate_username("username")
```

### Core.Services (бизнес-логика):
```python
from core import AuthenticationService, PasswordService
from core import Database

db = Database(db_path)
db.connect()

# Регистрация пользователя
success, msg = AuthenticationService.register_user(db, "john", "password123")

# Аутентификация
success, msg, user_id = AuthenticationService.authenticate_user(db, "john", "password123")

# Добавление пароля
success, msg = PasswordService.create_password(
    db, user_id, "Gmail", "john@gmail.com", "app_password", "master_password"
)

# Получение паролей
success, passwords, msg = PasswordService.get_user_passwords(db, user_id, "master_password")

db.close()
```

### Interface.Bot (обработчики):
```python
from interface.bot import AuthStates, MainMenuStates
from interface.bot import get_auth_keyboard, get_main_menu_keyboard
from interface.bot.handlers import init_routers

# Инициализация маршрутизаторов
main_router = init_routers()
dp.include_router(main_router)
```

## 🔐 Использование API

### Шифрование пароля:
```python
from core import EncryptionService

# Зашифровать пароль (возвращает строку: salt:encrypted)
master_pwd = "user_username"  # или любой другой master password
encrypted = EncryptionService.encrypt_password("GooglePassword123", master_pwd)
# Result: "dE3F...OA==:gAAAABpYrP0WRazg...Hqw=="

# Расшифровать пароль
plain = EncryptionService.decrypt_password(encrypted, master_pwd)
# Result: "GooglePassword123"
```

### Работа с репозиториями:
```python
from core import Database, UserRepository, PasswordRepository, User, Password

db = Database(db_path)
db.connect()

# Создание пользователя
user = User(username="alice", password_hash="encrypted_pass")
user_id = UserRepository.create(db, user)

# Поиск пользователя
user = UserRepository.get_by_username(db, "alice")

# Создание пароля
pwd = Password(user_id=user_id, service="VK", login="alice_vk", password="encrypted_pwd")
pwd_id = PasswordRepository.create(db, pwd)

# Получение паролей пользователя
passwords = PasswordRepository.get_by_user(db, user_id)

# Обновление пароля
pwd.password = "new_encrypted_pwd"
PasswordRepository.update(db, pwd)

# Удаление пароля
PasswordRepository.delete(db, pwd_id)

db.close()
```

## 🔄 Миграция БД

### Совместимость:
✓ Новая структура полностью совместима с существующей БД
✓ Таблицы users и passwords имеют такую же схему
✓ Все индексы сохранены

### Переход:
1. Скопировать `data/passwords.db` если уже есть
2. При первом запуске автоматически создаются таблицы
3. Все существующие данные остаются без изменений

### Примечание о шифровании:
⚠️ Старые пароли хранились в открытом виде
✓ Новые пароли шифруются автоматически
→ Рекомендуется пересохранить старые пароли для безопасности

## 🚀 Запуск и тестирование

### Запуск бота:
```bash
# Предварительно настроить .env
cp .env.example .env
# Отредактировать .env и добавить TELEGRAM_BOT_TOKEN

# Запустить
python main.py
```

### Запуск тестов:
```bash
# Все тесты
pytest tests/ -v

# Тесты с покрытием
pytest tests/ -v --cov=core --cov=interface

# Конкретный тест
pytest tests/test_structure.py -v
```

### Проверка качества кода:
```bash
# Форматирование
black . --exclude=venv

# Линтинг
flake8 . --exclude=venv

# Type checking
mypy . --ignore-missing-imports

# Security check
bandit -r core/ interface/
```

## ✅ Чеклист для разработчиков

- [ ] Обновлены импорты во всех файлах
- [ ] Установлены новые зависимости (cryptography)
- [ ] Протестирована шифрование/дешифрование
- [ ] Протестирована валидация данных
- [ ] Протестированы операции БД
- [ ] Запущены unit-тесты
- [ ] Проверено качество кода (black, flake8, mypy)
- [ ] Настроены переменные окружения (.env)
- [ ] Запущен бот и протестирована функциональность

## 🆘 Часто встречаемые проблемы

### ImportError: cannot import name 'X' from 'core'
**Решение:** Убедитесь, что используете правильные имена (UserRepository, не UserCRUD)

### Database initialization error
**Решение:** Убедитесь что папка `data/` существует, или она создастся автоматически

### Encryption/Decryption error
**Решение:** Проверьте что используете одинаковый master_password для encrypt/decrypt

### Module not found (config, core, interface)
**Решение:** Запустите из корневой папки проекта

## 📚 Дополнительные ресурсы

- [ARCHITECTURE_NEW.md](ARCHITECTURE_NEW.md) - детальная архитектура
- [REFACTORING_CHANGELOG.md](REFACTORING_CHANGELOG.md) - список всех изменений
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - CI/CD конфигурация

---
**Last Updated:** January 10, 2026
**Version:** 2.0.0
