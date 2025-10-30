import os
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("Set BOT_TOKEN env var")
    exit(1)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    @dp.message(commands=['start'])
    async def start(message: types.Message):
        WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://your-railway-url.example.com/")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        webapp = WebAppInfo(url=WEBAPP_URL)
        keyboard.add(types.KeyboardButton(text="Ruda Mini Ilova", web_app=webapp))
        await message.answer("Mini ilovani ochish uchun tugmani bosing 👇", reply_markup=keyboard)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
