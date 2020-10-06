import os

from flask import Flask, request

import telebot
from line2rhyme import line2rhyme

TOKEN = '808816333:AAGV8d3W2cwi4u1fnS2WIqCRPB3Eq1n45gM'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, ' + message.from_user.first_name + '\nЕсли ты напишешь мне что-то, то я постараюсь подобать рифму из стихотворений А.Блока')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
	rhyme = line2rhyme(message.text)
	bot.reply_to(message, rhyme)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://alexblock-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
