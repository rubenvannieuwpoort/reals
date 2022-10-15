from reals._computation.base import Computation
from reals._computation.algebraic import AlgebraicComputation

from fractions import Fraction
from typing import Generator


def _sin_computation_helper(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    x_squared = x * x
    y_squared = y * y
    x_squared_y_squared = x_squared * y_squared
    yield (0, x)
    yield (y, x_squared * y)

    n = 2
    while True:
        coeff = n * (n + 1)
        a = coeff * y_squared - x_squared
        assert a > 0
        yield (a, coeff * x_squared_y_squared)
        n += 2


# compute sin(x) for -pi/2 < x < pi/2
def sin_frac_computation(f: Fraction) -> Computation:
    x, y = f.as_integer_ratio()
    return AlgebraicComputation(_sin_computation_helper(x, y))
