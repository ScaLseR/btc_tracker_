from datetime import datetime
import sqlite3


class SqlStorage:
    """класс создания и работы с БД sqlite3"""
    def __init__(self, db_name='tracker'):
        """присваиваем имя нашей БД, настраиваем коннект"""
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self._cr_table()

    def _cr_table(self):
        """если таблицы нет - создаем, если уже есть то пропускаем"""
        cursor = self._connection.cursor()
        cursor.execute('create table if not exist historydata(date text, price real, unique(date))')
        self._connection.commit()

    def save_to_db(self, data: dict):
        """сохраняем в базу значения data"""
        cursor = self._connection.cursor()
        for key, value in data.items():
            cursor.execute('insert or ignore into historydata(date, price) values (?, ?)',
                           (key, value))
        self._connection.commit()

    def load_from_db(self, start, end_):
        """получаем из базы значения в интревале start -> end"""
        cursor = self._connection.cursor()
        cursor.execute('select * from historydata where date >= ' + start + ' and date < ' + end_)
        result = cursor.fetchall()
        return result
