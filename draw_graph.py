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
        x_new = x_coord[::kol]
        y_new = y_coord[::kol]
        if x_new[-1] != x_coord[-1]:
            x_new.append(x_coord[-1])
            y_new.append(y_coord[-1])
        plt.plot(x_new, y_new, color='g')
    plt.show()
