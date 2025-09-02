import os
import telebot
from flask import Flask, request
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
WEBHOOK_PATH = "/webhook"

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

BOT_USERNAMES = ["assistant", "bot", "بات"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام ✌️ من آماده پاسخگویی با Gemini AI هستم!")

@bot.message_handler(func=lambda m: m.text and (
        m.chat.type == "private" or any(name in m.text.lower() for name in BOT_USERNAMES)
))
def reply_with_gemini_flash(message):
    try:
        user_text = message.text
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        bot.reply_to(message, response.text)
        logging.info(f"AI reply sent: {response.text}")
    except Exception as ex:
        logging.error(f"Error in AI handler: {ex}")
        bot.reply_to(message, "یه مشکلی پیش اومد 😔")

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
