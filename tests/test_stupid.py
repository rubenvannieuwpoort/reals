from reals import exp_int, rational_bounds


def test_stupid():
    x = exp_int(5)
    lo, hi = rational_bounds(x, 1)
    assert 1 == 1
