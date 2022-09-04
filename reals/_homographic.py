import reals._term

from typing import Optional


class Homographic:
    a: int
    b: int
    c: int
    d: int

    def __init__(self, a: int, b: int, c: int, d: int) -> None:
        self.a, self.b, self.c, self.d = a, b, c, d

    # replace x by (n + m/x), and bring the resulting expression into homographic form again
    def ingest(self, term: reals._term.Term) -> None:
        n, m = reals._term.expand_term(term)
        self.a, self.b = n * self.a + self.b, m * self.a
        self.c, self.d = n * self.c + self.d, m * self.c

    def ingest_inf(self) -> bool:
        self.b, self.d = self.a, self.c
        return self.c == 0 and self.d == 0

    def emit(self, term: reals._term.Term) -> bool:
        n, m = reals._term.expand_term(term)
        self.a, self.b = self.a - n * self.c, self.b - n * self.d
        terminated = self.a == 0 and self.b == 0
        self.a, self.b, self.c, self.d = m * self.c, m * self.d, self.a, self.b
        return terminated

    # returns an integer n such that self.evaluate(n) = n or self.evaluate(n) = n + 1
    def fix_point(self) -> Optional[int]:
        current_guess = self.guess_int()

        if not current_guess:
            return None

        while True:
            value = self.evaluate_int(current_guess)
            assert value
            next_guess = (current_guess + value) // 2

            if next_guess == current_guess or next_guess == current_guess + 1:
                return current_guess

            current_guess = next_guess

    # evaluate the homographic form at an integer and floor the result
    # returns None if the denominator is zero when evaluated at n
    def evaluate_int(self, n: int) -> Optional[int]:
        denominator = self.c * n + self.d
        if denominator == 0:
            return None
        return (self.a * n + self.b) // denominator

    # returns an integer that makes the denominator positive, or None if it's impossible
    # (this happens when denominator is of form 0x + n for some nonpositive n)
    def guess_int(self) -> Optional[int]:
        if self.c == 0:
            if self.d <= 0:
                return None
            return 0

        if self.c > 0:
            return max(-self.d // self.c + 1, 0)
        else:
            assert self.c < 0
            return min(-(self.d // self.c) - 1, 0)
