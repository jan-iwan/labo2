import matplotlib.pyplot as plt
import logging
import numpy as np

logger = logging.getLogger(__name__)

opt_show_plots = False

plt.rcParams.update({"font.size": 14})

def save(*args, **kwargs):
    logger.info(f"Saving figure '{args[0]}'.")
    plt.tight_layout()
    plt.savefig(*args, bbox_inches='tight', **kwargs)

    if opt_show_plots:
        logger.info(f"Showing plot por '{args[0]}'.")
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
    y_error,
    title: str = None,
    label: str = None,
    xlabel: str = None,
    ylabel: str = None,
    figsize=(8, 6),
    **kwargs
):
    """
    Plot data with errors.
    """

    fig, ax = plt.subplots(
        figsize=figsize,
        *kwargs
    )

    ax.errorbar(x_data, y_data, yerr=y_error, fmt="o", label=label)

    ax.set(xlabel=xlabel if xlabel is not None else x_data.name)
    ax.set(ylabel=ylabel if ylabel is not None else y_data.name)
    ax.grid()

    if label is not None:
        ax.legend()

    return


def data_polar(
    theta_data,
    r_data,
    rerr=None,
    terr=None,
    title: str = None,
    label: str = None,
    figsize=(8, 6),
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


def data_and_fit(
    x_data,
    y_data,
    y_error,
    y_fit,
    title: str = None,
    label: str = "Datos",
    fitlabel: str = None,
    xlabel: str = None,
    ylabel: str = "Ajuste",
    figsize=(8, 6),
    nofit=False,
    **kwargs
):
    """
    Plot data, fit and residue.
    """

    fig, ax = plt.subplots(
        2,
        1,
        sharex=True,
        figsize=figsize,
        gridspec_kw={"height_ratios": (2, 1)},
        *kwargs
    )

    # Graph data and fit (y_fit) on top of each other
    ax[0].errorbar(
        x_data,
        y_data,
        yerr=y_error,
        fmt=".",
        label=label
    )

    if not nofit:
        ax[0].plot(x_data, y_fit, label=fitlabel)

    # Graph differences between measurement and prediction (fit) in a
    # separate subplot
    residue = y_fit - y_data
    ax[1].errorbar(x_data, residue, yerr=y_error, fmt=".")

    # Change looks for each subplot
    ax[0].set_title(title)
    ax[0].set(ylabel=ylabel if ylabel is not None else y_data.name)
    ax[0].legend()
    ax[0].grid()

    ax[1].set(xlabel=xlabel if xlabel is not None else x_data.name)
    ax[1].set(ylabel="Residuos")
    ax[1].axhline(0, color="black")
    ax[1].grid()

    return fig, ax
