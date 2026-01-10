"""FSM states for Telegram Bot"""
from aiogram.fsm.state import State, StatesGroup


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
    UPDATE_PASSWORD_SERVICE = State()
    UPDATE_PASSWORD_LOGIN = State()
    UPDATE_PASSWORD_PASSWORD = State()
