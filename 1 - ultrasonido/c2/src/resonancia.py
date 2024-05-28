from common import data, plot, fit
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

CELL_RANGE = "G3:J49"
WORKSHEET = "Hoja 1"


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        # path,
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

    f = fit.f.lorentz
    param_opt, param_err = fit.utils.find(
        f,
        freq_sent,
        freq_recv,
        p0=[40.3, 1.52, 11_000_000.0],
        yerr=error
    )

    # Save result
    data.save(
        path/f"results/{__name__}.csv",
        {
            "w_0": [f"{param_opt[0]} ± {param_err[0]}"],
            "gamma": [f"{param_opt[1]} ± {param_err[1]}"],
            "amplitud": [f"{param_opt[2]} ± {param_err[2]}"],
        }
    )

    plot.data(
        freq_sent,
        freq_recv,
        error,
        figsize=(10, 8)
    )

    # Plot result
    # fit_found = f.f(freq_sent, *param_opt)
    # plot.data_and_fit(
    #     freq_sent,
    #     freq_recv,
    #     error,
    #     fit_found,
    #     xlabel=cols[0],
    #     ylabel=cols[1]
    # )

    plot.save(path/f"plots/{__name__}.png")
