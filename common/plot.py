import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Any
from pathlib import Path

logger = logging.getLogger(__name__)

opt_show_plots = False

plt.rcParams.update({"font.size": 14})

DEFAULT_FIGSIZE = (8, 6)


def save(filename, **kwargs):
    plt.tight_layout()

    if filename is not None:
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


def data(
    x_data,
    y_data,
    error,
    fmt=".",
    nosave=False,
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

    # error may be (x_err, y_err) or just y_err
    xerr, yerr = error if isinstance(error, tuple) else None, error

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

    if not nosave:
        save(saveto)

    return fig, ax


def plot_residue(
    x_data,
    residue,
    yerr,
    xlabel: str = None,
    ylabel: str = None,
    saveto: Path = None
):
    fig_res, ax_res = plt.subplots(
        figsize=DEFAULT_FIGSIZE
    )

    ax_res.errorbar(x_data, residue, yerr=yerr, fmt=".")

    ylabel = f"Residuos {get_units(ylabel)}"

    ax_res.set(xlabel=xlabel)
    ax_res.set(ylabel=ylabel)

    ax_res.grid(True)

    ax_res.axhline(0, color="black")

    if saveto is not None:
        # Append '-residue' to path to save figure
        saveto = saveto.parent / f"{saveto.stem}-residue{saveto.suffix}"

        logger.info(f"Saving residue plot to '{saveto}'")

    save(saveto)


def data_and_fit(
    x_data,
    y_data,
    error,
    y_fit,
    nosave=False,
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

    fig, ax = data(
        x_data,
        y_data,
        error,
        nosave=True,
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

    if not nosave:
        save(saveto)

    # Plot residue separately

    residue = y_fit - y_data

    reserr = error[1] if isinstance(error, tuple) else error,

    plot_residue(
        x_data,
        residue,
        reserr,
        xlabel=xlabel if xlabel is not None else x_data.name,
        ylabel=ylabel if ylabel is not None else y_data.name,
        saveto=saveto
    )

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
