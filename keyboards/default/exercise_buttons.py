from aiogram.types import ReplyKeyboardMarkup

exercise_buttons = ['Приседания', 'Румынская тяга', 'Подтягивания']
end_button = 'Закончить тренировку'
exercise_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
exercise_keyboard.add(*exercise_buttons).add(end_button)
