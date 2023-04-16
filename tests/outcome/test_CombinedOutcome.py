from typing import List
import math
from probability_calculator.outcome import DiskreteOutcome, CombinedOutcome
from probability_calculator.outcome import ExportedOutcome


class TestCombinedOutcome():
    def _exportIsClose(self, l1: List[ExportedOutcome], l2: List[ExportedOutcome]) -> bool:
        if len(l1) != len(l2):
            return False
        
        for e1, e2 in zip(l1, l2):
            if not math.isclose(e1["value"], e2["value"]) or not math.isclose(e1["prob"], e2["prob"]):
                return False
            
        return True


    def test_simple(self):
        o = CombinedOutcome([DiskreteOutcome(1, 1./4), DiskreteOutcome(5, 3./4)])
        assert str(o) == "CombinedOutcome(value1=1.0, prob1=0.25, value2=5.0, prob2=0.75)"
        assert o.export() == [
            {"value": 1., "prob": 0.25},
            {"value": 5., "prob": 0.75},
        ]
        assert o.getValue() == 4.
        assert o.getProb() == 1.

    def test_complex(self):
        o = CombinedOutcome([
            CombinedOutcome([DiskreteOutcome(1, 1./8), DiskreteOutcome(5, 3./8)]),
            DiskreteOutcome(4, 1./4)
        ])
        assert self._exportIsClose(o.export(), [
            {"value": 2.5, "prob": 0.1875},
            {"value": 4.5, "prob": 0.5625},
        ])

        # checking that minv and maxv get submitted
        o2 = CombinedOutcome([o, DiskreteOutcome(4, 1./4)])
        assert o2.minv == o.minv
        assert o2.maxv == o.maxv
