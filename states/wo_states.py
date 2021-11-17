from aiogram.dispatcher.filters.state import StatesGroup, State


class WorkoutStates(StatesGroup):
    exercise = State()
