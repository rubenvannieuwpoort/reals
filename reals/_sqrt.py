from reals._computation import Computation
from reals._quadratic_computation import QuadraticComputation
from reals._real import Real
from reals._homographic import Homographic
from reals._term import Term

from fractions import Fraction
from typing import Union


# compute sqrt(n) where n is an integer
class SqrtComputation(Computation):
    def __init__(self, n: int):
        if n < 0:
            raise ValueError()

        self.state = Homographic(0, n, 1, 0)

    def __next__(self) -> Term:
        n = self.state.fix_point()

        # TODO(Ruben): this is a hack to handle the case where n is a square
        # it seems to work in practice but I have no clue why it works
        # it would be nice to have a proof that it works
        if not n:
            raise StopIteration()

        self.state.ingest(n)
        self.state.emit(n)
        return n


def sqrt(f: Union[Fraction, int]) -> Real:
    p, q = f.as_integer_ratio()

    if p == 0:
        return Real.from_int(0)

    if p < 0:
        raise ValueError()

    assert p > 0

    if q == 1:
        return Real(SqrtComputation(p))

    # simply returning SqrtComputation(Homographic(0, p, q, 0)) works for most fractions except when p, q are squares
    # and q > 1 for q = 1 and p square a hack is in place which seems to work in practice, so this way of computing
    # works when p and q > 1 are squares

    # this is a variation on Real(SqrtComputation(p)) / Real(SqrtComputation(q)) with less overhead
    return Real(
        QuadraticComputation(
            SqrtComputation(p),
            SqrtComputation(q),
            (0, 1, 0, 0, 0, 0, 1, 0)
        ))
