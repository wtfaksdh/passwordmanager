from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from infrastructure.entrypoints.telegram.keyboards import main_menu
from infrastructure.entrypoints.telegram.presenters import (
    welcome_text,
    password_saved,
    ask_service,
    ask_login,
    ask_password,
)

from bootstrap.wiring import build_use_cases

router = Router()
use_cases = build_use_cases()

# FSM
class AddPassword(StatesGroup):
    service = State()
    login = State()
    password = State()

# /start
@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        welcome_text(),
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# Нажали "Добавить пароль"
@router.callback_query(F.data == "add_password")
async def add_password(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPassword.service)
    await callback.message.answer(ask_service())

# Ввод сервиса
@router.message(AddPassword.service)
async def service_step(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(AddPassword.login)
    await message.answer(ask_login())

# Ввод логина
@router.message(AddPassword.login)
async def login_step(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(AddPassword.password)
    await message.answer(ask_password())

# 🔥 ВЫЗОВ BACKEND
@router.message(AddPassword.password)
async def password_step(message: Message, state: FSMContext):
    data = await state.get_data()

    use_cases["create_password"].execute(
        service=data["service"],
        login=data["login"],
        password=message.text,
        telegram_id=message.from_user.id
    )

    await state.clear()
    await message.answer(
        password_saved(),
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
