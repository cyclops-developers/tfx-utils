# -*- coding: utf-8 -*-

import pytest
from laguro.skeleton import fib

__author__ = "Danilo Nunes"
__copyright__ = "Danilo Nunes"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
