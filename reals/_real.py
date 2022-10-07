from __future__ import annotations

import reals._term
import reals._inverse
import reals._computation
import reals._homographic
import reals._algebraic_computation
import reals._quadratic_computation

from decimal import Decimal
from fractions import Fraction
from typing import Any, Generator, Iterable, Iterator, Union

DEFAULT_DIGITS = 5


class CachedComputation(reals._computation.Computation):
    def __init__(self, iterator: Iterator[reals._term.Term], cache: list[reals._term.Term]):
        self.cache = cache
        self.iterator = iterator
        self.index = 0

    def __next__(self) -> reals._term.Term:
        assert self.index <= len(self.cache)

        if self.index == len(self.cache):
            self.cache.append(next(self.iterator))

        index = self.index
        self.index += 1
        return self.cache[index]


class Real:
    def __init__(self, it: Union[Iterator[reals._term.Term], Iterable[reals._term.Term]]) -> None:
        self.iterator = iter(it)
        self.cache: list[reals._term.Term] = []

    def compute(self) -> reals._computation.Computation:
        return CachedComputation(self.iterator, self.cache)

    @staticmethod
    def from_number(x: Union[int, Fraction, Decimal, Real]):
        if not (isinstance(x, int) or isinstance(x, Fraction) or isinstance(x, Decimal) or isinstance(x, Real)):
            raise TypeError(f'Unexpected type {type(x)}')

        if isinstance(x, Real):
            return x

        if isinstance(x, int):
            return Real.from_int(x)

        assert type(x) in [Fraction, Decimal]

        p, q = x.as_integer_ratio()
        return Real(reals._algebraic_computation.AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_int(n: int) -> 'Real':
        return Real([n])

    @staticmethod
    def from_fraction(f: Fraction) -> 'Real':
        if not isinstance(f, Fraction):
            raise TypeError(f'Expected Fraction, got {type(f)}')
        p, q = f.as_integer_ratio()
        return Real(reals._algebraic_computation.AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_decimal(d: Decimal) -> 'Real':
        if not isinstance(d, Decimal):
            raise TypeError(f'Expected Decimal, got {type(d)}')
        p, q = d.as_integer_ratio()
        return Real(reals._algebraic_computation.AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_float(f: float) -> 'Real':
        if not isinstance(f, Fraction):
            raise TypeError(f'Expected float, got {type(f)}')
        p, q = f.as_integer_ratio()
        return Real(reals._algebraic_computation.AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_iter(i: Iterator[reals._term.Term]) -> 'Real':
        return Real(i)

    def inverse(self):
        return Real(reals._inverse.InverseComputation(self.compute()))

    def __neg__(self):
        return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (-1, 0, 0, 1)))

    def __mul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (p, 0, 0, q)))
        elif isinstance(other, Real):
            return Real(reals._quadratic_computation.QuadraticComputation(
                    self.compute(),
                    other.compute(),
                    (1, 0, 0, 0, 0, 0, 0, 1)))
        else:
            raise_typeerror(other)

    def __rmul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (p, 0, 0, q)))
        else:
            raise_typeerror(other)

    def __add__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (q, p, 0, q)))
        elif isinstance(other, Real):
            return Real(reals._quadratic_computation.QuadraticComputation(self.compute(), other.compute(),
                                                                          (0, 1, 1, 0, 0, 0, 0, 1)))
        else:
            raise_typeerror(other)

    def __radd__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (q, p, 0, q)))
        else:
            raise_typeerror(other)

    def __sub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (q, -p, 0, q)))
        elif isinstance(other, Real):
            return Real(reals._quadratic_computation.QuadraticComputation(self.compute(),
                                                                          other.compute(), (0, 1, -1, 0, 0, 0, 0, 1)))
        else:
            raise_typeerror(other)

    def __rsub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (-q, p, 0, q)))
        else:
            raise_typeerror(other)

    def __truediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (q, 0, 0, p)))
        elif isinstance(other, Real):
            return Real(reals._quadratic_computation.QuadraticComputation(self.compute(),
                                                                          other.compute(), (0, 1, 0, 0, 0, 0, 1, 0)))
        else:
            raise_typeerror(other)

    def __rtruediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(reals._algebraic_computation.AlgebraicComputation(self.compute(), (0, p, q, 0)))
        else:
            raise_typeerror(other)

    def __pow__(self, other):
        import reals._logarithm
        import reals._exponential
        return reals._exponential.exp(reals._logarithm.log(self) * other)

    def __lt__(self, other: Real) -> bool:
        from reals._compare import compare, ComparisonResult
        return compare(self, other) == ComparisonResult.SMALLER

    def __gt__(self, other: Real) -> bool:
        from reals._compare import compare, ComparisonResult
        return compare(self, other) == ComparisonResult.GREATER

    def __eq__(self, other) -> bool:
        from reals._compare import compare, ComparisonResult
        return compare(self, other) == ComparisonResult.UNKNOWN

    def evaluate(self, n: int, round: bool = True) -> str:
        return rounded_digits(self, n) if round else digits(self, n)

    def to_decimal(self, n: int) -> Decimal:
        return Decimal(self.evaluate(n))

    def to_float(self) -> float:
        import reals.approximation  # this is ugly but necessary to avoid circular imports
        return reals.approximation.closest_float(self)  # noqa

    def __format__(self, spec):
        assert spec[0] == '.'
        assert spec[-1] == 'f'
        num_digits = int(spec[1:-1])
        return rounded_digits(self, num_digits)

    def __str__(self):
        return rounded_digits(self, DEFAULT_DIGITS)

    def __repr__(self):
        return (f'<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))} '
                f'(approximate value: {str(self)})>')


def rounded_digits(x: Real, n: int) -> str:
    rounding_constant = Fraction(1, 2 * 10**n)
    return digits(x + rounding_constant, n)


def digits(x: Real, n: int) -> str:
    digit_generator = digits_helper(x.compute())
    digits = str(next(digit_generator))
    try:
        digits += '.'
        for _ in range(n):
            digits += next(digit_generator)
    except StopIteration:
        return digits
    return digits


def digits_helper(c: reals._computation.Computation) -> Generator[str, None, None]:
    h = reals._homographic.Homographic(1, 0, 0, 1)
    terminated = False
    is_negative = False

    assert not (h.c == 0 and h.d == 0)

    while not (h.c == 0 and h.d == 0):
        if h.c != 0 and h.c + h.d != 0:
            n1 = h.a // h.c
            n2 = (h.a + h.b) // (h.c + h.d)
            if n1 == n2:
                digit = n1

                h.a, h.b = h.a - digit * h.c, h.b - digit * h.d
                h.a, h.b = h.a * 10, h.b * 10

                if (not is_negative) and digit < 0:
                    is_negative = True
                    digit += 1
                    if digit == 0:
                        yield '-' + str(digit)
                    else:
                        yield str(digit)
                elif is_negative:
                    if digit > 0 and h.a == 0 and h.b == 0:
                        digit = 10 - digit
                        is_negative = False
                    else:
                        digit = 9 - digit
                    yield str(digit)
                else:
                    yield str(digit)

                continue

        assert not terminated
        try:
            h.ingest(next(c))
        except StopIteration:
            h.ingest_inf()
            terminated = True


Number = Union[int, Decimal, Fraction, Real]


def ensure_real(x: Number) -> Real:
    if isinstance(x, Real):
        return x
    if isinstance(x, Fraction):
        return Real.from_fraction(x)
    if isinstance(x, int):
        return Real.from_int(x)
    if isinstance(x, Decimal):
        return Real.from_decimal(x)
    raise TypeError()


def raise_typeerror(other: Any) -> None:
    if type(other) == float:
        raise TypeError('Mixing float with reals is not supported. Use Real.from_float if you want to convert '
                        'a float to a real.')
    raise TypeError(f'Mixing {type(other)} with reals is not supported.')
