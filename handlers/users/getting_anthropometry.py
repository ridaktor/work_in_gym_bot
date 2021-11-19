from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from data_base.sqlite_db import db_add, db_fill
from input_handling import answer_validate, state_translate, put_question_message_id, \
    delete_reply_markup
from keyboards.inline.interrupt_buttons import choice
from keyboards.default.data_buttons import data_keyboard
from states.anthropometry_states import AnthropometryStates
from loader import dp, bot


@dp.message_handler(text='Ввод данных', state=None)
@dp.message_handler(commands='enter_data', state=None)
@dp.callback_query_handler(text="next", state="*")
async def _state_switch_forward(message: Message, state: FSMContext):
    """TODO"""
    current_state = await state.get_state()
    if current_state:
        # Continued collection of anthropometry
        await delete_reply_markup(message, state)
        await AnthropometryStates.next()
        current_state = await state.get_state()

        if current_state == 'AnthropometryStates:the_end':
            # End of anthropometry collection
            await bot.send_message(chat_id=message.from_user.id, text='Сбор данных завершен', reply_markup=data_keyboard)
            await db_add(state)
            await state.reset_state()

        else:
            answer_message = await state_translate(current_state, question=True)
            question = await bot.send_message(chat_id=message.from_user.id, text=answer_message, reply_markup=choice)
            await put_question_message_id(question, state)

    else:
        # Beginning of anthropometry collection
        await db_fill()
        await AnthropometryStates.first()
        await _state_switch_forward(message, state)
        # current_state = await state.get_state()
        #
        # answer_message = await state_translate(current_state, question=True)
        # question = await bot.send_message(chat_id=message.from_user.id, text=answer_message, reply_markup=choice)
        # await put_question_message_id(question, state)


for each_state in AnthropometryStates.all_states:
    @dp.message_handler(state=each_state)
    async def _get_anthropometry(message: Message, state: FSMContext):
        """Get anthropometry data in a list of all states"""
        valid_answer = await answer_validate(message.text)
        if isinstance(valid_answer, str):
            await message.answer(valid_answer)
        else:
            current_state = await state.get_state()
            translated_state = await state_translate(current_state)
            async with state.proxy() as data:
                data[translated_state] = valid_answer
            await _state_switch_forward(message, state)


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_getting(call: CallbackQuery, state: FSMContext):
    """Abort data collection"""
    await call.message.delete_reply_markup()
    await db_add(state)
    await state.reset_state()
    await call.message.answer('Сбор данных прерван', reply_markup=data_keyboard)
    await call.answer('Вы отменили сбор', show_alert=True)
