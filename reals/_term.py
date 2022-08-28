from typing import Union

Term = Union[int, tuple[int, int]]


def expand_term(term: Term) -> tuple[int, int]:
    if isinstance(term, tuple):
        return term
    return (term, 1)
