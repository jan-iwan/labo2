from common import plot, fit
import numpy as np


def main(angle, volt, error) -> None:
    volt_fit, (p_opt, _) = fit.utils.fitnsave(
        fit.f.cos_sq,
        angle,
        volt,
        p0=[0, 1, 1, -10 * np.pi / 180],
        yerr=error
    )

    plot.data_and_fit(
        angle,
        volt,
        error,
        volt_fit,
    )
