from reals._computation import Computation
from reals._algebraic_computation import AlgebraicComputation
from reals._quadratic_computation import QuadraticComputation

import itertools
from fractions import Fraction
from typing import Callable, Generator, Iterable


class Real:
    def __init__(self, start_computation: Callable[[], Computation]) -> None:
        self.start_computation = start_computation

    def __iter__(self) -> Computation:
        return self.start_computation()

    @staticmethod
    def from_int(n: int) -> 'Real':
        return Real.from_scf_term_iterable([n])

    @staticmethod
    def from_fraction(f: Fraction) -> 'Real':
        p, q = f.as_integer_ratio()
        return Real(lambda: AlgebraicComputation(iter([]), (p, p, q, q)))

    @staticmethod
    def from_scf_term_iterable(i: Iterable[int]) -> 'Real':
        return Real(lambda: iter(map(lambda n: (n, 1), i)))

    @staticmethod
    def from_scf_term_generator(f: Callable[[], Generator[int, None, None]]) -> 'Real':
        return Real(lambda: map(lambda n: (n, 1), f()))

    @staticmethod
    def from_scf_term_function(f: Callable[[int], int]) -> 'Real':
        return Real(lambda: map(lambda n: (f(n), 1), itertools.count(1)))

    @staticmethod
    def from_gcf_term_iterable(i: Iterable[tuple[int, int]]) -> 'Real':
        return Real(lambda: iter(i))

    @staticmethod
    def from_gcf_term_generator(f: Callable[[], Generator[tuple[int, int], None, None]]) -> 'Real':
        return Real(lambda: f())

    @staticmethod
    def from_gcf_term_function(f: Callable[[int], tuple[int, int]]) -> 'Real':
        return Real(lambda: map(f, itertools.count(1)))

    def __mul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (p, 0, 0, q)))
        elif isinstance(other, Real):
            return Real(lambda: QuadraticComputation(iter(self), iter(other), (1, 0, 0, 0, 0, 0, 0, 1)))
        else:
            raise TypeError()

    def __rmul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (p, 0, 0, q)))
        else:
            raise TypeError()

    def __add__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (q, p, 0, q)))
        elif isinstance(other, Real):
            return Real(lambda: QuadraticComputation(iter(self), iter(other), (0, 1, 1, 0, 0, 0, 0, 1)))
        else:
            raise TypeError()

    def __radd__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (q, p, 0, q)))
        else:
            raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (q, -p, 0, q)))
        elif isinstance(other, Real):
            return Real(lambda: QuadraticComputation(iter(self), iter(other), (0, 1, -1, 0, 0, 0, 0, 1)))
        else:
            raise TypeError()

    def __rsub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (-q, p, 0, q)))
        else:
            raise TypeError()

    def __truediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (q, 0, 0, p)))
        elif isinstance(other, Real):
            return Real(lambda: QuadraticComputation(iter(self), iter(other), (0, 1, 0, 0, 0, 0, 1, 0)))
        else:
            raise TypeError()

    def __rtruediv__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            p, q = other.as_integer_ratio()
            return Real(lambda: AlgebraicComputation(iter(self), (0, p, q, 0)))
        else:
            raise TypeError()
