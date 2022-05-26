from decimal import Decimal
from typing import Any, Callable, Generator, Union
from fractions import Fraction

# Reals
# =====
# Real arithmetic using generalized continued fractions

# Examples
# --------
# Compute a rational interval containing pi / e^2:
# ```
# from reals import pi, e, minmax
# # find the lower and upper bound after 6 iterations
# lo, hi = minmax(pi / (e * e), 6)
# print('pi / e^2 is in [{:.5f}, {:.5f}]'.format(float(lo), float(hi)))
# ```
#
# Compute the best rational approximation of sqrt(7) * pi
# from reals import best_fraction, pi, sqrt, minmax
# find the lower and upper bound after 10 iterations
# print(f'{best_fraction(sqrt(7) * pi, 6)}')


# Overview
# - Datastructures: contains datastructures for holomorphic and biholomorphic expressions
# - Types: contains the 'Real' type
# - Algorithms: contains implementations of the algebraic and quadratic algorithms due to Gosper
# - Computation: contains various helper functions as well as functions to compute squareroots of fractions
# - Numbers: contains definitions of e and pi
# - Consumers: contains various functions that consume a real and return some human-readable form

# Roadmap
# -------
# Currently, +, -, *, / are supported. It is possible to compute the squareroot of fractions, but not of irrational
# reals. Next steps: more/better consumers, squareroots of reals, exponentional function and logarithms.
# The stability/robustness probably needs to be improved.

# Technical improvements
# ----------------------
# - Add unit tests
# - Add a README.md with both a mathematical and technical/architectural introduction/description
# - Improve setup.py if necessary
# - Set up a CI/CD pipeline that uses flake8 and mypy
# - Structure the project better

# References
# ----------
# The following sources have used to brush up my knowledge of continued fractions:
# [1] "Continued Fraction Arithmetic" by Bill Gosper (https://perl.plover.com/classes/cftalk/INFO/gosper.txt)
# [2] "Exact real computer arithmetic with continued fractions" by J. Vuillemin
#     (https://hal.inria.fr/inria-00075792/document)
# [3] Continued fractions - Wikipedia (https://en.wikipedia.org/wiki/Continued_fraction)
# [4] Generalized continued fractions - Wikipedia (https://en.wikipedia.org/wiki/Generalized_continued_fraction)


# SECTION DATASTRUCTURES

class Homographic:
    a: int
    b: int
    c: int
    d: int

    def __init__(self, coeffs: tuple[int, int, int, int]) -> None:
        self.a, self.b, self.c, self.d = coeffs

    # replace x by (n + m/x), and bring the resulting expression into holomorphic form again
    def ingest(self, term: tuple[int, int]) -> None:
        n, m = term
        self.a, self.b = n * self.a + self.b, m * self.a
        self.c, self.d = n * self.c + self.d, m * self.c

    def ingest_inf(self) -> None:
        self.b, self.d = self.a, self.c

    # replace the holomorphic expression e = (ax + b) / (cx + d) by m / (e - n)
    def emit(self, term: tuple[int, int]) -> None:
        n, m = term
        self.a, self.b = self.a - n * self.c, self.b - n * self.d
        self.a, self.b, self.c, self.d = m * self.c, m * self.d, self.a, self.b

    def emit_digit(self, n: int, base: int = 10) -> None:
        self.a, self.b = self.a - n * self.c, self.b - n * self.d
        self.a, self.b = self.a * base, self.b * base

    def evaluate_int(self, x: int) -> int:
        return (self.a * x + self.b) // (self.c * x + self.b)

    def __repr__(self) -> str:
        a = str(self.a)
        b = str(self.b)
        c = str(self.c)
        d = str(self.d)
        return f'{a}x + {b}\n' + ('-' * (4 + max(len(a) + len(b), len(c) + len(d)))) + f'\n{c}x + {d}'


class Bihomographic:
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int
    g: int
    h: int

    def __init__(self, coeffs: tuple[int, int, int, int, int, int, int, int]) -> None:
        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = coeffs

    # replace x by (n + m/x), and bring the resulting expression into biholomorphic form again
    def x_ingest(self, term: tuple[int, int]) -> None:
        n, m = term
        self.a, self.b, self.c, self.d = n * self.a + self.c, n * self.b + self.d, m * self.a, m * self.b
        self.e, self.f, self.g, self.h = n * self.e + self.g, n * self.f + self.h, m * self.e, m * self.f

    def x_ingest_inf(self) -> None:
        self.c, self.d, = self.a, self.b
        self.g, self.h = self.e, self.f

    # replace y by (n + m/y), and bring the resulting expression into biholomorphic form again
    def y_ingest(self, term: tuple[int, int]) -> None:
        n, m = term
        self.a, self.b, self.c, self.d = n * self.a + self.b, m * self.a, n * self.c + self.d, m * self.c
        self.e, self.f, self.g, self.h = n * self.e + self.f, m * self.e, n * self.g + self.h, m * self.g

    def y_ingest_inf(self) -> None:
        self.b, self.d = self.a, self.c
        self.f, self.h = self.e, self.g

    # replace the biholomorphic expression e by m / (e - n)
    def emit(self, term: tuple[int, int]) -> None:
        n, m = term
        self.a, self.b, self.c, self.d = \
            self.a - n * self.e, self.b - n * self.f, self.c - n * self.g, self.d - n * self.h
        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = \
            m * self.e, m * self.f, m * self.g, m * self.h, self.a, self.b, self.c, self.d

    def __repr__(self) -> str:
        a = str(self.a)
        b = str(self.b)
        c = str(self.c)
        d = str(self.d)
        e = str(self.e)
        f = str(self.f)
        g = str(self.g)
        h = str(self.h)
        length_of_top_expression = 13 + len(a) + len(b) + len(c) + len(d)
        length_of_bottom_expression = 13 + len(e) + len(f) + len(g) + len(h)
        return (
            f'{a}xy + {b}x + {c}y + {d}\n' +
            ('-' * max(length_of_top_expression, length_of_bottom_expression)) + '\n' +
            f'{e}xy + {f}x + {g}y + {h}'
        )


# SECTION TYPES

Computation = Generator[tuple[int, int], None, None]


class Real():
    def __init__(self, x: Union[Callable[[], Computation], int, Fraction, Decimal]):
        if callable(x):
            self.start_computation = x
        elif isinstance(x, Fraction) or isinstance(x, int) or isinstance(x, Decimal):
            p, q = x.as_integer_ratio()
            self.start_computation = lambda: algebraic_computation(Real(empty), (p, p, q, q))
        else:
            raise TypeError(f'Cannot initialize Real from argument of type {type(x)}')

    @staticmethod
    def _convert(thing: Any) -> 'Real':
        if isinstance(thing, Real):
            return thing
        if isinstance(thing, int):
            return Real(thing)
        if isinstance(thing, Fraction):
            return Real(thing)
        else:
            raise TypeError(f'Cannot convert argument of type {type(thing)} to Real')

    def __neg__(self):
        return quadratic(self, Real(lambda: from_int(0)), (0, -1, 0, 0, 0, 0, 0, 1))

    def __add__(self, other: 'Real') -> 'Real':
        return quadratic(self, Real._convert(other), (0, 1, 1, 0, 0, 0, 0, 1))

    def __radd__(self, other: 'Real') -> 'Real':
        return quadratic(Real._convert(other), self, (0, 1, 1, 0, 0, 0, 0, 1))

    def __sub__(self, other: 'Real') -> 'Real':
        return quadratic(self, Real._convert(other), (0, 1,-1, 0, 0, 0, 0, 1))

    def __rsub__(self, other: 'Real') -> 'Real':
        return quadratic(Real._convert(other), self, (0, 1,-1, 0, 0, 0, 0, 1))

    def __mul__(self, other: 'Real') -> 'Real':
        return quadratic(self, Real._convert(other), (1, 0, 0, 0, 0, 0, 0, 1))

    def __rmul__(self, other: 'Real') -> 'Real':
        return quadratic(Real._convert(other), self, (1, 0, 0, 0, 0, 0, 0, 1))

    def __truediv__ (self, other: 'Real') -> 'Real':
        return quadratic(self, Real._convert(other), (0, 1, 0, 0, 0, 0, 1, 0))

    def __rtruediv__ (self, other: 'Real') -> 'Real':
        return quadratic(Real._convert(other), self, (0, 1, 0, 0, 0, 0, 1, 0))


# SECTION ALGORITHMS

MAX_INGESTIONS_BEFORE_EMISSION = 10


def algebraic(x: Real, coeffs: tuple[int, int, int, int]) -> Real:
    return Real(lambda: algebraic_computation(x, coeffs))


def algebraic_computation(xf: Real, coeffs: tuple[int, int, int, int]) -> Computation:
    h = Homographic(coeffs)
    ingestions_after_last_emission = 0
    terminated = False
    x = xf.start_computation()

    assert not(h.c == 0 and h.d == 0)

    while not (h.c == 0 and h.d == 0):
        if h.c != 0 and h.c + h.d != 0:
            n1 = h.a // h.c
            n2 = (h.a + h.b) // (h.c + h.d)
            if n1 == n2:
                term = (n1, 1)
                yield term
                h.emit(term)
                ingestions_after_last_emission = 0
                continue

        # if not(terminated):
        assert not(terminated)
        if ingestions_after_last_emission < MAX_INGESTIONS_BEFORE_EMISSION:
            try:
                h.ingest(next(x))
            except StopIteration:
                h.ingest_inf()
                terminated = True
            ingestions_after_last_emission += 1
        else:
            n = min(n1, n2)
            m = max(n1, n1) - n + 1
            term = (n, m)
            yield term
            h.emit(term)
            ingestions_after_last_emission = 0


def quadratic(xf: Real, yf: Real,
              coeffs: tuple[int, int, int, int, int, int, int, int]
              ) -> Real:
    return Real(lambda: quadratic_computation(xf, yf, coeffs))


def quadratic_computation(xf: Real,
                          yf: Real,
                          coeffs: tuple[int, int, int, int, int, int, int, int]
                          ) -> Computation:

    b = Bihomographic(coeffs)
    ingestions_after_last_emission = 0
    max_nominator = 1

    x = xf.start_computation()
    y = yf.start_computation()
    x_terminated = False
    y_terminated = False

    while not(b.a == 0 and b.b == 0 and b.c == 0 and b.d == 0):
        x_ingest = (b.e + b.f + b.g + b.h == 0) or (b.e + b.f == 0) or (b.e == 0)
        y_ingest = (b.e + b.f + b.g + b.h == 0) or (b.e + b.g == 0) or (b.e == 0)

        if not(x_ingest or y_ingest):
            n00 = (b.a + b.b + b.c + b.d) // (b.e + b.f + b.g + b.h)
            n10 = (b.a + b.b) // (b.e + b.f)
            n01 = (b.a + b.c) // (b.e + b.g)
            n11 = b.a // b.e

            x_ingest = not(abs(n00 - n10) < max_nominator and abs(n01 - n11) < max_nominator)
            y_ingest = not(abs(n00 - n01) < max_nominator and abs(n10 - n11) < max_nominator)

            if not(x_ingest or y_ingest) or ingestions_after_last_emission >= MAX_INGESTIONS_BEFORE_EMISSION:
                n = min(n00, n01, n10, n11)
                m = max(n00, n01, n10, n11) - n + 1
                term = (n, m)
                yield term
                b.emit(term)
                max_nominator = m
                ingestions_after_last_emission = 0
                continue

        ingestions_after_last_emission += 1

        if x_ingest:
            assert not(x_terminated)
            try:
                term = next(x)
                b.x_ingest(term)
            except StopIteration:
                b.x_ingest_inf()
                x_terminated = True

        if y_ingest:
            assert not(y_terminated)
            try:
                term = next(y)
                b.y_ingest(term)
            except StopIteration:
                b.y_ingest_inf()
                y_terminated = True


# SECTION COMPUTATION

def empty() -> Computation:
    return
    yield


def from_int(n: int) -> Computation:
    yield (n, 1)


def gcd(x: int, y: int) -> int:
    x = abs(x)
    y = abs(y)
    while y:
        x, y = y, x % y
    return x


def int_sqrt(n: int):
    assert(n >= 0)
    k, k_squared = 1, 1
    while k_squared <= n:
        k_squared += 2 * k + 1
        k += 1
    return k - 1


def sqrt_int(n: int) -> 'Real':
    return Real(lambda: sqrt_int_computation(n))


def sqrt_int_computation(n: int) -> Computation:
    int_sqr = int_sqrt(n)
    if int_sqr * int_sqr == n:
        yield (int_sqr, 1)
        return

    a, b, c = 1, 0, 1

    while True:
        assert a == 1
        integer_part = (int_sqr + b) // c
        yield (integer_part, 1)
        b -= integer_part * c
        a, b, c = a * c, -c * b, a * a * n - b * b
        g = gcd(gcd(a, b), c)
        a, b, c = a // g, b // g, c // g


def sqrt(x: Union[int, Fraction, Decimal]) -> 'Real':
    if isinstance(x, int):
        return sqrt_int(x)
    elif isinstance(x, Fraction):
        p, q = x.as_integer_ratio()
        return quadratic(sqrt_int(p), sqrt_int(q), (0, 1, 0, 0, 0, 0, 1, 0))
    else:
        raise TypeError(f'Cannot compute sqrt of argument of type {type(x)}')


# SECTION NUMBERS

# e
# -
# uses the simple continued fraction for e:
# e = [2; 1 2 1 1 4 1 1 6 1 1 8 1 ...]
def e_computation() -> Computation:
    yield (2, 1)
    n = 2
    while True:
        yield (1, 1)
        yield (n, 1)
        yield (1, 1)
        n += 2


e = Real(e_computation)


# π
# -
# This uses the following generalized continued fraction for pi:
#              4
# π = -------------------
#                 1²
#       1 + -------------
#                   2²
#           3 + ---------
#                     3²
#               5 + -----
#                    ...
# this is the last example for pi on https://en.wikipedia.org/wiki/Generalized_continued_fraction#Examples
def pi_computation() -> Computation:
    yield (0, 4)
    i = 1
    j = 1
    while True:
        yield (i, j)
        i += 2
        j += i


pi = Real(pi_computation)


# SECTION CONSUMERS

def rational_bounds(x: Real, num_iters: int) -> tuple[Fraction, Fraction]:
    xc = x.start_computation()
    h = Homographic((1, 0, 0, 1))
    try:
        for _ in range(0, num_iters):
            h.ingest(next(xc))
    except StopIteration:
        h.ingest_inf()
    f1 = Fraction(h.a + h.b, h.c + h.d)
    f2 = Fraction(h.a, h.c)
    return (f1, f2) if num_iters % 2 == 0 else (f2, f1)


def best_fraction(x: Real, num_iters: int) -> Fraction:
    xc = x.start_computation()
    h = Homographic((1, 0, 0, 1))
    is_simple_continued_fraction = True
    try:
        for _ in range(0, num_iters):
            term = next(xc)
            _, m = term
            if m != 1:
                is_simple_continued_fraction = False
            h.ingest(term)
    except StopIteration:
        h.ingest_inf()
        return Fraction(h.a, h.b)

    if is_simple_continued_fraction:
        return Fraction(h.a, h.c)

    f1 = Fraction(h.a + h.b, h.c + h.d)
    f2 = Fraction(h.a, h.c)
    (low, high) = (f1, f2) if num_iters % 2 == 0 else (f2, f1)

    low_cf, high_cf = Real(low), Real(high)
    low_computation = low_cf.start_computation()
    high_computation = high_cf.start_computation()

    h = Homographic((1, 0, 0, 1))

    while True:
        low_term = next(low_computation)
        high_term = next(high_computation)

        low_n, low_m = low_term
        high_n, high_m = high_term

        assert low_m == 1 and high_m == 1

        if low_n != high_n:
            output_term = min(low_n, high_n)
            is_last = False
            if low_n < high_n:
                try:
                    next(low_computation)
                except StopIteration:
                    is_last = True
            else:
                try:
                    next(high_computation)
                except StopIteration:
                    is_last = True

            if not(is_last):
                output_term += 1

            h.ingest((output_term, 1))
            return Fraction(h.a, h.c)

        h.ingest((low_n, 1))


def approximate(x: Real, n: int) -> float:
    computation = x.f()
    h = Homographic((1, 0, 0, 1))
    for _ in range(0, n):
        try:
            h.ingest(next(computation))
        except StopIteration:
            h.ingest_inf()
            break
    return h.a / h.c


def normalize(x: Real) -> Real:
    return algebraic(x, (1, 0, 0, 1))


def terms(x: Real, n: int) -> list[int]:
    collected_terms = []
    computation = x.start_computation()
    for _ in range(0, n):
        try:
            collected_terms.append(next(computation))
        except StopIteration:
            break
    return collected_terms
