from typing import Optional, List
from .outcome import Outcome, ExportedOutcome, DiskreteOutcome


class DiscreteDensity:
    def __init__(self, outcomes=[], _outcomes: Optional[List[Outcome]]=None):
        self._outcomes: List[Outcome] = _outcomes if _outcomes is not None else []

        for o in outcomes:
            self._outcomes.append(
                DiskreteOutcome(value=o["value"], prob=o["prob"])
            )

    def exportOutcomes(self):
        outcomes: List[ExportedOutcome] = []
        for o in self._outcomes:
            outcomes.extend(o.export())

        return outcomes

    def __mul__(self, other):
        outcomes = []
        for o1 in self._outcomes:
            for o2 in other._outcomes:
                outcomes.append(o1+o2)

        return DiscreteDensity(_outcomes=outcomes)

    def __pow__(self, other):
        if isinstance(other, int):
            if other == 1:
                return self
            elif other > 1:
                return self * (self**(other-1))

        return NotImplemented


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
