from reals._term import Term

from typing import Generator


def e_computation() -> Generator[Term, None, None]:
    yield 2
    k = 2
    while True:
        yield 1
        yield k
        yield 1
        k += 2
