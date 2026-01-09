from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить пароль", callback_data="add_password")],
            [InlineKeyboardButton(text="📋 Список паролей", callback_data="list_passwords")],
            [InlineKeyboardButton(text="❌ Удалить пароль", callback_data="delete_password")]
        ]
    )
