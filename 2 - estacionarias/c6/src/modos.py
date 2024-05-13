from common import data, plot, fit
from pathlib import Path
import matplotlib.pyplot as plt
import logging
import numpy as np

WORKSHEET = "Hoja 1"
CELL_RANGE = "A13:E36"


def main(path: Path) -> None:
    df = data.find(
        path,
        f"{__name__}-max",
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )
    return
