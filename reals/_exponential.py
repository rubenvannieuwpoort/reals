
from fractions import Fraction
from typing import Generator
from reals._real import Real
from reals._bounds import IntervalComputation
from reals._homographic import Homographic
from reals.approximation import _approximate_epsilon_helper
from reals._algebraic_computation import AlgebraicComputation
from reals._normalize import normalize


def exp_int_computation(n: int) -> Generator[tuple[int, int], None, None]:
    m = 6
    while True:
        yield (m, n * n)
        m += 4


def exp_int(n: int) -> Real:
    n_squared = n * n
    computation = iter(Real.from_gcf_term_generator(lambda: exp_int_computation(n)))
    return normalize(Real(lambda: AlgebraicComputation(computation, (2 + n, n_squared, 2 - n, n_squared))))


# TODO(Ruben)
def exp_frac(x: Real) -> Real:
    return x


def exp(x: Real) -> Real:
    epsilon = Fraction(1, 1000)
    c = IntervalComputation(iter(x))
    _approximate_epsilon_helper(Homographic(1, 0, 0, 1), c, epsilon)
    upper_bound = c.lower_bound
    assert upper_bound
    p, q = upper_bound.as_integer_ratio()
    n = (p + q - 1) // q
    rest = x - n
    return exp_int(n) * exp_frac(rest)
