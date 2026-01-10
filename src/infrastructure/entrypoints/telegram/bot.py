import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))  # добавляем src

import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

import infrastructure.entrypoints.telegram.handlers as handlers
import infrastructure.entrypoints.telegram.middlewares as middlewares
from bootstrap.wiring import container

load_dotenv()
# Use TELEGRAM_TOKEN as defined in project .env
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Telegram token not found in environment variable TELEGRAM_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(handlers.router)
    dp.update.middleware(middlewares.AuthMiddleware())

    # Подключаем DI — передаем модули, а не экземпляры
    container.wire(modules=[handlers, middlewares])

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
