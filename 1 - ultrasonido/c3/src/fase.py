from common import data, plot
from pathlib import Path
import numpy as np

CELL_RANGE = "A2:F39"
WORKSHEET = "fase"

# Resonance
FREQ = 40_750

usec_by_sec = 1_000_000

THETA_ERROR = 1 * np.pi / 180.0


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    cols = df.columns.values.tolist()

    angle = df[cols[0]] + 90
    phase = df[cols[5]]

    # Angle in degrees shuold be in radians
    angle *= np.pi / 180.0

    # phase = 2 * pi * freq
    # phase is in microseconds
    phase *= 2 * np.pi * FREQ / usec_by_sec

    # Checkear error del osciloscopio
    error = 0.2

    # No offset
    plot.data_polar(
        angle,
        phase,
        rerr=error,
        terr=THETA_ERROR,
    )

    plot.save(path/f"plots/{__name__}.png")

    # Offset origin
    plot.data_polar(
        angle,
        phase,
        rerr=error,
        terr=THETA_ERROR,
        rorigin=-10
    )

    plot.save(path/f"plots/{__name__}-offset.png")
