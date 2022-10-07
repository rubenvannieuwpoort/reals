# TODO(Ruben): this needs to be rewritten to use absolute imports
import reals._real
import reals._term
from reals._computation import Computation
from reals.approximation import Approximation
from reals._algebraic_computation import AlgebraicComputation

from typing import Generator
from fractions import Fraction


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


def log_frac(f: Fraction) -> reals._real.Real:
    x, y = f.as_integer_ratio()
    computation = reals._real.Real(log_frac_computation(x, y)).compute()
    return reals._real.Real(AlgebraicComputation(computation, (1, 0, 0, 1)))


class LogarithmicComputation(Computation):
    def __init__(self, x: reals._real.Real):
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


def log(x: reals._real.Real) -> reals._real.Real:
    return reals._real.Real(LogarithmicComputation(x))
