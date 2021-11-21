import aiosqlite
from input_handling import state_translate
from states.anthropometry_states import AnthropometryStates

table_name = 'anthropometry'


async def db_start():
    """Creates a table with three columns"""
    async with aiosqlite.connect('data_base/main.db') as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS {}(
            body_part_name TEXT PRIMARY KEY, 
            length REAL DEFAULT 0, 
            weight REAL)""".format(table_name)
        )
        await db.commit()


async def db_fill():
    """Fills the table with body part names in order"""
    async with aiosqlite.connect('data_base/main.db') as db:
        # state_name_without_prefix = state_name.replace('AnthropometryStates:', '')
        translated_names = [name.replace('AnthropometryStates:', '') for name in AnthropometryStates.all_states_names[1:-1]]
        await db.executemany(
            """INSERT OR IGNORE INTO {} (
            body_part_name) VALUES (?)""".format(table_name), list(zip(translated_names))
        )
        await db.commit()


async def db_add(state):
    """Updates the value im the table"""
    async with aiosqlite.connect('data_base/main.db') as db:
        async with state.proxy() as data:
            data.pop('question_message_id')
            reversed_tuple = [t[::-1] for t in tuple(data.items())]
            await db.executemany(
                """UPDATE {} SET length == ? WHERE body_part_name == ?""".format(table_name), reversed_tuple
            )
            await db.commit()


async def db_read():
    """Reads the table and returns non-zero rows"""
    async with aiosqlite.connect('data_base/main.db') as db:
        cursor = await db.execute("""SELECT body_part_name, length FROM {}""".format(table_name))
        all_rows = await cursor.fetchall()
        not_empty_rows = [i for i in all_rows if i[1] != 0]
        return not_empty_rows
