from typing import Optional, Tuple, List, Literal
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
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
        X, Y = kernelDensityEstimation(
            X, Y, gridsize=gridsize)


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
        gridsize: int = 1000) -> Tuple[List[float], List[float]]:
    """
    estimates the density by using a trapez-like kernel
    """

    deltaX = (X[-1]-X[0])/gridsize
    kdeX = np.linspace(X[0]-deltaX, X[-1]+deltaX, gridsize+3)

    # bw_method parameter optimized for the evenly spaced case
    kernel = stats.gaussian_kde(
        X, weights=Y, bw_method=(X[-1]-X[0])/max(1000, 5*len(X))
    )
    kdeY = kernel(kdeX)

    return kdeX.tolist(), kdeY.tolist()
