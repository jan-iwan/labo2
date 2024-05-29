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
    img = df["Posición de la pantalla [mm]"] - lente
    error_img = 15

    indirect_err = error_img / img ** 2

    f = fit.f.linear

    fit_found, _ = fit.utils.fitnsave(
        path/f"results/{__name__}.csv",
        f,
        1/obj,
        1/img,
        yerr=indirect_err
    )

    # ax.plot(1/obj, f.f(1/obj, *p_opt))
    plot.data_and_fit(
        1/obj,
        1/img,
        indirect_err,
        fit_found
    )

    plot.save(path/f"plots/{__name__}.png")
