from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass
import itertools
from typing import Generator
from typing import Callable


# represents an expression of the form (ax + b)/(cx + d)
@dataclass
class HomographicExpression:
    a: int
    b: int
    c: int
    d: int


# represents an expression of the form (axy + bx + cy + d)/(exy + fx + gy + h)
@dataclass
class BihomographicExpression:
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int
    g: int
    h: int


class Refinement(ABC):
    pass


class IntegerRefinement(Refinement):
    def __init__(self, n: int, m: int = 1):
        self.n = n
        self.m = m


class InfiniteRefinement(Refinement):
    def __init__(self):
        pass


class RefinementStream:
    def __init__(self,
                 refinement_generator: Generator[Refinement, None, None],
                 terminated=False
                 ) -> None:
        self.refinement_generator = refinement_generator
        self._terminated = terminated

    def has_terminated(self) -> bool:
        return self._terminated

    def __next__(self):
        if self.has_terminated:
            raise RuntimeError('next called on terminated RefinementStream object')

        try:
            return next(self.refinement_generator)
        except StopIteration:
            self.has_terminated = True
            raise


class Computation(ABC):
    @abstractmethod
    def has_terminated(self) -> bool:
        pass

    @abstractmethod
    def __copy__(self) -> 'Computation':
        pass

    @abstractmethod
    def step(self) -> Refinement:
        pass


class ComputationFromContinuedFraction(Computation):
    def __init__(self, cf: Generator[tuple[int, int], None, None]):
        self._terminated = False
        self._cf = cf

    def __copy__(self) -> 'ComputationFromContinuedFraction':
        self._cf, generator_copy = itertools.tee(self.cf)  # type: ignore
        return ComputationFromContinuedFraction(generator_copy)  # type: ignore

    def has_terminated(self) -> bool:
        return self._terminated

    def step(self) -> Refinement:
        if self._terminated:
            raise RuntimeError('step called on terminated computation')
        try:
            term = next(self._cf)
            if isinstance(term, int):
                n, m = term, 1
            elif isinstance(term, tuple) and len(term) == 2:
                n, m = term
            else:
                raise TypeError('expected either int or tuple[int, int] as term')
            return IntegerRefinement(n, m)
        except StopIteration:
            self._terminated = True
            return InfiniteRefinement()


class AlgebraicComputation(Computation):
    def __init__(self, input_computation: Computation,
                 state: HomographicExpression = HomographicExpression(1, 0, 0, 1)
                 ) -> None:
        self.state = state
        self.input_computation = input_computation

    def __copy__(self) -> 'AlgebraicComputation':
        return AlgebraicComputation(copy(self.input_computation), copy(self.state))

    def has_terminated(self) -> bool:
        return self.state.a == self.state.b and self.state.c == self.state.d

    def step(self) -> Refinement:
        # TODO
        pass


class Real:
    def __init__(self, x: Callable[[], Computation]) -> None:
        assert callable(x)
        self.start_computation = x


def continued_fraction(cf: Callable[[], Generator[tuple[int, int], None, None]]) -> Real:
    return Real(lambda: ComputationFromContinuedFraction(cf()))
