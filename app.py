from flask import Flask, request
import telebot
import os

# 🔹 Environment o'zgaruvchilarni o'qish (Railway Variables'dan)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 🔹 Telegram webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# 🔹 Oddiy home route
@app.route("/")
def home():
    return "Bot is running on Railway 🚀"

# 🔹 Flask 3.0 uchun to'g'ri start event
@app.before_request
def startup_once():
    if not getattr(app, "initialized", False):
        app.initialized = True
        # webhook ni o'rnatish
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBAPP_URL}/{BOT_TOKEN}")
        print("✅ Webhook set successfully!")

# 🔹 Har bir yangi xabar uchun handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Salom! 👋 Bot muvaffaqiyatli ishlamoqda 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# 🔹 Flask serverni ishga tushirish
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
