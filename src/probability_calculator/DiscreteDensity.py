import matplotlib.pyplot as plt


class DiscreteDensity:
    def __init__(self, outcomes=[]):
        self._outcomes = []

        for o in outcomes:
            self._outcomes.append(
                SimpleOutcome(value=o["value"], prob=o["prob"])
            )

    def plot(self):
        X, Y = self._getPlotData()

        fig1, ax = plt.subplots()
        ax.plot(X, Y, "o")
        ax.set_ylim(bottom=0)
        plt.show()
        return fig1, ax

    def _getPlotData(self, precision=1e-6):
        points = []

        for o in self._outcomes:
            points.append((o.value, o.prob))

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


class SimpleOutcome:
    def __init__(self, value, prob):
        self.value = value
        self.prob = prob
