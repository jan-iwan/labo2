from common import plot, fit
from pathlib import Path
import numpy as np
import pandas as pd
import logging
import sys

logger = logging.getLogger("MAIN")

THETA_ERROR = 0.5 * np.pi / 180


# df entries are "avg+-err", I want avg, err
def read_entry(df_entry: str):
    entry_as_list = df_entry.split("+-")

    avg = float(entry_as_list[0])
    err = float(entry_as_list[1])

    return avg, err


def indirect_measure(df, t, t_err):
    y_0, y_0_err = read_entry(df["y_0"].iloc[0])
    A, A_err = read_entry(df["A"].iloc[0])
    w, w_err = read_entry(df["w"].iloc[0])
    t_0, t_0_err = read_entry(df["theta_0"].iloc[0])

    var_A = (np.cos(w * (t - t_0)) ** 2 * A_err) ** 2

    var_y_0 = y_0_err ** 2

    var_common = (2 * A * np.sin(2 * w * (t - t_0))) ** 2

    var_t_0 = (w * t_0_err) ** 2
    var_t = (w * t_err) ** 2
    var_w = ((t - t_0) * w_err) ** 2

    sigma = np.sqrt(var_A + var_common * (var_w + var_t + var_t_0) + var_y_0)

    cos2 = y_0 + A * np.cos(w * (t - t_0)) ** 2

    return cos2, sigma


def main(cos2_result: Path, theta, volt, volt_error) -> None:
    if not cos2_result.is_file:
        logger.error(f"File {cos2_result} does not exist.")

        sys.exit(1)

    result_df = pd.read_csv(cos2_result)

    cos2, error = indirect_measure(result_df, theta, THETA_ERROR)

    cos2_fit = fit.utils.fitnsave(
        fit.f.linear,
        volt,
        cos2,
        yerr=error
    )

    plot.data_and_fit(
        volt,
        cos2,
        (volt_error, error),
        cos2_fit,
        xlabel="Tensión medida [V]",
        ylabel="Coseno cuadrado del ángulo",
    )
