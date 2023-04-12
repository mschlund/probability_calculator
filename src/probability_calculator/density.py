import matplotlib.pyplot as plt
from .outcome import SimpleOutcome


class DiscreteDensity:
    def __init__(self, outcomes=[]):
        self._outcomes = []

        for o in outcomes:
            self._outcomes.append(
                SimpleOutcome(value=o["value"], prob=o["prob"])
            )

    def exportOutcomes(self):
        outcomes = []
        for o in self._outcomes:
            outcomes.append({"value": o.value, "prob": o.prob})

        return outcomes

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


class Dice(DiscreteDensity):
    def __init__(self, n):
        """
        Generates a fair dice with n sides
        """
        prob = 1./n
        outcomes = []
        for i in range(1, n+1):
            outcomes.append({"value": i, "prob": prob})

        super().__init__(outcomes)
