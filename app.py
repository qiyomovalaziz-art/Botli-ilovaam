# app.py
import os
from flask import Flask, render_template, request, jsonify
from db import init_db, ensure_user, get_balance, change_balance

init_db()
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    # WebApp URL bo'lib bot web_app ga shu URL beriladi
    return render_template("index.html")

# API: foydalanuvchi id bilan balansni olish
@app.route("/api/balance", methods=["POST"])
def api_balance():
    data = request.json or {}
    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"ok": False, "error": "user_id required"}), 400
    ensure_user(user_id, data.get("first_name", ""))
    bal = get_balance(user_id)
    return jsonify({"ok": True, "balance": bal})

# API: "ruda" coin claim qilish (bepul coin berish misoli)
@app.route("/api/claim", methods=["POST"])
def api_claim():
    data = request.json or {}
    user_id = data.get("user_id")
    amount = float(data.get("amount", 1))  # default 1 Ruda
    if user_id is None:
        return jsonify({"ok": False, "error": "user_id required"}), 400
    new_bal = change_balance(user_id, amount)
    return jsonify({"ok": True, "balance": new_bal, "added": amount})

# API: depozit (pul qo'yish) — demo (real payment integratsiya emas)
@app.route("/api/deposit", methods=["POST"])
def api_deposit():
    data = request.json or {}
    user_id = data.get("user_id")
    amount = float(data.get("amount", 0))
    if user_id is None or amount <= 0:
        return jsonify({"ok": False, "error": "user_id and positive amount required"}), 400
    new_bal = change_balance(user_id, amount)
    return jsonify({"ok": True, "balance": new_bal})

# API: withdraw (yechib olish) — demo: balansdan kamaytiradi
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
