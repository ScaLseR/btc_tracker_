import argparse


def get_args():
    """ Получаем и обрабатываем аргументы командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', dest="start", type=str)
    parser.add_argument('-end', dest="end", type=str)
    parser.add_argument('-N', dest="N", type=int)
    args = parser.parse_args()
    print(args.start)
    print(args.end)
    print(args.N)

if __name__ == "__main__":
    get_args()