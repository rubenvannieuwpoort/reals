from reals._real import Real
from reals._term import Term
from reals._normalize import normalize

from typing import Generator


def e_term_generator() -> Generator[Term, None, None]:
    yield 2
    k = 2
    while True:
        yield 1
        yield k
        yield 1
        k += 2


e = Real(e_term_generator())


def pi_term_generator() -> Generator[Term, None, None]:
    yield (0, 4)

    m = 1
    n = 1
    while True:
        yield (m, n)
        m += 2
        n += m


pi_unnormalized = Real(pi_term_generator())

pi = normalize(pi_unnormalized)


def phi_term_generator() -> Generator[Term, None, None]:
    while True:
        yield 1


phi = Real(phi_term_generator())
