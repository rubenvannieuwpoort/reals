import reals._real
import reals._algebraic_computation


DEFAULT_MAX_INGESTIONS = 100


def normalize(x: reals._real.Real, max_ingestions=DEFAULT_MAX_INGESTIONS) -> reals._real.Real:
    return reals._real.Real(
        reals._algebraic_computation.AlgebraicComputation(x.compute(), (1, 0, 0, 1), max_ingestions))
