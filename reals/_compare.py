from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reals._real import Real

from enum import Enum, auto
from fractions import Fraction


EPSILON = Fraction(1, 100000)


class ComparisonResult(Enum):
    SMALLER = auto()
    GREATER = auto()
    UNKNOWN = auto()


# TODO(Ruben): this is very ugly, needs a rewrite
def compare(x: Real, y: Real, epsilon: Fraction = EPSILON) -> ComparisonResult:
    from reals.approximation import Approximation
    x_approximation = Approximation(x)
    x_approximation.improve()
    y_approximation = Approximation(y)
    y_approximation.improve()

    while True:
        x_lower = x_approximation.lower_bound_fraction()
        x_upper = x_approximation.upper_bound_fraction()
        y_lower = y_approximation.lower_bound_fraction()
        y_upper = y_approximation.upper_bound_fraction()

        if x_upper and y_lower and x_upper < y_lower:
            return ComparisonResult.SMALLER

        if x_lower and y_upper and y_upper < x_lower:
            return ComparisonResult.GREATER

        x_eps = x_approximation.epsilon_fraction()
        y_eps = y_approximation.epsilon_fraction()

        if not x_eps:
            x_approximation.improve()
        elif x_eps > epsilon / 2:
            x_approximation.improve()

        if not y_eps:
            y_approximation.improve()
        elif y_eps > epsilon / 2:
            y_approximation.improve()

        if x_eps is not None and x_eps < epsilon / 2 and y_eps is not None and y_eps < epsilon / 2:
            break

    return ComparisonResult.UNKNOWN
