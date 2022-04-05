import matplotlib.pyplot as plt


def draw_graph(data: dict):
    plt.title('График изменения цены BTC')
    plt.xlabel('Цена')
    plt.ylabel('Дата')
    plt.grid(False)
    plt.plot(list(data.keys()), data.values(), color='g')
    plt.show()
