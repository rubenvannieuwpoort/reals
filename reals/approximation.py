from reals._homographic import Homographic
from reals._real import Real

from fractions import Fraction


def rational_approximation(x: Real, iterations: int) -> Fraction:
    h = Homographic(1, 0, 0, 1)
    computation = iter(x)
    for i in range(0, iterations):
        try:
            h.ingest(next(computation))
        except StopIteration:
            h.ingest_inf()
            break
    return Fraction(h.a, h.c)


def floating_point_approximation(x: Real, iterations: int) -> float:
    p, q = rational_approximation(x, iterations).as_integer_ratio()
    return p / q
