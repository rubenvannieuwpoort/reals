
from typing import Iterable, Iterator, Union


Term = Union[int, tuple[int, int]]


Computation = Iterator[Term]


class CachedComputation(Computation):
    def __init__(self, iterator: Iterator[Term], cache: list[Term]):
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


class Real:
    def __init__(self, it: Union[Iterator[Term], Iterable[Term]]) -> None:
        self.iterator = iter(it)
        self.cache: list[Term] = []

    def compute(self) -> Computation:
        return CachedComputation(self.iterator, self.cache)
