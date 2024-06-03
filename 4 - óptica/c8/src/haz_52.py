from common import data, plot, fit

CELL_RANGE = "A2:E21"
WORKSHEET = "PERFIL 0.52m"


def main(erf) -> None:
    # Find dataframe
    df = data.find(
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    pos = df["Posición [mm]"]
    volt = df["Voltaje [V]"]
    error = df["Error intens"]

    fit_found = fit.utils.fitnsave(
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
    )
