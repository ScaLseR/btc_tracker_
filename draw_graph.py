import matplotlib.pyplot as plt


def draw_graph(data: dict):
    plt.bar(list(data.keys()), data.values(), color='g')
    plt.show()
