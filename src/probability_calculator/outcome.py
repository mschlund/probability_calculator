from typing import Protocol, TypeVar, TypedDict, List
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

    @abstractmethod
    def addProb(self, prob: float) -> None:
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

    def addProb(self, prob: float):
        self.prob += prob

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
