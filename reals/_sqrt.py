from reals._real import Real
import reals._computation
import reals._quadratic_computation
import reals._homographic
import reals._term

from fractions import Fraction
from decimal import Decimal
from typing import Union


# compute sqrt(n) where n is an integer
class SqrtComputation(reals._computation.Computation):
    def __init__(self, n: int):
        if n < 0:
            raise ValueError()

        self.state = reals._homographic.Homographic(0, n, 1, 0)

    def __next__(self) -> reals._term.Term:
        n = self.state.fix_point()

        # TODO(Ruben): this is a hack to handle the case where n is a square
        # it seems to work in practice but I have no clue why it works
        # it would be nice to have a proof that it works
        if not n:
            raise StopIteration()

        self.state.ingest(n)
        self.state.emit(n)
        return n


def sqrt_frac(f: Union[Fraction, int, Decimal]) -> Real:
    p, q = f.as_integer_ratio()

    if p == 0:
        return Real.from_int(0)

    if p < 0:
        raise ValueError()

    assert p > 0

    if q == 1:
        return Real(SqrtComputation(p))

    # simply returning SqrtComputation(Homographic(0, p, q, 0)) works for most fractions except when p, q are squares
    # and q > 1 for q = 1 and p square -- a hack is in place which seems to work in practice, so this way of computing
    # works when p and q > 1 are squares

    # this is a variation on Real(SqrtComputation(p)) / Real(SqrtComputation(q)) with less overhead
    return Real(
        reals._quadratic_computation.QuadraticComputation(
            SqrtComputation(p),
            SqrtComputation(q),
            (0, 1, 0, 0, 0, 0, 1, 0)
        ))


def sqrt(x: Union[Real, Fraction, int, Decimal]) -> Real:
    if isinstance(x, Real):
        return x.__pow__(Fraction(1, 2))
    if isinstance(x, Fraction) or isinstance(x, int) or isinstance(x, Decimal):
        return sqrt_frac(x)
    raise TypeError()
