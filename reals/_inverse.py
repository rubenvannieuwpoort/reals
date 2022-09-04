from reals._computation import Computation
from reals._term import Term, expand_term

from typing import Optional


class InverseComputation(Computation):
    def __init__(self, computation: Computation):
        self.computation = computation
        self.first = True
        self.cached_term: Optional[Term] = None

    def __next__(self) -> Term:
        if self.cached_term:
            term = self.cached_term
            self.cached_term = None
            return term

        next_term = next(self.computation)
        if self.first:
            self.first = False

            n, _ = expand_term(next_term)

            if n == 0:
                return next(self.computation)
            else:
                self.cached_term = next_term
                return 0

        return next_term
