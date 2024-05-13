import numpy as np


class Function:
    """
    Mathematical function wrapper with metadata.
    """

    def __init__(
        self,
        func,  # Callable
        params: list[str],  # Parameter names
        eq: str = None  # LaTeX formula
    ):
        self.f = func
        self.params = params
        self.eq = eq


linear = Function(
    lambda x, m, b:
        m * x + b,
    ["m", "b"],
    r"$m\,x + b$"
)

harmonic = Function(
    lambda x, x_0, k, alpha:
        k / (x - x_0) ** alpha,
    ["x_0", "k", "alpha"],
    r"$y_0 + \frac{k}{(x-x_0)^\alpha}$"
)


# Damped harmonic oscillator
lorentz = Function(
    lambda w, w_0, gamma, A:
        A / ((w_0**2 - w**2)**2 + (gamma * w)**2),
    ["w_0", "gamma", "Amplitud"]
)


# Damped oscillator and receiver
def _double_lorentz(w, w_1, w_2, g_1, g_2, A):
    num_left = ((w_1**2 - w**2) * (w_2**2 - w**2) - g_1 * g_2 * w**2)**2
    num_right = ((w_2**2 - w**2) * g_1 * w + (w_1**2 - w**2) * g_2 * w)**2
    den_left = (w_1**2 - w**2)**2 + (g_1 * w)**2
    den_right = (w_1**2 - w**2)**2 + (g_1 * w)**2

    return A * np.sqrt((num_left + num_right) / (den_left + den_right)**2)


double_lorentz = Function(
    _double_lorentz,
    ["w_1", "w_2", "g_1", "g_2", "A"]
)


# Amplitude of wave + relfection
def _fabry_perot(x, x_0, c_1, c_2, alpha, wavelen):
    ampl = c_1 / (x - x_0) ** alpha

    freq = 4 * np.pi / wavelen

    return ampl * np.sqrt(1 + c_2 * np.cos(freq * (x - x_0)))


fabry_perot = Function(
    _fabry_perot,
    ["x_0", "c_1", "c_2", "alpha", "lambda"],
    r"$\frac{c_1}{(x-x_0)^\alpha} \sqrt{1 + c_2\cos(4\pi\frac{\lambda}{x-x_0})}$"
)


def _fabry_perot2(x, x_0, a, R, alpha, wavelen):
    ampl = a * R * np.sqrt(1 / 3 ** alpha) / (x - x_0) ** alpha

    root_term = 3 ** alpha / (2 * R**2) + R**2 / (3**alpha)

    freq = 4 * np.pi / wavelen

    return ampl * np.sqrt(root_term + np.cos(freq * (x - x_0)))


fabry_perot2 = Function(
    _fabry_perot,
    ["x_0", "a", "R", "alpha", "lambda"]
)
