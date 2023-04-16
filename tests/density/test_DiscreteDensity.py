import math
import unittest
from probability_calculator.density import DiscreteDensity


class TestDiscreteDensity(unittest.TestCase):
    def assert_export_outcomes_equal(self, a, b):
        assert len(a) == len(b)
        for o, e in zip(a, b):
            assert math.isclose(o["value"], e["value"])
            assert math.isclose(o["probability"], e["probability"])

    def test_export_outcomes(self):
        d = DiscreteDensity(outcomes=[
            {"value": 1, "probability": 1. / 6},
            {"value": 2, "probability": 1. / 3},
            {"value": 1, "probability": 1. / 6},
            {"value": 3, "probability": 1. / 3}
        ])
        expected = [
            {"value": 1, "probability": 1. / 3},
            {"value": 2, "probability": 1. / 3},
            {"value": 3, "probability": 1. / 3}
        ]
        assert d.export_outcomes() == expected

    def test_mul(self):
        d1 = DiscreteDensity(outcomes=[
            {"value": 1, "probability": 0.1},
            {"value": 2, "probability": 0.3}]
        )
        d2 = DiscreteDensity(outcomes=[
            {"value": 4, "probability": 0.4},
            {"value": 8, "probability": 0.8}]
        )
        d = d1 * d2
        outcomes = d.export_outcomes()
        expected = [
            {"value": 5, "probability": 0.04},
            {"value": 6, "probability": 0.12},
            {"value": 9, "probability": 0.08},
            {"value": 10, "probability": 0.24}
        ]
        self.assert_export_outcomes_equal(outcomes, expected)

    def test_pow1(self):
        d1 = DiscreteDensity(outcomes=[
            {"value": 1, "probability": 0.1},
            {"value": 2, "probability": 0.3}]
        )
        d = d1**1
        outcomes = d.export_outcomes()
        expected = d1.export_outcomes()
        self.assert_export_outcomes_equal(outcomes, expected)

    def test_pow3(self):
        d1 = DiscreteDensity(outcomes=[
            {"value": 1, "probability": 0.5},
            {"value": 2, "probability": 0.5}]
        )
        d = d1**3
        outcomes = d.export_outcomes()
        expected = [
            {"value": 3, "probability": 0.125},
            {"value": 4, "probability": 0.375},
            {"value": 5, "probability": 0.375},
            {"value": 6, "probability": 0.125}
        ]
        self.assert_export_outcomes_equal(outcomes, expected)
