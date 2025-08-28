import telebot
from feed import getFeed

bot = telebot.TeleBot("8263720925:AAEGv3BpmnshbjFJFoiQh2oq9KBLN0BsVwI", parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        feeds = getFeed(6)
    except Exception as ex:
        feeds = []
    bot.reply_to(message, feeds)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
