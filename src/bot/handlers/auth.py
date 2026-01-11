"""Authentication handlers for Telegram Bot"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from config import BTN_REGISTER, BTN_LOGIN, BTN_CANCEL, WELCOME_MESSAGE, MAIN_MENU_MESSAGE
from src.bot.states import AuthStates, MainMenuStates
from src.bot.keyboards import (
    get_auth_keyboard,
    get_main_menu_keyboard,
    get_cancel_keyboard,
)
from src import Database, AuthenticationService, Validators
from config import DB_PATH

router = Router()

user_sessions = {}

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    user_id = message.from_user.id
    
    await state.clear()
    
    if user_id in user_sessions:

        await message.answer(MAIN_MENU_MESSAGE, reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
    else:

        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.set_state(AuthStates.START)


@router.message(AuthStates.START, F.text == BTN_REGISTER)
async def register_start(message: Message, state: FSMContext):
    """Start registration process"""
    await message.answer(
        "Введите имя пользователя (только буквы, цифры, - и _):",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(AuthStates.REGISTER_USERNAME)


@router.message(AuthStates.REGISTER_USERNAME)
async def register_username(message: Message, state: FSMContext):
    """Handle username input during registration"""

    if message.text == BTN_CANCEL:
        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.set_state(AuthStates.START)
        return
    
    username = message.text.strip()

    is_valid, error_msg = Validators.validate_username(username)
    if not is_valid:
        await message.answer(error_msg)
        return
    

    db = Database(DB_PATH)
    db.connect()
    
    from src.database.crud import UserRepository
    existing_user = UserRepository.get_by_username(db, username)
    db.close()
    
    if existing_user:
        await message.answer(
            "❌ Пользователь с таким именем уже существует"
        )
        return
    
    await state.update_data(username=username)
    await message.answer(
        "Введите пароль (минимум 4 символа):",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(AuthStates.REGISTER_PASSWORD)


@router.message(AuthStates.REGISTER_PASSWORD)
async def register_password(message: Message, state: FSMContext):
    """Handle password input during registration"""

    if message.text == BTN_CANCEL:
        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.clear()
        await state.set_state(AuthStates.START)
        return
    
    password = message.text.strip()
    
    is_valid, error_msg = Validators.validate_password(password)
    if not is_valid:
        await message.answer(error_msg)
        return
    
    data = await state.get_data()
    username = data.get("username")

    db = Database(DB_PATH)
    db.connect()
    
    success, msg = AuthenticationService.register_user(db, username, password)
    db.close()
    
    if success:

        db = Database(DB_PATH)
        db.connect()
        from src.database.crud import UserRepository
        user = UserRepository.get_by_username(db, username)
        db.close()
        
        if user:
            user_sessions[message.from_user.id] = user.id
            await message.answer(
                f"✅ {msg}",
                reply_markup=get_main_menu_keyboard(),
            )
            await state.set_state(MainMenuStates.MENU)
    else:
        await message.answer(f"❌ {msg}")
        await state.set_state(AuthStates.START)


@router.message(AuthStates.START, F.text == BTN_LOGIN)
async def login_start(message: Message, state: FSMContext):
    """Start login process"""
    await message.answer(
        "Введите имя пользователя:",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(AuthStates.LOGIN_USERNAME)


@router.message(AuthStates.LOGIN_USERNAME)
async def login_username(message: Message, state: FSMContext):
    """Handle username input during login"""

    if message.text == BTN_CANCEL:
        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.set_state(AuthStates.START)
        return
    
    username = message.text.strip()
    
    await state.update_data(username=username)
    await message.answer(
        "Введите пароль:",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(AuthStates.LOGIN_PASSWORD)


@router.message(AuthStates.LOGIN_PASSWORD)
async def login_password(message: Message, state: FSMContext):
    """Handle password input during login"""

    if message.text == BTN_CANCEL:
        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.clear()
        await state.set_state(AuthStates.START)
        return
    
    password = message.text.strip()
    
    data = await state.get_data()
    username = data.get("username")
    
    db = Database(DB_PATH)
    db.connect()
    
    success, msg, user_id = AuthenticationService.authenticate_user(
        db, username, password
    )
    db.close()
    
    if success:
        user_sessions[message.from_user.id] = user_id
        await message.answer(
            f"✅ {msg}",
            reply_markup=get_main_menu_keyboard(),
        )
        await state.set_state(MainMenuStates.MENU)
    else:
        await message.answer(f"❌ {msg}")
        await state.set_state(AuthStates.START)


@router.message(F.text == BTN_CANCEL)
async def cancel_handler(message: Message, state: FSMContext):
    """Handle cancel button"""
    current_state = await state.get_state()
    
    if current_state and current_state.startswith("AuthStates"):
        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.set_state(AuthStates.START)
    elif current_state and current_state.startswith("MainMenuStates"):
        await message.answer(MAIN_MENU_MESSAGE, reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
