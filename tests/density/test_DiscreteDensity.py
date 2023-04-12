import math
from probability_calculator.density import DiscreteDensity


class TestDiscreteDensity():
    def assertExportOutcomesEqual(self, a, b):
        assert len(a) == len(b)
        for o, e in zip(a, b):
            assert math.isclose(o["value"], e["value"])
            assert math.isclose(o["prob"], e["prob"])

    def test_exportOutcomes(self):
        outcomes = [
            {"value": 1, "prob": 1./6},
            {"value": 2, "prob": 1./3},
            {"value": 1, "prob": 1./6},
            {"value": 3, "prob": 1./3}
        ]
        d = DiscreteDensity(outcomes=outcomes)
        assert d.exportOutcomes() == outcomes

    def test_mul(self):
        d1 = DiscreteDensity(outcomes=[
            {"value": 1, "prob": 0.1},
            {"value": 2, "prob": 0.3}]
        )
        d2 = DiscreteDensity(outcomes=[
            {"value": 4, "prob": 0.4},
            {"value": 8, "prob": 0.8}]
        )
        d = d1*d2
        outcomes = d.exportOutcomes()
        expected = [
            {"value": 5, "prob": 0.04},
            {"value": 9, "prob": 0.08},
            {"value": 6, "prob": 0.12},
            {"value": 10, "prob": 0.24}
        ]
        self.assertExportOutcomesEqual(outcomes, expected)

    def test_pow1(self):
        d1 = DiscreteDensity(outcomes=[
            {"value": 1, "prob": 0.1},
            {"value": 2, "prob": 0.3}]
        )
        d = d1**1
        outcomes = d.exportOutcomes()
        expected = d1.exportOutcomes()
        self.assertExportOutcomesEqual(outcomes, expected)


    def test_pow3(self):
        d1 = DiscreteDensity(outcomes=[
            {"value": 1, "prob": 0.5},
            {"value": 2, "prob": 0.5}]
        )
        d = d1**3
        outcomes = d.exportOutcomes()
        expected = [
            {"value": 3, "prob": 0.125},
            {"value": 4, "prob": 0.125},
            {"value": 4, "prob": 0.125},
            {"value": 5, "prob": 0.125},
            {"value": 4, "prob": 0.125},
            {"value": 5, "prob": 0.125},
            {"value": 5, "prob": 0.125},
            {"value": 6, "prob": 0.125}
        ]
        self.assertExportOutcomesEqual(outcomes, expected)