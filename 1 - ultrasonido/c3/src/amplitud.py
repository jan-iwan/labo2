from common import data, plot, fit
from pathlib import Path
import matplotlib.pyplot as plt
import logging
import numpy as np

CELL_RANGE = "A2:D85"
WORKSHEET = "amplitud"
LAMBDA = 8.6484

logger = logging.getLogger(__name__)


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        path,
        f"{__name__}-max",
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    dist = df["Distancia [mm]"]
    ampl = df["Amplitud [mVpp]"]
    div = df["Escala [mVpp]"]
    err = df["Error [mVpp]"]

    # 3% del valor medido, 5% por la división y el error en el promedio
    error = 0.03 * ampl + 0.05 * div + err

    f = fit.f.fabry_perot

    ampl_fit, (p_opt, _) = fit.utils.fitnsave(
        path/f"results/{__name__}.csv",
        f,
        dist,
        ampl,
        p0=[-1, 100000, 0.6, 1.5, LAMBDA],
        yerr=error,
    )

    plt.figure(figsize=(10, 5))
    plt.grid()
    plt.xlabel("Posición [mm]")
    plt.ylabel("Amplitud [Vpp]")

    plt.errorbar(
        dist[:-5],
        ampl[:-5] / 1000,
        yerr=error[:-5] / 1000,
        fmt=".",
        label="Mediciones",
    )

    X = np.linspace(dist.iloc[0], dist.iloc[-5], 1000)
    plt.plot(
        X,
        f.f(X, *p_opt) / 1000,
        label="Ajuste"
    )

    plt.legend()

    plot.save(path/f"plots/{__name__}.svg")

    plt.figure(figsize=(10, 5))
    plt.grid()
    plt.xlabel("Posición [mm]")
    plt.ylabel("Amplitud [mVpp]")

    residue = ampl_fit - ampl

    plt.errorbar(
        dist[:-5],
        residue[:-5],
        yerr=error[:-5],
        fmt=".",
    )

    plt.axhline(0, color="black")

    plot.save(path/f"plots/{__name__}-residue.svg")
