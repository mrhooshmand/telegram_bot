import telebot
from flask import Flask, request
import logging
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from google import genai
from google.genai import types
from weather import get_weather

# بارگذاری متغیرها از .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
CHAT_ID = int(os.getenv("CHAT_ID"))  # گروه من
GROUP_ID = int(os.getenv("GROUP_ID"))  # گروه خانواده


# تنظیمات ربات و لاگ
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

WEBHOOK_PATH = "/webhook"

# اتصال به Gemini
client = genai.Client(api_key=GEMINI_KEY)

def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )
        return response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return "⚠️ مشکلی در ارتباط با Gemini پیش اومد."


# هندلر شروع
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام ✌️ من فعالم و به پیام‌هات با Gemini جواب میدم.")

@bot.message_handler(commands=['getid'])
def send_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Chat ID: {chat_id}")
    print(f"Chat ID: {chat_id}")  # در کنسول هم چاپ می‌شود


# هندلر چت خصوصی یا منشن در گروه
BOT_USERNAMES = ["assistant", "bot", "باتی", "بات"]

def clean_message(text: str) -> str:
    for word in BOT_USERNAMES:
        text = text.replace(word, "")
    return " ".join(text.split())  # حذف فاصله‌های اضافه

@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/') and (
        m.chat.type == "private" or
        any(name in m.text.lower() for name in BOT_USERNAMES) or
        (m.reply_to_message and m.reply_to_message.from_user.is_bot) or
        any(f"@{name.lower()}" in m.text.lower() for name in BOT_USERNAMES)
))
def reply_to_message(message):
    # کد پاکسازی و ارسال به AI
    user_text = message.text
    for word in BOT_USERNAMES + [f"@{name}" for name in BOT_USERNAMES]:
        user_text = user_text.replace(word, "")
    user_text = " ".join(user_text.split())

    if user_text.strip() == '':
        bot.reply_to(message, 'بله، بفرمایین 🙂')
    else:
        ai_response = ask_gemini(user_text)
        bot.reply_to(message, ai_response)
        logging.info(f"AI reply sent: {ai_response}")

def reply_to_message(message):
    user_text = clean_message(message.text)

    if user_text.strip() == '':
        bot.reply_to(message, 'بله، بفرمایین 🙂')
    else:
        ai_response = ask_gemini(user_text)
        bot.reply_to(message, ai_response)
        logging.info(f"AI reply sent: {ai_response}")


# پیام‌های زمان‌بندی شده
MORNING_MESSAGE = "☀️ صبح بخیر! امیدوارم روز فوق‌العاده‌ای شروع کنید."
EVENING_MESSAGE = "السلام علیک یا علی ابن موسی الرضا  آمدم ای شاه پناهم بده * خط امانی ز گناهم بده * ای حرمت ملجأ درماندگان * دور مران از در و راهم بده"

def send_morning_message():
    try:
        bot.send_message(chat_id=GROUP_ID, text=MORNING_MESSAGE)
        logging.info("Morning message sent")
    except Exception as e:
        logging.error(f"Error sending morning message: {e}")

def send_evening_message():
    try:
        bot.send_photo(CHAT_ID, photo=open('haram.jpg', "rb"), caption=EVENING_MESSAGE)
        bot.send_photo(GROUP_ID, photo=open('haram.jpg', "rb"), caption=EVENING_MESSAGE)
        print("Evening message sent")
    except Exception as e:
        print(f"Error sending evening message: {e}")

def show_weather():
    try:
        weather_data=get_weather('mashhad')
        bot.send_message(chat_id=CHAT_ID, text=f"{weather_data}")
    except Exception as e:
        print(f"Error sending evening message: {e}")

@bot.message_handler(commands=['weather'])
def chat_weather(message):
    chat_id = message.chat.id
    try:
        weather_data=get_weather('mashhad')
        # photo_url = weather_data.current.condition.icon
        # caption_text = f"دمای فعلی: {weather_data.current.temp_c}°C\nوضعیت: {weather_data.current.condition.text}"
        # print(weather_data)
        # bot.send_photo(CHAT_ID, photo=photo_url, caption=caption_text)
        bot.reply_to(message, f"{weather_data}")
    except Exception as e:
        print(f"Error sending evening message: {e}")
    print(f"Chat ID: {chat_id}")  # در کنسول هم چاپ می‌شود

# زمان‌بندی ب به وقت تهران
scheduler = BackgroundScheduler(timezone=timezone("Asia/Tehran"))
scheduler.add_job(send_morning_message, "cron", hour=5, minute=0)
scheduler.add_job(send_evening_message, "cron", hour=8, minute=0)
scheduler.add_job(show_weather, "cron", hour=7, minute=0)
scheduler.add_job(send_evening_message, "cron", hour=20, minute=0)

scheduler.start()


@app.route('/', methods=['GET'])
def index():
    return "Webhook ربات فعال ✅"

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    try:
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "ok", 200
    except Exception as ex:
        logging.error(f"Error processing update: {ex}")
        return f"Error: {ex}", 500

@app.route('/setwebhook')
def set_webhook():
    bot.remove_webhook()
    url = f"https://hooshmand.pythonanywhere.com{WEBHOOK_PATH}"
    bot.set_webhook(url)
    return f"Webhook set to {url}", 200
