from probability_calculator.density import DiscreteDensity


class TestDiscreteDensity():
    def test_exportOutcomes(self):
        outcomes = [
            {"value": 1, "prob": 1./6},
            {"value": 2, "prob": 1./3},
            {"value": 1, "prob": 1./6},
            {"value": 3, "prob": 1./3}
        ]
        d = DiscreteDensity(outcomes=outcomes)
        assert d.exportOutcomes() == outcomes
