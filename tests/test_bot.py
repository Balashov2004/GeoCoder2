import unittest
from unittest.mock import Mock, patch
import sqlite3
from bot.handlers import handle_start, handle_geocoder, handle_address_input, handle_help, handle_default, users_state

class TestBotHandlers(unittest.TestCase):

    def setUp(self):
        self.bot = Mock()
        self.chat_id = 12345
        # Используем тестовую базу данных
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            street TEXT NOT NULL,
            housenumber TEXT NOT NULL,
            full_address TEXT,
            latitude REAL,
            longitude REAL
        )
        ''')
        self.conn.commit()
        # Мокаем get_adrress.get_address для использования тестовой БД
        patcher = patch('get_adrress.get_address', self.mock_get_address)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock_get_address(self, street, housenumber):
        self.cursor.execute('INSERT INTO addresses (street, housenumber, full_address, latitude, longitude) VALUES (?, ?, ?, ?, ?)',
                            (street, housenumber, f"{street}, {housenumber}", 55.7558, 37.6173))
        self.conn.commit()
        return f"{street}, {housenumber}: 55.7558, 37.6173"

    def test_handle_start(self):
        handle_start(self.bot, self.chat_id)
        self.bot.send_message.assert_called_once_with(self.chat_id, 'Привет, рад тебя видеть, чтобы получить координаты введите /geocoder')
        self.assertEqual(users_state[self.chat_id], 0)

    def test_handle_geocoder(self):
        handle_geocoder(self.bot, self.chat_id)
        self.bot.send_message.assert_called_once_with(self.chat_id, 'Введите адрес для поиска:')
        self.assertEqual(users_state[self.chat_id], 1)

    def test_handle_address_input(self):
        users_state[self.chat_id] = 1
        handle_address_input(self.bot, self.chat_id, 'Московская 10')
        self.bot.send_message.assert_called_once_with(self.chat_id, 'Московская, 10: 55.7558, 37.6173')
        self.assertEqual(users_state[self.chat_id], 0)

    def test_handle_help(self):
        handle_help(self.bot, self.chat_id)
        self.bot.send_message.assert_called_once_with(self.chat_id, 'Введи /start')

    def test_handle_default(self):
        handle_default(self.bot, self.chat_id)
        self.bot.send_message.assert_called_once_with(self.chat_id, 'Введи /help')

if __name__ == '__main__':
    unittest.main()
