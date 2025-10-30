# bot.py
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("Set BOT_TOKEN env var")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Railway yoki sizning URL ni quyiga qo'ying, masalan: https://your-app.up.railway.app/
    WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://your-railway-url.example.com/")
    webapp = types.WebAppInfo(url=WEBAPP_URL)
    keyboard.add(types.KeyboardButton(text="Ruda Mini Ilova", web_app=webapp))
    await message.answer("Mini ilovani ochish uchun tugmani bosing 👇", reply_markup=keyboard)

if __name__ == "__main__":
    # Botni worker sifatida ishga tushiring (railway worker)
    executor.start_polling(dp)
