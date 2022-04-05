import sqlite3


class Sqldata:

    def __init__(self, db_name='tracker'):
        """присваиваем имя нашей БД, настраиваем коннект"""
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self._cr_table()

    def _cr_table(self):
        """если таблицы нет - создаем, если уже есть то пропускаем"""
        cursor = self._connection.cursor()
        cursor.execute('create table if not exist (date text, price real, unique(date))')
        self._connection.commit()

    def save_to_db(self, data):
        """сохраняем в базу значения"""
        pass

    def load_from_db(self, start, end):
        """получаем из базы значения в интревале start -> end"""
        pass
