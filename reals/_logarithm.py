from reals._real import Real, Number
from reals._computation import Computation
from reals.approximation import Approximation
from reals._algebraic_computation import AlgebraicComputation

from decimal import Decimal
from fractions import Fraction
from typing import Generator


def log_frac_computation(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    x -= y
    yield (0, x)

    m, n = x, y
    incr = 2 * y
    while True:
        yield (n, m)
        yield (2, m)
        m += x
        n += incr


def log_frac(f: Fraction) -> Real:
    x, y = f.as_integer_ratio()
    computation = Real(log_frac_computation(x, y)).compute()
    return Real(AlgebraicComputation(computation, (1, 0, 0, 1)))


class LogarithmicComputation(Computation):
    def __init__(self, x: Real):
        self.a = Approximation(x)
        self.n = 0
        self.increase_precision()

    def increase_precision(self):
        self.a.improve(10)
        self.lo = log_frac(self.a.lower_bound_fraction()).compute()
        self.hi = log_frac(self.a.upper_bound_fraction()).compute()
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


def log(x: Number) -> Real:
    if isinstance(x, int) or isinstance(x, Fraction) or isinstance(x, Decimal):
        p, q = x.as_integer_ratio()
        return log_frac(Fraction(p, q))

    if isinstance(x, Real):
        return Real(LogarithmicComputation(x))

    raise TypeError()
