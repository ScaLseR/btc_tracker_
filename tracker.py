from datetime import datetime
import argparse



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


if __name__ == "__main__":
    get_args()