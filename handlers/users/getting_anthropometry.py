from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from input_check import answer_validation, state_translator
from keyboards.inline.interrupt_buttons import choice
from keyboards.default.data_buttons import data_keyboard
from states.anthropometrics import GetAnthropometryData
from loader import bot, dp


# ToDo: попробовать сделать список всех собиаремых данных и один модуль добавления/изменения данных
short_list = ['вес', 'рост']
full_list = ['ступня', 'голеностоп', 'голень', 'бедро', 'таз', 'торс', 'шея и голова', 'плечо', 'предплечье', 'кисть']


async def getting_anthropometry(message, state):
    current_state = await state.get_state()
    if current_state is not None:
        i = state_translator(current_state)
    answer = message.text
    filtered_answer = answer_validation(answer)
    data = await state.get_data()
    amount_of_answer_attempts = data['amount_of_answer_attempts'] + 1  # Counting user answer attempts
    message_id = data['message_id'] + 2
    if type(filtered_answer) is not str:
        # Revert to the message id with the inline keyboard
        message_id = data['message_id'] - amount_of_answer_attempts * 2 + 2
        # Removing the inline keyboard because a valid answer was received
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_id, reply_markup=None)
        await state.update_data({
            i: filtered_answer
        })
        await GetAnthropometryData.next()
        current_state = await state.get_state()
        # if current_state is not None:
        #     i = state_translator(current_state) Подумать тут, может вернуть?
        if current_state == 'GetAnthropometryData:waiting_for_end':
            await message.answer('Сбор данных полностью завершен', reply_markup=data_keyboard)
            await state.reset_state(with_data=False)  # finish (reset only state)
        else:
            i = state_translator(current_state)
            answer_message = f'Какой у тебя {i} в см?' if i == 'рост' else f'Какой длины у тебя {i} в см?'
            await message.answer(answer_message, reply_markup=choice)
            message_id = message.message_id + 1
            await state.update_data({
                "message_id": message_id,
                "amount_of_answer_attempts": 0
            })


    else:
        await message.answer(filtered_answer)
        await state.update_data({
            "message_id": message_id,
            "amount_of_answer_attempts": amount_of_answer_attempts
        })


@dp.message_handler(text='Ввод данных', state=None)
@dp.message_handler(commands='enter_data', state=None)
async def start_getting_anthropometry(message: types.Message, state: FSMContext):
    await message.answer('Сколько ты весишь в кг?', reply_markup=choice)
    await GetAnthropometryData.waiting_for_body_weight.set()
    message_id = message.message_id + 1
    await state.update_data({
        "message_id": message_id,
        "amount_of_answer_attempts": 0
    })


@dp.message_handler(text="next", state="*")
@dp.message_handler(state=GetAnthropometryData.waiting_for_body_weight)
async def get_body_height(message: types.Message, state: FSMContext):
    await getting_anthropometry(message, state)


@dp.message_handler(text="next", state="*")
@dp.message_handler(state=GetAnthropometryData.waiting_for_body_height)
async def get_body_weight(message: types.Message, state: FSMContext):
    await getting_anthropometry(message, state)
    # answer = message.text
    # filtered_answer = answer_validation(answer)
    # data = await state.get_data()
    # answer_amount = data['answer_amount'] + 1  # Counting user answer attempts
    # message_id = data['message_id'] + 2
    # if type(filtered_answer) is not str:
    #     message_id = data['message_id'] - answer_amount * 2 + 2
    #     await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_id, reply_markup=None)
    #     await state.update_data({
    #         "Рост": filtered_answer
    #     })
    #     await message.answer('Сбор данных завершен', reply_markup=data_keyboard)
    #     await state.reset_state(with_data=False)  # finish (reset only state)
    #     message_id = message.message_id + 1
    #     await state.update_data({
    #         "message_id": message_id,
    #         "answer_amount": 0
    #     })
    #     # await state.finish() # finish (reset state and data)
    # else:
    #     await message.answer(filtered_answer)
    #     await state.update_data({
    #         "message_id": message_id,
    #         "answer_amount": answer_amount
    #     })


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_getting(call: CallbackQuery, state: FSMContext):
    await call.answer('Вы отменили сбор', show_alert=True)
    await call.message.delete_reply_markup()
    await state.reset_state(with_data=False)
    await call.message.answer('Сбор данных завершен', reply_markup=data_keyboard)
    await state.update_data({
        "amount_of_answer_attempts": 0
    })


@dp.callback_query_handler(text="next", state="*")
async def next_getting(call: CallbackQuery, state: FSMContext):
    await GetAnthropometryData.next()
    current_state = await state.get_state()
    if current_state is not None and current_state != 'GetAnthropometryData:waiting_for_end':
        answer = state_translator(current_state)
        await call.message.delete_reply_markup()
        answer_message = f'Какой у тебя {answer} в см?' if answer == 'рост' else f'Какой длины у тебя {answer} в см?'
        await call.message.answer(answer_message, reply_markup=choice)
        state_id = await state.get_data()
        message_id = state_id['message_id'] + 1
        await state.update_data({
            "message_id": message_id
        })
    else:
        await call.message.delete_reply_markup()
        await call.message.answer('Сбор данных завершен', reply_markup=data_keyboard)
        await state.reset_state(with_data=False)
    await state.update_data({
        "amount_of_answer_attempts": 0
    })
