from sqlite3 import InterfaceError, OperationalError, ProgrammingError
import aiosqlite


class DBCommands:
    db_name = 'data_base/main.db'

    def __init__(self, table_name, *args):
        self.table_name = table_name
        self.columns_names = args

    async def db_create(self):
        """Creates a table with columns"""
        async with aiosqlite.connect(DBCommands.db_name) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS {}({} TEXT PRIMARY KEY)""".format(self.table_name, self.columns_names[0]))
            for name in self.columns_names[1:]:
                try:
                    await db.execute("""ALTER TABLE {} ADD COLUMN {}""".format(self.table_name, name))
                except OperationalError:
                    pass
            await db.commit()

    async def db_insert(self, column_list, value):
        """Inserts data in a table"""
        columns_numb = ','.join(['?'] * (len(value) if type(value) is tuple else len(value[0])))
        async with aiosqlite.connect(DBCommands.db_name) as db:
            try:
                await db.execute("""
                INSERT OR IGNORE INTO {}({}) VALUES ({})""".format(self.table_name, column_list, columns_numb), value)
            except (InterfaceError, ProgrammingError):
                await db.executemany("""
                INSERT OR IGNORE INTO {}({}) VALUES ({})""".format(self.table_name, column_list, columns_numb),value)
            await db.commit()

    async def db_update(self, column_name, row_name, value):
        """Updates data in a table"""
        columns = [', '.join(['{} = ?'.format(i) for i in column_name.split(', ')])][0]
        async with aiosqlite.connect(DBCommands.db_name) as db:
            await db.executemany(
                """UPDATE {} SET {} WHERE {} = ?""".format(self.table_name, columns, row_name), value)
            await db.commit()

    async def db_read(self, column_list, condition=None):
        """Returns a list of tuple(s) with selected data from a table"""
        async with aiosqlite.connect(DBCommands.db_name) as db:
            if condition:
                cursor = await db.execute(
                    """SELECT {} FROM {} WHERE {}""".format(column_list, self.table_name, condition))
                db_data = await cursor.fetchall()
            else:
                cursor = await db.execute("""SELECT {} FROM {}""".format(column_list, self.table_name))
                db_data = await cursor.fetchall()
            return db_data
