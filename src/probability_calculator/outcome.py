import math


class SimpleOutcome:
    def __init__(self, value, prob):
        self.value = value
        self.prob = prob

    def __str__(self) -> str:
        return f"SimpleOutcome(value={self.value}, prob={self.prob})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SimpleOutcome):
            return math.isclose(self.value, other.value) and math.isclose(self.prob, other.prob)

        return False

    def __add__(self, other):
        if isinstance(other, SimpleOutcome):
            value = self.value + other.value
            prob = self.prob * other.prob
            return SimpleOutcome(value, prob)

        return NotImplemented
