from typing import Generator
from reals._real import Real, CachedComputation
from reals._sqrt import sqrt
from reals._algebraic_computation import AlgebraicComputation
from reals._quadratic_computation import QuadraticComputation
from fractions import Fraction
from reals.approximation import Approximation

import pytest


def test_real_cache_is_shared() -> None:
    x = Real([1, 2, 3, 4, 5])

    c1 = x.compute()
    assert isinstance(c1, CachedComputation)

    c2 = x.compute()
    assert isinstance(c2, CachedComputation)

    next(c1)
    next(c1)
    next(c1)

    next(c2)

    assert x.cache == [1, 2, 3]
    assert c1.cache == [1, 2, 3]
    assert c2.cache == [1, 2, 3]

    assert c1.index == 3
    assert c2.index == 1


MAX_ITERATIONS = 100


def get_rational_from_real(x: Real) -> Fraction:
    a = Approximation(x)
    a.improve(MAX_ITERATIONS)
    fraction = a.lower_bound_fraction()
    assert fraction == a.upper_bound_fraction()
    assert fraction
    return fraction


def test_rational_real_terminates() -> None:
    x = Real.from_fraction(Fraction(123, 456))
    c = x.compute()
    terms = []
    for _ in range(0, 7):
        terms.append(next(c))

    assert terms == [0, 3, 1, 2, 2, 2, 2]

    with pytest.raises(StopIteration):
        next(c)


def test_terminating_algebraic_computation() -> None:
    x = Real.from_fraction(Fraction(1, 10))
    c = AlgebraicComputation(x.compute(), (2, 0, 0, 1))
    assert next(c) == 0
    assert next(c) == 5

    with pytest.raises(StopIteration):
        next(c)


def test_terminating_quadratic_computation() -> None:
    x = Real.from_fraction(Fraction(2, 1))
    y = Real.from_fraction(Fraction(1, 10))
    c = QuadraticComputation(x.compute(), y.compute(), (1, 0, 0, 0, 0, 0, 0, 1))
    assert next(c) == 0
    assert next(c) == 5

    with pytest.raises(StopIteration):
        next(c)

    with pytest.raises(StopIteration):
        next(c)


def test_terminating_quadratic_computation2() -> None:
    x = Real.from_fraction(Fraction(2, 1))
    y = Real.from_fraction(Fraction(1, 10))
    c = QuadraticComputation(x.compute(), y.compute(), (1, 0, 0, 0, 0, 0, 0, 1))
    assert next(c) == 0
    assert next(c) == 5

    with pytest.raises(StopIteration):
        next(c)


def test_termination() -> None:
    f = get_rational_from_real(Fraction(2, 1) * Real.from_fraction(Fraction(1, 10)))
    assert f == Fraction(1, 5)


def sqrt2_gen() -> Generator[int, None, None]:
    yield 1
    while True:
        yield 2


def test_generalized_continued_fractions() -> None:
    sqrt2 = Real(sqrt2_gen())
    a = Approximation(sqrt2 * sqrt2)
    a.improve_epsilon(Fraction(1, 1000))

    lo = a.lower_bound_fraction()
    assert lo

    hi = a.upper_bound_fraction()
    assert hi

    assert lo < 2 and 2 < hi


def test_sqrt_of_square_fractions() -> None:
    x = sqrt(Fraction(16, 9))
    assert x == Real.from_fraction(Fraction(4, 3))
