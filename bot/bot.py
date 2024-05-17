import telebot
from config import Config
from handlers import handle_start, handle_geocoder, handle_address_input, handle_help, handle_default, users_state

bot = telebot.TeleBot(Config.TOKEN)

@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    text = message.text

    if text == '/start':
        handle_start(bot, chat_id)
    elif text == '/geocoder':
        handle_geocoder(bot, chat_id)
    elif chat_id in users_state and users_state[chat_id] == 1:
        handle_address_input(bot, chat_id, text)
    elif text == '/help':
        handle_help(bot, chat_id)
    else:
        handle_default(bot, chat_id)
