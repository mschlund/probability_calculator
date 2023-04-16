from typing import Optional, Tuple, List, Literal
import math
import matplotlib.pyplot as plt
from .outcome import ExportedOutcome


def plot_density(
        density,
        xscale: Literal["linear", "log"] = "linear",
        yscale: Literal["linear", "log"] = "linear",
        kde=False,
        gridsize: int = 1000,
        **args):
    outcomes = density.exportOutcomes()
    X, Y = get_plot_data(outcomes, **args)

    if kde:
        X, Y = kernel_density_estimation(X, Y, gridsize=gridsize, log_xscale=xscale == "log")

    fig, ax = plt.subplots()
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ax.plot(X, Y, "o" if not kde else "-")
    if yscale == "linear":
        ax.set_ylim(bottom=0)
    plt.show()
    plt.close()
    return fig, ax


def get_plot_data(outcomes: List[ExportedOutcome], merge_tol=1e-6) -> Tuple[List[float], List[float]]:
    points = [(o["value"], o["probability"]) for o in outcomes]

    x: List[float] = []
    y: List[float] = []
    last_value = None
    for value, probability in sorted(points):
        if last_value is not None and math.isclose(value, last_value, abs_tol=merge_tol):
            # multiple times the same point -> add probabilities together
            y[-1] += probability
        else:
            x.append(value)
            y.append(probability)
            last_value = value

    return x, y


def kernel_density_estimation(
        X: List[float],
        Y: List[float],
        log_xscale: bool = False,
        gridsize: int = 1000):
    """
    estimates the density by using a triangular kernel
    """

    gridsize = min(gridsize, len(X))

    if log_xscale:
        X = [math.log(x) for x in X]

    delta_x = (X[-1] - X[0]) / gridsize
    bandwidth = delta_x
    current_x = X[0] - bandwidth
    last_x = X[-1] + bandwidth

    kde_x: List[float] = []
    kde_y: List[Optional[float]] = []

    while current_x <= last_x:
        kde_x.append(current_x)
        local_y = 0
        for i in range(len(X)):
            diff_x = abs(X[i] - current_x)
            if diff_x < bandwidth:
                if not math.isclose(bandwidth, diff_x, rel_tol=1e-13):
                    # isclose keeps numerical issues around 0 away
                    local_y += (bandwidth - diff_x) / bandwidth * Y[i]
        kde_y.append(local_y)

        current_x += delta_x

    if log_xscale:
        kde_x = [math.exp(x) for x in kde_x]

    return kde_x, kde_y
