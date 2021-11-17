from aiogram.types import Message

from loader import dp


@dp.message_handler(text='Начать тренировку', state=None)
@dp.message_handler(commands='wo_start', state=None)
async def start_wo(message: Message):
    """"""
    await message.answer('Тренировка начата, выбери упражнение')#, reply_markup=wo_keyboard)
