from typing import Protocol, TypeVar, TypedDict, List, Optional
from abc import abstractmethod
import math

ExportedOutcome = TypedDict("ExportedOutcome", {"value": float, "prob": float})

T = TypeVar("T", covariant=True)


class Outcome(Protocol[T]):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other: object) -> T:
        raise NotImplementedError

    @abstractmethod
    def getValue(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def getProb(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def export(self) -> List[ExportedOutcome]:
        raise NotImplementedError

class DiskreteOutcome(Outcome):
    def __init__(self, value: float, prob: float):
        self.value = value
        self.prob = prob

    def export(self) -> List[ExportedOutcome]:
        return [{"value": self.value, "prob": self.prob}]

    def getValue(self):
        return self.value

    def getProb(self):
        return self.prob

    def __str__(self) -> str:
        return f"DiskreteOutcome(value={self.value}, prob={self.prob})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DiskreteOutcome):
            return math.isclose(self.value, other.value) and math.isclose(self.prob, other.prob)

        return False

    def __add__(self, other):
        if isinstance(other, DiskreteOutcome):
            value = self.value + other.value
            prob = self.prob * other.prob
            return DiskreteOutcome(value, prob)

        return NotImplemented

class CombinedOutcome(Outcome):

    def __init__(self, outcomes: List[Outcome]):
        # calculate total maxv, minv, prob, ev, and evv of given outcomes
        prob: float = 0.
        ev: float = 0.
        evv: float = 0.
        maxv: Optional[float] = None
        minv: Optional[float] = None
        for o in outcomes:
            for e in o.export():
                if maxv is None or maxv < e["value"]:
                    maxv = e["value"]
                if minv is None or minv > e["value"]:
                    minv = e["value"]
                prob += e["prob"]
                ev += e["prob"]*e["value"]
                evv += e["prob"]*e["value"]**2
            if isinstance(o, CombinedOutcome):
                if minv is None or minv > o.minv:
                    minv = o.minv
                if maxv is None or maxv < o.maxv:
                    maxv = o.maxv
        
        if minv is None or maxv is None:
            raise Exception("No outcomes found to combine")

        # generate two outcomes which represent the same prob, ev, and evv
        self.prob: float = prob
        self.value: float = ev / prob
        f1: float = (maxv - self.value) / (maxv-minv) if not math.isclose(minv, maxv) else 0.5
        print(minv, maxv, f1)
        prob1: float = f1 * prob
        prob2: float = prob - prob1
        t: float = math.sqrt((evv-ev**2/prob)/f1/(1-f1))

        self.prob1: float = prob1
        self.prob2: float = prob2
        self.value1: float = self.value - (1-f1)*t
        self.value2: float = self.value + f1*t
        self.minv: float = minv
        self.maxv: float = maxv

    def export(self) -> List[ExportedOutcome]:
        return [
            {"value": self.value1, "prob": self.prob1},
            {"value": self.value2, "prob": self.prob2}
        ]

    def getValue(self):
        return self.value

    def getProb(self):
        return self.prob

    def __str__(self) -> str:
        return f"CombinedOutcome(value1={self.value1}, prob1={self.prob1}, value2={self.value2}, prob2={self.prob2})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CombinedOutcome):
            return math.isclose(self.value1, other.value1) and \
                math.isclose(self.prob1, other.prob1) and \
                math.isclose(self.value2, other.value2) and \
                math.isclose(self.prob2, other.prob2)
        
        return False


    def __add__(self, other):
        return NotImplemented
