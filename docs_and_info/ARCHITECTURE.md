# Архитектура Password Manager

## Обзор

Password Manager - это Telegram бот для управления паролями с использованием SQLite3 базы данных и фреймворка aiogram.

## Компоненты

### 1. Database Layer (`src/database/`)

#### `models.py` - Модели данных
- **User**: Модель пользователя с полями username, password, timestamps
- **Password**: Модель для хранения паролей с полями service, login, password

#### `db.py` - Управление БД
- **Database**: Класс для работы с SQLite3 соединением
- **init_db()**: Функция инициализации БД с созданием таблиц и индексов

**Таблица users**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Таблица passwords**:
```sql
CREATE TABLE passwords (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    service TEXT NOT NULL,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### `crud.py` - CRUD операции

**UserCRUD**:
- `create()` - Создание пользователя
- `get_by_username()` - Поиск по имени
- `get_by_id()` - Поиск по ID
- `verify_password()` - Проверка пароля
- `delete()` - Удаление пользователя

**PasswordCRUD**:
- `create()` - Создание записи пароля
- `get_by_id()` - Получение по ID
- `get_by_user_id()` - Получение всех паролей пользователя
- `update()` - Обновление пароля
- `delete()` - Удаление пароля
- `delete_by_user_id()` - Удаление всех паролей пользователя

### 2. Bot Layer (`src/bot/`)

#### `states.py` - Состояния FSM (Finite State Machine)

**AuthStates** (Аутентификация):
- START - Начальное состояние
- REGISTER / LOGIN - Выбор действия
- REGISTER_USERNAME / REGISTER_PASSWORD - Регистрация
- LOGIN_USERNAME / LOGIN_PASSWORD - Вход

**MainMenuStates** (Главное меню):
- MENU - Главное меню
- ADD_PASSWORD_* - Добавление пароля (сервис, логин, пароль)
- VIEW_PASSWORDS - Просмотр паролей
- DELETE_PASSWORD - Удаление пароля
- UPDATE_PASSWORD - Обновление пароля

#### `keyboards.py` - Клавиатуры

- `get_auth_keyboard()` - Клавиатура аутентификации
- `get_main_menu_keyboard()` - Главное меню
- `get_cancel_keyboard()` - Отмена
- `get_confirm_keyboard()` - Подтверждение
- `get_passwords_inline_keyboard()` - Встроенные кнопки для выбора пароля

#### `handlers.py` - Обработчики команд

**Основные обработчики**:
- `/start` - Инициализация
- Регистрация (username → password)
- Вход (username → password)
- Добавление пароля (service → login → password)
- Просмотр всех паролей
- Обновление пароля
- Удаление пароля
- Выход из аккаунта

**Управление сессиями**:
```python
user_sessions = {}  # {telegram_user_id: database_user_id}
```

### 3. Configuration (`src/config.py`)

- Пути к БД
- Телеграм токен
- Константы состояний (States)
- Текстовые сообщения
- Названия кнопок

### 4. Utilities (`src/utils.py`)

- `is_valid_username()` - Валидация имени пользователя
- `is_valid_password()` - Валидация пароля
- `is_valid_email()` - Валидация email
- `format_password_display()` - Форматирование вывода

## Поток выполнения

### Регистрация
```
1. User → /start → START state
2. User → "Регистрация" → REGISTER_USERNAME state
3. User → enters username → REGISTER_PASSWORD state
4. User → enters password → create user in DB → MAIN state
```

### Вход
```
1. User → /start → START state
2. User → "Вход" → LOGIN_USERNAME state
3. User → enters username → LOGIN_PASSWORD state
4. User → enters password → verify in DB → MAIN state or START state
```

### Добавление пароля
```
1. User → "Добавить пароль" → ADD_PASSWORD_SERVICE
2. User → enters service → ADD_PASSWORD_LOGIN
3. User → enters login → ADD_PASSWORD_PASSWORD
4. User → enters password → save to DB → MAIN state
```

## Взаимодействие компонентов

```
┌─────────────────┐
│   Telegram      │
│   User          │
└────────┬────────┘
         │
    aiogram FSM
         │
    ┌────▼────────────────────┐
    │   Bot Layer             │
    │   handlers.py           │
    │   states.py             │
    │   keyboards.py          │
    │                         │
    │  user_sessions dict     │
    └────┬────────────────────┘
         │
    ┌────▼────────────────────┐
    │   Database Layer        │
    │   crud.py               │
    │   db.py                 │
    │   models.py             │
    └────┬────────────────────┘
         │
    ┌────▼────────────────────┐
    │   SQLite3               │
    │   passwords.db          │
    │   ├── users table       │
    │   └── passwords table   │
    └─────────────────────────┘
```

## Безопасность

### Текущие ограничения ⚠️

- Пароли хранятся в открытом виде
- Нет шифрования данных
- Сессии хранятся в памяти (теряются при перезагрузке)
- Нет двухфакторной аутентификации

### Рекомендации для production

1. **Шифрование паролей**:
   - Использовать `cryptography.fernet` или bcrypt
   - Хешировать пароли пользователей

2. **Безопасность сессий**:
   - Использовать Redis вместо памяти
   - Добавить токены с истечением

3. **Логирование**:
   - Записывать все действия
   - Мониторить подозрительную активность

4. **API Security**:
   - Использовать HTTPS
   - Добавить rate limiting
   - Валидировать все входные данные

## Тестирование

### Unit тесты (`tests/`)

**test_database.py**:
- Тесты UserCRUD: create, get, verify, delete
- Тесты PasswordCRUD: create, get, update, delete

**test_validators.py**:
- Тесты валидации username, password, email

## Развертывание

### CI/CD Pipeline (`.github/workflows/ci.yml`)

На каждый push в `main` или `develop`:
1. Установка зависимостей
2. Запуск тестов (pytest)
3. Проверка кода (flake8)
4. Проверка типов (mypy)
5. Загрузка покрытия кода

### Локальное развертывание

```bash
# 1. Инициализировать БД
python3 scripts/init_db.py

# 2. Запустить бота
python3 main.py

# 3. Запустить тесты
pytest tests/ -v
```

## Расширение функционала

### Добавление новой команды

1. **Добавить состояние** в `src/bot/states.py`:
```python
class MainMenuStates(StatesGroup):
    NEW_FEATURE = State()
```

2. **Добавить кнопку** в `src/config.py`:
```python
BTN_NEW_FEATURE = "🎯 Новая функция"
```

3. **Добавить в клавиатуру** в `src/bot/keyboards.py`:
```python
def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(text=BTN_NEW_FEATURE)],
    ])
```

4. **Добавить обработчик** в `src/bot/handlers.py`:
```python
@router.message(MainMenuStates.MENU, F.text == BTN_NEW_FEATURE)
async def new_feature_handler(message: Message, state: FSMContext):
    await message.answer("Ваше сообщение")
    await state.set_state(MainMenuStates.NEW_FEATURE)
```

5. **Написать тест** в `tests/test_*.py`

## References

- [aiogram documentation](https://docs.aiogram.dev/)
- [SQLite3 documentation](https://www.sqlite.org/docs.html)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
