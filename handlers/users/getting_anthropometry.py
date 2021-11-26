from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from app import anthropometry_db
from handlers.users.anthropometry_calc import fill_body_part_weight_column
from input_handling import answer_validate, state_translate, put_question_message_id, \
    delete_reply_markup, close_anthropometry_state
from keyboards.inline.interrupt_buttons import choice
from keyboards.default.data_buttons import data_keyboard
from states.anthropometry_states import AnthropometryStates
from loader import dp, bot


@dp.message_handler(text='Ввод данных', state=None)
@dp.message_handler(commands='enter_data', state=None)
@dp.callback_query_handler(text="next", state=AnthropometryStates.all_states)
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
            await close_anthropometry_state(state)
            warning = await fill_body_part_weight_column()
            if warning:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Сбор данных завершен, но измерения имеют большую погрешность или не все "
                                            "данные внесены, рекомендуется повторить измерения "
                                            "\n/show_data - посмотреть введенные данные"
                                            "\n/enter_data - ввести данные",
                                       reply_markup=data_keyboard)
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Сбор данных успешно завершен, можно "
                                                                          "тренироватсья"
                                                                          "\n/start_wo - начать тренировку",
                                       reply_markup=data_keyboard)

        else:
            question_text = await state_translate(current_state, question=True)
            question = await bot.send_message(chat_id=message.from_user.id, text=question_text, reply_markup=choice)
            await put_question_message_id(question, state)
    else:
        # Beginning of anthropometry collection
        translated_names = [name.replace('AnthropometryStates:', '') for name in
                            AnthropometryStates.all_states_names[1:-1]]
        await anthropometry_db.db_insert('body_part_name', list(zip(translated_names)))
        await AnthropometryStates.first()
        await _state_switch_forward(message, state)


@dp.message_handler(state=AnthropometryStates.all_states)
async def _get_anthropometry(message: Message, state: FSMContext):
    """Get anthropometry data in a list of all states"""
    valid_answer = await answer_validate(message.text)
    if isinstance(valid_answer, str):
        await message.answer(valid_answer)
    else:
        current_state = await state.get_state()
        state_name = current_state.replace('AnthropometryStates:', '')
        async with state.proxy() as data:
            data[state_name] = valid_answer
        await _state_switch_forward(message, state)


@dp.callback_query_handler(text="cancel", state=AnthropometryStates.all_states)
async def cancel_getting(call: CallbackQuery, state: FSMContext):
    """Abort data collection"""
    await call.message.delete_reply_markup()
    await close_anthropometry_state(state)
    warning = await fill_body_part_weight_column()
    if warning:
        await call.message.answer("Сбор данных прерван. Имеется большая погрешность или не все данные внесены, "
                                  "рекомендуется потворно ввести данные."
                                  "\n/show_data - посмотреть введенные данные"
                                  "\n/enter_data - ввести данные",
                                  reply_markup=data_keyboard)
        await call.answer('Вы отменили сбор', show_alert=True)
    else:
        await call.message.answer("Изменения успешно внесены, можно тренироватсья\n/start_wo - начать тренировку",
                                  reply_markup=data_keyboard)
        await call.answer('Вы отменили сбор', show_alert=True)

