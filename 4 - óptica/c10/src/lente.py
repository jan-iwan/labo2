from common import data, plot, fit
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

CELL_RANGE = "D4:E22"
WORKSHEET = "ECUACIÓN DE LA LENTE"

# ec. de lente:
# 1/img - 1/obj = 1/f
# con x_lente = 0

# y = mx + b
# (1/img) = 1(1/obj) + 1/f
# m = 1, b = 1/f


def main(path: Path, args: list[str]) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    lente = df["Posición la lente [mm]"]
    obj = 40 - lente

    img = df["Posición de la pantalla [mm]"]
    img -= lente

    error_img = 15

    indirect_err = error_img / img ** 2

    f = fit.f.linear

    y_fit, _ = fit.utils.fitnsave(
        path/f"results/{__name__}.csv",
        f,
        1/obj,
        1/img,
        yerr=indirect_err
    )

    plot.data_and_fit(
        1/obj,
        1/img,
        indirect_err,
        y_fit,
        saveto=path/f"plots/{__name__}.png",
        xlabel=r"Inversa de la posición del objeto [mm$^{-1}$]",
        ylabel=r"Inversa de la posición de la imagen [mm$^{-1}$]",
    )
