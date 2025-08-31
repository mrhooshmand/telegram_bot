import telebot
from flask import Flask, request
import logging

TOKEN = "8263720925:AAHjNG9dFBqN4WSbHF_VvEvS40pSMQN5Wuc"

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

WEBHOOK_PATH = "/webhook"

BOT_USERNAMES = ["assistant", "bot", "بات"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام ✌️ من روی PythonAnywhere فعالم.")

@bot.message_handler(func=lambda m: m.text and (
        m.chat.type == "private" or any(name in m.text.lower() for name in BOT_USERNAMES)
))
def reply_to_message(message):
    logging.info(f"Replying to message: {message.text}")
    bot.reply_to(message, f"{message.text}")

@app.route('/', methods=['GET'])
def index():
    return "Webhook ربات فعاله ✅"

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    try:
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])   # این باید هندلرها رو تریگر کنه
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
