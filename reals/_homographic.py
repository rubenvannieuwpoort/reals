class Homographic:
    a: int
    b: int
    c: int
    d: int

    def __init__(self, a: int, b: int, c: int, d: int) -> None:
        self.a, self.b, self.c, self.d = a, b, c, d

    # replace x by (n + m/x), and bring the resulting expression into holomorphic form again
    def ingest(self, term: tuple[int, int]) -> None:
        n, m = term
        self.a, self.b = n * self.a + self.b, m * self.a
        self.c, self.d = n * self.c + self.d, m * self.c

    def ingest_inf(self):
        self.b, self.d = self.a, self.c

    def emit(self, term: tuple[int, int]) -> bool:
        n, m = term
        self.a, self.b = self.a - n * self.c, self.b - n * self.d
        terminated = self.a == 0 and self.b == 0
        self.a, self.b, self.c, self.d = m * self.c, m * self.d, self.a, self.b
        return terminated
