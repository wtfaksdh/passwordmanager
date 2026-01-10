from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dependency_injector.wiring import Provide, inject
from bootstrap.wiring import Container

from infrastructure.entrypoints.telegram.keyboards import main_menu
from infrastructure.entrypoints.telegram.presenters import (
    welcome_text,
    password_saved,
    ask_service,
    ask_login,
    ask_password,
)
from core.application.dto.user_context import UserContext
from core.application.dto.password_input import PasswordInput
from core.domain.enums.category import Category
from core.domain.value_objects.url import URL
from core.domain.enums.cipher_type import CipherType
from core.domain.entities.user import User
from core.domain.value_objects.email import Email
from core.domain.policies.password_policy import PasswordPolicy
from core.domain.exceptions.weak_password import WeakPasswordError
import os
import hashlib
import sqlite3

router = Router()

class RegistrationState(StatesGroup):
    email = State()
    password = State()
    confirm_password = State()

class AddPassword(StatesGroup):
    service = State()
    login = State()
    password = State()

# Helper to create password hash
def hash_password(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

@router.message(Command("start"))
async def start(message: Message):
    """Show registration or main menu"""
    await message.answer(
        "Добро пожаловать в Password Manager! 🔐\n\n"
        "Что вы хотите сделать?",
        reply_markup=await get_auth_keyboard()
    )

async def get_auth_keyboard():
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Зарегистрироваться", callback_data="register")],
        [InlineKeyboardButton(text="🔓 Войти в систему", callback_data="login")],
    ])

async def get_main_keyboard():
    return main_menu()

@router.callback_query(F.data == "register")
async def register_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.email)
    await callback.message.answer(
        "Введите вашу электронную почту:\n\n"
        "Пример: user@example.com"
    )

@router.message(RegistrationState.email)
async def register_email(message: Message, state: FSMContext):
    email_text = message.text.strip()
    try:
        # Validate email format
        email = Email(email_text)
        await state.update_data(email=email_text)
        await state.set_state(RegistrationState.password)
        await message.answer(
            "Введите пароль.\n\n"
            "Требования к паролю:\n"
            "✓ Минимум 8 символов\n"
            "✓ Одна большая буква (A-Z)\n"
            "✓ Одна маленькая буква (a-z)\n"
            "✓ Одна цифра (0-9)\n"
            "✓ Один специальный символ (!@#$%^&* и т.д.)"
        )
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {str(e)}\n\nПожалуйста, введите корректный email:")

@router.message(RegistrationState.password)
async def register_password(message: Message, state: FSMContext):
    password = message.text.strip()
    try:
        # Validate password strength
        PasswordPolicy.validate(password)
        await state.update_data(password=password)
        await state.set_state(RegistrationState.confirm_password)
        await message.answer("Подтвердите пароль еще раз:")
    except WeakPasswordError as e:
        await message.answer(f"❌ Пароль не соответствует требованиям:\n{str(e)}\n\nПожалуйста, введите пароль заново:")

@router.message(RegistrationState.confirm_password)
@inject
async def register_confirm(
    message: Message,
    state: FSMContext,
    user_repo = Provide[Container.user_repository],
    key_store = Provide[Container.key_store],
):
    password = message.text.strip()
    data = await state.get_data()
    
    if password != data["password"]:
        await message.answer("❌ Пароли не совпадают. Введите пароль заново:")
        await state.set_state(RegistrationState.password)
        return
    
    try:
        # Create user data
        user_id = message.from_user.id
        email = Email(data["email"])
        password_hash = hash_password(data["password"])
        salt = os.urandom(16)

        username = f"user_{user_id}"

        # Check existing by id or username
        if user_repo.get_user(user_id) is not None:
            await state.clear()
            await message.answer("✅ Вы уже зарегистрированы.", reply_markup=await get_main_keyboard())
            return
        if user_repo.find_by_username(username) is not None:
            await state.clear()
            await message.answer("❌ Пользователь с таким именем уже существует. Пожалуйста, войдите.", reply_markup=await get_auth_keyboard())
            return

        new_user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt
        )

        try:
            user_repo.create_user(new_user)
        except sqlite3.IntegrityError:
            await state.clear()
            await message.answer("❌ Пользователь уже существует (конфликт). Попробуйте войти.", reply_markup=await get_auth_keyboard())
            return

        # Generate and store encryption key
        encryption_key = os.urandom(32)
        key_store.store_key(user_id, encryption_key)

        await state.clear()
        await message.answer(
            f"✅ Регистрация успешна!\n"
            f"Email: {data['email']}\n\n"
            f"Добро пожаловать в Password Manager! 🎉",
            reply_markup=await get_main_keyboard()
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при регистрации: {str(e)}")
        await state.clear()

@router.callback_query(F.data == "login")
@inject
async def login_start(
    callback: CallbackQuery,
    state: FSMContext,
    user_repo = Provide[Container.user_repository],
):
    # Check if user exists
    user = user_repo.get_user(callback.from_user.id)
    if user:
        # User already registered
        await callback.message.answer(
            "✅ Вы уже в системе!",
            reply_markup=await get_main_keyboard()
        )
    else:
        await callback.message.answer(
            "❌ Вы еще не зарегистрированы.\n\n"
            "Пожалуйста, зарегистрируйтесь сначала.",
            reply_markup=await get_auth_keyboard()
        )

@router.callback_query(F.data == "add_password")
async def add_password(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPassword.service)
    await callback.message.answer(ask_service())

@router.message(AddPassword.service)
async def service_step(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(AddPassword.login)
    await message.answer(ask_login())

@router.message(AddPassword.login)
async def login_step(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(AddPassword.password)
    await message.answer(ask_password())

@router.message(AddPassword.password)
@inject
async def password_step(
    message: Message,
    state: FSMContext,
    create_password_use_case = Provide[Container.create_password_use_case],
):
    try:
        data = await state.get_data()
        user_context = UserContext(user_id=message.from_user.id)
        pwd_input = PasswordInput(
            name=data["service"],
            category=Category.PERSONAL,
            url=URL("https://example.com"),
            password=message.text,
            cipher_type=CipherType.AES_GCM
        )
        create_password_use_case.execute(user_context, pwd_input)
        await state.clear()
        await message.answer(password_saved(), reply_markup=await get_main_keyboard(), parse_mode="Markdown")
    except Exception as e:
        await state.clear()
        await message.answer(f"❌ Ошибка: {str(e)}", reply_markup=await get_main_keyboard())

@router.callback_query(F.data == "list_passwords")
@inject
async def list_passwords(
    callback: CallbackQuery,
    list_passwords_use_case = Provide[Container.list_passwords_use_case],
):
    try:
        user_context = UserContext(user_id=callback.from_user.id)
        passwords = list_passwords_use_case.execute(user_context)
        if not passwords:
            text = "📭 Список паролей пуст"
        else:
            text = "🔐 Ваши сохраненные пароли:\n\n" + "\n".join([f"🔑 {p.name}\n   Пароль: {p.password}" for p in passwords])
        await callback.message.answer(text, reply_markup=await get_main_keyboard())
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {str(e)}", reply_markup=await get_main_keyboard())
