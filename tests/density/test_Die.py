import unittest
from probability_calculator.density import Dice


class TestDice(unittest.TestCase):
    def test_dice3(self):
        d = Dice(3)
        expected = [
            {"value": 1, "p": 1. / 3},
            {"value": 2, "p": 1. / 3},
            {"value": 3, "p": 1. / 3}
        ]
        assert d.export_outcomes() == expected

    def test_dice6(self):
        d = Dice(6)
        expected = [
            {"value": 1, "p": 1. / 6},
            {"value": 2, "p": 1. / 6},
            {"value": 3, "p": 1. / 6},
            {"value": 4, "p": 1. / 6},
            {"value": 5, "p": 1. / 6},
            {"value": 6, "p": 1. / 6}
        ]
        assert d.export_outcomes() == expected
