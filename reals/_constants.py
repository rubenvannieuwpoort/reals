import reals._real
import reals._term
import reals._normalize

from typing import Generator


def e_term_generator() -> Generator[reals._term.Term, None, None]:
    yield 2
    k = 2
    while True:
        yield 1
        yield k
        yield 1
        k += 2


e = reals._real.Real(e_term_generator())


def pi_term_generator() -> Generator[reals._term.Term, None, None]:
    yield (0, 4)

    m = 1
    n = 1
    while True:
        yield (m, n)
        m += 2
        n += m


pi_unnormalized = reals._real.Real(pi_term_generator())

pi = reals._normalize.normalize(pi_unnormalized)


def phi_term_generator() -> Generator[reals._term.Term, None, None]:
    while True:
        yield 1


phi = reals._real.Real(phi_term_generator())
