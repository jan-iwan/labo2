from common import data, plot, fit
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

CELL_RANGE = "A1:E10"
WORKSHEET = "APERTURA NUMÉRICA"


def main(path: Path, args: list[str]) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    diametro = df["apertura del diafragma (0.02mm)"] / 1000  # mm -> m
    intensidad = df["Intensidad [lx]"]
    error = df["Error [lx]"]

    area = np.pi * (diametro / 2) ** 2

    f = fit.f.linear

    fit_found, _ = fit.utils.fitnsave(
        f,
        area,
        intensidad,
        yerr=error
    )

    plot.data_and_fit(
        area,
        intensidad,
        error,
        fit_found,
    )
