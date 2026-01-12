"""Telegram Bot handlers"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from src.config import *
from src.bot.keyboards import (
    get_auth_keyboard,
    get_main_menu_keyboard,
    get_cancel_keyboard,
    get_confirm_keyboard,
    get_passwords_inline_keyboard,
)
from src.database.db import Database
from src.database.crud import UserRepository, PasswordRepository
from src.database.models import Password, User
from src.security.encryption import EncryptionService

router = Router()

user_sessions = {}


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Start command handler"""
    user_id = message.from_user.id
    if user_id in user_sessions:
        await message.answer(MAIN_MENU, reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
    else:
        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.set_state(AuthStates.START)


@router.message(AuthStates.START, F.text == BTN_REGISTER)
async def register_start(message: Message, state: FSMContext):
    """Start registration"""
    await message.answer("Введите имя пользователя:", reply_markup=get_cancel_keyboard())
    await state.set_state(AuthStates.REGISTER_USERNAME)


@router.message(AuthStates.REGISTER_USERNAME)
async def register_username(message: Message, state: FSMContext):
    """Register username"""
    username = message.text.strip()

    if len(username) < 3:
        await message.answer("Имя пользователя должно содержать минимум 3 символа.")
        return

    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_username(db, username)
    db.disconnect()

    if user:
        await message.answer(ERROR_USER_EXISTS)
        return

    await state.update_data(username=username)
    await message.answer("Введите пароль:", reply_markup=get_cancel_keyboard())
    await state.set_state(AuthStates.REGISTER_PASSWORD)


@router.message(AuthStates.REGISTER_PASSWORD)
async def register_password(message: Message, state: FSMContext):
    """Register password"""
    password = message.text.strip()

    if len(password) < 4:
        await message.answer("Пароль должен содержать минимум 4 символа.")
        return

    data = await state.get_data()
    username = data.get("username")

    encrypted_password = EncryptionService.encrypt_password(password, password)
    user = User(username=username, password_hash=encrypted_password)
    db = Database(DB_PATH)
    db.connect()
    user_id = UserRepository.create(db, user)
    db.disconnect()

    if user_id:
        user_sessions[message.from_user.id] = user_id
        await message.answer(REGISTER_SUCCESS, reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
    else:
        await message.answer("Ошибка при создании аккаунта. Попробуйте еще раз.")
        await state.set_state(AuthStates.START)


@router.message(AuthStates.START, F.text == BTN_LOGIN)
async def login_start(message: Message, state: FSMContext):
    """Start login"""
    await message.answer("Введите имя пользователя:", reply_markup=get_cancel_keyboard())
    await state.set_state(AuthStates.LOGIN_USERNAME)


@router.message(AuthStates.LOGIN_USERNAME)
async def login_username(message: Message, state: FSMContext):
    """Login username"""
    username = message.text.strip()
    await state.update_data(username=username)
    await message.answer("Введите пароль:", reply_markup=get_cancel_keyboard())
    await state.set_state(AuthStates.LOGIN_PASSWORD)


@router.message(AuthStates.LOGIN_PASSWORD)
async def login_password(message: Message, state: FSMContext):
    """Login password"""
    password = message.text.strip()
    data = await state.get_data()
    username = data.get("username")

    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_username(db, username)
    db.disconnect()
    
    user_found = None
    if user:
        try:
            decrypted = EncryptionService.decrypt_password(user.password_hash, password)
            if decrypted == password:
                user_found = user
        except:
            user_found = None
    
    if user_found:
        user_sessions[message.from_user.id] = user_found.id
        await message.answer(LOGIN_SUCCESS, reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
    else:
        await message.answer(ERROR_INVALID_CREDENTIALS)
        await state.set_state(AuthStates.START)


@router.message(MainMenuStates.MENU, F.text == BTN_ADD_PASSWORD)
async def add_password_service(message: Message, state: FSMContext):
    """Add password - service"""
    await message.answer("Введите название сервиса (например: Gmail, GitHub):", reply_markup=get_cancel_keyboard())
    await state.set_state(MainMenuStates.ADD_PASSWORD_SERVICE)


@router.message(MainMenuStates.ADD_PASSWORD_SERVICE)
async def add_password_login(message: Message, state: FSMContext):
    """Add password - login"""
    service = message.text.strip()
    if not service:
        await message.answer("Название сервиса не может быть пустым.")
        return

    await state.update_data(service=service)
    await message.answer("Введите логин/email:", reply_markup=get_cancel_keyboard())
    await state.set_state(MainMenuStates.ADD_PASSWORD_LOGIN)


@router.message(MainMenuStates.ADD_PASSWORD_LOGIN)
async def add_password_password(message: Message, state: FSMContext):
    """Add password - password"""
    login = message.text.strip()
    if not login:
        await message.answer("Логин не может быть пустым.")
        return

    await state.update_data(login=login)
    await message.answer("Введите пароль:", reply_markup=get_cancel_keyboard())
    await state.set_state(MainMenuStates.ADD_PASSWORD_PASSWORD)


@router.message(MainMenuStates.ADD_PASSWORD_PASSWORD)
async def save_password(message: Message, state: FSMContext):
    """Save password"""
    password = message.text.strip()
    if not password:
        await message.answer("Пароль не может быть пустым.")
        return

    data = await state.get_data()
    user_id = user_sessions.get(message.from_user.id)

    if not user_id:
        await message.answer("Ошибка: аккаунт не найден.")
        await state.set_state(AuthStates.START)
        return

    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    db.disconnect()
    
    if not user:
        await message.answer("Ошибка: аккаунт не найден.")
        await state.set_state(AuthStates.START)
        return
    
    encrypted_pwd = EncryptionService.encrypt_password(password, user.password_hash.split(':')[0])
    pwd_obj = Password(
        user_id=user_id,
        service=data.get("service"),
        login=data.get("login"),
        password=encrypted_pwd,
    )

    db = Database(DB_PATH)
    db.connect()
    pwd_id = PasswordRepository.create(db, pwd_obj)
    db.disconnect()

    if pwd_id:
        await message.answer(
            "✅ Пароль сохранен успешно!",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer("❌ Ошибка при сохранении пароля.")

    await state.set_state(MainMenuStates.MENU)


@router.message(MainMenuStates.MENU, F.text == BTN_VIEW_PASSWORDS)
async def view_passwords(message: Message, state: FSMContext):
    """View passwords"""
    user_id = user_sessions.get(message.from_user.id)

    if not user_id:
        await message.answer("Ошибка: аккаунт не найден.")
        await state.set_state(AuthStates.START)
        return

    db = Database(DB_PATH)
    db.connect()
    passwords = PasswordRepository.get_by_user(db, user_id)
    user = UserRepository.get_by_id(db, user_id)
    db.disconnect()

    if not passwords:
        await message.answer(
            "У вас нет сохраненных паролей.",
            reply_markup=get_main_menu_keyboard()
        )
        await state.set_state(MainMenuStates.MENU)
        return

    response = "📝 Ваши пароли:\n\n"
    for pwd in passwords:
        try:
            decrypted_pwd = EncryptionService.decrypt_password(pwd.password, user.password_hash.split(':')[0])
        except:
            decrypted_pwd = "[Не удалось расшифровать]"
        response += f"🔹 <b>{pwd.service}</b>\n"
        response += f"   Логин: <code>{pwd.login}</code>\n"
        response += f"   Пароль: <code>{decrypted_pwd}</code>\n\n"

    await message.answer(response, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    await state.set_state(MainMenuStates.MENU)


@router.message(MainMenuStates.MENU, F.text == BTN_DELETE_PASSWORD)
async def delete_password_menu(message: Message, state: FSMContext):
    """Delete password menu"""
    user_id = user_sessions.get(message.from_user.id)

    if not user_id:
        await message.answer("Ошибка: аккаунт не найден.")
        await state.set_state(AuthStates.START)
        return

    db = Database(DB_PATH)
    db.connect()
    passwords = PasswordRepository.get_by_user(db, user_id)
    db.disconnect()

    if not passwords:
        await message.answer(
            "У вас нет сохраненных паролей.",
            reply_markup=get_main_menu_keyboard()
        )
        await state.set_state(MainMenuStates.MENU)
        return

    password_ids = [pwd.id for pwd in passwords]
    password_data = [(pwd.service, pwd.login) for pwd in passwords]

    await message.answer(
        "Выберите пароль для удаления:",
        reply_markup=get_passwords_inline_keyboard(password_ids, password_data)
    )
    await state.set_state(MainMenuStates.DELETE_PASSWORD)


@router.callback_query(MainMenuStates.DELETE_PASSWORD)
async def delete_password_confirm(callback: CallbackQuery, state: FSMContext):
    """Delete password confirm"""
    pwd_id = int(callback.data.split("_")[1])
    await state.update_data(password_id=pwd_id)

    db = Database(DB_PATH)
    db.connect()
    pwd = PasswordRepository.get_by_id(db, pwd_id)
    db.disconnect()

    if pwd:
        await callback.message.answer(
            f"Вы уверены, что хотите удалить пароль для <b>{pwd.service}</b>?",
            reply_markup=get_confirm_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(MainMenuStates.DELETE_PASSWORD)
    else:
        await callback.message.answer("Пароль не найден.", reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)

    await callback.answer()


@router.message(MainMenuStates.DELETE_PASSWORD, F.text == BTN_CONFIRM)
async def delete_password_execute(message: Message, state: FSMContext):
    """Execute delete password"""
    data = await state.get_data()
    pwd_id = data.get("password_id")

    if pwd_id:
        db = Database(DB_PATH)
        db.connect()
        success = PasswordRepository.delete(db, pwd_id)
        db.disconnect()

        if success:
            await message.answer(
                "✅ Пароль удален успешно!",
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await message.answer(
                "❌ Ошибка при удалении пароля.",
                reply_markup=get_main_menu_keyboard()
            )

    await state.set_state(MainMenuStates.MENU)


@router.message(MainMenuStates.MENU, F.text == BTN_UPDATE_PASSWORD)
async def update_password_menu(message: Message, state: FSMContext):
    """Update password menu"""
    user_id = user_sessions.get(message.from_user.id)

    if not user_id:
        await message.answer("Ошибка: аккаунт не найден.")
        await state.set_state(AuthStates.START)
        return

    db = Database(DB_PATH)
    db.connect()
    passwords = PasswordRepository.get_by_user(db, user_id)
    db.disconnect()

    if not passwords:
        await message.answer(
            "У вас нет сохраненных паролей.",
            reply_markup=get_main_menu_keyboard()
        )
        await state.set_state(MainMenuStates.MENU)
        return

    password_ids = [pwd.id for pwd in passwords]
    password_data = [(pwd.service, pwd.login) for pwd in passwords]

    await message.answer(
        "Выберите пароль для обновления:",
        reply_markup=get_passwords_inline_keyboard(password_ids, password_data)
    )
    await state.set_state(MainMenuStates.UPDATE_PASSWORD)


@router.callback_query(MainMenuStates.UPDATE_PASSWORD)
async def update_password_select(callback: CallbackQuery, state: FSMContext):
    """Update password select"""
    pwd_id = int(callback.data.split("_")[1])
    await state.update_data(password_id=pwd_id)

    db = Database(DB_PATH)
    db.connect()
    pwd = PasswordRepository.get_by_id(db, pwd_id)
    db.disconnect()

    if pwd:
        await callback.message.answer(
            f"Что вы хотите обновить для <b>{pwd.service}</b>?\n"
            f"1️⃣ Логин\n"
            f"2️⃣ Пароль",
            reply_markup=get_cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(MainMenuStates.UPDATE_PASSWORD)
    else:
        await callback.message.answer("Пароль не найден.", reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)

    await callback.answer()


@router.message(MainMenuStates.MENU, F.text == BTN_LOGOUT)
async def logout(message: Message, state: FSMContext):
    """Logout"""
    user_id = message.from_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]

    await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
    await state.set_state(AuthStates.START)


@router.message(F.text == BTN_CANCEL)
async def cancel_operation(message: Message, state: FSMContext):
    """Cancel operation"""
    user_id = message.from_user.id

    current_state = await state.get_state()

    try:
        await state.clear()
    except Exception:
        try:
            await state.clear_data()
        except Exception:
            pass

    if current_state and ("REGISTER" in current_state or "LOGIN" in current_state):
        await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
        await state.set_state(AuthStates.START)
        return

    if user_id in user_sessions:
        await message.answer(MAIN_MENU, reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
        return

    await message.answer(WELCOME_MESSAGE, reply_markup=get_auth_keyboard())
    await state.set_state(AuthStates.START)

@router.message(MainMenuStates.UPDATE_PASSWORD)
async def update_password_choice(message: Message, state: FSMContext):
    """Handle choice: update login or password"""
    text = message.text.strip().lower()

    if text in ("1", "1️⃣", "логин", "login"):
        await message.answer("Введите новый логин:", reply_markup=get_cancel_keyboard())
        await state.set_state(MainMenuStates.UPDATE_PASSWORD_LOGIN)
        return

    if text in ("2", "2️⃣", "пароль", "password"):
        await message.answer("Введите новый пароль:", reply_markup=get_cancel_keyboard())
        await state.set_state(MainMenuStates.UPDATE_PASSWORD_PASSWORD)
        return

    await message.answer("Пожалуйста, введите '1' для логина или '2' для пароля.")


@router.message(MainMenuStates.UPDATE_PASSWORD_LOGIN)
async def update_password_login(message: Message, state: FSMContext):
    """Update the login for the selected password record"""
    new_login = message.text.strip()
    data = await state.get_data()
    pwd_id = data.get("password_id")

    if not pwd_id:
        await message.answer("Ошибка: выбранный пароль не найден.", reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
        return

    db = Database(DB_PATH)
    db.connect()
    pwd = PasswordRepository.get_by_id(db, pwd_id)
    db.disconnect()
    
    if not pwd:
        await message.answer("Ошибка: пароль не найден.", reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
        return

    pwd.login = new_login
    db = Database(DB_PATH)
    db.connect()
    success = PasswordRepository.update(db, pwd)
    db.disconnect()

    if success:
        await message.answer("✅ Логин успешно обновлен.", reply_markup=get_main_menu_keyboard())
    else:
        await message.answer("❌ Ошибка при обновлении логина.", reply_markup=get_main_menu_keyboard())

    await state.set_state(MainMenuStates.MENU)


@router.message(MainMenuStates.UPDATE_PASSWORD_PASSWORD)
async def update_password_password(message: Message, state: FSMContext):
    """Update the password for the selected password record"""
    new_password = message.text.strip()
    data = await state.get_data()
    pwd_id = data.get("password_id")

    if not pwd_id:
        await message.answer("Ошибка: выбранный пароль не найден.", reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
        return

    db = Database(DB_PATH)
    db.connect()
    pwd = PasswordRepository.get_by_id(db, pwd_id)
    user = UserRepository.get_by_id(db, pwd.user_id)
    db.disconnect()
    
    if not pwd or not user:
        await message.answer("Ошибка: пароль или пользователь не найден.", reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
        return

    encrypted_pwd = EncryptionService.encrypt_password(new_password, user.password_hash.split(':')[0])
    pwd.password = encrypted_pwd
    db = Database(DB_PATH)
    db.connect()
    success = PasswordRepository.update(db, pwd)
    db.disconnect()

    if success:
        await message.answer("✅ Пароль успешно обновлен.", reply_markup=get_main_menu_keyboard())
    else:
        await message.answer("❌ Ошибка при обновлении пароля.", reply_markup=get_main_menu_keyboard())

    await state.set_state(MainMenuStates.MENU)
