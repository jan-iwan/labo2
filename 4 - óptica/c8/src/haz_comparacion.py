from common import plot
from pathlib import Path
import pandas as pd
import numpy as np

A37 = 40826.839434 / 38424
A52 = 35193.929024 / 38424

# Separación: 2 w sqrt(1/2 ln(2))


def gaussiana(x, a, w):
    return np.sqrt(2 / np.pi) * a / (w ** 2) * np.exp(-2 * (x / w) ** 2)


def calc_div(w):
    # From formula
    sep = 2 * w * np.sqrt(1/2 * np.log(2))

    var = np.abs(np.diff(sep)[0]) / 2
    dx = 520 - 370

    angle = 2 * np.arctan(var / dx) * 180 / np.pi

    return angle


def read_entries(entries):
    avgs = []
    errs = []

    for entry in entries:
        entry_as_list = entry.split("+-")

        avgs.append(float(entry_as_list[0]))
        errs.append(float(entry_as_list[1]))

    return np.array(avgs), np.array(errs)


def main(path: Path) -> None:
    results = [
        pd.read_csv(path/"results/haz_37.csv"),
        pd.read_csv(path/"results/haz_52.csv"),
    ]

    w_entries = [result["w"][0] for result in results]

    w, w_err = read_entries(w_entries)

    x = np.linspace(-1, 1, 100000)
    y = [
        gaussiana(x, A37, w[0]),
        gaussiana(x, A52, w[1])
    ]

    print(f"El ángulo de divergencia es {calc_div(w)} deg.")

    plot.data(
        x, y, None,
        xlabel="Punto en el haz [mm]",
        ylabel="Intensidad [lx]",
        label=["37 cm", "52 cm"],
        plot_method="smooth"
    )
