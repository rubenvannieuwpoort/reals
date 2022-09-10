import reals._term
import reals._utils
import reals._computation
import reals._bihomographic


DEFAULT_MAX_INGESTIONS = 5


class QuadraticComputation(reals._computation.Computation):
    def __init__(self,
                 x: reals._computation.Computation,
                 y: reals._computation.Computation,
                 coeffs: tuple[int, int, int, int, int, int, int, int],
                 max_ingestions=DEFAULT_MAX_INGESTIONS) -> None:
        a, b, c, d, e, f, g, h = coeffs
        self.state = reals._bihomographic.Bihomographic(a, b, c, d, e, f, g, h)
        self.x, self.y = x, y
        self.terminated = False
        self.max_ingestions = max_ingestions

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

    def __next__(self) -> reals._term.Term:
        if self.terminated:
            raise StopIteration()

        assert not (self.state.e == 0 and self.state.f == 0 and
                    self.state.g == 0 and self.state.h == 0)

        ingestions = 0
        while True:
            d00 = self.state.e + self.state.f + self.state.g + self.state.h
            d10 = self.state.e + self.state.f
            d01 = self.state.e + self.state.g
            d11 = self.state.e

            if (ingestions > self.max_ingestions and
                    (d00 != 0 and d10 != 0 and d01 != 0 and d11 != 0)):
                break

            x_ingest = False
            y_ingest = False

            s00 = reals._utils.sign(d00)
            if (d00 != 0 and reals._utils.sign(d01) != s00 or
                    reals._utils.sign(d10) != s00 or reals._utils.sign(d11) != s00):
                x_ingest = True
                y_ingest = True
            else:
                q00 = (self.state.a + self.state.b + self.state.c + self.state.d) // d00
                q11 = self.state.a // d11

                if q00 != q11:
                    x_ingest = True
                    y_ingest = True
                else:
                    q01 = (self.state.a + self.state.c) // d01
                    q10 = (self.state.a + self.state.b) // d10
                    x_ingest = q00 != q10 or q01 != q11
                    y_ingest = q00 != q01 or q10 != q11

            if x_ingest or y_ingest:
                ingestions += 1
                if x_ingest:
                    self.ingest_x()
                if y_ingest:
                    self.ingest_y()
                if self.terminated:
                    raise StopIteration()
                continue

            self.terminated = self.state.emit(q00)
            return q00

        d00 = self.state.e + self.state.f + self.state.g + self.state.h
        q00 = (self.state.a + self.state.b + self.state.c + self.state.d) // d00
        q10 = (self.state.a + self.state.b) // (self.state.e + self.state.f)
        q01 = (self.state.a + self.state.c) // (self.state.e + self.state.g)
        q11 = self.state.a // self.state.e

        n = min(q00, q10, q01, q11)
        m = max(q00, q10, q01, q11) - n + 1
        self.terminated = self.state.emit((n, m))
        return (n, m)
