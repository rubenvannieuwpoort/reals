import reals._real
import reals._constants
import reals._computation
import reals.approximation
import reals._exponential

from fractions import Fraction


def sin(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return _sin(x)


def sinh(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return (reals._exponential.exp(x) - reals._exponential.exp(-x)) / 2


def csc(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return 1 / _sin(x)


def csch(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return 2 / (reals._exponential.exp(x) - reals._exponential.exp(-x))


def cos(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return _cos(x)


def cosh(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return (reals._exponential.exp(x) + reals._exponential.exp(-x)) / 2


def sec(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return 1 / _cos(x)


def sech(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    return 2 / (reals._exponential.exp(x) + reals._exponential.exp(-x))


def tan(x: reals._real.Number) -> reals._real.Real:
    x = reals._real.ensure_real(x)
    return _sin(x) / _cos(x)


def tanh(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    exponential = reals._exponential.exp(2 * x)
    return (exponential - 1) / (exponential + 1)


def cot(x: reals._real.Number) -> reals._real.Real:
    x = reals._real.ensure_real(x)
    return _cos(x) / _sin(x)


def coth(x: reals._real.Number):
    x = reals._real.ensure_real(x)
    exponential = reals._exponential.exp(2 * x)
    return (exponential + 1) / (exponential - 1)


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
        self.current_term = self.current_term * self.x2 / (self.n * (self.n + 1))
        return term

    def improve(self):
        self.hi = self.lo + self.next_term()
        self.lo = self.hi + self.next_term()
        self.lo_comp = self.lo.compute()
        self.hi_comp = self.hi.compute()
        for _ in range(0, self.terms):
            next(self.lo_comp)
            next(self.hi_comp)

    def __next__(self) -> tuple[int, int]:
        while True:
            n_lo = next(self.lo_comp)
            n_hi = next(self.hi_comp)

            if n_lo == n_hi:
                self.terms += 1
                return n_lo
            else:
                self.improve()


# set n=1 for cosine, n=2 for sin/x
class TrigComputation(reals._computation.Computation):
    def __init__(self, n: int, x: reals._real.Real) -> None:
        self.terms = 0
        self.n = n
        self.current_term = reals._real.Real.from_int(1)
        self.x2 = -x * x
        self.lo = self.next_term()
        self.hi = self.lo + self.next_term()
        self.lo_comp = self.lo.compute()
        self.hi_comp = self.hi.compute()

    def next_term(self):
        term = self.current_term
        self.current_term = self.current_term * self.x2 / (self.n * (self.n + 1))
        self.n += 2
        return term

    def improve(self):
        self.lo = self.hi + self.next_term()
        self.hi = self.lo + self.next_term()
        self.lo_comp = self.lo.compute()
        self.hi_comp = self.hi.compute()
        for _ in range(0, self.terms):
            next(self.lo_comp)
            next(self.hi_comp)

    def __next__(self) -> tuple[int, int]:
        while True:
            n_lo = next(self.lo_comp)
            n_hi = next(self.hi_comp)

            if n_lo == n_hi:
                self.terms += 1
                return n_lo
            else:
                self.improve()


# reduce to [-pi, pi] (plus or minus epsilon)
def reduce(x: reals._real.Real) -> reals._real.Real:
    a = reals.approximation.Approximation(x / (reals._constants.pi * 2) + Fraction(1, 2))
    epsilon = Fraction(1, 1000)
    a.improve_epsilon(epsilon)
    frac = a.as_fraction()
    assert frac
    p, q = frac.as_integer_ratio()
    return x - reals._constants.pi * 2 * (p // q)


def _sin(x: reals._real.Real) -> reals._real.Real:
    xr = reduce(x)
    a = reals.approximation.Approximation(2 * xr / reals._constants.pi + Fraction(1, 2))
    epsilon = Fraction(1, 1000)
    a.improve_epsilon(epsilon)
    frac = a.as_fraction()
    assert frac
    p, q = frac.as_integer_ratio()
    n = p // q
    if n == -2:
        return -_sin2(reals._constants.pi + xr)
    if n == -1:
        return -_cos2(xr + reals._constants.pi / 2)
    if n == 0:
        return _sin2(xr)
    if n == 1:
        return _cos2(xr - reals._constants.pi / 2)
    if n == 2:
        return _sin2(reals._constants.pi - xr)
    raise Exception()


def _cos(x: reals._real.Real) -> reals._real.Real:
    xr = reduce(x)
    a = reals.approximation.Approximation(2 * xr / reals._constants.pi + Fraction(1, 2))
    epsilon = Fraction(1, 1000)
    a.improve_epsilon(epsilon)
    frac = a.as_fraction()
    assert frac
    p, q = frac.as_integer_ratio()
    n = p // q
    if n == -2:
        return -_cos2(xr + reals._constants.pi)
    if n == -1:
        return _sin2(reals._constants.pi / 2 + xr)
    if n == 0:
        return _cos2(xr)
    if n == 1:
        return _sin2(reals._constants.pi / 2 - xr)
    if n == 2:
        return -_cos2(xr - reals._constants.pi)
    raise Exception()


def _sin2(x: reals._real.Real) -> reals._real.Real:
    return x * reals._real.Real(TrigComputation(2, x))


def _cos2(x: reals._real.Real) -> reals._real.Real:
    return reals._real.Real(TrigComputation(1, x))
