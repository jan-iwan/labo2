from common import plot, fit
from pathlib import Path
import numpy as np
import pandas as pd
import logging
import sys
from src import pol_cos2

logger = logging.getLogger("MAIN")


def main(path: Path, angle, volt, error) -> None:
    csv_file = path/f"results/{pol_cos2.__name__}.csv"
    if not csv_file.is_file:
        logger.error(f"File {csv_file} does not exist.")

        sys.exit(1)

    df_fit = pd.read_csv(csv_file)
    theta_0 = df_fit["theta_0"].iloc[0]
    theta_0 = float(theta_0.split(" ")[0])

    x = np.cos(angle - theta_0) ** 2

    f = fit.f.linear

    fit_found, _ = fit.utils.fitnsave(
        f,
        x,
        volt,
        yerr=error
    )

    plot.data_and_fit(
        np.cos(angle - theta_0) ** 2,
        volt,
        error,
        fit_found,
        x_error=1
    )
