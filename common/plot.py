from common import utils, fit
import logging
import numpy as np
import matplotlib.pyplot as plt

# Types
from pandas.core.series import Series
from matplotlib.figure import Figure
from typing import Any
from pathlib import Path

ArrayLike = np._typing.ArrayLike

PLOTS_DIR = "plots"
DEFAULT_EXT = "png"
DEFAULT_FIGSIZE = (8, 6)
DPI = 100
FONT_SIZE = 18
DEFAULT_FMT = "o"

logger = logging.getLogger(__name__)

opt_show_plots = False

plt.rcParams.update({"font.size": FONT_SIZE})


def save(
    filename: Path = None,
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
    x_data, y_data,
    xerr, yerr,
    fmt, label, xlabel, ylabel
):

    # Simple plot
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


def _plot_smooth(
    ax,
    x_data, y_data,
    xerr, yerr,
    fmt, label, xlabel, ylabel
):
    # Simple plot
    ax.plot(
        x_data,
        y_data,
        label=label
    )

    ax.set(xlabel=xlabel if xlabel is not None else _data_name(x_data))
    ax.set(ylabel=ylabel if ylabel is not None else _data_name(y_data))

    ax.grid(True)

    if label is not None:
        ax.legend()


plot_functions = {
    "errorbar": _plot_errorbar,
    "smooth": _plot_smooth,
}


def data(
    x_data: Any,
    y_data: Any | list[Any],
    error: Any | tuple[Any],
    fmt=DEFAULT_FMT,
    label: str | list[str] = None,
    xlabel: str = None,
    ylabel: str = None,
    figsize=DEFAULT_FIGSIZE,
    noshow=False,           # don't show the plot
    saveto: Path = None,    # custom save path
    separate_rows=False,    # use a different row for each plot if provided
    plot_method: str = "errorbar",
    **kwargs
) -> tuple[Figure, Any]:
    """
    Plot data with errors. Accepts multiple `y_data` asociated with the same
    `x_data` (i.e. multiple sets of data), if that is the case, either all sets
    of data will be plotted together or each one will be in a separate row.
    `error` can be either the error in `y_data` or a tuple containing
    the errors in `x_data` and `y_data`, i.e. `(x_err, y_err)`. If `y_data` is a
    list of y_datas, y_err shuold be a list as well.
    """

    # There may be multiple y_data
    multiplot = False if not isinstance(y_data, list) else len(y_data)

    if not multiplot and separate_rows:
        logger.warning(
            "Specified separate rows but there is only one set of data"
        )

    # if specified separate_rows, plot
    rows = 1 if not multiplot or not separate_rows else multiplot
    cols = 1

    fig, ax = plt.subplots(
        rows,
        cols,
        figsize=figsize,
        sharex=False if rows == 1 else True,
        **kwargs
    )

    # error may be (x_err, y_err) or just y_err
    (xerr, yerr) = error if isinstance(error, tuple) else (None, error)

    if yerr is None:
        yerr = [0 for _ in range(multiplot)] if multiplot else 0

    plot_function = plot_functions[plot_method]

    # Simple plot for only one set of data
    if rows == 1:
        if not multiplot:
            logger.info("Plotting data.")

            plot_function(
                ax,
                x_data, y_data,
                xerr, yerr,
                fmt, label, xlabel, ylabel
            )

        # There are multiple y_data, plot them together
        else:
            logger.info(f"Plotting {len(y_data)} sets of data.")

            for i in range(multiplot):
                lab = label[i] if isinstance(label, list) else label

                plot_function(
                    ax,
                    x_data, y_data[i],
                    xerr, yerr[i],
                    fmt, lab, xlabel, ylabel
                )

    # There may be multiple y_data, plot them in separate rows
    else:
        logger.info(f"Plotting {rows} rows.")

        for i in range(rows):
            plot_function(
                ax[i],
                x_data, y_data[i],
                xerr, yerr[i],
                fmt, label, xlabel, ylabel
            )

    # noshow is useful if wanting to add something to the plot
    if not noshow:
        save(saveto)

    return fig, ax


def data_and_fit(
    x_data: Any,
    y_data: Any,
    error: Any | tuple[Any],
    fit_func: fit.f.EvalFunction,
    fmt=DEFAULT_FMT,
    figsize=DEFAULT_FIGSIZE,
    datalabel: str = "Mediciones",
    fitlabel: str = "Ajuste",
    xlabel: str = None,
    ylabel: str = None,
    residue_units: tuple[float, str] = None,
    noshow=False,
    saveto: Path = None,
    **kwargs
):
    """
    Plot data, fit and residue. Works similar to `plot.data()` except that
    `y_data` may only contain a single array of data.
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
        fmt=fmt,
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

    yerr = error[1] if isinstance(error, tuple) else error

    if residue_units is None:
        # Use units from ylabel
        ylabel = f"Residuos {get_units(ylabel)}"

    else:
        # Change units for residue
        fit_func.residue *= residue_units[0]
        yerr *= residue_units[0]

        ylabel = f"Residuos [{residue_units[1]}]"

    ax_res.errorbar(
        x_data,
        fit_func.residue,
        yerr=yerr,
        fmt=fmt)

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
    fmt=DEFAULT_FMT,
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
        fmt=fmt,
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
