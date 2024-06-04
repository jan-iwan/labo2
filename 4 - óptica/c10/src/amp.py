from common import data, plot, fit
import numpy as np

CELL_RANGE = "A1:E10"
WORKSHEET = "APERTURA NUMÉRICA"

ERR_DIAMETRO = 0.02  # mm


def main(args: list[str]) -> None:
    # Find dataframe
    df = data.find(
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    diametro = df["apertura del diafragma [mm]"]
    intensidad = df["Intensidad [lx]"]
    error = df["Error [lx]"]

    area = np.pi * (diametro / 2) ** 2

    indirect_error = np.pi * diametro * ERR_DIAMETRO

    fit_func = fit.utils.fitnsave(
        fit.f.linear,
        area,
        intensidad,
        yerr=indirect_error
    )

    plot.data_and_fit(
        area,
        intensidad,
        (indirect_error, error),
        fit_func,
        xlabel=r"Área de apertura del diafragma [mm$^2$]",
        fmt="o"
    )
