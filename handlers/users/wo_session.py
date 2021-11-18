from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from input_handling import answer_validate
from keyboards.default.data_buttons import data_keyboard
from keyboards.default.exercise_buttons import exercise_keyboard
from loader import dp
from states.wo_states import WorkoutStates


# TODO
@dp.message_handler(text='Начать тренировку', state=None)
@dp.message_handler(commands='wo_start', state=None)
async def start_wo(message: Message):
    """"""
    await message.answer('Тренировка начата, выбери упражнение', reply_markup=exercise_keyboard)
    await WorkoutStates.workout.set()


@dp.message_handler(text="Приседания", state="WorkoutStates:workout")
async def squats(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if data:
            await message.answer('Работа на приседе равна {}'.format(data.items()), reply_markup=exercise_keyboard)
            await state.reset_state()
            await WorkoutStates.workout.set()
        else:
            await message.answer('Введи вес штанги', reply_markup=None)
            await WorkoutStates.barbell_weight.set()


@dp.message_handler(text="Румынская тяга", state="WorkoutStates:workout")
async def romanian_deadlift(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if data:
            await message.answer('Работа на Румынской тяге равна {}'.format(data.items()), reply_markup=exercise_keyboard)
            await state.reset_state()
            await WorkoutStates.workout.set()
        else:
            await message.answer('Введи вес штанги', reply_markup=None)
            await WorkoutStates.barbell_weight.set()


@dp.message_handler(text="Подтягивания", state="WorkoutStates:workout")
async def pullups(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if data:
            await message.answer('Работа на Подтягиваниях равна {}'.format(data.items()), reply_markup=exercise_keyboard)
            await state.reset_state()
            await WorkoutStates.workout.set()
        else:
            await message.answer('Введи вес штанги', reply_markup=None)
            await WorkoutStates.barbell_weight.set()


@dp.message_handler(text="Закончить тренировку", state="WorkoutStates:workout")
async def end_wo(message: Message, state: FSMContext):
    await message.answer('Тренировка закончена', reply_markup=data_keyboard)
    await state.reset_state()


@dp.message_handler(state=WorkoutStates.barbell_weight)
async def get_barbell_weight(message: Message, state: FSMContext):
    valid_answer = await answer_validate(message.text)
    if isinstance(valid_answer, str):
        await message.answer(valid_answer)
    else:
        async with state.proxy() as data:
            data['barbell_weight'] = valid_answer
        await WorkoutStates.number_of_reps.set()
        await message.answer('Введи количество повторений', reply_markup=None)


@dp.message_handler(state=WorkoutStates.number_of_reps)
async def get_number_of_reps(message: Message, state: FSMContext):
    valid_answer = await answer_validate(message.text)
    if isinstance(valid_answer, str):
        await message.answer(valid_answer)
    else:
        async with state.proxy() as data:
            data['number_of_reps'] = valid_answer
        await WorkoutStates.number_of_sets.set()
        await message.answer('Введи количество подходов', reply_markup=None)


@dp.message_handler(state=WorkoutStates.number_of_sets)
async def get_number_of_sets(message: Message, state: FSMContext):
    valid_answer = await answer_validate(message.text)
    if isinstance(valid_answer, str):
        await message.answer(valid_answer)
    else:
        async with state.proxy() as data:
            data['number_of_sets'] = valid_answer
        await squats(message, state)
