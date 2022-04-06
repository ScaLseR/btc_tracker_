"""модуль отрисовки графика цены BTC за выбранный период времени"""
import matplotlib.pyplot as plt


def draw_graph(data: dict):
    """вывод графика цены BTC за выбранный период времени"""
    plt.title('График изменения цены BTC')
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.grid(False)
    plt.plot(list(data.keys()), data.values(), color='g')
    plt.show()
