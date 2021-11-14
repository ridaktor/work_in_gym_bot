import aiosqlite
from states.anthropometry_states import AnthropometryStates


async def db_start():
    async with aiosqlite.connect('data_base/main.db') as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS anthropometry(row_id INTEGER PRIMARY KEY, body_part_name TEXT, value REAL)"""
        )
        await db.commit()

        number = []
        for i in range(len(AnthropometryStates.all_states)):
            number.append(i+1)
        print(number)

        c = await db.cursor()
        for item in number:
            await c.execute(""" INSERT OR REPLACE INTO anthropometry (row_id) VALUES (?)""", (item,))
        await db.commit()


async def db_add(state):
    async with aiosqlite.connect('data_base/main.db') as db:
        async with state.proxy() as data:
            del data['question_message_id']
            await db.executemany(
                """INSERT OR REPLACE INTO anthropometry (body_part_name, value) VALUES (?, ?)""", data.items()
            )
            await db.commit()


async def db_read():
    async with aiosqlite.connect('data_base/main.db') as db:
        cursor = await db.execute("""SELECT * FROM anthropometry""")
        rows = await cursor.fetchall()
        return rows

