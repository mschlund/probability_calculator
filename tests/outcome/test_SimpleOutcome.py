from probability_calculator.outcome import DiscreteOutcome


class TestDiscreteOutcome():
    def test_str(self):
        o = DiscreteOutcome(1, 1. / 2)
        assert str(o) == "DiscreteOutcome(value=1, probability=0.5)"

    def test_eq(self):
        assert DiscreteOutcome(1, 1. / 2) == DiscreteOutcome(1, 1. / 2 + 1e-10)
        assert DiscreteOutcome(1, 1. / 2) != DiscreteOutcome(1, 1. / 2 + 1e-7)
        assert DiscreteOutcome(1, 1. / 2) == DiscreteOutcome(1 + 1e-10, 1. / 2)
        assert DiscreteOutcome(1, 1. / 2) != DiscreteOutcome(1 + 1e-7, 1. / 2)

    def test_add(self):
        o1 = DiscreteOutcome(1, 1. / 2)
        o2 = DiscreteOutcome(2, 1. / 3)
        result1 = o1 + o2
        result2 = o2 + o1
        expected = DiscreteOutcome(3, 1. / 6)
        print(result1, result1 == expected)
        assert result1 == expected
        assert result2 == expected
