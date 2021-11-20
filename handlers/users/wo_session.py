from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from handlers.users.exercise import Exercise
from input_handling import answer_validate
from keyboards.default.data_buttons import data_keyboard
from keyboards.default.exercise_buttons import exercise_keyboard
from loader import dp
from states.wo_states import WorkoutStates

exercise_list = ['Приседания', 'Румынская тяга', 'Подтягивания']


@dp.message_handler(text='Начать тренировку', state=None)
@dp.message_handler(commands='wo_start', state=None)
async def start_wo(message: Message):
    """Start workout"""
    await message.answer('Тренировка начата, выбери упражнение', reply_markup=exercise_keyboard)
    await WorkoutStates.workout.set()


@dp.message_handler(text=exercise_list, state="WorkoutStates:workout")
async def select_exercise(message: Message, state: FSMContext):
    """Select exercise"""
    async with state.proxy() as data:
        data['name_of_exercise'] = message.text
    await message.answer('Введи дополнительный вес', reply_markup=None)
    await WorkoutStates.extra_weight.set()


@dp.message_handler(state=WorkoutStates.all_states[1:])
async def get_exercise_params(message: Message, state: FSMContext):
    """Gets exercise parameters (extra weight, number of reps and number of sets)"""
    current_state = await state.get_state()
    valid_answer = await answer_validate(message.text)
    if isinstance(valid_answer, str):
        await message.answer(valid_answer)
    else:
        async with state.proxy() as data:
            data[current_state] = valid_answer
        await WorkoutStates.next()
        if current_state == 'WorkoutStates:number_of_sets':
            async with state.proxy() as data:
                name_of_exercise = data['name_of_exercise']
                extra_weight = data['WorkoutStates:extra_weight']
                reps = data['WorkoutStates:number_of_reps']
                sets = data['WorkoutStates:number_of_sets']
            exercise = Exercise(name_of_exercise, extra_weight, reps, sets)
            work = exercise.get_work()
            await message.answer('Работа равна {}'.format(work), reply_markup=exercise_keyboard)
            await state.reset_state()
            await WorkoutStates.workout.set()
        else:
            current_state = await state.get_state()
            await message.answer('Введи {}'.format(current_state), reply_markup=None)


@dp.message_handler(text="Закончить тренировку", state="WorkoutStates:workout")
async def end_wo(message: Message, state: FSMContext):
    """End workout"""
    await message.answer('Тренировка закончена', reply_markup=data_keyboard)
    await state.reset_state()
