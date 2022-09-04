import reals._computation
import reals._term

from typing import Optional


class InverseComputation(reals._computation.Computation):
    def __init__(self, computation: reals._computation.Computation):
        self.computation = computation
        self.first = True
        self.cached_term: Optional[reals._term.Term] = None

    def __next__(self) -> reals._term.Term:
        if self.cached_term:
            term = self.cached_term
            self.cached_term = None
            return term

        next_term = next(self.computation)
        if self.first:
            self.first = False

            n, _ = reals._term.expand_term(next_term)

            if n == 0:
                return next(self.computation)
            else:
                self.cached_term = next_term
                return 0

        return next_term
