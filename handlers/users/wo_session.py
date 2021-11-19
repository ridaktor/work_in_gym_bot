from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from handlers.users.exercise import Exercise
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
            name_of_exercise = 'Приседания'
            extra_weight = data['WorkoutStates:extra_weight']
            reps = data['WorkoutStates:number_of_reps']
            sets = data['WorkoutStates:number_of_sets']
            exercise = Exercise(name_of_exercise, extra_weight, reps, sets)
            work = exercise.get_work()
            await message.answer('Работа равна {}'.format(work), reply_markup=exercise_keyboard)
            await state.reset_state()
            await WorkoutStates.workout.set()
        else:
            await get_exercise_parameters(message)


async def get_exercise_parameters(message):
    await message.answer('Введи дополнительный вес', reply_markup=None)
    await WorkoutStates.extra_weight.set()

    for each_state in WorkoutStates.all_states:
        @dp.message_handler(state=each_state)
        async def processing(message, state):
            current_state = await state.get_state()
            valid_answer = await answer_validate(message.text)
            if isinstance(valid_answer, str):
                await message.answer(valid_answer)
            else:
                async with state.proxy() as data:
                    data[current_state] = valid_answer
                await WorkoutStates.next()
                if current_state == 'WorkoutStates:number_of_sets':
                    await WorkoutStates.workout.set()
                    await squats(message, state)
                else:
                    current_state = await state.get_state()
                    await message.answer('Введи {}'.format(current_state), reply_markup=None)


# @dp.message_handler(text="Румынская тяга", state="WorkoutStates:workout")
# async def romanian_deadlift(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         if data:
#             await message.answer('Работа на Румынской тяге равна {}'.format(data.items()),
#                                  reply_markup=exercise_keyboard)
#             await state.reset_state()
#             await WorkoutStates.workout.set()
#         else:
#             await get_exercise_parameters(message)
#
#
# @dp.message_handler(text="Подтягивания", state="WorkoutStates:workout")
# async def pullups(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         if data:
#             await message.answer('Работа на Подтягиваниях равна {}'.format(data.items()),
#                                  reply_markup=exercise_keyboard)
#             await state.reset_state()
#             await WorkoutStates.workout.set()
#         else:
#             await get_exercise_parameters(message)


@dp.message_handler(text="Закончить тренировку", state="WorkoutStates:workout")
async def end_wo(message: Message, state: FSMContext):
    await message.answer('Тренировка закончена', reply_markup=data_keyboard)
    await state.reset_state()
