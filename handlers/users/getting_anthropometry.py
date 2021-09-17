from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from input_check import _answer_validate, _state_translate
from keyboards.inline.interrupt_buttons import choice
from keyboards.default.data_buttons import data_keyboard
from states.anthropometry_states import AnthropometryStates
from loader import bot, dp


@dp.message_handler(text='Ввод данных', state=None)
@dp.message_handler(commands='enter_data', state=None)
async def start_getting_anthropometry(message: types.Message, state: FSMContext):
    await message.answer('Сколько ты весишь в кг?', reply_markup=choice)
    await AnthropometryStates.body_weight.set()
    async with state.proxy() as data:
        data['bot_question_message_id'] = message.message_id + 1
        data['amount_of_answer_attempts'] = 0


for each_state in AnthropometryStates.all_states:
    @dp.message_handler(text="next", state="*")
    @dp.message_handler(state=each_state)
    async def _get_anthropometry(message: types.Message, state: FSMContext):
        filtered_answer = _answer_validate(message.text)

        async with state.proxy() as data:
            amount_of_answer_attempts = data['amount_of_answer_attempts'] + 1
            bot_question_message_id = data['bot_question_message_id'] + 2

        if type(filtered_answer) is not str:
            # Removing the inline keyboard because a valid answer was received
            bot_question_message_id = data['bot_question_message_id'] \
                                      - amount_of_answer_attempts * 2 + 2  # Revert to the message with the inline keyboard
            await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                                message_id=bot_question_message_id, reply_markup=None)

            current_state = await state.get_state()
            translated_state = _state_translate(current_state)
            async with state.proxy() as data:
                data[translated_state] = filtered_answer

            await AnthropometryStates.next()
            current_state = await state.get_state()

            if current_state != 'AnthropometryStates:the_end':
                translated_state = _state_translate(current_state)
                answer_message = f'Какой у тебя {translated_state} в см?' if translated_state == 'рост' \
                    else f'Какой длины у тебя {translated_state} в см?'
                await message.answer(answer_message, reply_markup=choice)

                async with state.proxy() as data:
                    data['bot_question_message_id'] = message.message_id + 1
                    data['amount_of_answer_attempts'] = 0

            else:
                await message.answer('Сбор данных полностью завершен', reply_markup=data_keyboard)
                await state.reset_state(with_data=False)  # finish (reset only state)
        else:
            await message.answer(filtered_answer)
            async with state.proxy() as data:
                data['bot_question_message_id'] = bot_question_message_id
                data['amount_of_answer_attempts'] = amount_of_answer_attempts


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_getting(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()  # Removing the inline keyboard because it has been used
    await state.reset_state(with_data=False)
    await call.message.answer('Сбор данных завершен', reply_markup=data_keyboard)
    await call.answer('Вы отменили сбор', show_alert=True)


@dp.callback_query_handler(text="next", state="*")
async def next_getting(call: CallbackQuery, state: FSMContext):
    await AnthropometryStates.next()
    current_state = await state.get_state()
    await call.message.delete_reply_markup()  # Removing the inline keyboard because it has been used

    if current_state != 'AnthropometryStates:the_end':
        translated_state = _state_translate(current_state)
        answer_message = f'Какой у тебя {translated_state} в см?' if translated_state == 'рост' \
            else f'Какой длины у тебя {translated_state} в см?'
        await call.message.answer(answer_message, reply_markup=choice)

        async with state.proxy() as data:
            data['bot_question_message_id'] += 1
            data['amount_of_answer_attempts'] = 0
    else:
        await call.message.answer('Сбор данных завершен', reply_markup=data_keyboard)
        await state.reset_state(with_data=False)


