from scipy.optimize import curve_fit
import numpy as np
from . import f
from pathlib import Path
from common import data
import pprint
import logging
import sys

opt_show_result = False
logger = logging.getLogger(__name__)


def find(
    func: f.Function,
    data_x,
    data_y,
    p0=None,
    yerr=None
):
    """
    Fit a function to data.
    """

    try:
        param_opt, param_cov = curve_fit(
            func.f,
            data_x,
            data_y,
            p0=p0,
            sigma=yerr,
            absolute_sigma=True
        )
    except RuntimeError as e:
        logger.error("Failed to fit function :(.")
        logger.error(e)
        sys.exit(1)

    # Error in parameters
    param_err = np.sqrt(np.diag(param_cov))

    return param_opt, param_err


# reduced chi-squared
def chi2_r(
    residue,
    y_err,
    n_data,
    n_params
):
    return np.sum((residue / y_err) ** 2) / (n_data - n_params)


# R squared
def r2(
    y_data,
    residuos
):
    return 1 - np.var(residuos) / np.var(y_data)


def result(
    func: f.Function,
    p_opt,
    p_err,
    chi,
    r_sq
) -> list[dict]:
    # Fit statistics
    stats = {
        "Chi^2 red": f"{chi}",
        "R^2": f"{r_sq}",
    } if chi is not None else {
        "R^2": f"{r_sq}",
    }

    # Mean and error of parameters
    params = {
        p: f"{opt} ± {err}"
        for p, opt, err
        in zip(func.params, p_opt, p_err)
    }

    # Bundle into one dictionary
    res: dict = stats
    res.update(params)

    if opt_show_result:
        pprint.pp(res)

    return [res]


def fitnsave(
    func: f.Function,
    x_data,
    y_data,
    saveto: Path | str = None,
    p0=None,
    yerr=None
):
    """
    Fit a function to data and save results.
    Returns y_fit and (param_opt, param_err)
    """

    p_opt, p_err = find(
        func,
        x_data,
        y_data,
        p0=p0,
        yerr=yerr
    )

    y_fit = func.f(x_data, *p_opt)

    residue = y_fit - y_data

    # chi squared is only relevant for lineal fits
    chi_sq_red = chi2_r(
        residue,
        yerr,
        len(residue),
        len(p_opt)
    ) if func is f.linear else None

    r_sq = r2(y_data, residue)

    res = result(
        func,
        p_opt,
        p_err,
        chi_sq_red,
        r_sq
    )

    # Save result to disk
    data.save(res, filename=saveto)

    return y_fit, (p_opt, p_err)
