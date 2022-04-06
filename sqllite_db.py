from datetime import datetime
import sqlite3


class SqlStorage:
    """класс создания и работы с БД sqlite3"""
    def __init__(self, db_name='DefaultName'):
        """присваиваем имя нашей БД, настраиваем коннект"""
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self._cr_table()

    def _cr_table(self):
        """если таблицы нет - создаем, если уже есть то пропускаем"""
        cursor = self._connection.cursor()
        cursor.execute('create table if not exists historydata(date text, price real, unique(date))')
        self._connection.commit()

    def save_to_db(self, data: dict):
        """сохраняем в базу значения data"""
        cursor = self._connection.cursor()
        for key, value in data.items():
            cursor.execute('insert or ignore into historydata(date, price) values (?, ?)',
                           (key, value))
        self._connection.commit()

    def load_from_db(self, start: datetime, end: datetime) -> dict:
        """получаем из базы значения в интревале start -> end"""
        cursor = self._connection.cursor()
        cursor.execute("select * from historydata where date >= " + "'" + str(start) +
                       "'" + " and date < " + "'" + str(end) + "'")
        result = cursor.fetchall()
        self._connection.commit()
        data_dict = {}
        for data in result:
            data_dict[data[0]] = data[1]
        return data_dict
