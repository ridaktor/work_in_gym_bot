from loader import storage, dp
from aiogram.types import Message
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands
from aiogram.dispatcher import FSMContext
from keyboards.default.data_buttons import data_keyboard


async def on_startup(dispatcher):
    """Set default commands and notify admins when bot starts"""
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    """Close storage and notify admins when bot is stopped"""
    await storage.close()
    await on_shutdown_notify(dispatcher)


@dp.message_handler(commands='help')
async def send_menu(message: Message):
    """Send a list of commands"""
    await message.reply(text='''
/enter_data -- Ввести данные антропометрии
/show_data -- Просмотр введенных данных антропометрии''', reply=False)


@dp.message_handler(commands='start')
async def start_command(message: Message):
    """Hello user"""
    await message.reply('Привет, этот бот расчетывает затраченную работу в тренажерном зале, '
                        'но для начала нужно знать твои антропометрические данные', reply_markup=data_keyboard)
    # await send_menu(message=message)


@dp.message_handler(text='Просмотр данных')
@dp.message_handler(commands='show_data')
async def show_anthropometry(message: Message, state: FSMContext):
    """Sends tha state_data collected"""
    state_data = await state.get_data()
    if state_data:
        state_data.pop('question_message_id')
    if state_data:
        await message.answer('\n'.join("{}: {} кг".format(k, v) if k == 'Вес' else "{}: {} см".format(k, v)
                                       for k, v in state_data.items()), reply_markup=data_keyboard)
    else:
        await message.answer('Данных нет', reply_markup=data_keyboard)


# Bot startup
if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
