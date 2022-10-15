import reals._term
import reals._utils
import reals._computation
import reals._bihomographic


DEFAULT_MAX_INGESTIONS = 15


class QuadraticComputation(reals._computation.Computation):
    def __init__(self,
                 x: reals._computation.Computation,
                 y: reals._computation.Computation,
                 coeffs: tuple[int, int, int, int, int, int, int, int],
                 max_ingestions=DEFAULT_MAX_INGESTIONS) -> None:
        a, b, c, d, e, f, g, h = coeffs
        self.state = reals._bihomographic.Bihomographic(a, b, c, d, e, f, g, h)
        self.x, self.y = x, y
        self.max_ingestions = max_ingestions
        self.terminated = False
        self.simple_mode = True

    def ingest_x(self) -> None:
        try:
            self.state.x_ingest(next(self.x))
        except StopIteration:
            self.terminated = self.state.x_ingest_inf()

    def ingest_y(self) -> None:
        try:
            self.state.y_ingest(next(self.y))
        except StopIteration:
            self.terminated = self.state.y_ingest_inf()

    def close_enough(self, a: int, b: int) -> bool:
        return (a == b) or (not self.simple_mode) and (a == b + 1 or b == a + 1)

    def __next__(self) -> reals._term.Term:
        if self.terminated:
            raise StopIteration()

        assert not (self.state.e == 0 and self.state.f == 0 and
                    self.state.g == 0 and self.state.h == 0)

        ingestions = 0
        while True:
            self.simple_mode = self.simple_mode and ingestions < self.max_ingestions

            n00 = self.state.a + self.state.b + self.state.c + self.state.d
            d00 = self.state.e + self.state.f + self.state.g + self.state.h
            n10 = self.state.a + self.state.b
            d10 = self.state.e + self.state.f
            n01 = self.state.a + self.state.c
            d01 = self.state.e + self.state.g
            n11 = self.state.a
            d11 = self.state.e

            x_ingest = (d00 == 0 or d10 == 0 or d11 == 0 or
                        reals._utils.sign(d00) != reals._utils.sign(d10) or
                        reals._utils.sign(d01) != reals._utils.sign(d11))
            y_ingest = (d00 == 0 or d01 == 0 or d11 == 0 or
                        reals._utils.sign(d00) != reals._utils.sign(d01) or
                        reals._utils.sign(d10) != reals._utils.sign(d11))

            if not x_ingest and not y_ingest:
                q00 = n00 // d00
                q01 = n01 // d01
                q10 = n10 // d10
                q11 = n11 // d11
                too_far = not self.close_enough(q10, q01)
                x_ingest = too_far or not self.close_enough(q00, q10) or not self.close_enough(q01, q11)
                y_ingest = too_far or not self.close_enough(q00, q01) or not self.close_enough(q10, q11)

            if not x_ingest and not y_ingest:
                if self.simple_mode:
                    self.terminated = self.state.emit(q00)
                    return q00
                else:
                    n = min(q00, q10, q01, q11)
                    m = max(q00, q10, q01, q11) - n + 1
                    if m == 1:
                        self.simple_mode = True
                        self.terminated = self.state.emit(n)
                        return n
                    self.terminated = self.state.emit((n, m))
                    assert not self.terminated
                    return (n, m)

            ingestions += 1
            if x_ingest:
                self.ingest_x()
            if y_ingest:
                self.ingest_y()
            if self.terminated:
                raise StopIteration()
