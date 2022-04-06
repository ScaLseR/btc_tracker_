from datetime import datetime, timedelta
from sqllite_db import SqlStorage
from btc_api import BtcApi
from draw_graph import draw_graph
import argparse


def find_first_valid_data():
    """находим первую валидную дату с ценой"""
    date_format = "%Y-%m-%d"
    start = datetime.strptime('2000-01-01', date_format).date()
    end = datetime.strptime('2022-01-01', date_format).date()
    n = 30
    api = BtcApi(n)
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


def get_data_by_time_interval(start, end, n):
    """получаем данные за период <n, сначала смотрим в базе
    , если нет то отправляем запрос к API"""
    storage = SqlStorage('test')
    data_from_storage = storage.load_from_db(start, end)
    if len(data_from_storage) == (end - start).days:
        draw_graph(data_from_storage)
    else:
        api = BtcApi(n)
        data_from_api = api.load_start_end(start, end)
        storage.save_to_db(data_from_api)
        draw_graph(data_from_api)


def get_args():
    """ Получаем и обрабатываем аргументы командной строки"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--start', type=str, default=False, help='Input start date: yyyy-mm-dd')
    parser.add_argument('--end', type=str, default=False, help='Input end date: yyyy-mm-dd')
    parser.add_argument('--n', type=int, default=False, help='Input N < 100')
    parser.add_argument('--fv', default=False, help='Finding the first valid day of historical data')
    args = parser.parse_args()

    if args.fv and not args.start and not args.end and not args.n:
        find_first_valid_data()

    if args.start and args.end and args.n and not args.fv:
        if args.n >= 100:
            n = int(input('Введите N < 100 '))
        else:
            n = args.n
        date_format = "%Y-%m-%d"
        start = datetime.strptime(args.start, date_format).date()
        end = datetime.strptime(args.end, date_format).date()
        get_data_by_time_interval(start, end, n)


if __name__ == "__main__":
    get_args()
