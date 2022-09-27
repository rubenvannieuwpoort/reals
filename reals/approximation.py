import reals._real
import reals._homographic
import reals._computation

from fractions import Fraction
from typing import Optional, Union


class Approximation:
    def __init__(self, x: Union[reals._real.Real, reals._computation.Computation]):
        self.ingestions = 0
        self.state = reals._homographic.Homographic(1, 0, 0, 1)
        if isinstance(x, reals._real.Real):
            self.computation = x.compute()
        else:
            self.computation = x

    def improve(self, n: int = 1) -> None:
        for _ in range(0, n):
            try:
                self.ingestions += 1
                next_term = next(self.computation)
                self.state.ingest(next_term)
            except StopIteration:
                self.state.ingest_inf()
                break

    def improve_epsilon(self, epsilon: Fraction) -> None:
        while not (eps := self.epsilon_fraction()) or eps > epsilon:
            try:
                self.ingestions += 1
                next_term = next(self.computation)
                self.state.ingest(next_term)
            except StopIteration:
                self.state.ingest_inf()
                assert self.epsilon_fraction() == 0
                break

    def as_fraction(self) -> Optional[Fraction]:
        if self.state.c != 0:
            return Fraction(self.state.a, self.state.c)
        return None

    def as_float(self) -> Optional[float]:
        if self.state.c != 0:
            return self.state.a / self.state.c
        return None

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

    def lower_bound_float(self) -> Optional[float]:
        if self.ingestions == 0:
            return None
        p, q = self._lower()
        return p / q if q != 0 else None

    def upper_bound_fraction(self) -> Optional[Fraction]:
        p, q = self._upper()
        return Fraction(p, q) if q != 0 else None

    def upper_bound_float(self) -> Optional[float]:
        p, q = self._upper()
        return p / q if q != 0 else None

    def interval_fraction(self) -> tuple[Optional[Fraction], Optional[Fraction]]:
        return (self.lower_bound_fraction(), self.upper_bound_fraction())

    def interval_float(self) -> tuple[Optional[float], Optional[float]]:
        return (self.lower_bound_float(), self.upper_bound_float())

    def epsilon_fraction(self) -> Optional[Fraction]:
        lower, upper = self.interval_fraction()
        if lower and upper:
            return upper - lower
        return None

    def float_epsilon(self) -> Optional[float]:
        rational_epsilon = self.epsilon_fraction()
        if rational_epsilon:
            return float(rational_epsilon)
        return None

    def closest_float(self) -> float:
        while not (lo := self.lower_bound_float()) or not (hi := self.upper_bound_float()) or lo != hi:
            self.improve()

        assert lo
        return lo


def closest_float(x: reals._real.Real) -> float:
    return Approximation(x).closest_float()


def best_rational_approximations(x: reals._real.Real, n: int):
    a = Approximation(x)

    result: list[Fraction] = []
    for _ in range(0, n):
        a.improve()
        rational_approximation = a.as_fraction()
        assert rational_approximation is not None
        result.append(rational_approximation)

    return result
