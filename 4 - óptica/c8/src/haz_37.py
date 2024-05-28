from common import data, plot
from pathlib import Path
import numpy as np

CELL_RANGE = "A2:E16"
WORKSHEET = "BIENPERFIL 0.37m"


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    pos = df["Posición [mm]"]
    volt = df["Voltaje [V]"]
    # error =

    plot.data(pos, volt, 0)
    plot.save()
