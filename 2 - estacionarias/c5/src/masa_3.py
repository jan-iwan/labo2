from common import data, plot
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

CELL_RANGE = "A3:F12"
WORKSHEET = "TENSION 320"


def main(path) -> None:
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    mode = df["Modo"]
    freq = df["Frecuencia [Hz]"]
    internode = df["longitud entre 2 nodos [m]"]

    long_eff = _
    lmbda = _

    fig, ax = plt.subplots(
        1,
        2,
        figsize=(12, 6)
    )
    ax[0].set_title(freq.name)
    ax[1].set_title(internode.name)

    ax[0].plot(mode, freq, label=freq.name)
    ax[1].plot(mode, internode, label=internode.name)
    ax[0].legend()
    ax[0].grid()
    ax[1].legend()
    ax[1].grid()

    plt.show()

    return


if __name__ == "__main__":
    main()
