
from typing import Generator
from reals._real import Real
from reals._algebraic_computation import AlgebraicComputation
from reals._normalize import normalize


def exp_int_computation(n: int) -> Generator[tuple[int, int], None, None]:
    m = 6
    while True:
        yield (m, n * n)
        m += 4


def exp_int(n: int) -> Real:
    n_squared = n * n
    computation = iter(Real.from_gcf_term_generator(lambda: exp_int_computation(n)))
    return normalize(Real(lambda: AlgebraicComputation(computation, (2 + n, n_squared, 2 - n, n_squared))))
