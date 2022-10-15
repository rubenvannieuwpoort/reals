from reals._term import Term
from reals._computation.approximation import ApproximatingComputation
from reals._computation.base import Computation

from fractions import Fraction
from typing import Callable, Iterator


class MonotonicComputation(Computation):
    def __init__(self, c: Computation,
                 generator_function: Callable[[Fraction], Iterator[Term]]) -> None:
        self.generator_function = generator_function
        self.a = ApproximatingComputation(c)
        self.n = 0
        self.increase_precision()

    def increase_precision(self):
        self.a.improve(10)

        self.c1 = self.generator_function(self.a.upper_bound_fraction())
        self.c2 = self.generator_function(self.a.lower_bound_fraction())

        for _ in range(0, self.n):
            next(self.c1)
            next(self.c2)

    def __next__(self) -> tuple[int, int]:
        while True:
            term1 = next(self.c1)
            term2 = next(self.c2)
            if term1 == term2:
                self.n += 1
                return term1
            else:
                self.increase_precision()
