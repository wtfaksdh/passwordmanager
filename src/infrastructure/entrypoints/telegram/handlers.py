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

router = Router()

class AddPassword(StatesGroup):
    service = State()
    login = State()
    password = State()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        welcome_text(),
        reply_markup=main_menu(),
        parse_mode="Markdown"
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
    data = await state.get_data()
    create_password_use_case.execute(
        service=data["service"],
        login=data["login"],
        password=message.text,
        telegram_id=message.from_user.id
    )
    await state.clear()
    await message.answer(password_saved(), reply_markup=main_menu(), parse_mode="Markdown")

@router.callback_query(F.data == "list_passwords")
@inject
async def list_passwords(
    callback: CallbackQuery,
    list_passwords_use_case = Provide[Container.list_passwords_use_case],
):
    passwords = list_passwords_use_case.execute(telegram_id=callback.from_user.id)
    if not passwords:
        text = "📭 Список паролей пуст"
    else:
        text = "\n".join([f"{p.service}: {p.login} / {p.encrypted_password}" for p in passwords])
    await callback.message.answer(text, reply_markup=main_menu())
