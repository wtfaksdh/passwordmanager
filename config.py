"""Application configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "passwords.db"

DATA_DIR.mkdir(exist_ok=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

DATABASE_URL = f"sqlite:///{DB_PATH}"
DATABASE_CHECK_SAME_THREAD = False

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

WELCOME_MESSAGE = """Добро пожаловать в Password Manager! 🔐

Управляйте своими паролями безопасно в Telegram."""

MAIN_MENU_MESSAGE = "Выберите действие:"

BTN_REGISTER = "📝 Зарегистрироваться"
BTN_LOGIN = "🔓 Войти"
BTN_ADD = "➕ Добавить пароль"
BTN_VIEW = "👁️ Посмотреть пароли"
BTN_UPDATE = "✏️ Обновить пароль"
BTN_DELETE = "❌ Удалить пароль"
BTN_BACK = "⬅️ Назад"
BTN_CANCEL = "🚫 Отмена"
BTN_CONFIRM = "✅ Подтвердить"

ERROR_USER_EXISTS = "Пользователь с таким именем уже существует"
ERROR_WRONG_CREDENTIALS = "Неверное имя пользователя или пароль"
ERROR_DATABASE = "Ошибка базы данных"
