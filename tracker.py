from datetime import datetime, timedelta
import argparse
from sqllite_db import SqlStorage
from btc_api import BtcApi
from draw_graph import draw_graph


def get_data_by_n_days(start, n):
    pass

def get_data_by_time_interval(start, end):
    pass

def get_args():
    """ Получаем и обрабатываем аргументы командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', dest="start", type=str)
    parser.add_argument('-end', dest="end", type=str)
    parser.add_argument('-N', dest="N", type=int)
    args = parser.parse_args()
    date_format = "%Y-%m-%d"
    start = datetime.strptime(args.start, date_format).date()
    if args.end is not None:
        end = datetime.strptime(args.end, date_format).date()
    else:
        end = None

    if args.N >= 100:
        n = int(input('Введите N < 100 '))
    else:
        n = args.N

    storage = SqlStorage('test')
    api = BtcApi(n)
    rez = api.load_start_end(start, end)
    storage.save_to_db(rez)
    print('rez= ', rez)

    rez2 = storage.load_from_db(start, end)
    print('rez2= ', rez2)
    draw_graph(rez)

if __name__ == "__main__":
    get_args()