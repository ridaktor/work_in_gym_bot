from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from input_check import answer_validate, state_translate
from keyboards.inline.interrupt_buttons import choice
from keyboards.default.data_buttons import data_keyboard
from states.anthropometry_states import AnthropometryStates
from loader import bot, dp

# ToDo: попробовать сделать список всех собиаремых данных и один модуль добавления/изменения данных
short_list = ['вес', 'рост']
full_list = ['ступня', 'голеностоп', 'голень', 'бедро', 'таз', 'торс', 'шея и голова', 'плечо', 'предплечье', 'кисть']


async def _get_anthropometry(message, state):
    answer = message.text
    filtered_answer = answer_validate(answer)

    state_data = await state.get_data()
    amount_of_answer_attempts = state_data['amount_of_answer_attempts'] + 1  # Counting user answer attempts
    bot_question_message_id = state_data['bot_question_message_id'] + 2

    if type(filtered_answer) is not str:
        # Removing the inline keyboard because a valid answer was received
        bot_question_message_id = state_data['bot_question_message_id'] \
                                  - amount_of_answer_attempts * 2 + 2  # Revert to the message with the inline keyboard
        await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                            message_id=bot_question_message_id, reply_markup=None)

        current_state = await state.get_state()
        translated_state = state_translate(current_state)
        await state.update_data({
            translated_state: filtered_answer
        })

        await AnthropometryStates.next()
        current_state = await state.get_state()
        if current_state == 'AnthropometryStates:the_end':
            await message.answer('Сбор данных полностью завершен', reply_markup=data_keyboard)
            await state.reset_state(with_data=False)  # finish (reset only state)
        else:
            translated_state = state_translate(current_state)
            answer_message = f'Какой у тебя {translated_state} в см?' if translated_state == 'рост' \
                else f'Какой длины у тебя {translated_state} в см?'
            await message.answer(answer_message, reply_markup=choice)
            bot_question_message_id = message.message_id + 1
            await state.update_data({
                "bot_question_message_id": bot_question_message_id,
                "amount_of_answer_attempts": 0
            })
    else:
        await message.answer(filtered_answer)
        await state.update_data({
            "bot_question_message_id": bot_question_message_id,
            "amount_of_answer_attempts": amount_of_answer_attempts
        })


@dp.message_handler(text='Ввод данных', state=None)
@dp.message_handler(commands='enter_data', state=None)
async def start_getting_anthropometry(message: types.Message, state: FSMContext):
    await message.answer('Сколько ты весишь в кг?', reply_markup=choice)
    await AnthropometryStates.body_weight.set()
    bot_question_message_id = message.message_id + 1
    await state.update_data({
        "bot_question_message_id": bot_question_message_id,
        "amount_of_answer_attempts": 0
    })


@dp.message_handler(text="next", state="*")
@dp.message_handler(state=AnthropometryStates.body_weight)
async def get_body_height(message: types.Message, state: FSMContext):
    await _get_anthropometry(message, state)


@dp.message_handler(text="next", state="*")
@dp.message_handler(state=AnthropometryStates.body_height)
async def get_body_weight(message: types.Message, state: FSMContext):
    await _get_anthropometry(message, state)


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
    await AnthropometryStates.next()
    current_state = await state.get_state()
    if current_state is not None and current_state != 'AnthropometryStates:the_end':
        answer = state_translate(current_state)
        await call.message.delete_reply_markup()
        answer_message = f'Какой у тебя {answer} в см?' if answer == 'рост' else f'Какой длины у тебя {answer} в см?'
        await call.message.answer(answer_message, reply_markup=choice)
        state_id = await state.get_data()
        bot_question_message_id = state_id['bot_question_message_id'] + 1
        await state.update_data({
            "bot_question_message_id": bot_question_message_id
        })
    else:
        await call.message.delete_reply_markup()
        await call.message.answer('Сбор данных завершен', reply_markup=data_keyboard)
        await state.reset_state(with_data=False)
    await state.update_data({
        "amount_of_answer_attempts": 0
    })
