from aiogram.dispatcher.filters.state import StatesGroup, State


class WorkoutStates(StatesGroup):
    workout = State()
    extra_weight = State()
    number_of_reps = State()
    number_of_sets = State()
