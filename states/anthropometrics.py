from aiogram.dispatcher.filters.state import StatesGroup, State


class Anthropometrics(StatesGroup):
    body_weight = State()
    body_height = State()
