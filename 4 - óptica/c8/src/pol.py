from common import data
from pathlib import Path
import numpy as np

CELL_RANGE = "A2:G21"
WORKSHEET = "DETECTOR"


def main(path: Path, args: list[str]) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    angle = df["Ángulo rotado [deg]"] * np.pi / 180
    volt = df["Voltaje [V]"]
    error = df["Error [V]"]

    match args:
        case "cos2":
            from src import pol_cos2
            pol_cos2.main(path, angle, volt, error)

        case "fit":
            from src import pol_fit
            pol_fit.main(path, angle, volt, error)

        case "slider":
            from src import pol_slider
            pol_slider.main(angle, volt, error)
