from decimal import Decimal
import math
from reals._homographic import Homographic
from reals._computation import Computation
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


def _approximate_epsilon_helper(h: Homographic, computation: Computation, epsilon: Fraction) \
        -> tuple[Homographic, Computation]:
    i = 0
    while h.c == 0 or h.d == 0 or abs(Fraction(h.a, h.c) - Fraction(h.b, h.d)) > epsilon:
        h.ingest(next(computation))
        i += 1
    return (h, computation)


def approximate_epsilon(x: Real, epsilon: Fraction | Decimal | int | float) -> Fraction:
    h, _ = _approximate_epsilon_helper(Homographic(1, 0, 0, 1), iter(x), Fraction(epsilon))
    return Fraction(h.a, h.c)


def closest_float(x: Real) -> float:
    h, computation = _approximate_epsilon_helper(Homographic(1, 0, 0, 1), iter(x), Fraction(1))
    as_float = h.a / h.c
    epsilon = Fraction(math.nextafter(as_float, math.inf) - as_float)
    h, computation = _approximate_epsilon_helper(h, computation, epsilon)
    while h.a / h.c != h.b / h.d:
        h.ingest(next(computation))
    return h.a / h.c
