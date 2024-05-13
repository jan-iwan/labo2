from common import data, plot
from pathlib import Path
import numpy as np

CELL_RANGE = "B62:E95"
WORKSHEET = "Hoja 1"


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    cols = df.columns.values.tolist()

    distance = df[cols[0]]
    ampl_recv = df[cols[1]]
    div = df[cols[2]]
    err = df[cols[3]]

    # 3% del valor medido, 5% por la división y el error en el promedio
    error = 0.03 * ampl_recv + 0.05 * div + err

    # Plot result
    plot.data(
        distance,
        ampl_recv,
        error,
        xlabel=cols[0],
        ylabel=cols[1]
    )

    plot.save(path/f"plots/{__name__}.png")
