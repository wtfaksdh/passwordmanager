# 🔐 Password Manager Bot

Telegram-бот для безопасного хранения и управления паролями с шифрованием.

---

## 🚀 Быстрый старт

### Требования

* Python 3.10+
* Telegram Bot Token

### Установка

```bash
git clone <repository-url>
cd passwordmanager
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Конфигурация

Скопируйте и настройте `.env`:

```bash
cp .env.example .env
```

Добавьте токен:

```env
TELEGRAM_BOT_TOKEN=your_token_here
```

### Запуск

```bash
python main.py
```

---

## ✨ Функции

* 📝 Регистрация и безопасный вход
* ➕ Добавление, 👁️ просмотр, ✏️ обновление и 🗑️ удаление паролей
* 🔐 AES-128 шифрование с уникальной солью
* 🔑 PBKDF2-HMAC-SHA256 для ключей
* 🚪 Выход из аккаунта

---

## 🗂️ Структура проекта

```
main.py
config.py
requirements.txt
.env / .env.example
src/
├─ bot/           # Telegram-бот
├─ database/      # Модели и CRUD
├─ security/      # Шифрование
├─ services/      # Логика
└─ utils.py
tests/            # Тесты
.github/workflows/ # CI/CD
```

---

## 🛢️ База данных

**users**: id, username, password, created_at, updated_at
**passwords**: id, user_id, service, login, password, created_at, updated_at

---

## 🔒 Безопасность

* Все пароли **зашифрованы AES-128**
* Уникальная соль для каждого пароля
* Ключ генерируется через PBKDF2-HMAC-SHA256 (100 000 итераций)

---

## 🧪 Разработка

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
black src/ tests/
flake8 src/ tests/
mypy src/
```

---

## 🔄 CI/CD

* Автотесты на Python 3.9–3.12
* Линтинг, проверка типов и покрытие кода через GitHub Actions
