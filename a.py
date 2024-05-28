import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 8))

x = np.linspace(0, 1, 100)
y = np.linspace(0, 3, 100)

ax.plot(x, y)

v = [1, 20, 50, 77]

ax.vlines(v, 0, 1, color="black")
plt.show()
