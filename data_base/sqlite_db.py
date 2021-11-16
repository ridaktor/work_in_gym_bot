import aiosqlite
from input_handling import _state_translate
from states.anthropometry_states import AnthropometryStates

table_name = 'anthropometry'


async def db_start():
    """Creates a table with three columns"""
    async with aiosqlite.connect('data_base/main.db') as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS {}(row_id INTEGER, body_part_name TEXT PRIMARY KEY, value REAL)""".format(table_name)
        )
        await db.commit()


async def db_fill():
    """Fills the table with body part names in order"""
    async with aiosqlite.connect('data_base/main.db') as db:
        names = AnthropometryStates.all_states_names[:-1]
        row_id = [i for i in range(1, len(names)+1)]
        translated_body_part_name = [await _state_translate(name) for name in names]
        zeros = [0] * len(names)
        values = list(zip(row_id, translated_body_part_name, zeros))
        await db.executemany(
            """INSERT OR IGNORE INTO {} (row_id, body_part_name, value) VALUES (?, ?, ?)""".format(table_name), values
        )
        await db.commit()


async def db_add(state):
    """Updates the value im the table"""
    async with aiosqlite.connect('data_base/main.db') as db:
        async with state.proxy() as data:
            data.pop('question_message_id')
            reversed_tuple = [t[::-1] for t in tuple(data.items())]
            await db.executemany(
                """UPDATE {} SET value == ? WHERE body_part_name == ?""".format(table_name), reversed_tuple
            )
            await db.commit()


async def db_read():
    """Reads the table and returns non-zero rows"""
    async with aiosqlite.connect('data_base/main.db') as db:
        cursor = await db.execute("""SELECT body_part_name, value FROM {} ORDER BY row_id""".format(table_name))
        all_rows = await cursor.fetchall()
        not_empty_rows = [i for i in all_rows if i[1] != 0]
        return not_empty_rows
