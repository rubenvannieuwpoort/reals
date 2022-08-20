from reals._computation import Computation
from reals._homographic import Homographic
from reals._utils import sign


DEFAULT_MAX_INGESTIONS = 15


class AlgebraicComputation(Computation):
    def __init__(
            self,
            x: Computation,
            coeffs: tuple[int, int, int, int],
            max_ingestions=DEFAULT_MAX_INGESTIONS) -> None:
        a, b, c, d = coeffs
        self.state = Homographic(a, b, c, d)
        self.x = x
        self.max_ingestions = max_ingestions
        self.terminated = False

    def ingest_x(self) -> None:
        try:
            self.state.ingest(next(self.x))
        except StopIteration:
            self.state.ingest_inf()

    def __next__(self) -> tuple[int, int]:
        if self.terminated:
            raise StopIteration()

        assert not (self.state.c == 0 and self.state.d == 0)

        ingestions = 0
        while ingestions < self.max_ingestions:
            if self.state.c != 0 and sign(self.state.c) == sign(self.state.c + self.state.d):
                n1 = self.state.a // self.state.c
                n2 = (self.state.a + self.state.b) // (self.state.c + self.state.d)

                if n1 == n2:
                    self.terminated = self.state.emit((n1, 1))
                    return (n1, 1)

            self.ingest_x()
            ingestions += 1

        n = min(n1, n2)
        m = max(n1, n1) - n + 1
        self.terminated = self.state.emit((n, m))
        return (n, m)
