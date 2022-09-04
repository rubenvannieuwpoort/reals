from __future__ import annotations

from reals._term import Term
from reals._inverse import InverseComputation
from reals._computation import Computation
from reals._homographic import Homographic
from reals._compare import compare, ComparisonResult
from reals._algebraic_computation import AlgebraicComputation
from reals._quadratic_computation import QuadraticComputation

from decimal import Decimal
from fractions import Fraction
from typing import Generator, Iterable, Iterator, Union

DEFAULT_DIGITS = 5


class CachedComputation(Computation):
    def __init__(self, iterator: Iterator[Term], cache: list[Term]):
        self.cache = cache
        self.iterator = iterator
        self.index = 0

    def __next__(self) -> Term:
        assert self.index <= len(self.cache)

        if self.index == len(self.cache):
            self.cache.append(next(self.iterator))

        index = self.index
        self.index += 1
        return self.cache[index]


class Real:
    def __init__(self, it: Union[Iterator[Term], Iterable[Term]]) -> None:
        self.iterator = iter(it)
        self.cache: list[Term] = []

    def compute(self) -> Computation:
        return CachedComputation(self.iterator, self.cache)

    @staticmethod
    def from_number(x: Union[int, Fraction, Decimal]):
        if isinstance(x, int):
            return Real.from_int(x)

        p, q = x.as_integer_ratio()
        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_int(n: int) -> 'Real':
        return Real([n])

    @staticmethod
    def from_fraction(f: Fraction) -> 'Real':
        p, q = f.as_integer_ratio()
        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_decimal(d: Decimal) -> 'Real':
        p, q = d.as_integer_ratio()
        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_float(f: float) -> 'Real':
        p, q = f.as_integer_ratio()
        return Real(AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_iter(i: Iterator[Term]) -> 'Real':
        return Real(i)

    def inverse(self):
        return Real(InverseComputation(self.compute()))

    def __neg__(self):
        return Real(AlgebraicComputation(self.compute(), (-1, 0, 0, 1)))

    def __mul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (p, 0, 0, q)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(
                    self.compute(),
                    other.compute(),
                    (1, 0, 0, 0, 0, 0, 0, 1)))
        else:
            raise TypeError()

    def __rmul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (p, 0, 0, q)))
        else:
            raise TypeError()

    def __add__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, p, 0, q)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(self.compute(), other.compute(),
                                             (0, 1, 1, 0, 0, 0, 0, 1)))
        else:
            raise TypeError()

    def __radd__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, p, 0, q)))
        else:
            raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, -p, 0, q)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(self.compute(),
                                             other.compute(), (0, 1, -1, 0, 0, 0, 0, 1)))
        else:
            raise TypeError()

    def __rsub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (-q, p, 0, q)))
        else:
            raise TypeError()

    def __truediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (q, 0, 0, p)))
        elif isinstance(other, Real):
            return Real(QuadraticComputation(self.compute(),
                                             other.compute(), (0, 1, 0, 0, 0, 0, 1, 0)))
        else:
            raise TypeError()

    def __rtruediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(AlgebraicComputation(self.compute(), (0, p, q, 0)))
        else:
            raise TypeError()

    def __lt__(self, other: Real) -> bool:
        return compare(self, other) == ComparisonResult.SMALLER

    def __gt__(self, other: Real) -> bool:
        return compare(self, other) == ComparisonResult.GREATER

    def __eq__(self, other) -> bool:
        return compare(self, other) == ComparisonResult.UNKNOWN

    def __format__(self, spec):
        assert spec[0] == '.'
        assert spec[-1] == 'f'
        num_digits = int(spec[1:-1])
        return digits(self.compute(), num_digits)

    def __str__(self):
        return digits(self.compute(), DEFAULT_DIGITS)

    def __repr__(self):
        return (f'<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))} '
                f'(approximate value: {str(self)})>')


def digits(c: Computation, n: int) -> str:
    digit_generator = digits_helper(c)
    digits = str(next(digit_generator))
    try:
        digits += '.'
        for _ in range(n):
            digits += next(digit_generator)
    except StopIteration:
        return digits
    return digits


def digits_helper(c: Computation) -> Generator[str, None, None]:
    h = Homographic(1, 0, 0, 1)
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
