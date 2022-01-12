from pytest import raises
from unittest.mock import call
from py_unittest_tools import asserts
import numpy as np


def test_assert_call_lists_equals():
    asserts.assert_call_lists_equals([], [])
    asserts.assert_call_lists_equals([
        call(1, 2, 3, a=123),
        call().A(1, 2, 3)
    ], [
        call(1, 2, 3, a='123'),
        call().A(1, 2, 3)
    ])

    with raises(AssertionError):
        asserts.assert_call_lists_equals([call()], [])

    with raises(AssertionError):
        asserts.assert_call_lists_equals([call(1)], [call(2)])

    with raises(AssertionError):
        asserts.assert_call_lists_equals([call(1)], [call(1, 2)])


def test_assert_values_equal():
    asserts.assert_values_equal(1, 1)
    asserts.assert_values_equal(1, '1')
    asserts.assert_values_equal([1], np.array([1]))

    with raises(AssertionError):
        asserts.assert_values_equal('1', 1)

    with raises(AssertionError):
        asserts.assert_values_equal(1, 2)

    with raises(AssertionError):
        asserts.assert_values_equal([1], np.array([2]))
        asserts.assert_values_equal([1], np.array([1, 2]))

