import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
from flask import Flask
import os

# ========== تنظیمات ربات ==========
TOKEN = "8671080185:AAEebKGBWKApR5GB5XzRAH3mYzzFhIK_X0A"
bot = telebot.TeleBot(TOKEN)

CHANNEL_USERNAME = "@donyaye_serial_kootah"
YOUTUBE_LINK = "https://youtube.com/@donyaye_serial_kootah"
INSTAGRAM_LINK = "https://instagram.com/donyaye_serial_kootah"

MOVIES = {
    "film1": "BAACAgQAAxkBAAMCapglaTbvNfwDeoRsoPg2Lxs8D1wAArofAALXGUlTgCTlkU4zRto9BA","film2":"BAACAgEAAxkBAAMUapgt1kl1eAag01C7Ov8z7efcePYAAu0CAAKJfyBGhlhcpeLk5Ck9BA",
    # ... مابقی فیلم‌ها
}

# ========== توابع ربات (بدون تغییر) ==========
def delete_after_delay(chat_id, message_id, delay=60):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

def is_member(user_id):
    try:
        return bot.get_chat_member(CHANNEL_USERNAME, user_id).status in ["member", "creator", "administrator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_member(user_id):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📺 یوتیوب", url=YOUTUBE_LINK),
            InlineKeyboardButton("📸 اینستاگرام", url=INSTAGRAM_LINK),
            InlineKeyboardButton("📢 کانال تلگرام", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        )
        bot.send_message(
            user_id,
            f"🎬 برای دریافت فیلم، ابتدا در کانال {CHANNEL_USERNAME} عضو شوید.",
            reply_markup=markup
        )
        return
    bot.send_message(user_id, "سلام! فیلم مورد نظرت رو با کلمه کلیدی اش درخواست کن.\nمثال: film1")

@bot.message_handler(func=lambda m: True)
def handle_movie_request(message):
    user_id = message.from_user.id
    if not is_member(user_id):
        bot.send_message(user_id, f"لطفاً ابتدا در کانال {CHANNEL_USERNAME} عضو شوید.")
        return
    text = message.text.strip()
    if text in MOVIES and MOVIES[text]:
        try:
            sent_msg = bot.send_video(user_id, MOVIES[text], caption=f"✅ فیلم {text} ارسال شد.")
            threading.Thread(target=delete_after_delay, args=(user_id, sent_msg.message_id, 60)).start()
        except Exception as e:
            bot.send_message(user_id, f"❌ خطا: {e}")
    else:
        bot.send_message(user_id, "❌ کلمه کلیدی اشتباه.\nلیست: " + "\n".join([k for k, v in MOVIES.items() if v]))

# ========== کد جدید برای اجرا روی Render ==========
app = Flask(__name__)

@app.route('/')
def index():
    return "ربات در حال اجراست!"

def run_bot():
    print("✅ ربات با موفقیت روشن شد!")
    bot.infinity_polling()

if __name__ == "__main__":
    # ربات رو در یک ترد جداگانه اجرا کن تا وب‌سرور هم کار کنه
    thread = threading.Thread(target=run_bot)
    thread.start()
    
    # وب‌سرور Flask رو روشن کن تا Render ما رو زنده نگه داره
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
