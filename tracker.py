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
    start = args.start
    end = args.end
    if args.N >= 100:
        n = int(input('Введите N < 100 '))
    else:
        n = args.N


if __name__ == "__main__":
    get_args()