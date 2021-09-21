from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from input_check import _answer_validate, _state_translate
from keyboards.inline.interrupt_buttons import choice
from keyboards.default.data_buttons import data_keyboard
from states.anthropometry_states import AnthropometryStates
from loader import bot, dp


@dp.message_handler(text='Ввод данных', state=None)
@dp.message_handler(commands='enter_data', state=None)
async def start_getting_anthropometry(message: Message, state: FSMContext):
    """Start of anthropometry collection"""
    await AnthropometryStates.first()
    question = await message.answer('Сколько ты весишь в кг?', reply_markup=choice)
    async with state.proxy() as data:
        data['question_message_id'] = question.message_id


@dp.callback_query_handler(text="next", state="*")
async def _state_switch_forward(message: Message, state: FSMContext):
    """Switch to another state and send the following question"""
    await AnthropometryStates.next()
    async with state.proxy() as data:
        question_message_id = data['question_message_id']
    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=question_message_id, reply_markup=None)

    current_state = await state.get_state()
    if current_state == 'AnthropometryStates:the_end':
        await bot.send_message(chat_id=message.from_user.id, text='Сбор данных завершен', reply_markup=data_keyboard)
        await state.reset_state(with_data=False)
    else:
        translated_state = _state_translate(current_state)
        answer_message = f'Какой у тебя {translated_state} в см?' if translated_state == 'рост' \
            else f'Какой длины у тебя {translated_state} в см?'
        question = await bot.send_message(chat_id=message.from_user.id, text=answer_message, reply_markup=choice)
        async with state.proxy() as data:
            data['question_message_id'] = question.message_id


for each_state in AnthropometryStates.all_states:
    @dp.message_handler(state=each_state)
    async def _get_anthropometry(message: Message, state: FSMContext):
        """Get anthropometry data in a list of all states"""
        valid_answer = _answer_validate(message.text)
        if isinstance(valid_answer, str):
            await message.answer(valid_answer)
        else:
            current_state = await state.get_state()
            translated_state = _state_translate(current_state)
            async with state.proxy() as data:
                data[translated_state] = valid_answer
            await _state_switch_forward(message, state)


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_getting(call: CallbackQuery, state: FSMContext):
    """Abort data collection"""
    await call.message.delete_reply_markup()
    await state.reset_state(with_data=False)
    await call.message.answer('Сбор данных прерван', reply_markup=data_keyboard)
    await call.answer('Вы отменили сбор', show_alert=True)
