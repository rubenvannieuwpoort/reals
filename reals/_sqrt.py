from reals._computation import Computation
from reals._inverse import InverseComputation
from reals._real import Real
from reals._homographic import Homographic
from reals._term import Term

from fractions import Fraction
from typing import Union


class SqrtComputation(Computation):
    def __init__(self, state: Homographic):
        self.state = state

    def __next__(self) -> Term:
        n = self.state.fix_point()
        assert n
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

    # TODO(Ruben): this doesn't handle fractions that are squares yet...

    if p > q:
        return Real(SqrtComputation(Homographic(0, p, q, 0)))
    else:
        return Real(InverseComputation(SqrtComputation(Homographic(0, q, p, 0))))
