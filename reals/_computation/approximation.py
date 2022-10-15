from fractions import Fraction
from typing import Optional
from reals._classes.homographic import Homographic
# TODO(Ruben): remove this if there's no use for this

from reals._computation.base import Computation
from reals._term import Term


class ApproximatingComputation:
    def __init__(self, c: Computation):
        self.ingestions = 0
        self.state = Homographic(1, 0, 0, 1)
        self.computation = c
        self.terminated = False

    def __next__(self) -> Term:
        if self.terminated:
            raise StopIteration

        try:
            nxt = next(self.computation)
            self.ingestions += 1
            self.state.ingest(nxt)
            return nxt
        except StopIteration:
            self.ingestions += 1
            self.terminated = True
            self.state.ingest_inf()
            raise

    def improve(self, n: int = 1) -> None:
        for _ in range(0, n):
            try:
                self.__next__()
            except StopIteration:
                break

    def _lower(self) -> tuple[int, int]:
        if self.ingestions % 2 == 1:
            return (self.state.a, self.state.c)
        else:
            return (self.state.a + self.state.b, self.state.c + self.state.d)

    def _upper(self) -> tuple[int, int]:
        if self.ingestions % 2 == 1:
            return (self.state.a + self.state.b, self.state.c + self.state.d)
        else:
            return (self.state.a, self.state.c)

    def lower_bound_fraction(self) -> Optional[Fraction]:
        if self.ingestions == 0:
            return None
        p, q = self._lower()
        return Fraction(p, q) if q != 0 else None

    def upper_bound_fraction(self) -> Optional[Fraction]:
        p, q = self._upper()
        return Fraction(p, q) if q != 0 else None
