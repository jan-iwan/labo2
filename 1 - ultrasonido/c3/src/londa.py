from common import data, plot, fit
from pathlib import Path

CELL_RANGE = "A3:B17"
WORKSHEET = "lambda"


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    cols = df.columns.values.tolist()

    dist = df[cols[0]]
    wavelen = df[cols[1]]

    error = 1

    fit_found, _ = fit.utils.fitnsave(
        path/f"results/{__name__}.csv",
        fit.f.linear,
        wavelen,
        dist,
        yerr=error
    )

    # Plot result
    plot.data_and_fit(
        wavelen,
        dist,
        error,
        fit_found,
    )

    plot.save(path/f"plots/{__name__}.png")
