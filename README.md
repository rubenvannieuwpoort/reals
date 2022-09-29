<img src="media/logo.png" alt="reals logo" width="250px"/>

A lightweight python3 library for arithmetic with real numbers.

[![Build status](https://github.com/rubenvannieuwpoort/reals/actions/workflows/verify-on-push.yml/badge.svg?branch=master)](https://github.com/rubenvannieuwpoort/reals/actions) [![PyPI version](https://badge.fury.io/py/reals.svg)](https://pypi.org/project/reals/)


# What is Reals?

'Reals' is a lightweight Python library for arbitrary precision arithmetic. It allows you to compute approximations to an arbitrary degree of precision, and, contrary to most other libraries, *guarantees that all digits it displays are correct*. It works by using [interval arithmetic](https://en.wikipedia.org/wiki/Interval_arithmetic) and [continued fractions](https://en.wikipedia.org/wiki/Continued_fraction). The bulk of this code is based on [Bill Gosper's notes on continued fractions](https://perl.plover.com/classes/cftalk/INFO/gosper.txt) in which he presents algorithms for doing arithmetic on continued fractions.

The reals library is characterized by:
- Correctness; the reals library uses interval arithmetic to ensure that all the digits are correct.
- Calculations are done in a streaming way; the result of previous calculations can be re-used.
- Uses no external libraries.
- Focus on usability.


# Installation

The recommended way of installing is using `pip`:

```
pip install reals
```


# Why use Reals?

With Reals, it is easy to get the result of a numerical calculation: The digits of your results are *correct*, rather than only an approximation like in most other arbitrary-precision libraries.

For example, consider that we want to evaluate the first 10 digits of the expression
$$100000 \cdot (22873 \cdot e - 19791 \cdot \pi)$$

In native Python, we can do
```
$ python
>>> from math import pi, e
>>> print('{:.10f}'.format(100000 * (22873 * e - 19791 * pi)))
5.5148142565
```

However, we might suspect that there would be some floating-point error that crept in this result (and we would be right). So, we `pip install mpmath` and try again:

```
$ pip install mpmath
$ python
>>> from mpmath import pi, e
>>> 100000 * (22873 * e - 19791 * pi)
mpf('5.5148149840533733')
```

Now, it is not clear how much of these digits are correct. On the other hand, using the `reals` library we do
```
$ pip install reals
$ python
>>> from reals import pi, e
>>> print('{:.10f}'.format(100000 * (22873 * e - 19791 * pi)))
5.5148143686
```

And get only correct digits (note that the last digit might be rounded up). You don't have to take my word from it, you can check the result on [Wolfram Alpha](https://www.wolframalpha.com/input?i=100000+*+%2822873+*+e+-+19791+*+pi%29).


# Why *not* use Reals?

The feature set of Reals is still a bit limited. Certain functions are not mature yet and their implementation should still be made more robust and optimized.


# Quick start guide

It is easiest to import any function or number that you need from the reals package:

```
>>> from reals import sqrt
```

Now, you're ready to go:
```
>>> sqrt2 = sqrt(2)
>>> sqrt2
<reals._real.Real object at 0x10d182560 (approximate value: 1.41421)>
```

If you want to see more digits, there are multiple options. Let's say we want 10 digits. Then any of the following would work:
```
>>> sqrt2.evaluate(10)
'1.4142135624'
>>> '{:.10f}'.format(sqrt2)
'1.4142135624'
>>> sqrt2.to_decimal(10)
Decimal('1.4142135624')
```

Currently, the following constants and functions are supported and exported in the `reals` package:
- Constants: `pi`, `e`, `phi`
- Functions: `sqrt` (only for integers and rationals), `exp` (still very slow)
- Operators: negation, addition, subtraction, multiplication, division
- Trigonometric functions: `sin`, `sinh`, `csc`, `csch`, `cos`, `cosh`, `sec`, `sech`, `tan`, `tanh`, `cot`, `coth`


# Development status

The library is in pre-1.0 version at the moment. This means it is still under development and can not be considered stable yet.

Next steps are:
- Implement `sqrt` for non-rationals
- Implement `exp` in a faster and more stable way
- Implement `log`
- Implement exponentiation of real numbers (e.g. `x**y` where `x` and `y` are real numbers)


## Examples

Print [10000 digits](https://www.math.utah.edu/~pa/math/e.html) of Euler's number $e$:
```
from reals import e

print('{:.10000f}'.format(e))
```

Comparing the first 20 digits of `reals.pi` and `math.pi`:
```
from math import pi as math_pi
from reals import pi as real_pi

print('{:.20f}'.format(math_pi))
print('{:.20f}'.format(real_pi))
```


Get the first [10 best rational approximations](https://www.johndcook.com/blog/2018/05/22/best-approximations-for-pi/) to $\pi$:
```
from reals import pi
from reals.approximation import best_rational_approximations

print(best_rational_approximations(pi, 10))
```


Print the floating point number that is closest to $\frac{\pi}{e}$:
```
from reals import pi, e
from reals.approximation import Approximation

print(Approximation(pi / e).closest_float())
```


Print a rational approximation of $e^\pi$ that has an error of less than $10^{-20}$ (again this can be checked with [Wolfram Alpha](https://www.wolframalpha.com/input?i=231604552633%2F10008540207-e%5Epi)):
```
from reals import pi, exp
from reals.approximation import Approximation

from fractions import Fraction


epsilon = Fraction(1, 10**20)

approximation = Approximation(exp(pi))
approximation.improve_epsilon(epsilon)

print(approximation.as_fraction())
```


Calculate a rational interval smaller than $10^{-10}$ that contains $\pi^2 - e^2$:
```
from reals import pi, e
from reals.approximation import Approximation

from fractions import Fraction


epsilon = Fraction(1, 10**10)

approximation = Approximation(pi * pi - e * e)
approximation.improve_epsilon(epsilon)

lower_bound, upper_bound = approximation.interval_fraction()
assert upper_bound - lower_bound < epsilon

print(lower_bound, upper_bound)
```


> Continued fractions are not only perfectly amenable to arithmetic, they are
amenable to perfect arithmetic.

 -- Bill Gosper