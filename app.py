from flask import Flask, render_template, request, jsonify
import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")  # sizning telegram ID’ingiz
WEBAPP_URL = os.environ.get("WEBAPP_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Har bir foydalanuvchi uchun tanga miqdori (oddiy xotirada)
users_data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/click", methods=["POST"])
def click():
    user_id = request.form.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id kerak"}), 400

    users_data[user_id] = users_data.get(user_id, 0) + 1
    return jsonify({"coins": users_data[user_id]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    user_id = data["user_id"]
    address = data["address"]
    amount = data["amount"]

    text = f"💰 Yangi yechish so‘rovi:\n👤 ID: {user_id}\n💸 Miqdor: {amount} TIN\n🏦 Hamyon: {address}"
    bot.send_message(ADMIN_ID, text)
    return jsonify({"status": "success"})

@app.route("/admin_confirm", methods=["POST"])
def admin_confirm():
    data = request.get_json()
    user_id = data["user_id"]
    bot.send_message(user_id, "✅ Sizga pul hamyoningizga tushdi!")
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
