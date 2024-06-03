from common import utils, fit
import logging
import numpy as np
import matplotlib.pyplot as plt

# Types
from pandas.core.series import Series
from matplotlib.figure import Figure
from typing import Any
from pathlib import Path

PLOTS_DIR = "plots"

DEFAULT_EXT = "png"

DEFAULT_FIGSIZE = (8, 6)
DPI = 100

logger = logging.getLogger(__name__)

opt_show_plots = False

plt.rcParams.update({"font.size": 14})


def save(
    filename,
    append: str = None,
    **kwargs
):
    plt.tight_layout()

    # Default save location
    if filename is None:
        path, name = utils.get_caller_name()

        stem = f"{name}.{DEFAULT_EXT}"

        filename = path / PLOTS_DIR / stem

    if append is not None:
        filename = filename.parent / \
            f"{filename.stem}-{append}{filename.suffix}"

    logger.info(f"Saving figure at '{filename}'.")
    plt.savefig(filename, **kwargs)

    if opt_show_plots:
        logger.info(f"Showing plot for '{filename.stem}'.")
        plt.show()

    plt.close()


def get_units(label: str) -> str:
    """
    Extract units from a string.
    If `label` is "Weight [Kg]", the units are "[Kg]".
    """

    if label is None:
        return ""

    # Units are always at the end of a string
    units = label.split(" ")[-1]

    # Units are enclosed by "[]"
    if units[0] == '[' and units[-1] == ']':
        return units

    else:
        return ""


def _data_name(data) -> str | None:
    if isinstance(data, Series):
        return data.name

    else:
        logger.warning("Label not specified")
        return None


def _plot_errorbar(
    ax,
    x_data,
    y_data,
    error,
    fmt,
    label,
    xlabel,
    ylabel
):
    # error may be (x_err, y_err) or just y_err
    (xerr, yerr) = error if isinstance(error, tuple) else (None, error)

    ax.errorbar(
        x_data,
        y_data,
        xerr=xerr,
        yerr=yerr,
        fmt=fmt,
        label=label
    )

    ax.set(xlabel=xlabel if xlabel is not None else _data_name(x_data))
    ax.set(ylabel=ylabel if ylabel is not None else _data_name(y_data))

    ax.grid(True)

    if label is not None:
        ax.legend()


def data(
    x_data,
    y_data,
    error: Any | tuple[Any],
    fmt=".",
    noshow=False,           # don't show the plot
    saveto: Path = None,    # custom save path
    label: str = None,
    xlabel: str = None,
    ylabel: str = None,
    figsize=DEFAULT_FIGSIZE,
    **kwargs
) -> tuple[Figure, Any]:
    """
    Plot data with errors. Accepts multiple `y_data` asociated with the same
    `x_data`, if that is the case, the plot will have as many rows as there are
    elements in `y_data`
    . `error` can be either the error in `y_data` or a tuple containing
    the errors in `x_data` and `y_data`, i.e. `(x_err, y_err)`
    """

    # There may be multiple y_data
    # if y_data is a list of y_datas, create a subplot with as many rows as
    # there are elements in the list.

    rows = 1 if not isinstance(y_data, list) else len(y_data)
    cols = 1

    fig, ax = plt.subplots(
        rows,
        cols,
        figsize=figsize,
        sharex=False if rows == 1 else True,
        **kwargs
    )

    if rows == 1:
        logger.debug("Plotting data")
        _plot_errorbar(
            ax,
            x_data, y_data,
            error,
            fmt, label, xlabel, ylabel
        )

    # There may be multiple y_data
    else:
        logger.info(f"Plotting {rows} rows.")

        for i in range(rows):
            _plot_errorbar(
                ax[i],
                x_data[i], y_data[i],
                error[i],
                fmt, label, xlabel, ylabel
            )

    # noshow is useful if wanting to add something to ax later in the code
    if not noshow:
        save(saveto)

    return fig, ax


def data_and_fit(
    x_data,
    y_data,
    error,
    fit_func: fit.f.EvalFunction,
    noshow=False,
    saveto: Path = None,
    datalabel: str = "Mediciones",
    fitlabel: str = "Ajuste",
    xlabel: str = None,
    ylabel: str = None,
    figsize=DEFAULT_FIGSIZE,
    **kwargs
):
    """
    Plot data, fit and residue.
    """

    xlabel = xlabel if xlabel is not None else _data_name(x_data)
    ylabel = ylabel if ylabel is not None else _data_name(y_data)

    fig, ax = data(
        x_data,
        y_data,
        error,
        noshow=True,
        label=datalabel,
        xlabel=xlabel,
        ylabel=ylabel,
        **kwargs,
    )

    # If function is linear, use only 2 points for y_fit
    if fit_func.func is fit.f.linear:
        x_fit = np.array([min(x_data), max(x_data)])

    # else, create a higher resolution y_fit
    else:
        # Number of points depends on plot width
        n_points = DEFAULT_FIGSIZE[0] * DPI
        logger.info(f"Using {n_points} points to plot fit.")

        x_fit = np.linspace(min(x_data), max(x_data), n_points)

    y_fit = fit_func.func.f(x_fit, *fit_func.params)

    # Plot fit in 'ax' (on top of the data)
    ax.plot(
        x_fit,
        y_fit,
        label=fitlabel
    )

    if fitlabel is not None:
        ax.legend()

    if not noshow:
        save(saveto, append="fit")

    # Plot residue separately

    fig_res, ax_res = plt.subplots(
        figsize=DEFAULT_FIGSIZE
    )

    ax_res.errorbar(
        x_data,
        fit_func.residue,
        yerr=error[1] if isinstance(error, tuple) else error,
        fmt=".")

    ylabel = f"Residuos {get_units(ylabel)}"

    ax_res.set(xlabel=xlabel)
    ax_res.set(ylabel=ylabel)

    ax_res.grid(True)

    ax_res.axhline(0, color="black")

    # Append '-residue' to path to save figure
    save(saveto, append="residue")

    return fig, ax


def data_polar(
    theta_data,
    r_data,
    rerr=None,
    terr=None,
    title: str = None,
    label: str = None,
    figsize=DEFAULT_FIGSIZE,
    rorigin=None,
    rlabel=None,
    **kwargs
):
    """
    Plot data in polar coordinates.
    """

    fig, ax = plt.subplots(
        figsize=figsize,
        subplot_kw={'projection': 'polar'},
        *kwargs
    )

    ax.errorbar(
        theta_data,
        r_data,
        xerr=terr,
        yerr=rerr,
        fmt=".",
        label=label
    )

    ax.set_thetamin(np.min(theta_data * 180 / np.pi))
    ax.set_thetamax(np.max(theta_data * 180 / np.pi))
    ax.set(ylabel=rlabel)

    if rorigin is not None:
        ax.set_rorigin(rorigin)

    if label is not None:
        ax.legend()

    return
