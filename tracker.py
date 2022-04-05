from datetime import datetime
import argparse
from draw_graph import draw_graph


def get_data_by_time(start, end):
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
    end = datetime.strptime(args.end, date_format).date()
    if args.N >= 100:
        n = int(input('Введите N < 100 '))
    else:
        n = args.N
    print(start)
    print(end)
    print(n)
    dictq = {1: 27, 3: 72, 4: 62, 5: 33, 6: 36, 7: 20, 8: 12, 9: 9, 10: 6, 11: 5, 12: 8, 14: 4,
                  15: 3, 16: 1, 17: 1, 18: 1, 19: 1, 21: 1, 27: 2}
    draw_graph(dictq)

if __name__ == "__main__":
    get_args()