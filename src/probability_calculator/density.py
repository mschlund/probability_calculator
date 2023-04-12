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
