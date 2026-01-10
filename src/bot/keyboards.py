"""Keyboards for Telegram Bot"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from src.config import *


def get_auth_keyboard() -> ReplyKeyboardMarkup:
    """Get authentication menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_REGISTER), KeyboardButton(text=BTN_LOGIN)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ADD_PASSWORD)],
            [KeyboardButton(text=BTN_VIEW_PASSWORDS)],
            [KeyboardButton(text=BTN_DELETE_PASSWORD)],
            [KeyboardButton(text=BTN_UPDATE_PASSWORD)],
            [KeyboardButton(text=BTN_LOGOUT)],
        ],
        resize_keyboard=True,
    )
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Get cancel keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CANCEL)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    """Get confirm keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CONFIRM), KeyboardButton(text=BTN_CANCEL)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def get_passwords_inline_keyboard(password_ids: list[int], password_data: list[tuple]) -> InlineKeyboardMarkup:
    """Get inline keyboard for password selection"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{data[0]} ({data[1]})", callback_data=f"pass_{pwd_id}")]
            for pwd_id, data in zip(password_ids, password_data)
        ]
    )
    return keyboard
