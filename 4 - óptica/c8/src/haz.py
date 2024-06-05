from common import fit
from scipy.special import erf
import numpy as np


A52 = 35193.929024 / (2 * 38424)

A37 = 40826.839434 / (2 * 38424)


def erf_gen(A):
    return fit.f.Function(
        lambda x, x_0, w:
            A * (1 - erf(np.sqrt(2) * (x - x_0) / w)),
        ["x_0", "w"]
    )


def main(path, args: list[str]) -> None:
    match args:
        case "1":
            from src import haz_52
            haz_52.main(erf_gen(A52))

        case "2":
            from src import haz_37
            haz_37.main(erf_gen(A37))

        case "comp":
            from src import haz_comparacion
            haz_comparacion.main(path)

        case _:
            print("No argument passed!")
