from reals._real import Real, CachedComputation


def test_real_cache_is_shared() -> None:
    x = Real([1, 2, 3, 4, 5])

    c1 = x.compute()
    assert isinstance(c1, CachedComputation)

    c2 = x.compute()
    assert isinstance(c2, CachedComputation)

    next(c1)
    next(c1)
    next(c1)

    next(c2)

    assert x.cache == [1, 2, 3]
    assert c1.cache == [1, 2, 3]
    assert c2.cache == [1, 2, 3]

    assert c1.index == 3
    assert c2.index == 1
