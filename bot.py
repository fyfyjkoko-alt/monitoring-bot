import os
import json
from datetime import datetime
from telebot import TeleBot

# اقرأ التوكن من متغيرات البيئة (أفضل أمان)
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
OWNER_ID = 123456789  # ضع آيدي حسابك هنا

bot = TeleBot(BOT_TOKEN)

FILES = {
    "blocked": "blocked.json",
    "logs": "logs.txt"
}

SUSPICIOUS_WORDS = ["ddos", "attack", "udp", "tcp", "flood"]

def init_files():
    if not os.path.exists(FILES["blocked"]):
        with open(FILES["blocked"], "w", encoding="utf-8") as f:
            json.dump([], f)

def log_event(text):
    with open(FILES["logs"], "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {text}\n")

def load_blocked():
    with open(FILES["blocked"], "r", encoding="utf-8") as f:
        return json.load(f)

def save_blocked(data):
    with open(FILES["blocked"], "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def is_blocked(user_id):
    return user_id in load_blocked()

def block_user(user_id):
    blocked = load_blocked()
    if user_id not in blocked:
        blocked.append(user_id)
        save_blocked(blocked)

@bot.message_handler(commands=["start"])
def start(msg):
    if is_blocked(msg.from_user.id):
        return
    bot.reply_to(msg, "🛡️ بوت المراقبة يعمل")

@bot.message_handler(commands=["status"])
def status(msg):
    bot.reply_to(msg, "✅ البوت يعمل بدون مشاكل")

@bot.message_handler(commands=["blocked"])
def blocked_list(msg):
    if msg.from_user.id != OWNER_ID:
        return
    blocked = load_blocked()
    bot.reply_to(msg, "🚫 المحظورون:\n" + "\n".join(map(str, blocked)))

@bot.message_handler(commands=["unblock"])
def unblock(msg):
    if msg.from_user.id != OWNER_ID:
        return
    try:
        _, uid = msg.text.split()
        uid = int(uid)
        blocked = load_blocked()
        if uid in blocked:
            blocked.remove(uid)
            save_blocked(blocked)
        bot.reply_to(msg, f"✅ تم فك الحظر عن {uid}")
    except:
        bot.reply_to(msg, "❌ استخدم: /unblock USER_ID")

@bot.message_handler(func=lambda m: True)
def monitor(msg):
    user = msg.from_user
    text = (msg.text or "").lower()

    if is_blocked(user.id):
        return

    if any(word in text for word in SUSPICIOUS_WORDS):
        log_event(f"BLOCKED | user_id={user.id} | username={user.username} | text={msg.text}")
        block_user(user.id)

        try:
            bot.send_message(
                OWNER_ID,
                f"🚨 حظر تلقائي\n👤 ID: {user.id}\n👤 USER: @{user.username}\n💬 MSG: {msg.text}"
            )
        except:
            pass

        bot.reply_to(msg, "🚫 تم حظرك بسبب نشاط مشبوه")

init_files()
print("🛡️ Monitoring Bot Running...")
bot.infinity_polling()
