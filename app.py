from flask import Flask, render_template, request
import os
import telebot

app = Flask(__name__)

# 🔹 Environment variable'larni o'qish
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 🔹 Agar token yoki URL yo‘q bo‘lsa — xato chiqaramiz
if not BOT_TOKEN or not WEBAPP_URL:
    raise ValueError("❌ BOT_TOKEN yoki WEBAPP_URL topilmadi. Railway Variables bo‘limini tekshiring!")

bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Telegram webhookni sozlash
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def getMessage():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/")
def index():
    return render_template("index.html")  # templates/index.html ni ochadi


# 🔹 Webhook o‘rnatish
@app.before_first_request
def before_first_request():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBAPP_URL}/{BOT_TOKEN}")


# 🔹 Bot komandasi
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 Ruda mini ilova ishga tushdi!")


if __name__ == "__main__":
    # Railway avtomatik PORT beradi
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
