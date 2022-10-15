from reals._computation.algebraic import AlgebraicComputation
from reals._computation.base import Computation
from reals._term import Term

from typing import Generator


def pi_computation_helper() -> Generator[Term, None, None]:
    yield (0, 4)

    m = 1
    n = 1
    while True:
        yield (m, n)
        m += 2
        n += m


def pi_computation() -> Computation:
    return AlgebraicComputation(pi_computation_helper())
