from loader import bot, storage, dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from keyboards.inline.interrupt_buttons import start_keyboard
from utils.notify_admins import on_startup_notify, on_shutdown_notify


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    await on_shutdown_notify(dispatcher)
    await bot.close()
    await storage.close()


@dp.message_handler(Text(equals="Помощь"))
@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    """Send list of commands"""
    await message.reply(text='''
/help -- Увидеть это сообщение
/anthropometry -- Ввести данные антропометрии
/get_anthropometry_data -- просмотр введенных данных антропометрии''', reply=False)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Hello user"""
    await message.reply('Привет, этот бот расчетывает затраченную работу в тренажерном зале, '
                        'но для начала нужно знать твои антропометрические данные', reply_markup=start_keyboard)
    # await send_menu(message=message)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
