from reals._constants import pi
from reals._computation.constants.pi import pi_computation
from reals._computation.functions.exp import exp_frac_computation
from reals._computation.functions.log import log_frac_computation
from reals._computation.functions.sin import sin_frac_computation
from reals._computation.monotonic import MonotonicComputation
from reals._computation.quadratic import QuadraticComputation
from reals._real import Real, Number
from reals._term import expand_term

from typing import Optional
from fractions import Fraction
from decimal import Decimal


def _log(x: Number):
    if isinstance(x, int) or isinstance(x, Fraction) or isinstance(x, Decimal):
        a, b = x.as_integer_ratio()
        # TODO(Ruben): or should this be normalized by AlgebraicComputation?
        return log_frac_computation(Fraction(a, b))
    return Real(MonotonicComputation(x.compute(), log_frac_computation))


def log(x: Number, base: Optional[Number] = None):
    if base is None:
        return _log(x)
    return Real(QuadraticComputation(_log(x), _log(base), (0, 0, 0, 1, 1, 0, 0, 0)))


def exp(x: Number) -> Real:
    if isinstance(x, int) or isinstance(x, Fraction) or isinstance(x, Decimal):
        a, b = x.as_integer_ratio()
        # TODO(Ruben): or should this be normalized by AlgebraicComputation?
        return Real(exp_frac_computation(Fraction(a, b)))
    return Real(MonotonicComputation(x.compute(), exp_frac_computation))


def _sin(x: Real) -> Real:
    return Real(MonotonicComputation(x.compute(), sin_frac_computation))


# TODO(Ruben): support for rational arguments?
def sqrt(x: Number) -> Real:
    x = Real.from_number(x)
    return exp(log(x) / 2)


# TODO(Ruben): support for rational arguments?
def sin(x: Number) -> Real:
    xr = Real.from_number(x)
    n, m = expand_term(next(QuadraticComputation(xr.compute(), pi_computation(), (0, 2, 0, 0, 0, 0, 1, 0))))
    assert m == 1 or m == 2
    coeff = ((n + 1) // 2)
    x_adjusted = xr - coeff * pi
    if n % 2 == 1 or m == 1:
        # TODO(Ruben): verify that -pi / 2 <= x_adjusted <= pi / 2
        if coeff % 2 == 1:
            return -_sin(x_adjusted)
        else:
            return _sin(x_adjusted)
    else:
        print('ping')  # TODO(Ruben): remove this
        s = _sin(x_adjusted - pi / 2)
        return sqrt(1 - s * s)
