from reals._real import Real
from reals._normalize import normalize

from typing import Generator


def e_term_generator() -> Generator[int, None, None]:
    yield 2
    k = 2
    while True:
        yield 1
        yield k
        yield 1
        k += 2


e = Real.from_scf_term_generator(e_term_generator)


phi = Real.from_scf_term_function(lambda n: 1)


def pi_term_generator() -> Generator[tuple[int, int], None, None]:
    yield (0, 4)

    m = 1
    n = 1
    while True:
        yield (m, n)
        m += 2
        n += m


pi_unnormalized = Real.from_gcf_term_generator(pi_term_generator)

pi_normalized = normalize(pi_unnormalized)

sqrt2 = Real.from_scf_term_function(lambda n: 1 if n == 1 else 2)


def sqrt3_term_generator() -> Generator[int, None, None]:
    yield 1

    while True:
        yield 1
        yield 2


sqrt3 = Real.from_scf_term_generator(sqrt3_term_generator)
