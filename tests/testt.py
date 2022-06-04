from abc import ABC, abstractmethod
from typing import Generator
from typing import Callable


class RangeRefinement(ABC):
    pass


class IntegerRefinement(RangeRefinement):
    def __init__(self, base: int, numerator: int = 1) -> None:
        self.base = base
        self.numerator = numerator

    def is_infinite(self) -> bool:
        return False


class InfiniteRefinement(RangeRefinement):
    def is_infinite(self) -> bool:
        return True


class RangeInformation(ABC):
    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self) -> RangeRefinement:
        pass


class SimpleContinuedFraction:
    def __init__(self, term_generator: Callable[[], Generator[int, None, None]]) -> None:
        self.start_computation = lambda: SimpleContinuedFractionComputation(term_generator())
        self.is_terminated = False


class GeneralizedContinuedFraction(RangeInformation):
    def __init__(self, term_generator: Callable[[], Generator[tuple[int, int], None, None]]) -> None:
        self.term_generator = term_generator
        self.is_terminated = False

    def __next__(self):
        assert not self.is_terminated
        try:
            n, m = next(self.term_generator)
            return IntegerRefinement(n, m)
        except StopIteration:
            self.is_terminated = True
            return InfiniteRefinement()


class Computation(RangeInformation):
    pass


class SimpleContinuedFractionComputation(RangeInformation):
    def __init__(self, term_generator: Generator[int, None, None]) -> None:
        print('a')
        self.term_generator = term_generator
        self.is_terminated = False

    def __next__(self):
        print('b')
        assert not self.is_terminated
        try:
            print('c')
            ttt = next(self.term_generator)
            print(ttt)
            return IntegerRefinement(ttt)
        except StopIteration:
            print('d')
            self.is_terminated = True
            return InfiniteRefinement()
