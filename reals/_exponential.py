from reals._real import Real, Number
from reals._computation import Computation
from reals.approximation import Approximation
from reals._algebraic_computation import AlgebraicComputation

from decimal import Decimal
from fractions import Fraction
from typing import Generator


def exp_frac_computation(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    m = 6 * y
    x_squared = x * x
    incr = 4 * y
    while True:
        yield (m, x_squared)
        m += incr


def exp_frac(f: Fraction) -> Real:
    x, y = f.as_integer_ratio()
    x_squared = x * x
    computation = Real(exp_frac_computation(x, y)).compute()
    return Real(AlgebraicComputation(computation, (2 * y + x, x_squared, 2 * y - x, x_squared)))


class ExponentialComputation(Computation):
    def __init__(self, x: Real):
        self.a = Approximation(x)
        self.n = 0
        self.increase_precision()

    def increase_precision(self):
        self.a.improve(10)
        self.lo = exp_frac(self.a.lower_bound_fraction()).compute()
        self.hi = exp_frac(self.a.upper_bound_fraction()).compute()
        for _ in range(0, self.n):
            next(self.lo)
            next(self.hi)

    def __next__(self) -> tuple[int, int]:
        while True:
            lower = next(self.lo)
            upper = next(self.hi)
            if lower == upper:
                self.n += 1
                return lower
            else:
                self.increase_precision()


def exp(x: Number) -> Real:
    if isinstance(x, int) or isinstance(x, Fraction) or isinstance(x, Decimal):
        p, q = x.as_integer_ratio()
        return exp_frac(Fraction(p, q))

    if isinstance(x, Real):
        return Real(ExponentialComputation(x))

    raise TypeError()
