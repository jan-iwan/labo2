from common import plot, fit
from pathlib import Path
import numpy as np


def main(path: Path, angle, volt, error) -> None:
    f = fit.f.cos_sq

    volt_fit, (p_opt, _) = fit.utils.fitnsave(
        path/f"results/{__name__}.csv",
        f,
        angle,
        volt,
        p0=[1, -10 * np.pi / 180],
        yerr=error
    )

    plot.data_and_fit(
        angle,
        volt,
        error,
        volt_fit,
    )

    plot.save(path/f"plots/{__name__}.png")
