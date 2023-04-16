import unittest
from probability_calculator.density import DiscreteDensity
from probability_calculator.plot import get_plot_data, kernel_density_estimation


class TestPlot(unittest.TestCase):
    def test_getPlotData(self):
        d = DiscreteDensity(outcomes=[
            {"value": 1, "p": 1. / 6},
            {"value": 2, "p": 1. / 3},
            {"value": 1, "p": 1. / 6},
            {"value": 3, "p": 1. / 3}
        ])
        x, y = get_plot_data(d.export_outcomes())
        assert x == [1, 2, 3]
        assert y == [1. / 3, 1. / 3, 1. / 3]

    def test_kernelDensityEstimation(self):
        x = [1, 2.25, 2.75, 3]
        y = [1., 2, 3, 4]
        kde_x, kde_y = kernel_density_estimation(x, y, gridsize=4)
        assert kde_x == [0.5, 1, 1.5, 2, 2.5, 3, 3.5]
        assert kde_y == [0.0, 28.18432582492507, 0.0, 0.0, 0.0, 112.73730329970029, 0.0]
