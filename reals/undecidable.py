from . import Real, Homographic
from typing import Generator


def correct_digits(x: Real, n: int) -> str:
    digit_generator = correct_digits_helper(x)
    digits = str(next(digit_generator))
    try:
        digits += '.'
        for _ in range(n):
            digits += str(next(digit_generator))
    except StopIteration:
        return digits
    return digits


def correct_digits_helper(xf: Real) -> Generator[int, None, None]:
    h = Homographic((1, 0, 0, 1))
    terminated = False
    x = xf.start_computation()

    assert not(h.c == 0 and h.d == 0)

    while not (h.c == 0 and h.d == 0):
        if h.c != 0 and h.c + h.d != 0:
            n1 = h.a // h.c
            n2 = (h.a + h.b) // (h.c + h.d)
            if n1 == n2:
                digit = n1
                h.emit_digit(digit)
                yield digit
                continue

        # if not(terminated):
        assert not(terminated)
        try:
            h.ingest(next(x))
        except StopIteration:
            h.ingest_inf()
            terminated = True
