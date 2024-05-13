from common import data, plot, fit
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

WORKSHEET = "resonancia"
CELL_RANGE = "B3:E49"


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    cols = df.columns.values.tolist()

    freq_sent = df[cols[0]]
    freq_recv = df[cols[1]]
    div = df[cols[2]]
    err = df[cols[3]]

    # 3% del valor medido, 5% por la división y el error en el promedio
    error = 0.03 * freq_recv + 0.05 * div + err

    # fit_found, _ = fit.utils.fitnsave(
    #     path/f"results/{__name__}.csv",
    #     fit.f.double_lorentz,
    #     freq_sent,
    #     freq_recv,
    #     p0=[40, 40, 1, 1, 11],
    #     yerr=error
    # )

    # Plot result
    plot.data(
        freq_sent[3:-3],
        freq_recv[3:-3] / 1000,
        error[3:-3] / 1000,
        figsize=(8, 5),
        ylabel="Amplitud [Vpp]"
    )

    plot.save(path/f"plots/{__name__}.png")
