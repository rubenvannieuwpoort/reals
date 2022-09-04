import reals._real
import reals._constants
import reals._computation
import reals.approximation

from fractions import Fraction


class SineComputation(reals._computation.Computation):
    def __init__(self, x: reals._real.Real) -> None:
        self.terms = 0
        self.n = 0
        self.current_term = x
        self.x2 = x * x
        self.hi = self.next_term()
        self.lo = self.hi + self.next_term()
        self.lo_comp = self.lo.compute()
        self.hi_comp = self.hi.compute()

    def next_term(self):
        term = self.current_term
        self.n += 2
        self.current_term = self.current_term * self.x2 / self.n / (self.n + 1)
        return term

    def improve(self):
        self.hi = self.lo + self.next_term()
        self.lo = self.hi + self.next_term()

    def __next__(self) -> tuple[int, int]:
        while True:
            n_lo = next(self.lo_comp)
            n_hi = next(self.hi_comp)

            if n_lo == n_hi:
                self.terms += 1
                return n_lo

            self.improve()

            self.lo_comp = self.lo.compute()
            self.hi_comp = self.hi.compute()
            for _ in range(0, self.terms):
                next(self.lo_comp)
                next(self.hi_comp)


class CosineComputation(reals._computation.Computation):
    def __init__(self, x: reals._real.Real) -> None:
        self.terms = 0
        self.n = 1
        self.current_term = reals._real.Real.from_int(1)
        self.x2 = x * x
        self.hi = self.next_term()
        self.lo = self.hi + self.next_term()
        self.lo_comp = self.lo.compute()
        self.hi_comp = self.hi.compute()

    def next_term(self):
        term = self.current_term
        self.current_term = self.current_term * self.x2 / self.n / (self.n + 1)
        self.n += 2
        return term

    def improve(self):
        self.hi = self.lo + self.next_term()
        self.lo = self.hi + self.next_term()

    def __next__(self) -> tuple[int, int]:
        while True:
            n_lo = next(self.lo_comp)
            n_hi = next(self.hi_comp)

            if n_lo == n_hi:
                self.terms += 1
                return n_lo

            self.improve()
            self.lo_comp = self.lo.compute()
            self.hi_comp = self.hi.compute()

            for _ in range(0, self.terms):
                next(self.lo_comp)
                next(self.hi_comp)


# reduce to [-pi, pi] (plus or minus epsilon)
def reduce(x: reals._real.Real) -> reals._real.Real:
    a = reals.approximation.Approximation(x / (reals._constants.pi * 2) + Fraction(1, 2))
    epsilon = Fraction(1, 1000)
    a.improve_epsilon(epsilon)
    frac = a.as_fraction()
    assert frac
    p, q = frac.as_integer_ratio()
    return x - reals._constants.pi * 2 * (p // q)


def sin(x: reals._real.Real) -> reals._real.Real:
    xr = reduce(x)
    a = reals.approximation.Approximation(2 * xr / reals._constants.pi + Fraction(1, 2))
    epsilon = Fraction(1, 1000)
    a.improve_epsilon(epsilon)
    frac = a.as_fraction()
    assert frac
    p, q = frac.as_integer_ratio()
    n = p // q
    if n == -2:
        return sin2(reals._constants.pi + x)
    if n == -1:
        return cos2(x + reals._constants.pi / 2)
    if n == 0:
        return sin2(x)
    if n == 1:
        xx = x - reals._constants.pi / 2
        print(xx)
        return -cos2(xx)
    if n == 2:
        return sin2(reals._constants.pi - x)
    raise Exception()


def cos(x: reals._real.Real) -> reals._real.Real:
    xr = reduce(x)
    a = reals.approximation.Approximation(2 * xr / reals._constants.pi + Fraction(1, 2))
    epsilon = Fraction(1, 1000)
    a.improve_epsilon(epsilon)
    frac = a.as_fraction()
    assert frac
    p, q = frac.as_integer_ratio()
    n = p // q
    if n == -2:
        return -cos2(x + reals._constants.pi)
    if n == -1:
        return sin2(reals._constants.pi / 2 + x)
    if n == 0:
        return cos2(x)
    if n == 1:
        return sin2(reals._constants.pi / 2 - x)
    if n == 2:
        return cos2(x - reals._constants.pi)
    raise Exception()


def sin2(x: reals._real.Real) -> reals._real.Real:
    return reals._real.Real(SineComputation(x))


def cos2(x: reals._real.Real) -> reals._real.Real:
    return reals._real.Real(CosineComputation(x))
