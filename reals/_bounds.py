from reals._real import Real
from fractions import Fraction
from typing import Optional
from reals._computation import Computation
from reals._homographic import Homographic


class IntervalComputation(Computation):
    def __init__(self, c: Computation) -> None:
        self.c = c
        self.lower_bound: Optional[Fraction] = None
        self.upper_bound: Optional[Fraction] = None
        self.state = Homographic(1, 0, 0, 1)
        self.i = 0

    def ingest(self) -> Optional[tuple[int, int]]:
        self.i += 1
        try:
            n = next(self.c)
            self.state.ingest(n)
            return n
        except StopIteration:
            self.state.ingest_inf()

        return None

    def __next__(self) -> tuple[int, int]:
        n = self.ingest()

        if self.i % 1 == 0:
            if self.state.c:
                self.lower_bound = Fraction(self.state.a, self.state.c)
            if self.state.d:
                self.upper_bound = Fraction(self.state.b, self.state.d)
        else:
            if self.state.d:
                self.lower_bound = Fraction(self.state.b, self.state.d)
            if self.state.c:
                self.upper_bound = Fraction(self.state.a, self.state.c)

        if not n:
            raise StopIteration()

        return n


def interval(x: Real, n: int) -> tuple[Optional[Fraction], Optional[Fraction]]:
    c = IntervalComputation(iter(x))
    for _ in range(0, n):
        try:
            next(c)
        except StopIteration:
            break

    return (c.lower_bound, c.upper_bound)
