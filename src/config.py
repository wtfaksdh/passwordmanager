"""Configuration for Password Manager"""
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "passwords.db"

DATA_DIR.mkdir(exist_ok=True)


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


DATABASE_URL = f"sqlite:///{DB_PATH}"
DATABASE_CHECK_SAME_THREAD = False

class States:
    """User states for FSM (Finite State Machine)"""
    MAIN_MENU = "main_menu"
    REGISTER = "register"
    LOGIN = "login"
    REGISTER_USERNAME = "register_username"
    REGISTER_PASSWORD = "register_password"
    LOGIN_USERNAME = "login_username"
    LOGIN_PASSWORD = "login_password"
    MAIN_CHOICE = "main_choice"
    ADD_PASSWORD_SERVICE = "add_password_service"
    ADD_PASSWORD_LOGIN = "add_password_login"
    ADD_PASSWORD_PASSWORD = "add_password_password"
    VIEW_PASSWORDS = "view_passwords"
    DELETE_PASSWORD = "delete_password"
    UPDATE_PASSWORD = "update_password"

WELCOME_MESSAGE = """Добро пожаловать в Password Manager! 🔐

Управляйте своими паролями безопасно в Telegram."""

MAIN_MENU = "Выберите действие:"

LOGIN_SUCCESS = "Вы успешно вошли в аккаунт!"
REGISTER_SUCCESS = "Аккаунт создан успешно!"

ERROR_USER_EXISTS = "Пользователь с таким именем уже существует!"
ERROR_INVALID_CREDENTIALS = "Неверное имя пользователя или пароль!"
ERROR_USER_NOT_FOUND = "Пользователь не найден!"

BTN_REGISTER = "📝 Регистрация"
BTN_LOGIN = "🔑 Вход"
BTN_BACK = "⬅️ Назад"
BTN_CANCEL = "❌ Отмена"
BTN_ADD_PASSWORD = "➕ Добавить пароль"
BTN_VIEW_PASSWORDS = "👁️ Просмотр паролей"
BTN_DELETE_PASSWORD = "🗑️ Удалить пароль"
BTN_UPDATE_PASSWORD = "✏️ Обновить пароль"
BTN_LOGOUT = "🚪 Выход"
BTN_CONFIRM = "✅ Подтвердить"
