from reals._computation.base import Computation
from reals._computation.algebraic import AlgebraicComputation

from fractions import Fraction
from typing import Generator


def _log_frac_computation_helper(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield (0, x)

    m, n = x, y
    incr = 2 * y
    while True:
        yield (n, m)
        yield (2, m)
        m += x
        n += incr


def log_frac_computation(f: Fraction) -> Computation:
    x, y = f.as_integer_ratio()
    return AlgebraicComputation(_log_frac_computation_helper(x - y, y), (1, 0, 0, 1))
