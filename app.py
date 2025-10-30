import os
import threading
from flask import Flask, render_template, request, jsonify
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from db import init_db, ensure_user, get_balance, change_balance

# ---------------- Flask qismi ----------------
init_db()
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/balance", methods=["POST"])
def api_balance():
    data = request.json or {}
    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"ok": False, "error": "user_id required"}), 400
    ensure_user(user_id, data.get("first_name", ""))
    bal = get_balance(user_id)
    return jsonify({"ok": True, "balance": bal})

@app.route("/api/claim", methods=["POST"])
def api_claim():
    data = request.json or {}
    user_id = data.get("user_id")
    amount = float(data.get("amount", 1))
    if user_id is None:
        return jsonify({"ok": False, "error": "user_id required"}), 400
    new_bal = change_balance(user_id, amount)
    return jsonify({"ok": True, "balance": new_bal, "added": amount})

@app.route("/api/deposit", methods=["POST"])
def api_deposit():
    data = request.json or {}
    user_id = data.get("user_id")
    amount = float(data.get("amount", 0))
    if user_id is None or amount <= 0:
        return jsonify({"ok": False, "error": "user_id and positive amount required"}), 400
    new_bal = change_balance(user_id, amount)
    return jsonify({"ok": True, "balance": new_bal})

@app.route("/api/withdraw", methods=["POST"])
def api_withdraw():
    data = request.json or {}
    user_id = data.get("user_id")
    amount = float(data.get("amount", 0))
    if user_id is None or amount <= 0:
        return jsonify({"ok": False, "error": "user_id and positive amount required"}), 400
    current = get_balance(user_id)
    if current < amount:
        return jsonify({"ok": False, "error": "Insufficient balance"}), 400
    new_bal = change_balance(user_id, -amount)
    return jsonify({"ok": True, "balance": new_bal})

# ---------------- Aiogram (bot) qismi ----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://your-railway-url.example.com/")

if not BOT_TOKEN:
    print("⚠️ BOT_TOKEN environment variable not set!")
else:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        webapp = types.WebAppInfo(url=WEBAPP_URL)
        keyboard.add(types.KeyboardButton(text="Ruda Mini Ilova", web_app=webapp))
        await message.answer("Mini ilovani ochish uchun tugmani bosing 👇", reply_markup=keyboard)

    def start_bot():
        executor.start_polling(dp, skip_updates=True)

    # Botni alohida oqimda ishga tushiramiz
    threading.Thread(target=start_bot).start()

# ---------------- Flask ishga tushurish ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
