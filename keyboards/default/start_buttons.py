from aiogram.types import ReplyKeyboardMarkup


start_buttons = ['Помощь', 'Ввод данных', 'Просмотр данных']
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_keyboard.add(*start_buttons)
