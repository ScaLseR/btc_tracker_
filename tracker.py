"""Основной модуль трекера"""
import argparse
from datetime import datetime, timedelta
from sqllite_db import SqlStorage
from btc_api import BtcApi
from draw_graph import draw_graph


def find_first_valid_data(start, end):
    """находим первую валидную дату с ценой"""
    api = BtcApi()
    while (end - start).days != 3:
        center = start + timedelta(days=((end - start)/2).days)
        data_from_api = api.load_start_end(center + timedelta(days=-1), center + timedelta(days=+1))
        if len(data_from_api) == 3:
            end -= timedelta(days=((end - start)/2).days)
        else:
            start += timedelta(days=((end - start)/2).days)
        if len(data_from_api) == 2:
            break
    print('Первая валидный день исторических данных: ', str(start))


def get_data_by_time_interval(start, end, num):
    """получаем данные за период <n, сначала смотрим в базе
    , если нет то отправляем запрос к API"""
    storage = SqlStorage('test')
    data_from_storage = storage.load_from_db(start, end)
    if len(data_from_storage) == (end - start).days:
        draw_graph(data_from_storage)
    else:
        api = BtcApi(num)
        data_from_api = api.load_start_end(start, end)
        storage.save_to_db(data_from_api)
        draw_graph(data_from_api)


def convert_arg(arg):
    """конвертируем полученные аргументы в формат даты"""
    date_format = "%Y-%m-%d"
    return datetime.strptime(arg, date_format).date()


def get_args():
    """ Получаем и обрабатываем аргументы командной строки"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--start', type=str, default=False, help='Input start date: yyyy-mm-dd')
    parser.add_argument('--end', type=str, default=False, help='Input end date: yyyy-mm-dd')
    parser.add_argument('--n', type=int, default=False, help='Input N < 100')
    parser.add_argument('--fv', action='store_true', default=False,
                        help='Finding the first valid day of historical data')
    parser.add_argument('--md', action='store_true', default=False,
                        help='min data from api')
    args = parser.parse_args()
    #отработка аргумента --fv поиска первой валидной даты
    if args.fv and args.start and args.end:
        find_first_valid_data(convert_arg(args.start), convert_arg(args.end))
    #отработка аргументов --start --end --n для построения графика цены BTC
    if args.start and args.end and args.n and not args.fv:
        get_data_by_time_interval(convert_arg(args.start), convert_arg(args.end), args.n)


if __name__ == "__main__":
    get_args()
