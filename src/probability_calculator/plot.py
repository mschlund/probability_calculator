from typing import Optional, Tuple, List, Literal
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from .outcome import ExportedOutcome


def plotDensity(
        density,
        xscale: Literal["linear", "log"] = "linear",
        yscale: Literal["linear", "log"] = "linear",
        kde=False,
        gridsize: int = 1000,
        **args):
    outcomes = density.exportOutcomes()
    X, Y = getPlotData(outcomes, **args)

    if kde:
        X, Y = kernelDensityEstimation(
            X, Y, gridsize=gridsize)

    fig1, ax = plt.subplots()
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ax.plot(X, Y, "o" if not kde else "-")
    if yscale == "linear":
        ax.set_ylim(bottom=0)
    plt.show()
    return fig1, ax


def getPlotData(outcomes: List[ExportedOutcome], merge_tol=1e-6) -> Tuple[List[float], List[float]]:
    points = []

    for o in outcomes:
        points.append((o["value"], o["prob"]))

    X: List[float] = []
    Y: List[float] = []
    lastValue = None
    for value, prob in sorted(points):
        if lastValue is not None and math.isclose(value, lastValue, abs_tol=merge_tol):
            # multiple times the same point -> add probabilities together
            Y[-1] += prob
        else:
            X.append(value)
            Y.append(prob)
            lastValue = value

    return X, Y


def kernelDensityEstimation(
        X: List[float],
        Y: List[float],
        gridsize: int = 1000) -> Tuple[List[float], List[float]]:
    """
    estimates the density by using a trapez-like kernel
    """

    deltaX = (X[-1]-X[0])/gridsize
    kdeX = np.linspace(X[0]-2*deltaX, X[-1]+2*deltaX, gridsize)

    # bw_method parameter optimized for the evenly spaced case
    kernel = stats.gaussian_kde(
        X, weights=Y, bw_method=(X[-1]-X[0])/max(1000, 5*len(X))
    )
    kdeY = kernel(kdeX)

    return kdeX.tolist(), kdeY.tolist()
