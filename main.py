import telebot
from flask import Flask, request
import logging

TOKEN = "8263720925:AAHjNG9dFBqN4WSbHF_VvEvS40pSMQN5Wuc"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

WEBHOOK_PATH = "/webhook"

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.reply_to(message, "سلام ✌️ من روی PythonAnywhere فعالم.")
    except Exception as ex:
        logging.error(f"Error in start handler: {ex}")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        logging.info(f"Echoing message: {message.text}")
        bot.reply_to(message, message.text)
    except Exception as ex:
        logging.error(f"Error in echo handler: {ex}")


@app.route('/')
def index():
    return "سلام! Webhook ربات فعاله ✅"

@app.route(WEBHOOK_PATH, methods=['POST'])
def getMessage():
    try:
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)

        if hasattr(update, "message") and hasattr(update.message, "text"):
            logging.info(f"Directly calling echo_all for: {update.message.text}")
            echo_all(update.message)

        bot.process_new_updates([update])
        logging.info("Update processed")
    except Exception as ex:
        logging.error(f"Error processing update: {ex}")
        return f"Error: {ex}", 500
    return "ok", 200


@app.route('/setwebhook')
def set_webhook():
    try:
        bot.remove_webhook()
        url = f"https://hooshmand.pythonanywhere.com{WEBHOOK_PATH}"
        bot.set_webhook(url=url)
        logging.info(f"Webhook set to {url}")
        return f"Webhook set to {url}", 200
    except Exception as ex:
        logging.error(f"Error setting webhook: {ex}")
        return f"Error setting webhook: {ex}", 500
