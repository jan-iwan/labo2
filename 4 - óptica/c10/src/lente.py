from common import data, plot, fit

CELL_RANGE = "D4:E22"
WORKSHEET = "ECUACIÓN DE LA LENTE"

# ec. de lente:
# 1/img - 1/obj = 1/f
# con x_lente = 0

# y = mx + b
# (1/img) = 1(1/obj) + 1/f
# m = 1, b = 1/f

ERR_IMG = 5


def main(args: list[str]) -> None:
    # Find dataframe
    df = data.find(
        wsname=WORKSHEET,
        cellrange=CELL_RANGE
    )

    lente = df["Posición la lente [mm]"]
    obj = 40 - lente

    img = df["Posición de la pantalla [mm]"]
    img -= lente

    # Multiply by 1000 to convert 1/mm -> 1/m
    inv_obj = 1000 / obj
    inv_img = 1000 / img

    indirect_err = 1000 * ERR_IMG / img ** 2

    fit_func = fit.utils.fitnsave(
        fit.f.linear,
        inv_obj,
        inv_img,
        yerr=indirect_err
    )

    plot.data_and_fit(
        inv_obj,
        inv_img,
        indirect_err,
        fit_func,
        xlabel=r"Inversa de la posición del objeto [m$^{-1}$]",
        ylabel=r"Inversa de la posición de la imagen [m$^{-1}$]",
        fmt="o"
    )
