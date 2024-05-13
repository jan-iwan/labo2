from common import data, plot, fit
from pathlib import Path
import matplotlib.pyplot as plt
import logging
import numpy as np

WORKSHEET = "Extremo cerrado"
CELL_RANGE = "A13:E36"


def main(path: Path) -> None:
    df = data.find(
        path,
        f"{__name__}-max",
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    pos = df["Posición [mm]"]
    ampl = df["Amplitud [Vpp]"]
    ampl_err = df["Error A"]
    div = df["Escala [V]"]

    error = 0.03 * ampl + 0.05 * div + ampl_err

    # cosine
    f = fit.f.Function(
        lambda x, A, k: np.abs(A * np.cos(k * x)),
        ["A", "k"]
    )

    ampl_fit, (p_opt, _) = fit.utils.fitnsave(
        path/f"results/{__name__}.csv",
        f,
        pos,
        ampl,
        p0=[1, 1],
        yerr=error,
    )

    plot.data_and_fit(
        pos,
        ampl,
        error,
        ampl_fit
    )

    plot.save(path/f"plots/{__name__}.svg")
