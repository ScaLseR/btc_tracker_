"""Основной модуль трекера"""
import argparse
from datetime import datetime, timedelta
from sqllite_db import SqlStorage
from btc_api import BtcApi
from draw_graph import draw_graph


def find_first_valid_data(start: datetime.date, end: datetime.date):
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


def get_data_by_time_interval(start: datetime.date, end: datetime.date, num: int):
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
        data_from_storage = storage.load_from_db(start, end)
        draw_graph(data_from_storage)


def convert_to_date(arg: str) -> datetime.date:
    """конвертируем полученные аргументы в формат даты"""
    date_format = "%Y-%m-%d"
    return datetime.strptime(arg, date_format).date()


def get_data_min_time_interval(start: datetime.date, end: datetime.date, num: int):
    """минимизация получения данных с API """
    data_interval_list = []
    storage = SqlStorage('test')
    data_from_storage = storage.load_from_db(start, end)
    key_list = list(data_from_storage)
    if start < convert_to_date(key_list[0]):
        data_interval_list.append([start, convert_to_date(key_list[0])])
    if end > convert_to_date(key_list[-1]):
        data_interval_list.append([convert_to_date(key_list[-1]), end])
    for i in range(len(key_list) - 1):
        if (convert_to_date(key_list[i + 1]) - convert_to_date(key_list[i])).days > 1:
            data_interval_list.append([convert_to_date(key_list[i]),
                                       convert_to_date(key_list[i + 1])])
    api = BtcApi(num)
    for date in data_interval_list:
        data_from_api = api.load_start_end(date[0], date[1])
        storage.save_to_db(data_from_api)
    draw_graph(storage.load_from_db(start, end))


def get_min_request_api(start: datetime.date, end: datetime.date, num: int):
    """Минимизируем количество запросов к API"""
    storage = SqlStorage('test')
    if (end - start).days <= num:
        data_from_storage = storage.load_from_db(start, end)
        if (end - start).days == len(data_from_storage):
            draw_graph(data_from_storage)
        else:
            api = BtcApi(num)
            data_from_api = api.load_start_end(start, end)
            storage.save_to_db(data_from_api)
            data_from_storage = storage.load_from_db(start, end)
            draw_graph(data_from_storage)
    else:
        new_start = start
        while True:
            data_from_storage = storage.load_from_db(new_start, new_start + timedelta(days=num))
            if len(data_from_storage) == 0:
                api = BtcApi(num)
                data_from_api = api.load_start_end(new_start, new_start + timedelta(days=num))
                storage.save_to_db(data_from_api)
            if len(data_from_storage) == num:
                new_start = new_start + timedelta(days=num)
            if 0 < len(data_from_storage) < num:
                if new_start == data_from_storage[0]:
                    i = 0
                    while (data_from_storage[i + 1] - data_from_storage[i]).days == 1:
                        i += 1
                    print(i)
                key_list = list(data_from_storage)
                print(key_list)


def get_args():
    """ Получаем и обрабатываем аргументы командной строки"""
    parser = argparse.ArgumentParser(description='BTC Tracker')
    parser.add_argument('--start', type=str, default=False, help='Input start date: yyyy-mm-dd')
    parser.add_argument('--end', type=str, default=False, help='Input end date: yyyy-mm-dd')
    parser.add_argument('--n', type=int, default=False, help='Input N < 100')
    parser.add_argument('--fv', action='store_true', default=False,
                        help='Finding the first valid day of historical data')
    parser.add_argument('--md', action='store_true', default=False,
                        help='Get min data from api')
    parser.add_argument('--mr', action='store_true', default=False,
                        help='Get min requests to api')
    args = parser.parse_args()
    #отработка аргумента --fv поиска первой валидной даты
    if args.fv and args.start and args.end:
        find_first_valid_data(convert_to_date(args.start), convert_to_date(args.end))
    if args.start and args.end and args.n:
        # отработка аргументов --start --end --n построение графика BTC
        if not args.mr and not args.fv and not args.md:
            get_data_by_time_interval(convert_to_date(args.start),
                                      convert_to_date(args.end), args.n)
        # отработка аргументов --start --end --n --md с минимизацией запрашиваемых данных
        if args.md and not args.fv and not args.mr:
            get_data_min_time_interval(convert_to_date(args.start),
                                       convert_to_date(args.end), args.n)
        # отработка аргументов --start --end --n --mr с минимизацией количества запросов
        if args.mr and not args.md and not args.fv:
            get_min_request_api(convert_to_date(args.start),
                                convert_to_date(args.end), args.n)


if __name__ == "__main__":
    get_args()
