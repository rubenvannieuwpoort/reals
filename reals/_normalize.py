from reals._real import Real
from reals._algebraic_computation import AlgebraicComputation


DEFAULT_MAX_INGESTIONS = 100


def normalize(x: Real, max_ingestions=DEFAULT_MAX_INGESTIONS) -> Real:
    return Real(AlgebraicComputation(x.compute(), (1, 0, 0, 1), max_ingestions))
