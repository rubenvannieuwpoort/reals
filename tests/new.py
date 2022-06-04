from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from email.generator import Generator
from fractions import Fraction
import itertools
from typing import Callable, Union

# represents an expression of the form (ax + b)/(cx + d)
@dataclass
class HomographicExpression:
    a: int; b: int; c: int; d: int

# represents an expression of the form (axy + bx + cy + d)/(exy + fx + gy + h)
@dataclass
class BihomographicExpression:
    a: int; b: int; c: int; d: int; e: int; f: int; g:int; h: int

class Refinement(ABC):
    pass

class IntegerRefinement(Refinement):
    def __init__(self, n: int, m:int = 1):
        self.n = n
        self.m = m

class InfiniteRefinement(Refinement):
    def __init__(self):
        pass

class RefinementStream(ABC):
    pass

class NonEmptyRefinementStream(RefinementStream):
    def __init__(self,
                 refinement_generator: Generator[Refinement, None, None],
                 terminated = False
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

class EmptyRefinementStream(RefinementStream):
    def __init__(self) -> None:
        pass

    def has_terminated(self) -> bool:
        return True

class Computation(RefinementStream):
    @abstractmethod
    def __copy__(self) -> 'Computation':
        pass

    @abstractmethod
    def refine(n: int) -> None:
        pass

class AlgebraicComputation:
    def __init__(self, stream: RefinementStream,
                 state: HomographicExpression = HomographicExpression(1, 0, 0, 1)
                 ) -> None:
        self.state = state
        self.stream = stream

    def __copy__(self) -> 'AlgebraicComputation':
        self.stream, newstream = itertools.tee(self.stream)
        return AlgebraicComputation(newstream, self.state)

class Real:
    def __init__(self,
                 x: Union[Callable[[], Computation], Fraction, Decimal, int, str]) -> None:
        if isinstance(x, str):
            x = Decimal(x)

        if callable(x):
            self.start_computation = x
        elif isinstance(x, Fraction) or isinstance(x, Fraction) or isinstance(x, Fraction):
            p, q = x.as_integer_ratio()
            stream = EmptyRefinementStream()
            state = HomographicExpression(p, p, q, q)
            self.start_computation = lambda: AlgebraicComputation(stream, state)





class RangeInformation:
    pass
