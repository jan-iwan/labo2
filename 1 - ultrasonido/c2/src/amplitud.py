from common import data, plot, fit
from pathlib import Path
import numpy as np

CELL_RANGE = "B43:E53"
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

    ampl_sent = df[cols[0]]
    ampl_recv = df[cols[1]]
    div = df[cols[2]]
    err = df[cols[3]]

    # 3% del valor medido, 5% por la división y el error en el promedio
    error = 0.03 * ampl_recv + 0.05 * div + err

    # Fit data
    f = fit.f.linear
    param_opt, param_err = fit.utils.find(f, ampl_sent, ampl_recv)

    # Save result
    data.save(
        path/f"results/{__name__}.csv",
        {
            "Pendiente": [f"{param_opt[0]} ± {param_err[0]}"],
            "Ordenada": [f"{param_opt[1]} ± {param_err[1]}"],
        }
    )

    # Plot result
    pred = f.f(ampl_sent, *param_opt)
    plot.data_and_fit(
        ampl_sent,
        ampl_recv,
        error,
        pred,
        xlabel=cols[0],
        ylabel=cols[1]
    )

    plot.save(path/f"plots/{__name__}.png")
