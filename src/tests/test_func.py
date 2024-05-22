import pytest
from meterviewer import func as F


def test_must_loop():
    def func(x):
        assert x == 1

    class LoopError(Exception):
        pass

    F.must_loop([1, 1, 1], func, LoopError)

    assert pytest.raises(LoopError, F.must_loop, [], func, LoopError)
