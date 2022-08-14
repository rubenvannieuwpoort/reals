from reals._real import Real
from reals._algebraic_computation import AlgebraicComputation


def normalize(x: Real) -> Real:
    return Real(lambda: AlgebraicComputation(iter(x), (1, 0, 0, 1)))
