import math
import matplotlib.pyplot as plt


def plotDensity(density, **args):
    outcomes = density.exportOutcomes()
    X, Y = getPlotData(outcomes, **args)

    fig1, ax = plt.subplots()
    ax.plot(X, Y, "o")
    ax.set_ylim(bottom=0)
    plt.show()
    return fig1, ax


def getPlotData(outcomes, merge_tol=1e-6):
    points = []

    for o in outcomes:
        points.append((o["value"], o["prob"]))

    X = []
    Y = []
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
