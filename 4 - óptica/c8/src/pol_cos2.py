from common import plot, fit
import numpy as np

THETA_ERROR = 1 * np.pi / 180


def main(angle, volt, error) -> None:

    # V -> mV
    volt *= 1000

    volt_fit = fit.utils.fitnsave(
        fit.f.cos_sq,
        angle,
        volt,
        p0=[0, 1000, 1, -10 * np.pi / 180],
        yerr=error
    )

    plot.data_and_fit(
        angle,
        volt,
        (THETA_ERROR, error),
        volt_fit,
        xlabel="ángulo del analizador [rad]",
        ylabel="Voltaje [mV]",
    )
