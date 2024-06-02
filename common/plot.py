from common.data import get_caller_name
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Any
from pathlib import Path

DEFAULT_EXT = "png"

DEFAULT_FIGSIZE = (8, 6)

logger = logging.getLogger(__name__)

opt_show_plots = False

plt.rcParams.update({"font.size": 14})


def save(
    filename,
    append: str = None,
    **kwargs
):
    plt.tight_layout()

    if filename is None:
        path, name = get_caller_name()

        filename = path / f"plots/{name}.{DEFAULT_EXT}"

    if append is not None:
        filename = filename.parent / \
            f"{filename.stem}-{append}{filename.suffix}"

    logger.info(f"Saving figure '{filename}'.")
    plt.savefig(filename, **kwargs)

    if opt_show_plots:
        logger.info("Showing plot")
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


def _plot_errorbar(
    ax,
    x_data,
    y_data,
    xerr,
    yerr,
    fmt,
    label,
    xlabel,
    ylabel
):
    ax.errorbar(
        x_data,
        y_data,
        x_err=xerr,
        yerr=yerr,
        fmt=fmt,
        label=label
    )

    ax.set(xlabel=xlabel if xlabel is not None else x_data.name)
    ax.set(ylabel=ylabel if ylabel is not None else y_data.name)

    ax.grid(True)

    if label is not None:
        ax.legend()


def data(
    x_data,
    y_data,
    error,
    fmt=".",
    noshow=False,
    saveto: Path = None,
    label: str = None,
    xlabel: str = None,
    ylabel: str = None,
    figsize=DEFAULT_FIGSIZE,
    **kwargs
) -> tuple[Figure, Any]:
    """
    Plot data with errors.
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
        # error may be (x_err, y_err) or just y_err
        xerr, yerr = error if isinstance(error, tuple) else None, error

        xlabel = xlabel if xlabel is not None else x_data.name
        ylabel = ylabel if ylabel is not None else y_data.name

        _plot_errorbar(
            ax,
            x_data, y_data,
            xerr, yerr,
            fmt, label, xlabel, ylabel
        )

    # There may be multiple y_data
    else:
        logger.warning(f"Plotting {rows} rows.")

        for i in range(rows):
            # error may be (x_err, y_err) or just y_err
            err = error[i]
            xerr, yerr = err if isinstance(err[i], tuple) else None, err

            _plot_errorbar(
                ax[i],
                x_data[i], y_data[i],
                xerr, yerr,
                fmt, label, xlabel, ylabel
            )

    if not noshow:
        save(saveto)

    return fig, ax


def data_and_fit(
    x_data,
    y_data,
    error,
    y_fit,
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

    xlabel = xlabel if xlabel is not None else x_data.name
    ylabel = ylabel if ylabel is not None else y_data.name

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

    # Plot fit in 'ax' (on top of the data)
    ax.plot(
        x_data,
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
        y_fit - y_data,  # residue
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
