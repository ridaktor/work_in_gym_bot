from aiogram.types import ReplyKeyboardMarkup

exercise_buttons = ['Приседания', 'Румынская тяга', 'Подтягивания', 'Отжимания на брусьях']
end_button = 'Закончить тренировку'
exercise_keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
exercise_keyboard.add(exercise_buttons[0], exercise_buttons[1]).add(exercise_buttons[2], exercise_buttons[3]).add(end_button)
