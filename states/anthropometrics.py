from aiogram.dispatcher.filters.state import StatesGroup, State


class GetAnthropometryData(StatesGroup):
    waiting_for_body_weight = State()
    waiting_for_body_height = State()
    # waiting_for_foot = State()
    # waiting_for_ankle_to_ground = State()
    # waiting_for_tibia = State()
    # waiting_for_femur = State()
    # waiting_for_pelvis = State()
    # waiting_for_torso = State()
    # waiting_for_head_and_neck = State()
    # waiting_for_humerus = State()
    # waiting_for_forearm = State()
    # waiting_for_hand = State()
    waiting_for_end = State()
