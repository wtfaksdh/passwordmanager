"""Configuration for Password Manager"""
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup


load_dotenv()

# ==================== DATABASE ====================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "passwords.db"

DATA_DIR.mkdir(exist_ok=True)

# ==================== TELEGRAM ====================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# ==================== DATABASE SETTINGS ====================
DATABASE_URL = f"sqlite:///{DB_PATH}"
DATABASE_CHECK_SAME_THREAD = False

# ==================== LOGGING ====================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==================== FSM STATES ====================
class AuthStates(StatesGroup):
    """Authentication process states"""
    START = State()
    REGISTER = State()
    REGISTER_USERNAME = State()
    REGISTER_PASSWORD = State()
    LOGIN = State()
    LOGIN_USERNAME = State()
    LOGIN_PASSWORD = State()


class MainMenuStates(StatesGroup):
    """Main menu states"""
    MENU = State()
    ADD_PASSWORD = State()
    ADD_PASSWORD_SERVICE = State()
    ADD_PASSWORD_LOGIN = State()
    ADD_PASSWORD_PASSWORD = State()
    VIEW_PASSWORDS = State()
    DELETE_PASSWORD = State()
    UPDATE_PASSWORD = State()
    UPDATE_PASSWORD_ID = State()
    UPDATE_PASSWORD_CHOICE = State()
    UPDATE_PASSWORD_SERVICE = State()
    UPDATE_PASSWORD_LOGIN = State()
    UPDATE_PASSWORD_PASSWORD = State()


# ==================== MESSAGES ====================
WELCOME_MESSAGE = """Добро пожаловать в Password Manager! 🔐

Управляйте своими паролями безопасно в Telegram."""

MAIN_MENU = "Выберите действие:"
MAIN_MENU_MESSAGE = MAIN_MENU

LOGIN_SUCCESS = "Вы успешно вошли в аккаунт!"
REGISTER_SUCCESS = "Аккаунт создан успешно!"

# ==================== ERROR MESSAGES ====================
ERROR_USER_EXISTS = "Пользователь с таким именем уже существует!"
ERROR_INVALID_CREDENTIALS = "Неверное имя пользователя или пароль!"
ERROR_USER_NOT_FOUND = "Пользователь не найден!"
ERROR_WRONG_CREDENTIALS = ERROR_INVALID_CREDENTIALS
ERROR_DATABASE = "Ошибка базы данных"

# ==================== BUTTONS ====================
BTN_REGISTER = "📝 Регистрация"
BTN_LOGIN = "🔑 Вход"
BTN_ADD_PASSWORD = "➕ Добавить пароль"
BTN_ADD = BTN_ADD_PASSWORD
BTN_VIEW_PASSWORDS = "👁️ Просмотр паролей"
BTN_VIEW = BTN_VIEW_PASSWORDS
BTN_UPDATE_PASSWORD = "✏️ Обновить пароль"
BTN_UPDATE = BTN_UPDATE_PASSWORD
BTN_DELETE_PASSWORD = "🗑️ Удалить пароль"
BTN_DELETE = BTN_DELETE_PASSWORD
BTN_LOGOUT = "🚪 Выход"
BTN_BACK = "⬅️ Назад"
BTN_CANCEL = "❌ Отмена"
BTN_CONFIRM = "✅ Подтвердить"
