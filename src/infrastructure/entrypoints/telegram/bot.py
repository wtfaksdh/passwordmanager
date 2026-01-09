import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from infrastructure.entrypoints.telegram.handlers import router
from infrastructure.entrypoints.telegram.middlewares import AuthMiddleware
from bootstrap.wiring import container

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)
    dp.update.middleware(AuthMiddleware())

    # Подключаем DI
    container.wire(modules=[router, AuthMiddleware])

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

