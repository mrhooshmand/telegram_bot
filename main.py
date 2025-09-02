import telebot
from flask import Flask, request
import logging
import random

TOKEN = "8263720925:AAHjNG9dFBqN4WSbHF_VvEvS40pSMQN5Wuc"

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

WEBHOOK_PATH = "/webhook"
BOT_USERNAMES = ["assistant", "bot", "بات"]

# پاسخ شبیه‌ساز AI سبک
def ask_ai(prompt):
    prompt_lower = prompt.lower()
    greetings = ["سلام! چطوری؟", "سلام ✌️ خوبی؟", "سلام دوست من!"]
    farewells = ["خداحافظ 😔", "بدرود!", "مواظب خودت باش!"]

    if any(word in prompt_lower for word in ["سلام", "hi", "hello"]):
        return random.choice(greetings)
    elif any(word in prompt_lower for word in ["خداحافظ", "bye", "bye-bye"]):
        return random.choice(farewells)
    elif "حال" in prompt_lower:
        return "حالم خوبه 😊 مرسی از پرسشت!"
    else:
        return f"تو گفتی: {prompt}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام ✌️ من روی PythonAnywhere فعالم.")

@bot.message_handler(func=lambda m: m.text and (
        m.chat.type == "private" or any(name in m.text.lower() for name in BOT_USERNAMES)
))
def reply_to_ai(message):
    try:
        user_text = message.text
        ai_response = ask_ai(user_text)
        bot.reply_to(message, ai_response)
        logging.info(f"AI reply sent: {ai_response}")
    except Exception as ex:
        logging.error(f"Error in reply_to_ai handler: {ex}")
        bot.reply_to(message, "یه مشکلی پیش اومد 😔")

@app.route('/', methods=['GET'])
def index():
    return "Webhook ربات فعاله ✅"

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
