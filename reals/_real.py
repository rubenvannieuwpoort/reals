from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from reals._term import Term
from reals._computation.base import Computation
from reals._computation.cached import CachedComputation
from reals._computation.monotonic import MonotonicComputation
from reals._computation.algebraic import AlgebraicComputation
from reals._computation.quadratic import QuadraticComputation
from reals._computation.functions.exp import exp_frac_computation
from reals._computation.functions.log import log_frac_computation


# from decimal import Decimal
# from fractions import Fraction
from typing import Iterable, Iterator, Union

# DEFAULT_DIGITS = 5


Number = Union[int, Fraction, Decimal, 'Real']


class Real:
    def __init__(self, it: Union[Iterator[Term], Iterable[Term]]) -> None:
        self.iterator = iter(it)
        self.cache: list[Term] = []

    def compute(self) -> Computation:
        return CachedComputation(self.iterator, self.cache)

    @staticmethod
    def from_number(x: Number):
        if isinstance(x, Real):
            return x

        p, q = x.as_integer_ratio()

        if q == 1:
            return Real.from_int(p)

        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_int(n: int) -> 'Real':
        if not isinstance(n, int):
            raise TypeError(f'Expected Fraction, got {type(n)}')
        return Real([n])

    @staticmethod
    def from_fraction(f: Fraction) -> 'Real':
        if not isinstance(f, Fraction):
            raise TypeError(f'Expected Fraction, got {type(f)}')
        p, q = f.as_integer_ratio()
        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_decimal(d: Decimal) -> 'Real':
        if not isinstance(d, Decimal):
            raise TypeError(f'Expected Decimal, got {type(d)}')
        p, q = d.as_integer_ratio()
        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_float(f: float) -> 'Real':
        if not isinstance(f, float):
            raise TypeError(f'Expected float, got {type(f)}')
        p, q = f.as_integer_ratio()
        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_iter(i: Iterator[Term]) -> 'Real':
        return Real(i)

    def inverse(self):
        return Real(AlgebraicComputation(self.compute(), (0, 1, 1, 0)))

    def sqrt(self):
        log_computation = MonotonicComputation(self.compute(), log_frac_computation)
        half_log_computation = AlgebraicComputation(log_computation, (1, 0, 0, 2))
        return Real(MonotonicComputation(half_log_computation, exp_frac_computation))

    def pow(self, exponent: Number):
        log_computation = MonotonicComputation(self.compute(), log_frac_computation)
        exponent_times_log: Computation
        if isinstance(exponent, int) or isinstance(exponent, Fraction) or isinstance(exponent, Decimal):
            p, q = exponent.as_integer_ratio()
            exponent_times_log = AlgebraicComputation(log_computation, (p, 0, 0, q))
        else:
            exponent_times_log = QuadraticComputation(log_computation, exponent.compute(), (1, 0, 0, 0, 0, 0, 0, 1))
        return Real(MonotonicComputation(exponent_times_log, exp_frac_computation))

    def __neg__(self):
        return Real(AlgebraicComputation(self.compute(), (-1, 0, 0, 1)))

    def __mul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (p, 0, 0, q)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(self.compute(), other.compute(), (1, 0, 0, 0, 0, 0, 0, 1)))
        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Real' and '{type(other)}'")

    def __rmul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (p, 0, 0, q)))
        else:
            raise TypeError(f"unsupported operand type(s) for *: '{type(other)}' and 'Real'")

    def __add__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, p, 0, q)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(self.compute(), other.compute(), (0, 1, 1, 0, 0, 0, 0, 1)))
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Real' and '{type(other)}'")

    def __radd__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, p, 0, q)))
        else:
            raise TypeError(f"unsupported operand type(s) for +: '{type(other)}' and 'Real'")

    def __sub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, -p, 0, q)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(self.compute(), other.compute(), (0, 1, -1, 0, 0, 0, 0, 1)))
        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Real' and '{type(other)}'")

    def __rsub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (-q, p, 0, q)))
        else:
            raise TypeError(f"unsupported operand type(s) for -: '{type(other)}' and 'Real'")

    def __truediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, 0, 0, p)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(self.compute(), other.compute(), (0, 1, 0, 0, 0, 0, 1, 0)))
        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Real' and '{type(other)}'")

    def __rtruediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (0, p, q, 0)))
        else:
            raise TypeError(f"unsupported operand type(s) for /: '{type(other)}' and 'Real'")

    def __pow__(self, other):
        log_computation = MonotonicComputation(self.compute(), log_frac_computation)
        exponent_times_log: Computation
        if isinstance(other, int) or isinstance(other, Fraction) or isinstance(other, Decimal):
            p, q = other.as_integer_ratio()
            exponent_times_log = AlgebraicComputation(log_computation, (p, 0, 0, q))
        elif isinstance(other, Real):
            exponent_times_log = QuadraticComputation(log_computation, other.compute(), (1, 0, 0, 0, 0, 0, 0, 1))
        else:
            raise TypeError()
        return Real(MonotonicComputation(exponent_times_log, exp_frac_computation))
