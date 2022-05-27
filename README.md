# reals

[![Build status](https://github.com/rubenvannieuwpoort/reals/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/rubenvannieuwpoort/reals/actions)

[![PyPI version](https://badge.fury.io/py/reals.svg)](https://badge.fury.io/py/reals)

A lightweight python3 library for arithmetic with real numbers.

```
from reals import pi, e
from reals.undecidable import correct_digits

# print 1000 digits of e * pi
print(correct_digits(e * pi, 1000))
```