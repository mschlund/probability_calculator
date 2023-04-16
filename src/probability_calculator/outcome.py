from typing import Protocol, TypeVar, TypedDict, List
from abc import abstractmethod
import math

ExportedOutcome = TypedDict("ExportedOutcome", {"value": float, "probability": float})

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
    def get_probability(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def export(self) -> List[ExportedOutcome]:
        raise NotImplementedError

    @abstractmethod
    def add_probability(self, prob: float) -> None:
        raise NotImplementedError


class DiscreteOutcome(Outcome):
    def __init__(self, value: float, probability: float):
        self.value = value
        self.probability = probability

    def export(self) -> List[ExportedOutcome]:
        return [ExportedOutcome(value=self.value, probability=self.probability)]

    def get_value(self):
        return self.value

    def get_probability(self):
        return self.probability

    def add_probability(self, probability: float):
        self.probability += probability

    def __str__(self) -> str:
        return f"DiscreteOutcome(value={self.value}, probability={self.probability})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DiscreteOutcome):
            return math.isclose(self.value, other.value) and math.isclose(self.probability, other.probability)

        return False

    def __add__(self, other):
        if isinstance(other, DiscreteOutcome):
            value = self.value + other.value
            probability = self.probability * other.probability
            return DiscreteOutcome(value, probability)

        return NotImplemented
