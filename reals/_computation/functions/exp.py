from reals._computation.base import Computation
from reals._computation.algebraic import AlgebraicComputation

from fractions import Fraction
from typing import Generator


def _exp_frac_computation_helper(x_squared: int, y: int) -> Generator[tuple[int, int], None, None]:
    m = 6 * y
    incr = 4 * y
    while True:
        yield (m, x_squared)
        m += incr


def exp_frac_computation(f: Fraction) -> Computation:
    x, y = f.as_integer_ratio()
    x2 = x * x
    return AlgebraicComputation(_exp_frac_computation_helper(x2, y), (2 * y + x, x2, 2 * y - x, x2))
