"""Keyboard builders for Telegram Bot"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import BTN_REGISTER, BTN_LOGIN, BTN_ADD, BTN_VIEW, BTN_UPDATE, BTN_DELETE, BTN_BACK, BTN_CANCEL, BTN_CONFIRM


def get_auth_keyboard() -> ReplyKeyboardMarkup:
    """Get authentication menu keyboard"""
    keyboard = [
        [KeyboardButton(text=BTN_REGISTER)],
        [KeyboardButton(text=BTN_LOGIN)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = [
        [KeyboardButton(text=BTN_ADD), KeyboardButton(text=BTN_VIEW)],
        [KeyboardButton(text=BTN_UPDATE), KeyboardButton(text=BTN_DELETE)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Get cancel button keyboard"""
    keyboard = [[KeyboardButton(text=BTN_CANCEL)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_back_keyboard() -> ReplyKeyboardMarkup:
    """Get back button keyboard"""
    keyboard = [[KeyboardButton(text=BTN_BACK)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    """Get confirm/cancel keyboard"""
    keyboard = [
        [KeyboardButton(text=BTN_CONFIRM), KeyboardButton(text=BTN_CANCEL)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_passwords_inline_keyboard(passwords: list) -> InlineKeyboardMarkup:
    """
    Get inline keyboard for password selection.
    
    Args:
        passwords: List of password records
        
    Returns:
        InlineKeyboardMarkup with password options
    """
    keyboard = []
    for pwd in passwords:
        callback_data = f"pwd_{pwd['id']}"
        button_text = f"🔐 {pwd['service']} ({pwd['login']})"
        keyboard.append(
            [InlineKeyboardButton(text=button_text, callback_data=callback_data)]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
