import get_adrress
from telebot import TeleBot

users_state = {}

def handle_start(bot: TeleBot, chat_id: int):
    users_state[chat_id] = 0
    bot.send_message(chat_id, 'Привет, рад тебя видеть, чтобы получить координаты введите /geocoder')

def handle_geocoder(bot: TeleBot, chat_id: int):
    users_state[chat_id] = 1
    bot.send_message(chat_id, 'Введите адрес для поиска:')

def handle_address_input(bot: TeleBot, chat_id: int, message: str):
    users_state[chat_id] = 0
    street, housenumber = message.split()
    address = get_adrress.get_address(street, housenumber)
    bot.send_message(chat_id, address)

def handle_help(bot: TeleBot, chat_id: int):
    bot.send_message(chat_id, 'Введи /start')

def handle_default(bot: TeleBot, chat_id: int):
    bot.send_message(chat_id, 'Введи /help')
