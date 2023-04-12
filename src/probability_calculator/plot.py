import matplotlib.pyplot as plt


def plotDensity(density, precision=1e-6):
    outcomes = density.exportOutcomes()
    X, Y = getPlotData(outcomes, precision)

    fig1, ax = plt.subplots()
    ax.plot(X, Y, "o")
    ax.set_ylim(bottom=0)
    plt.show()
    return fig1, ax


def getPlotData(outcomes, precision=1e-6):
    points = []

    for o in outcomes:
        points.append((o["value"], o["prob"]))

    X = []
    Y = []
    lastValue = None
    for value, prob in sorted(points):
        if lastValue is not None and value - lastValue < precision:
            # multiple times the same point -> add probabilities together
            Y[-1] += prob
        else:
            X.append(value)
            Y.append(prob)
            lastValue = value

    return X, Y
