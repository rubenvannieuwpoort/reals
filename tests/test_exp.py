from reals import phi, exp

from fractions import Fraction
from decimal import Decimal

import pytest


def test_exp_int() -> None:
    computed = exp(5).evaluate(100, round=False)
    expected = '148.4131591025766034211155800405522796234876675938789890467528451109120648209585760796884094598990211412'  # noqa
    assert computed == expected


def test_exp_frac() -> None:
    computed = exp(Fraction(3, 5)).evaluate(100, round=False)
    expected = '1.8221188003905089748753676681628645133822388085464353863205474765888196502986192375060718416118245331'
    assert computed == expected


def test_exp_decimal() -> None:
    computed = exp(Decimal('1.23456')).evaluate(100, round=False)
    expected = '3.4368659669422447026568766082120403436743039295730280871650545957332739956580328655257881549299559275'
    assert computed == expected


def test_exp_real() -> None:
    computed = exp(phi).evaluate(100, round=False)
    expected = '5.0431656433600286513118821892854247103235901754138463603020001967777869609108929428415187821843384653'
    assert computed == expected


def test_exp_str() -> None:
    with pytest.raises(TypeError):
        _ = exp('lol').evaluate(100, round=False)  # type: ignore
