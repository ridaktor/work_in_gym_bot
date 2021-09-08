from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from input_check import answer_validation
from keyboards.inline.interrupt_buttons import choice, start_keyboard
from states.anthropometrics import Anthropometrics
import re
from loader import bot, dp


@dp.message_handler(text='Ввод данных', state=None)
@dp.message_handler(Command('anthropometry'), state=None)
async def get_anthropometry(message: types.Message, state: FSMContext):
    await message.answer('Введи вес в кг', reply_markup=choice)
    await Anthropometrics.body_weight.set()
    message_id = message.message_id + 1
    await state.update_data(
        {"message_id": message_id}
    )


@dp.message_handler(text="next", state="*")
@dp.message_handler(state=Anthropometrics.body_weight)
async def get_body_height(message: types.Message, state: FSMContext):
    answer = message.text
    filtered_answer = await answer_validation(answer, message)
    state_id = await state.get_data()
    message_id = state_id['message_id']
    if filtered_answer:
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_id, reply_markup=None)
        await state.update_data(
            {"Вес": filtered_answer}
        )
        await message.answer('Введи рост в см', reply_markup=choice)
        await Anthropometrics.next()
        message_id = message.message_id + 1
        await state.update_data(
            {"message_id": message_id}
        )


@dp.message_handler(text="next", state="*")
@dp.message_handler(state=Anthropometrics.body_height)
async def get_body_weight(message: types.Message, state: FSMContext):
    answer = message.text
    filtered_answer = await answer_validation(answer, message)
    state_id = await state.get_data()
    message_id = state_id['message_id']
    if filtered_answer:
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_id, reply_markup=None)
        await state.update_data(
            {"Рост": filtered_answer}
        )
        await message.answer('Сбор данных завершен', reply_markup=start_keyboard)
        await state.reset_state(with_data=False)  # finish (reset only state)
        # await state.finish() # finish (reset state and data)


@dp.message_handler(commands=['get_anthropometry_data'])
@dp.message_handler(text='Просмотр данных')
async def show_anthropometry(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data:
        data.pop('message_id')

    if data:
        await message.answer('\n'.join("{}: {} кг".format(k, v) if k == 'Вес' else "{}: {} см".format(k, v)
                                       for k, v in data.items()), reply_markup=start_keyboard)
    else:
        await message.answer('Данных нет', reply_markup=start_keyboard)


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_getting(call: CallbackQuery, state: FSMContext):
    await call.answer('Вы отменили сбор', show_alert=True)
    await call.message.delete_reply_markup()
    await state.reset_state(with_data=False)
    await call.message.answer('Сбор данных завершен', reply_markup=start_keyboard)


@dp.callback_query_handler(text="next", state="*")
async def next_getting(call: CallbackQuery, state: FSMContext):
    await Anthropometrics.next()
    current_state = await state.get_state()
    if current_state is not None:
        result = re.findall(r'\w+$', current_state)
        sub_dict = {'body_weight': 'вес', 'body_height': 'рост'}
        regex = '|'.join(sub_dict)
        answer = re.sub(regex, lambda m: sub_dict[m.group()], str(result[0]))
        await call.message.delete_reply_markup()
        await call.message.answer(f'Введи {answer} в см', reply_markup=choice)
        message_id = call.message.message_id+1
        await state.update_data(
            {"message_id": message_id}
        )
    else:
        await call.message.delete_reply_markup()
        await call.message.answer('Сбор данных завершен', reply_markup=start_keyboard)
        await state.reset_state(with_data=False)
