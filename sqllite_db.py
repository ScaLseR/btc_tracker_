import sqlite3


class Sqldata:

    def __init__(self, db_name='tracker'):
        """присваиваем имя нашей БД, настраиваем коннект"""
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self.cr_table()

    def cr_table(self):
        """если таблицы нет - создаем, если уже есть то пропускаем"""
        cursor = self._connection.cursor()
        cursor.execute('create table if not exist (date text, price real, unique(date))')
        self._connection.commit()