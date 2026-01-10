"""
Project structure documentation
"""

"""
Новая структура проекта Password Manager
=========================================

The project has been refactored into two main layers:

CORE LAYER (ядро приложения)
├── core/
│   ├── __init__.py                 # Package initialization with public API
│   ├── database/                   # Data persistence layer
│   │   ├── __init__.py
│   │   ├── db.py                   # Database connection and initialization
│   │   ├── models.py               # Data models (User, Password)
│   │   └── crud.py                 # Repository operations (UserRepository, PasswordRepository)
│   │
│   ├── security/                   # Security and validation
│   │   ├── __init__.py
│   │   ├── encryption.py           # Password encryption with Fernet (AES)
│   │   └── validators.py           # Input validation utilities
│   │
│   └── services/                   # Business logic
│       ├── __init__.py
│       ├── auth.py                 # AuthenticationService - user registration and login
│       └── password.py             # PasswordService - password CRUD with encryption


INTERFACE LAYER (интерфейс)
├── interface/
│   ├── __init__.py
│   └── bot/                        # Telegram Bot Interface
│       ├── __init__.py
│       ├── states.py               # FSM states (AuthStates, MainMenuStates)
│       ├── keyboards.py            # Telegram keyboard builders
│       └── handlers/               # Handler modules by feature
│           ├── __init__.py
│           ├── auth.py             # Authentication command handlers
│           └── password.py         # Password management command handlers


CONFIGURATION
├── config.py                       # Centralized configuration and settings
├── main.py                         # Application entry point
├── .env.example                    # Environment variables template


INFRASTRUCTURE
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI/CD Pipeline with GitHub Actions


TESTING & QUALITY
├── tests/                          # Test suite
├── requirements.txt                # Production dependencies (with cryptography)
└── requirements-dev.txt            # Development dependencies

════════════════════════════════════════════════════════════════

КЛЮЧЕВЫЕ УЛУЧШЕНИЯ
═════════════════

1. ШИФРОВАНИЕ ПАРОЛЯ (cryptography library)
   - Используется Fernet (симметричное шифрование на базе AES-128)
   - Каждый пароль шифруется с собственной солью (PBKDF2-SHA256)
   - Master password - имя пользователя (username)
   - Формат: base64(salt):base64(encrypted_password)

2. РАЗДЕЛЕНИЕ ОТВЕТСТВЕННОСТИ
   - Core: Бизнес-логика, шифрование, базы данных
   - Interface: Telegram bot interface, обработчики команд
   - Config: Централизованная конфигурация
   - Services: Уровень приложения между БД и интерфейсом

3. МОДУЛЬНАЯ АРХИТЕКТУРА
   - core.database: Работа с БД и репозитории
   - core.security: Шифрование и валидация
   - core.services: Бизнес-логика (Auth, Passwords)
   - interface.bot: Telegram interface
   - interface.bot.handlers: Разделённые обработчики (auth, password)

4. ЧИТАЕМОСТЬ КОДА
   - Каждый модуль имеет одну ответственность (SRP)
   - Типизация с помощью type hints
   - Подробная документация в docstrings
   - Логичная организация импортов

5. CI/CD PIPELINE (.github/workflows/ci.yml)
   - Поддержка Python 3.9, 3.10, 3.11, 3.12
   - Тестирование (pytest)
   - Проверка кода (flake8, black, mypy)
   - Security checks (bandit, safety)
   - Coverage report (codecov)
   - Auto deployment на main branch

════════════════════════════════════════════════════════════════

ИСПОЛЬЗОВАНИЕ
═════════════

1. Установка зависимостей:
   pip install -r requirements.txt

2. Конфигурация:
   cp .env.example .env
   # Отредактируйте .env и добавьте TELEGRAM_BOT_TOKEN

3. Запуск бота:
   python main.py

4. Тестирование:
   pytest tests/ -v --cov=core --cov=interface

5. Проверка качества кода:
   black . --exclude=venv
   flake8 . --exclude=venv
   mypy . --ignore-missing-imports

════════════════════════════════════════════════════════════════

ШИФРОВАНИЕ И БЕЗОПАСНОСТЬ
═════════════════════════

Encryption Flow:
1. User registration: password → PBKDF2(salt + password) → Fernet(key)
2. Password storage: plain_password → Fernet(master_password=username) → encrypted_password
3. Decryption: encrypted_password + username → decrypt → plain_password

Security Features:
✓ PBKDF2-SHA256 для управления ключами
✓ Фернет (AES-128) для шифрования
✓ Уникальная соль для каждого зашифрованного пароля
✓ Input validation для всех пользовательских данных
✓ Database-level constraints (foreign keys, unique indexes)

════════════════════════════════════════════════════════════════
"""
