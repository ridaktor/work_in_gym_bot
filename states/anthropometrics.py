from aiogram.dispatcher.filters.state import StatesGroup, State


class Anthropometrics(StatesGroup):
    body_height = State()
    body_weight = State()
