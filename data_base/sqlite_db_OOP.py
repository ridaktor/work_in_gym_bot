from sqlite3 import InterfaceError, OperationalError

import aiosqlite
import sqlite3
from states.anthropometry_states import AnthropometryStates


# table_name = 'anthropometry'

class DBCommands:
    db_name = 'dta.db'

    def __init__(self, table_name, *args):
        self.table_name = table_name
        self.columns_names = args

    def db_start(self):
        """"""
        with sqlite3.connect(DBCommands.db_name) as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS {}({} TEXT PRIMARY KEY)""".format(self.table_name, self.columns_names[0]))
            for name in self.columns_names[1:]:
                try:
                    db.execute("""ALTER TABLE {} ADD COLUMN {}""".format(self.table_name, name))
                except OperationalError:
                    pass
            db.commit()

    def db_insert(self, column_name, value):
        """"""
        with sqlite3.connect(DBCommands.db_name) as db:
            try:
                db.execute("""INSERT OR IGNORE INTO {}({}) VALUES (?)""".format(self.table_name, column_name), (value,))
            except InterfaceError:
                db.executemany("""INSERT OR IGNORE INTO {}({}) VALUES (?)""".format(self.table_name, column_name),
                               list(zip(value)))
            db.commit()

    def db_update(self, column_name, row_name, value):
        """"""
        with sqlite3.connect(DBCommands.db_name) as db:
            try:
                db.execute("""UPDATE {} SET {} == ? WHERE {} == ?""".format(self.table_name, column_name, row_name), value)
            except InterfaceError:
                db.executemany("""UPDATE {} SET {} == ? WHERE {} == ?""".format(self.table_name, column_name, row_name), value)
            db.commit()


A = DBCommands('anthropometry2', 'body_part_name', 'body_part_length', 'body_part_weight')
A.db_start()
translated_names = [name.replace('AnthropometryStates:', '') for name in AnthropometryStates.all_states_names[1:-1]]
A.db_insert('body_part_name', translated_names)

A.db_update('body_part_length', 'body_part_name', ((12122, 'foot'), (77, 'body_weight')))
# async with state.proxy() as data:
#     data.pop('question_message_id')
#     reversed_tuple = [t[::-1] for t in tuple(data.items())]
#

#
#
# async def db_read():
#     """Reads the table and returns non-zero rows"""
#     async with aiosqlite.connect('data_base/main.db') as db:
#         cursor = await db.execute("""SELECT body_part_name, length FROM {}""".format(table_name))
#         all_rows = await cursor.fetchall()
#         not_empty_rows = [i for i in all_rows if i[1] != 0]
#         return not_empty_rows
