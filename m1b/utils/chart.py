import numpy as np
import matplotlib.pyplot as plt


def bar_chart(labels: list, values: np.array):
    objects = tuple(labels)
    y_pos = np.arange(len(objects))

    plt.bar(y_pos * 2, values, align="center", alpha=0.5)
    plt.xticks(y_pos * 2, objects)

    plt.xlabel("Emotion")
    plt.ylabel("Predominance")
    plt.title("Emotion Predominance")

    plt.show()


def linear_char(labels: list, values_list: list, times: list):
    for values in values_list:
        plt.plot(times, values)

    plt.xlabel("Time (min.)")
    plt.ylabel("Predominance")
    plt.title("Emotion Predominance at Time")

    plt.legend(labels, loc=4)

    plt.show()


if __name__ == "__main__":
    linear_char(
        ["anger", "happy"],
        [[0, 0.5, 1, 0.5, 0.2], [1, 0.5, 0, 0.5, 0.8]],
        [0, 1, 2, 3, 4],
    )
