import asyncio
from aiogram import types
from infrastructure.entrypoints.telegram.bot import main

if __name__ == "__main__":
    asyncio.run(main())

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Бот работает!")

