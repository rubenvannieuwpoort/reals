
from fractions import Fraction
from math import factorial
from reals._computation import Computation
from typing import Generator
from reals._real import Real
from reals._bounds import IntervalComputation
from reals._homographic import Homographic
from reals.approximation import _approximate_epsilon_helper
from reals._algebraic_computation import AlgebraicComputation
from reals._normalize import normalize


def exp_int_computation(n: int) -> Generator[tuple[int, int], None, None]:
    m = 6
    while True:
        yield (m, n * n)
        m += 4


def exp_int(n: int) -> Real:
    n_squared = n * n
    computation = iter(Real.from_gcf_term_generator(lambda: exp_int_computation(n)))
    return normalize(Real(lambda: AlgebraicComputation(computation, (2 + n, n_squared, 2 - n, n_squared))))


def exp_frac(x: Real) -> Real:
    return Real(lambda: ExponentialComputation(x))


def pow(x: Real, n: int) -> Real:
    assert n >= 0
    if n == 0:
        return Real.from_int(1)
    result = x
    for _ in range(0, n - 1):
        result *= x
    return result


class ExponentialComputation(Computation):
    def __init__(self, x: Real) -> None:
        self.x = x
        self.lo = 1 + x + (x * x) / 2 + (x * x * x) / 6
        self.hi = self.lo + (x * x * x * x) / 24
        self.lo_comp = iter(self.lo)
        self.hi_comp = iter(self.hi)
        self.n = 0
        self.k = 5

    def __next__(self) -> tuple[int, int]:
        while True:
            n_lo = next(self.lo_comp)
            n_hi = next(self.hi_comp)

            if n_lo == n_hi:
                self.n += 1
                return n_lo

            self.lo = self.hi + pow(self.x, self.k) / factorial(self.k)
            self.k += 1
            self.hi = self.lo + pow(self.x, self.k) / factorial(self.k)
            self.k += 1

            self.lo_comp = iter(self.lo)
            self.hi_comp = iter(self.hi)
            for _ in range(0, self.n):
                next(self.lo_comp)
                next(self.hi_comp)


def exp(x: Real | int) -> Real:
    if isinstance(x, int):
        return exp_int(x)
    epsilon = Fraction(1, 1000)
    c = IntervalComputation(iter(x))
    _approximate_epsilon_helper(Homographic(1, 0, 0, 1), c, epsilon)
    upper_bound = c.lower_bound
    assert upper_bound
    p, q = upper_bound.as_integer_ratio()
    n = (p + q - 1) // q
    rest = x - n
    return exp_int(n) * exp_frac(rest)
