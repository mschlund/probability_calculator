from probability_calculator.DiscreteDensity import DiscreteDensity


class TestDiscreteDensity():
    def test_getPlotData(self):
        d = DiscreteDensity(outcomes=[
            {"value": 1, "prob": 1./6},
            {"value": 2, "prob": 1./3},
            {"value": 1, "prob": 1./6},
            {"value": 3, "prob": 1./3}
        ])
        X, Y = d._getPlotData()
        assert X == [1, 2, 3]
        assert Y == [1./3, 1./3, 1./3]

    def test_plot(self):
        d = DiscreteDensity(outcomes=[
            {"value": 1, "prob": 1./6},
            {"value": 2, "prob": 1./3},
            {"value": 1, "prob": 1./6},
            {"value": 3, "prob": 1./3}
        ])
        d.plot()
