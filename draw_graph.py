"""модуль отрисовки графика цены BTC за выбранный период времени"""
import matplotlib.pyplot as plt


def draw_graph(data: dict):
    """вывод графика цены BTC за выбранный период времени"""
    plt.title('График изменения цены BTC')
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.grid(False)
    x_coord = list(data.keys())
    y_coord = list(data.values())
    if len(x_coord) <= 10:
        kol = 1
    else:
        kol = int(len(x_coord)/10)
    if len(x_coord) == 1:
        plt.scatter(x_coord, y_coord, color='g')
    else:
        plt.plot(x_coord[::kol], y_coord[::kol], color='g')
    plt.show()
