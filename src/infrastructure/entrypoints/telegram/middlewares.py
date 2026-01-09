from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from dependency_injector.wiring import Provide, inject
from bootstrap.wiring import Container

class AuthMiddleware(BaseMiddleware):

    @inject
    def __init__(self, user_repo = Provide[Container.password_repository]):
        # Используем password_repository как пример, можно заменить на UserRepository
        self.user_repo = user_repo
        super().__init__()

    async def __call__(self, handler, event, data):
        telegram_id = None
        if isinstance(event, Message) or isinstance(event, CallbackQuery):
            telegram_id = event.from_user.id

        if telegram_id and not self.user_repo.exists(telegram_id):
            if isinstance(event, Message):
                await event.answer("❌ Вы не зарегистрированы. Пожалуйста, создайте аккаунт через init_user.py")
            elif isinstance(event, CallbackQuery):
                await event.message.answer("❌ Вы не зарегистрированы. Пожалуйста, создайте аккаунт через init_user.py")
            return  # блокируем обработку
        return await handler(event, data)
