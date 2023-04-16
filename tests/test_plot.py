import unittest
from probability_calculator.density import DiscreteDensity
from probability_calculator.plot import get_plot_data, kernel_density_estimation


class TestPlot(unittest.TestCase):
    def test_getPlotData(self):
        d = DiscreteDensity(outcomes=[
            {"value": 1, "probability": 1. / 6},
            {"value": 2, "probability": 1. / 3},
            {"value": 1, "probability": 1. / 6},
            {"value": 3, "probability": 1. / 3}
        ])
        X, Y = get_plot_data(d.export_outcomes())
        assert X == [1, 2, 3]
        assert Y == [1. / 3, 1. / 3, 1. / 3]

    def test_kernelDensityEstimation(self):
        X = [1, 2.25, 2.75, 3]
        Y = [1., 2, 3, 4]
        kdeX, kdeY = kernel_density_estimation(X, Y, gridsize=4)
        assert kdeX == [0.5, 1, 1.5, 2, 2.5, 3, 3.5]
        assert kdeY == [0.0, 28.18432582492507, 0.0, 0.0, 0.0, 112.73730329970029, 0.0]
