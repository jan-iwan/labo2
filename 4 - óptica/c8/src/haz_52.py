from common import data, plot, fit
from pathlib import Path
import numpy as np

CELL_RANGE = "A2:E21"
WORKSHEET = "PERFIL 0.52m"


def main(path: Path, erf) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    pos = df["Posición [mm]"]
    volt = df["Voltaje [V]"]
    error = df["Error intens"]

    fit_found, _ = fit.utils.fitnsave(
        path/f"results/{__name__}.csv",
        erf,
        pos,
        volt,
        yerr=error,
        p0=[100]
    )

    plot.data_and_fit(
        pos,
        volt,
        error,
        fit_found,
        saveto=path/f"plots/{__name__}.png"
    )
