from common import data, plot, fit
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

CELL_RANGE = "B12:M69"
WORKSHEET = "INTERFERENCIA"

phase_err = 0.2


def useg_to_rad(phase):
    FREQ = 40_750
    usec_by_sec = 1_000_000

    return 2 * np.pi * phase * FREQ / usec_by_sec


def psi_err(ampl, phi, err_ampl, err_phi):
    sigma_ampl = np.cos(phi) * err_ampl
    sigma_phi = ampl * np.sin(phi) * err_phi

    return np.sqrt(sigma_ampl ** 2 + sigma_phi ** 2)


def main(path: Path) -> None:
    # Find dataframe
    df = data.find(
        path,
        __name__,
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    pos = df["Posición del receptor [mm]"][:-3] - 330

    # Same for all
    err_phi = useg_to_rad(phase_err)

    # Separated

    ampl_1 = df["Amplitud 1 [mVpp]"][:-3]
    phase_1 = useg_to_rad(df["Fase 1 [useg]"][:-3])
    err_ampl_1 = 0.05 * df["Escala"][:-3] + df["Error 1 [mVpp]"][:-3]

    ampl_2 = df["Amplitud 2 [mVpp]"][:-3]
    phase_2 = useg_to_rad(df["Fase 2 [useg]"][:-3])
    err_ampl_2 = 0.05 * df["Escala"][:-3] + df["Error 2 [mVpp]"][:-3]

    phase_1 = np.unwrap(phase_1)
    phase_2 = np.unwrap(phase_2)
    psi_1 = ampl_1 * np.cos(phase_1)
    psi_2 = ampl_2 * np.cos(phase_2)

    err_psi_1 = psi_err(ampl_1, phase_1, err_ampl_1, err_phi)
    err_psi_2 = psi_err(ampl_2, phase_2, err_ampl_2, err_phi)

    ROWS = 2
    COLS = 2
    fig, ax = plt.subplots(
        ROWS,
        COLS,
        sharex=True,
        figsize=(12, 6)
    )

    for row in range(ROWS):
        for col in range(COLS):
            ax[row, col].grid()
            ax[row, col].axvline(50, color="red")
            ax[row, col].axvline(-50, color="green")

    ax[0, 0].set_title("Emisor 1")
    ax[0, 1].set_title("Emisor 2")
    ax[0, 0].set(ylabel="Fase [rad]")
    ax[1, 0].set(ylabel="Perturbación [mVpp]")
    ax[1, 0].set(xlabel=pos.name)
    lmbda = _
    ax[1, 1].set(xlabel=pos.name)
    ax[0, 0].errorbar(pos, phase_1, yerr=err_phi, fmt=".")
    ax[0, 1].errorbar(pos, phase_2, yerr=err_phi, fmt=".")
    ax[1, 0].errorbar(pos, psi_1, yerr=err_psi_1, fmt=".")
    ax[1, 1].errorbar(pos, psi_2, yerr=err_psi_2, fmt=".")

    plot.save(path/f"plots/{__name__}-separated.png")

    # Superposition

    ROWS = 1
    COLS = 2
    fig, ax = plt.subplots(
        ROWS,
        COLS,
        figsize=(12, 4)
    )

    for col in range(COLS):
        ax[col].grid()
        ax[col].axvline(50, color="red")
        ax[col].axvline(-50, color="green")

    ampl_12 = df["Amplitud 12 [mVpp]"][:-3]
    phase_12 = useg_to_rad(df["Fase 12 [useg]"][:-3])
    err_ampl_12 = 0.05 * df["Escala 12 [mVpp]"][:-3] + df["Error 12 [mVpp]"][:-3]

    phase_12 = np.unwrap(phase_12)

    psi_12 = ampl_12 * np.cos(phase_12)
    psi_calc = psi_1 + psi_2

    err_psi_12 = psi_err(ampl_12, phase_12, err_ampl_12, err_phi)

    err_psi_calc = np.sqrt(err_psi_1 ** 2 + err_psi_2 ** 2)

    ax[0].set(xlabel=pos.name)
    ax[1].set(xlabel=pos.name)
    ax[0].set(ylabel="Amplitud [mVpp]")
    ax[1].set(ylabel="Perturbación [mVpp]")

    # Amplitude only
    ax[0].errorbar(pos, ampl_12, yerr=err_ampl_12, fmt=".")

    # psi only
    ax[1].errorbar(pos, psi_12, yerr=err_psi_12, label="Medida", fmt=".")
    ax[1].errorbar(pos, psi_calc, yerr=err_psi_calc, label="Superposición", fmt=".")

    ax[1].legend()

    plot.save(path/f"plots/{__name__}-superpos.png")
