from probability_calculator.density import Dice


class TestDice():
    def test_dice3(self):
        d = Dice(3)
        expected = [
            {"value": 1, "prob": 1./3},
            {"value": 2, "prob": 1./3},
            {"value": 3, "prob": 1./3}
        ]
        assert d.exportOutcomes() == expected

    def test_dice6(self):
        d = Dice(6)
        expected = [
            {"value": 1, "prob": 1./6},
            {"value": 2, "prob": 1./6},
            {"value": 3, "prob": 1./6},
            {"value": 4, "prob": 1./6},
            {"value": 5, "prob": 1./6},
            {"value": 6, "prob": 1./6}
        ]
        assert d.exportOutcomes() == expected
