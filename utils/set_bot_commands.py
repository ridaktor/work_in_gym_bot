from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("enter_data", "Ввести данные антропометрии"),
            types.BotCommand("start_wo", "Начать тренировку"),
        ]
    )
