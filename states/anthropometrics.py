from aiogram.dispatcher.filters.state import StatesGroup, State


class Anthropometrics(StatesGroup):
    body_weight = State()
    body_height = State()
    foot = State()
    ankle_to_ground = State()
    tibia = State()
    femur = State()
    pelvis = State()
    torso = State()
    head_and_neck = State()
    humerus = State()
    forearm = State()
    hand = State()
