from common import data, plot, fit
import numpy as np

CELL_RANGE = "A1:E10"
WORKSHEET = "APERTURA NUMÉRICA"


def main(args: list[str]) -> None:
    # Find dataframe
    df = data.find(
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    diametro = df["apertura del diafragma (0.02mm)"] / 1000  # mm -> m
    intensidad = df["Intensidad [lx]"]
    error = df["Error [lx]"]

    area = np.pi * (diametro / 2) ** 2

    fit_func = fit.utils.fitnsave(
        fit.f.linear,
        area,
        intensidad,
        yerr=error
    )

    plot.data_and_fit(
        area,
        intensidad,
        error,
        fit_func,
    )
