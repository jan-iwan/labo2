from common import plot
import matplotlib.pyplot as plt
import numpy as np


def slider_update(line, fig, angles, val):
    line.set_ydata(np.cos(angles - val) ** 2)
    fig.canvas.draw_idle()


def main(angle, volt, error) -> None:
    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    line, = ax.plot(
        angle,
        np.cos(angle) ** 2,
        'o'
    )

    ax.plot(
        angle,
        volt,
        '.'
    )

    ax_slider = fig.add_axes([0.25, 0.1, 0.65, 0.03])

    slider = plot.Slider(
        ax=ax_slider,
        label="Slider",
        valmin=0,
        valmax=2 * np.pi,
        valinit=0
    )

    slider.on_changed(
        lambda val: slider_update(line, fig, angle, val)
    )

    plot.save()
