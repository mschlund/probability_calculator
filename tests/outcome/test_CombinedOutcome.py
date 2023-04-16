from typing import List
import math
from probability_calculator.outcome import DiscreteOutcome, CombinedOutcome
from probability_calculator.outcome import ExportedOutcome


class TestCombinedOutcome():
    def _exportIsClose(self, l1: List[ExportedOutcome], l2: List[ExportedOutcome]) -> bool:
        if len(l1) != len(l2):
            return False

        for e1, e2 in zip(l1, l2):
            if not math.isclose(e1["value"], e2["value"]) or not math.isclose(e1["p"], e2["p"]):
                return False

        return True

    def test_simple(self):
        o = CombinedOutcome(
            [DiscreteOutcome(1, 1. / 4), DiscreteOutcome(5, 3. / 4)])
        assert str(
            o) == "CombinedOutcome(value1=1.0, p1=0.25, value2=5.0, p2=0.75)"
        assert o.export() == [
            {"value": 1., "p": 0.25},
            {"value": 5., "p": 0.75},
        ]
        assert o.get_value() == 4.
        assert o.get_p() == 1.

    def test_complex(self):
        o = CombinedOutcome([
            CombinedOutcome([DiscreteOutcome(1, 1. / 8),
                            DiscreteOutcome(5, 3. / 8)]),
            DiscreteOutcome(4, 1. / 4)
        ])
        assert self._exportIsClose(o.export(), [
            {"value": 2.5, "p": 0.1875},
            {"value": 4.5, "p": 0.5625},
        ])

        # checking that min_value and max_value get submitted
        o2 = CombinedOutcome([o, DiscreteOutcome(4, 1. / 4)])
        assert o2.min_value == o.min_value
        assert o2.max_value == o.max_value
