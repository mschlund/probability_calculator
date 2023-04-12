from probability_calculator.outcome import SimpleOutcome


class TestSimpleOutcome():
    def test_str(self):
        o = SimpleOutcome(1, 1./2)
        assert str(o) == "SimpleOutcome(value=1, prob=0.5)"


    def test_eq(self):
        assert SimpleOutcome(1, 1./2) == SimpleOutcome(1, 1./2+1e-10)
        assert SimpleOutcome(1, 1./2) != SimpleOutcome(1, 1./2+1e-7)
        assert SimpleOutcome(1, 1./2) == SimpleOutcome(1+1e-10, 1./2)
        assert SimpleOutcome(1, 1./2) != SimpleOutcome(1+1e-7, 1./2)

    def test_add(self):
        o1 = SimpleOutcome(1, 1./2)
        o2 = SimpleOutcome(2, 1./3)
        result1 = o1+o2
        result2 = o2+o1
        expected = SimpleOutcome(3, 1./6)
        print(result1, result1 == expected)
        assert result1 == expected
        assert result2 == expected
