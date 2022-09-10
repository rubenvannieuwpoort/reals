# TODO(Ruben): this needs to be rewritten to use absolute imports
from reals._real import Real, Number, ensure_real
from reals._normalize import normalize
from reals._computation import Computation
from reals.approximation import Approximation
from reals._algebraic_computation import AlgebraicComputation

from math import factorial
from typing import Generator
from fractions import Fraction


def exp_int_computation(n: int) -> Generator[tuple[int, int], None, None]:
    m = 6
    while True:
        yield (m, n * n)
        m += 4


def exp_int(n: int) -> Real:
    n_squared = n * n
    computation = Real(exp_int_computation(n)).compute()
    return normalize(Real(AlgebraicComputation(computation, (2 + n, n_squared, 2 - n, n_squared))))


# compute exp(x) for small negative x
def exp_small(x: Real) -> Real:
    return Real(ExponentialComputation(x))


def pow(x: Real, n: int) -> Real:
    assert n >= 0
    if n == 0:
        return Real.from_int(1)
    result = x
    for _ in range(0, n - 1):
        result *= x
    return result


# compute exp(x) for small negative x
# Technically this method will converge for any x, the negativeness is needed to make the Taylor series
# alternating so that it can be used to obtain both lower and upper bounds. The smallness of x is needed
# to improve the convergence.
class ExponentialComputation(Computation):
    def __init__(self, x: Real) -> None:
        self.x = x
        self.lo = 1 + x + (x * x) / 2 + (x * x * x) / 6
        self.hi = self.lo + (x * x * x * x) / 24
        self.lo_comp = self.lo.compute()
        self.hi_comp = self.hi.compute()
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

            self.lo_comp = self.lo.compute()
            self.hi_comp = self.hi.compute()
            for _ in range(0, self.n):
                next(self.lo_comp)
                next(self.hi_comp)


# note that this might not be ideal to calculate exp for x of type Real which turns out to be integer
# (e.g. x = sqrt(3) * sqrt(3))
def exp(x: Number) -> Real:
    # if x is an integer it can be computed more efficiently
    if isinstance(x, int):
        return exp_int(x)

    x = ensure_real(x)

    # get numbers n and rest such that x = n + rest, n is an integer, and rest is a small negative number
    # more specifically, calculate n = ceil(upper_bound(x)) and rest = x - n
    epsilon = Fraction(1, 1000)
    a = Approximation(x)
    a.improve_epsilon(epsilon)
    upper_bound = a.upper_bound_fraction()
    assert upper_bound
    p, q = upper_bound.as_integer_ratio()

    n = (p + q - 1) // q
    rest = x - n

    return exp_int(n) * exp_small(rest)
