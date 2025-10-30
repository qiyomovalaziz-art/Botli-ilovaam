import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
import os
from flask import Flask, render_template

# Bot tokenni olamiz
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask ilova
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Aiogram setup
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Salom! Bot muvaffaqiyatli ishga tushdi 🚀")

async def run_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=8080)
