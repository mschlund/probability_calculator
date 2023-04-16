from typing import Protocol, TypeVar, TypedDict, List, Optional
from abc import abstractmethod
import math

ExportedOutcome = TypedDict("ExportedOutcome", {"value": float, "p": float})

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
    def get_value(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_p(self) -> float:
        """
        Returns the pability ot the outcome
        """
        raise NotImplementedError

    @abstractmethod
    def export(self) -> List[ExportedOutcome]:
        raise NotImplementedError


class DiscreteOutcome(Outcome):
    def __init__(self, value: float, p: float):
        self.value = value
        self.p = p

    def export(self) -> List[ExportedOutcome]:
        return [ExportedOutcome(value=self.value, p=self.p)]

    def get_value(self):
        return self.value

    def get_p(self):
        return self.p

    def __str__(self) -> str:
        return f"DiscreteOutcome(value={self.value}, p={self.p})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DiscreteOutcome):
            return math.isclose(self.value, other.value) and math.isclose(self.p, other.p)

        return False

    def __add__(self, other):
        if isinstance(other, DiscreteOutcome):
            value = self.value + other.value
            p = self.p * other.p
            return DiscreteOutcome(value, p)

        return NotImplemented


class CombinedOutcome(Outcome):

    def __init__(self, outcomes: List[Outcome]):
        # calculate total max_value, min_value, p, ev, and evv of given outcomes
        p: float = 0.
        ev: float = 0.
        evv: float = 0.
        max_value: Optional[float] = None
        min_value: Optional[float] = None
        for o in outcomes:
            for e in o.export():
                if max_value is None or max_value < e["value"]:
                    max_value = e["value"]
                if min_value is None or min_value > e["value"]:
                    min_value = e["value"]
                p += e["p"]
                ev += e["p"]*e["value"]
                evv += e["p"]*e["value"]**2
            if isinstance(o, CombinedOutcome):
                if min_value is None or min_value > o.min_value:
                    min_value = o.min_value
                if max_value is None or max_value < o.max_value:
                    max_value = o.max_value

        if min_value is None or max_value is None:
            raise Exception("No outcomes found to combine")

        # generate two outcomes which represent the same p, ev, and evv
        self.p: float = p
        self.value: float = ev / p
        f1: float = (max_value - self.value) / \
            (max_value-min_value) if not math.isclose(min_value, max_value) else 0.5
        p1: float = f1 * p
        p2: float = p - p1
        t: float = math.sqrt((evv-ev**2/p)/f1/(1-f1))

        self.p1: float = p1
        self.p2: float = p2
        self.value1: float = self.value - (1-f1)*t
        self.value2: float = self.value + f1*t
        self.min_value: float = min_value
        self.max_value: float = max_value

    def export(self) -> List[ExportedOutcome]:
        return [
            {"value": self.value1, "p": self.p1},
            {"value": self.value2, "p": self.p2}
        ]

    def get_value(self):
        return self.value

    def get_p(self):
        return self.p

    def __str__(self) -> str:
        return f"CombinedOutcome(value1={self.value1}, p1={self.p1}, value2={self.value2}, p2={self.p2})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CombinedOutcome):
            return math.isclose(self.value1, other.value1) and \
                math.isclose(self.p1, other.p1) and \
                math.isclose(self.value2, other.value2) and \
                math.isclose(self.p2, other.p2)

        return False

    def __add__(self, other):
        return NotImplemented
