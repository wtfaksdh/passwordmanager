"""Password management handlers for Telegram Bot"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import BTN_ADD, BTN_VIEW, BTN_UPDATE, BTN_DELETE, BTN_BACK, MAIN_MENU_MESSAGE
from src.bot.states import MainMenuStates
from src.bot.keyboards import (
    get_main_menu_keyboard,
    get_cancel_keyboard,
    get_back_keyboard,
    get_passwords_inline_keyboard,
)
from src import Database, PasswordService, Validators
from src.database.crud import PasswordRepository
from src.database.models import Password
from config import DB_PATH

# Router for password management
router = Router()

# Store session context
user_sessions = {}


@router.message(MainMenuStates.MENU, F.text == BTN_ADD)
async def add_password_start(message: Message, state: FSMContext):
    """Start adding new password"""
    await message.answer(
        "Введите название сервиса (например: Gmail, VK, Telegram):",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(MainMenuStates.ADD_PASSWORD_SERVICE)


@router.message(MainMenuStates.ADD_PASSWORD_SERVICE)
async def add_password_service(message: Message, state: FSMContext):
    """Handle service name input"""
    service = message.text.strip()
    
    # Validate service name
    is_valid, error_msg = Validators.validate_service(service)
    if not is_valid:
        await message.answer(error_msg)
        return
    
    await state.update_data(service=service)
    await message.answer(
        "Введите логин:",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(MainMenuStates.ADD_PASSWORD_LOGIN)


@router.message(MainMenuStates.ADD_PASSWORD_LOGIN)
async def add_password_login(message: Message, state: FSMContext):
    """Handle login input"""
    login = message.text.strip()
    
    # Validate login
    is_valid, error_msg = Validators.validate_login(login)
    if not is_valid:
        await message.answer(error_msg)
        return
    
    await state.update_data(login=login)
    await message.answer(
        "Введите пароль:",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(MainMenuStates.ADD_PASSWORD_PASSWORD)


@router.message(MainMenuStates.ADD_PASSWORD_PASSWORD)
async def add_password_password(message: Message, state: FSMContext):
    """Handle password input"""
    password = message.text.strip()
    
    # Validate password
    is_valid, error_msg = Validators.validate_password(password)
    if not is_valid:
        await message.answer(error_msg)
        return
    
    # Get data
    data = await state.get_data()
    service = data.get("service")
    login = data.get("login")
    
    # Get user ID and master password
    user_id = user_sessions.get(message.from_user.id)
    if not user_id:
        await message.answer("❌ Ошибка: пользователь не авторизован")
        return
    
    # Get user's master password (their login password)
    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    db.close()
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        return
    
    # Add password
    db = Database(DB_PATH)
    db.connect()
    
    success, msg = PasswordService.create_password(
        db,
        user_id,
        service,
        login,
        password,
        user.username,  # Use username as master password for encryption
    )
    db.close()
    
    if success:
        await message.answer(
            f"✅ {msg}",
            reply_markup=get_main_menu_keyboard(),
        )
    else:
        await message.answer(f"❌ {msg}")
    
    await state.set_state(MainMenuStates.MENU)


@router.message(MainMenuStates.MENU, F.text == BTN_VIEW)
async def view_passwords(message: Message, state: FSMContext):
    """View all user's passwords"""
    user_id = user_sessions.get(message.from_user.id)
    if not user_id:
        await message.answer("❌ Ошибка: пользователь не авторизован")
        return
    
    # Get user's master password
    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        db.close()
        return
    
    # Get passwords
    success, passwords, msg = PasswordService.get_user_passwords(
        db, user_id, user.username
    )
    db.close()
    
    if not success:
        await message.answer(f"❌ {msg}")
        await state.set_state(MainMenuStates.MENU)
        return
    
    if not passwords:
        await message.answer(
            "📭 У вас нет сохранённых паролей",
            reply_markup=get_main_menu_keyboard(),
        )
        await state.set_state(MainMenuStates.MENU)
        return
    
    # Show passwords
    message_text = "🔐 Ваши пароли:\n\n"
    for pwd in passwords:
        message_text += f"🔑 {pwd['service']}\n"
        message_text += f"   Логин: {pwd['login']}\n"
        message_text += f"   Пароль: {pwd['password']}\n\n"
    
    await message.answer(
        message_text,
        reply_markup=get_main_menu_keyboard(),
    )
    await state.set_state(MainMenuStates.MENU)


@router.message(MainMenuStates.MENU, F.text == BTN_DELETE)
async def delete_password_start(message: Message, state: FSMContext):
    """Start password deletion"""
    user_id = user_sessions.get(message.from_user.id)
    if not user_id:
        await message.answer("❌ Ошибка: пользователь не авторизован")
        return
    
    # Get user's master password
    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        db.close()
        return
    
    # Get passwords
    success, passwords, msg = PasswordService.get_user_passwords(
        db, user_id, user.username
    )
    db.close()
    
    if not passwords:
        await message.answer(
            "📭 У вас нет сохранённых паролей для удаления",
            reply_markup=get_main_menu_keyboard(),
        )
        await state.set_state(MainMenuStates.MENU)
        return
    
    # Show password selection
    await message.answer(
        "Выберите пароль для удаления:",
        reply_markup=get_passwords_inline_keyboard(passwords),
    )
    await state.set_state(MainMenuStates.DELETE_PASSWORD)


@router.message(MainMenuStates.MENU, F.text == BTN_UPDATE)
async def update_password_start(message: Message, state: FSMContext):
    """Start password update"""
    user_id = user_sessions.get(message.from_user.id)
    if not user_id:
        await message.answer("❌ Ошибка: пользователь не авторизован")
        return
    
    # Get user's master password
    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        db.close()
        return
    
    # Get passwords
    success, passwords, msg = PasswordService.get_user_passwords(
        db, user_id, user.username
    )
    db.close()
    
    if not passwords:
        await message.answer(
            "📭 У вас нет сохранённых паролей для обновления",
            reply_markup=get_main_menu_keyboard(),
        )
        await state.set_state(MainMenuStates.MENU)
        return
    
    # Show password selection
    await message.answer(
        "Выберите пароль для обновления:",
        reply_markup=get_passwords_inline_keyboard(passwords),
    )
    await state.set_state(MainMenuStates.UPDATE_PASSWORD_ID)


@router.message(F.text == BTN_BACK)
async def back_handler(message: Message, state: FSMContext):
    """Handle back button"""
    await message.answer(MAIN_MENU_MESSAGE, reply_markup=get_main_menu_keyboard())
    await state.set_state(MainMenuStates.MENU)
