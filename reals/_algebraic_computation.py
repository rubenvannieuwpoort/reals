import reals._term
import reals._utils
import reals._computation
import reals._homographic

DEFAULT_MAX_INGESTIONS = 15


class AlgebraicComputation(reals._computation.Computation):
    def __init__(
            self,
            x: reals._computation.Computation,
            coeffs: tuple[int, int, int, int],
            max_ingestions=DEFAULT_MAX_INGESTIONS) -> None:
        a, b, c, d = coeffs
        self.state = reals._homographic.Homographic(a, b, c, d)
        self.x = x
        self.max_ingestions = max_ingestions
        self.terminated = False
        self.simple_mode = True

    def ingest_x(self) -> None:
        try:
            self.state.ingest(next(self.x))
        except StopIteration:
            self.terminated = self.state.ingest_inf()

    def __next__(self) -> reals._term.Term:
        if self.terminated:
            raise StopIteration()

        assert not (self.state.c == 0 and self.state.d == 0)

        ingestions = 0
        while True:
            self.simple_mode = self.simple_mode and ingestions <= self.max_ingestions

            if (self.state.c != 0 and
                    reals._utils.sign(self.state.c) == reals._utils.sign(self.state.c + self.state.d)):
                n1 = self.state.a // self.state.c
                n2 = (self.state.a + self.state.b) // (self.state.c + self.state.d)

                if n1 == n2:
                    self.simple_mode = True
                    self.terminated = self.state.emit(n1)
                    return n1
                elif (not self.simple_mode) and (n1 == n2 + 1 or n1 + 1 == n2):
                    n = min(n1, n2)
                    m = max(n1, n2) - n + 1
                    assert m != 1
                    self.terminated = self.state.emit((n, m))
                    assert not self.terminated
                    return (n, m)

            self.ingest_x()
            if self.terminated:
                raise StopIteration()

            ingestions += 1
