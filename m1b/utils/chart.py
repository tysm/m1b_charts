from io import BytesIO

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

    imgdata = BytesIO()
    plt.savefig(imgdata, format="png")
    imgdata.seek(0)
    return imgdata.read()


def linear_char(labels: list, values_list: list, times: list):
    for values in values_list:
        plt.plot(times, values)

    plt.xlabel("Time (min.)")
    plt.ylabel("Predominance")
    plt.title("Emotion Predominance at Time")

    plt.legend(labels, loc=4)

    imgdata = BytesIO()
    plt.savefig(imgdata, format="png")
    imgdata.seek(0)
    return imgdata.read()
