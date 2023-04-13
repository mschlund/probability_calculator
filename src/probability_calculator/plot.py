from typing import Optional, Tuple, List, Literal
import math
import matplotlib.pyplot as plt
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
        X, Y = kernelDensityEstimation(X, Y, gridsize=gridsize, log_xscale=xscale == "log")

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
        log_xscale: bool = False,
        gridsize: int = 1000):
    """
    estimates the density by using a triangular kernel
    """

    gridsize = min(gridsize, len(X))

    if log_xscale:
        X = [math.log(x) for x in X]

    deltaX = (X[-1] - X[0]) / gridsize
    bandwidth = deltaX
    currentX = X[0] - bandwidth
    lastX = X[-1] + bandwidth

    kdeX: List[float] = []
    kdeY: List[Optional[float]] = []

    while currentX <= lastX:
        kdeX.append(currentX)
        localY = 0
        for i in range(len(X)):
            diffX = abs(X[i] - currentX)
            if diffX < bandwidth:
                if not math.isclose(bandwidth, diffX, rel_tol=1e-13):
                    # isclose keeps numerical issues around 0 away
                    localY += (bandwidth-diffX) / bandwidth * Y[i]
        kdeY.append(localY)

        currentX += deltaX

    if log_xscale:
        kdeX = [math.exp(x) for x in kdeX]

    return kdeX, kdeY
