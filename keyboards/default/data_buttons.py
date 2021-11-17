from aiogram.types import ReplyKeyboardMarkup


data_buttons = ['Ввод данных', 'Просмотр данных', 'Начать тренировку']
data_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
data_keyboard.add(*data_buttons)
