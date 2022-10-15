from reals._term import Term
from reals._computation.base import Computation

from typing import Iterator


class CachedComputation(Computation):
    def __init__(self, iterator: Iterator[Term], cache: list[Term] = []):
        self.cache = cache
        self.iterator = iterator
        self.index = 0

    def __next__(self) -> Term:
        assert self.index <= len(self.cache)

        if self.index == len(self.cache):
            self.cache.append(next(self.iterator))

        index = self.index
        self.index += 1
        return self.cache[index]
