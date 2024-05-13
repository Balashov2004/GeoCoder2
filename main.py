import telebot

import get_adrress
from config import Config


bot = telebot.TeleBot(Config.TOKEN)
users_state = {}
@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    message = message.text

    if message == '/start':
        users_state[chat_id] = 0
        send_message(chat_id, 'Привет, рад тебя видеть, чтобы получить координаты введите /geocoder')

    elif message == '/geocoder':
        users_state[chat_id] = 1
        send_message(chat_id, 'Введите адрес для поиска:')

    elif users_state[chat_id] == 1:
        users_state[chat_id] = 0
        street, housenumber = message.split()
        send_message(chat_id, get_adrress.get_address(street, housenumber))

    elif message == '/help':
        send_message(chat_id, 'Введи /start')

    else:
        send_message(chat_id, "Введи /help")

def send_message(chat_id, text) -> None:
    bot.send_message(chat_id, text)

bot.polling(none_stop=True)