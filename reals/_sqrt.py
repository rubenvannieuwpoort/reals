from reals._real import Real

from fractions import Fraction
from decimal import Decimal
from typing import Union


def sqrt(x: Union[Real, Fraction, int, Decimal]) -> Real:
    if not (isinstance(x, Real) or isinstance(x, Fraction) or isinstance(x, int) or isinstance(x, Decimal)):
        raise TypeError()
    return Real.from_number(x).__pow__(Fraction(1, 2))
