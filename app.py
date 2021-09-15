from loader import bot, storage, dp
from aiogram import types
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from aiogram.dispatcher import FSMContext
from keyboards.default.start_buttons import start_keyboard


async def on_startup(dispatcher):
    """Notify admins when bot starts"""
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    """Close bot and storage and
    notify admins when bot is stopped"""
    await on_shutdown_notify(dispatcher)
    await bot.close()
    await storage.close()


@dp.message_handler(text="Помощь")
@dp.message_handler(commands='help')
async def send_menu(message: types.Message):
    """Send a list of commands"""
    await message.reply(text='''
/help -- Увидеть это сообщение
/enter_data -- Ввести данные антропометрии
/show_data -- просмотр введенных данных антропометрии''', reply=False)


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    """Hello user"""
    await message.reply('Привет, этот бот расчетывает затраченную работу в тренажерном зале, '
                        'но для начала нужно знать твои антропометрические данные', reply_markup=start_keyboard)
    # await send_menu(message=message)


@dp.message_handler(text='Просмотр данных')
@dp.message_handler(commands='show_data')
async def show_anthropometry(message: types.Message, state: FSMContext):
    """Sends tha data collected"""
    data = await state.get_data()
    if data:
        data.pop('message_id')
        data.pop('answer_amount')
    if data:
        await message.answer('\n'.join("{}: {} кг".format(k, v) if k == 'Вес' else "{}: {} см".format(k, v)
                                       for k, v in data.items()), reply_markup=start_keyboard)
    else:
        await message.answer('Данных нет', reply_markup=start_keyboard)


# Bot startup
if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
