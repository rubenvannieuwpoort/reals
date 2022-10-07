from reals import log, pi

from fractions import Fraction
from decimal import Decimal

import pytest


def test_log_int() -> None:
    computed = log(101).evaluate(100, round=False)
    expected = '4.6151205168412594508841982669129891568908825871976047499312653617020118836023438715046801067419567578'
    assert computed == expected


def test_log_frac() -> None:
    computed = log(Fraction(1000, 3)).evaluate(100, round=False)
    expected = '5.8091429903140273606587291271305669181558139080635694763652893692652235358134484738343758604550628062'
    assert computed == expected


def test_log_decimal() -> None:
    computed = log(Decimal('1234.56')).evaluate(100, round=False)
    expected = '7.1184699102773095671272235598508897847732596241342302878299074433596989097525726349696283822921549090'
    assert computed == expected


def test_log_real() -> None:
    computed = log(pi).evaluate(100, round=False)
    expected = '1.1447298858494001741434273513530587116472948129153115715136230714721377698848260797836232702754897077'
    assert computed == expected


def test_log_str() -> None:
    with pytest.raises(TypeError):
        _ = log('hello').evaluate(100, round=False)  # type: ignore
