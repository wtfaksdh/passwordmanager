"""Password management handlers for Telegram Bot"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
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
from src.bot.handlers.auth import user_sessions

router = Router()

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
    

    is_valid, error_msg = Validators.validate_password(password)
    if not is_valid:
        await message.answer(error_msg)
        return
    
    data = await state.get_data()
    service = data.get("service")
    login = data.get("login")
    

    user_id = user_sessions.get(message.from_user.id)
    if not user_id:
        await message.answer("❌ Ошибка: пользователь не авторизован")
        return
    
    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    db.close()
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        return

    db = Database(DB_PATH)
    db.connect()
    
    success, msg = PasswordService.create_password(
        db,
        user_id,
        service,
        login,
        password,
        user.username,  
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
    

    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        db.close()
        return
    

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
    
    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        db.close()
        return
    

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

    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден")
        db.close()
        return

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


@router.message(MainMenuStates.DELETE_PASSWORD)
async def delete_password_handler(message: Message, state: FSMContext):
    """Handle password deletion after selection"""
    await message.answer("❌ Пожалуйста, выберите пароль из кнопок выше")


@router.callback_query(MainMenuStates.DELETE_PASSWORD)
async def delete_password_callback(callback: CallbackQuery, state: FSMContext):
    """Handle password deletion via callback"""
    try:
        password_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.message.answer("❌ Ошибка: неверный формат")
        await callback.answer()
        return
    
    db = Database(DB_PATH)
    db.connect()
    success = PasswordRepository.delete(db, password_id)
    db.close()
    
    if success:
        await callback.message.answer("✅ Пароль удален успешно!", reply_markup=get_main_menu_keyboard())
    else:
        await callback.message.answer("❌ Ошибка при удалении пароля", reply_markup=get_main_menu_keyboard())
    
    await state.set_state(MainMenuStates.MENU)
    await callback.answer()


@router.message(MainMenuStates.UPDATE_PASSWORD_ID)
async def update_password_id_handler(message: Message, state: FSMContext):
    """Handle password ID selection for update"""
    await message.answer("❌ Пожалуйста, выберите пароль из кнопок выше")


@router.callback_query(MainMenuStates.UPDATE_PASSWORD_ID)
async def update_password_id_callback(callback: CallbackQuery, state: FSMContext):
    """Handle password ID selection via callback"""
    try:
        password_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.message.answer("❌ Ошибка: неверный формат")
        await callback.answer()
        return

    db = Database(DB_PATH)
    db.connect()
    password = PasswordRepository.get_by_id(db, password_id)
    db.close()
    
    if not password:
        await callback.message.answer("❌ Ошибка: пароль не найден")
        await state.set_state(MainMenuStates.MENU)
        await callback.answer()
        return
    
    # Store password ID and ask what to update
    await state.update_data(password_id=password_id)
    await callback.message.answer(
        f"Выбран: {password.service}\n\nЧто обновить?\n1️⃣ Логин\n2️⃣ Пароль",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(MainMenuStates.UPDATE_PASSWORD_CHOICE)
    await callback.answer()


@router.message(MainMenuStates.UPDATE_PASSWORD_CHOICE)
async def update_password_choice_handler(message: Message, state: FSMContext):
    """Handle choice of what to update"""
    choice = message.text.strip().lower()
    
    if choice in ("1", "логин", "login", "1️⃣"):
        await message.answer("Введите новый логин:", reply_markup=get_cancel_keyboard())
        await state.set_state(MainMenuStates.UPDATE_PASSWORD_LOGIN)
    elif choice in ("2", "пароль", "password", "2️⃣"):
        await message.answer("Введите новый пароль:", reply_markup=get_cancel_keyboard())
        await state.set_state(MainMenuStates.UPDATE_PASSWORD_PASSWORD)
    else:
        await message.answer("❌ Пожалуйста, выберите 1 или 2")


@router.message(MainMenuStates.UPDATE_PASSWORD_LOGIN)
async def update_password_login_handler(message: Message, state: FSMContext):
    """Handle login update"""
    new_login = message.text.strip()
    
    data = await state.get_data()
    password_id = data.get("password_id")
    
    if not password_id:
        await message.answer("❌ Ошибка: пароль не найден")
        await state.set_state(MainMenuStates.MENU)
        return
    
    db = Database(DB_PATH)
    db.connect()
    password = PasswordRepository.get_by_id(db, password_id)
    
    if password:
        password.login = new_login
        success = PasswordRepository.update(db, password)
        db.close()
        
        if success:
            await message.answer("✅ Логин обновлен!", reply_markup=get_main_menu_keyboard())
        else:
            await message.answer("❌ Ошибка при обновлении", reply_markup=get_main_menu_keyboard())
    else:
        db.close()
        await message.answer("❌ Пароль не найден", reply_markup=get_main_menu_keyboard())
    
    await state.set_state(MainMenuStates.MENU)


@router.message(MainMenuStates.UPDATE_PASSWORD_PASSWORD)
async def update_password_password_handler(message: Message, state: FSMContext):
    """Handle password update"""
    new_password = message.text.strip()
    
    data = await state.get_data()
    password_id = data.get("password_id")
    user_id = user_sessions.get(message.from_user.id)
    
    if not password_id:
        await message.answer("❌ Ошибка: пароль не найден")
        await state.set_state(MainMenuStates.MENU)
        return
    
    if not user_id:
        await message.answer("❌ Ошибка: пользователь не авторизован")
        await state.set_state(MainMenuStates.MENU)
        return
    
    from src.database.crud import UserRepository
    db = Database(DB_PATH)
    db.connect()
    user = UserRepository.get_by_id(db, user_id)
    password = PasswordRepository.get_by_id(db, password_id)
    db.close()
    
    if not user or not password:
        await message.answer("❌ Ошибка: не найдены данные", reply_markup=get_main_menu_keyboard())
        await state.set_state(MainMenuStates.MENU)
        return
    
    from src.security import EncryptionService

    encrypted_pwd = EncryptionService.encrypt_password(new_password, user.username)
    password.password = encrypted_pwd
    
    db = Database(DB_PATH)
    db.connect()
    success = PasswordRepository.update(db, password)
    db.close()
    
    if success:
        await message.answer("✅ Пароль обновлен!", reply_markup=get_main_menu_keyboard())
    else:
        await message.answer("❌ Ошибка при обновлении пароля", reply_markup=get_main_menu_keyboard())
    
    await state.set_state(MainMenuStates.MENU)

