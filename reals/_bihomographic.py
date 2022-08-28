from reals._term import Term, expand_term


class Bihomographic:
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int
    g: int
    h: int

    def __init__(self, a: int, b: int, c: int, d: int, e: int, f: int, g: int, h: int) -> None:
        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = a, b, c, d, e, f, g, h

    # replace x by (n + m/x), and bring the resulting expression into biholomorphic form again
    def x_ingest(self, term: Term) -> None:
        n, m = expand_term(term)
        self.a, self.b, self.c, self.d = n * self.a + self.c, n * self.b + self.d, m * self.a, m * self.b
        self.e, self.f, self.g, self.h = n * self.e + self.g, n * self.f + self.h, m * self.e, m * self.f

    def x_ingest_inf(self) -> None:
        self.c, self.d, = self.a, self.b
        self.g, self.h = self.e, self.f

    # replace y by (n + m/y), and bring the resulting expression into biholomorphic form again
    def y_ingest(self, term: Term) -> None:
        n, m = expand_term(term)
        self.a, self.b, self.c, self.d = n * self.a + self.b, m * self.a, n * self.c + self.d, m * self.c
        self.e, self.f, self.g, self.h = n * self.e + self.f, m * self.e, n * self.g + self.h, m * self.g

    def y_ingest_inf(self) -> None:
        self.b, self.d = self.a, self.c
        self.f, self.h = self.e, self.g

    # replace the biholomorphic expression e by m / (e - n)
    def emit(self, term: Term) -> None:
        n, m = expand_term(term)
        self.a, self.b, self.c, self.d = \
            self.a - n * self.e, self.b - n * self.f, self.c - n * self.g, self.d - n * self.h
        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = \
            m * self.e, m * self.f, m * self.g, m * self.h, self.a, self.b, self.c, self.d
