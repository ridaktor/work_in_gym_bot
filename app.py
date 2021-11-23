from data_base.sqlite_db_commands import DBCommands
from input_handling import state_translate
from loader import storage, dp
from aiogram.types import Message
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands
from keyboards.default.data_buttons import data_keyboard

anthropometry_db = DBCommands('anthropometry', 'body_part_name', 'body_part_value', 'body_part_weight')
exercise_db = DBCommands('exercise_parameters', 'exercise_name', 'moved_distance', 'sprung_weight')


async def on_startup(dispatcher):
    """Set default commands and notify admins when bot starts"""
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await anthropometry_db.db_create()

    await exercise_db.db_create()
    await exercise_db.db_insert('exercise_name, moved_distance, sprung_weight', [('Приседания', 55, 70),
                                                                                 ('Румынская тяга', 60, 60),
                                                                                 ('Подтягивания', 35, 80)
                                                                                 ])



async def on_shutdown(dispatcher):
    """Close storage and notify admins when bot is stopped"""
    await storage.close()
    await on_shutdown_notify(dispatcher)


@dp.message_handler(commands='help')
async def send_menu(message: Message):
    """Send a list of commands"""
    await message.reply(text='''
/enter_data -- Ввести данные антропометрии
/show_data -- Просмотр введенных данных антропометрии
/wo_start -- Начать тренировку''', reply=False)


@dp.message_handler(commands='start')
async def start_command(message: Message):
    """Hello user"""
    await message.reply('Привет, этот бот расчетывает затраченную работу в тренажерном зале, '
                        'но для начала нужно знать твои антропометрические данные', reply_markup=data_keyboard)
    # await send_menu(message=message)


@dp.message_handler(text='Просмотр данных')
@dp.message_handler(commands='show_data')
async def show_anthropometry(message: Message):
    """Sends anthropometry data"""
    db_data = await anthropometry_db.db_read('body_part_name, body_part_value')
    not_empty_rows = [i for i in db_data if i[1] is not None]
    if not_empty_rows:
        body_part_name, body_part_value = zip(*not_empty_rows)
        db_data_rus = dict(zip([await state_translate(name) for name in body_part_name], body_part_value))
        answer = '\n'.join(
            "{}: {} кг".format(k, v if v % 1 > 0 else int(v)) if k == 'Вес' else
            "{}: {} см".format(k, v if v % 1 > 0 else int(v)) for k, v in db_data_rus.items())

        await message.answer(answer, reply_markup=data_keyboard)
    else:
        await message.answer('Данных нет', reply_markup=data_keyboard)

# Bot startup
if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
