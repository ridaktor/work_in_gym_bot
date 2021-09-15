from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


interrupt_buttons = ['Далее', 'Отмена']
interrupt_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
interrupt_keyboard.add(*interrupt_buttons)

choice = InlineKeyboardMarkup(row_width=2)

next_button = InlineKeyboardButton(text="Далее", callback_data="next")
choice.insert(next_button)

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
choice.insert(cancel_button)
