from probability_calculator.outcome import DiskreteOutcome


class TestDiskreteOutcome():
    def test_str(self):
        o = DiskreteOutcome(1, 1./2)
        assert str(o) == "DiskreteOutcome(value=1, prob=0.5)"


    def test_eq(self):
        assert DiskreteOutcome(1, 1./2) == DiskreteOutcome(1, 1./2+1e-10)
        assert DiskreteOutcome(1, 1./2) != DiskreteOutcome(1, 1./2+1e-7)
        assert DiskreteOutcome(1, 1./2) == DiskreteOutcome(1+1e-10, 1./2)
        assert DiskreteOutcome(1, 1./2) != DiskreteOutcome(1+1e-7, 1./2)

    def test_add(self):
        o1 = DiskreteOutcome(1, 1./2)
        o2 = DiskreteOutcome(2, 1./3)
        result1 = o1+o2
        result2 = o2+o1
        expected = DiskreteOutcome(3, 1./6)
        print(result1, result1 == expected)
        assert result1 == expected
        assert result2 == expected
