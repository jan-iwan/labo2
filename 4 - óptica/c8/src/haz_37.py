from common import data, plot, fit

CELL_RANGE = "A2:E16"
WORKSHEET = "BIENPERFIL 0.37m"


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
        p0=[9.2, 100]
    )

    pos_0 = fit_found.params[0]
    fit_found.params[0] = 0

    plot.data_and_fit(
        pos - pos_0,
        volt,
        error,
        fit_found,
        residue_units=(1000, "mVpp")
    )
