from typing import Any, List
from unittest.mock import call
import re
import numpy as np


def assert_call_lists_equals(calls: List, expected_calls: List):
    """
        Asserts wether two call lists are equal or not. The call arguments can be optionally converted to str before comparison.
    """

    if len(calls) != len(expected_calls):
        print("Expected Calls:\n    -", "\n    -".join(map(str, expected_calls)))
        print("Actual    Calls:\n    -", "\n    -".join(map(str, calls)))

    assert len(calls) == len(expected_calls), "Expected {} calls, got {}.".format(len(expected_calls), len(calls))

    for i, (call, expected_call) in enumerate(zip(calls, expected_calls)):
        try:
            assert call[0] == expected_call[0], "Expected callable to be {}, got {}".format(
                expected_call[0], call[0]
            )
            assert len(call.args) == len(expected_call.args), "Expected {} positional arguments, got {}.".format(
                len(expected_call.args), len(call.args)
            )
            assert len(call.kwargs) == len(expected_call.kwargs), "Expected {} keyword arguments, got {}.".format(
                len(expected_call.kwargs), len(call.kwargs)
            )

            for call_arg, expected_call_arg in zip(call.args, expected_call.args):
                assert_values_equal(call_arg, expected_call_arg)

            assert set(call.kwargs.keys()) == set(expected_call.kwargs.keys())

            for key, expected_call_arg in expected_call.kwargs.items():
                assert_values_equal(call.kwargs[key], expected_call_arg)
        except AssertionError:
            print(f"Expected Call #{i}: ", str(expected_call))
            print(f"Actual    Call #{i}: ", str(call))
            raise


def assert_values_equal(actual: Any, expected: Any):
    """
        Asserts wether two values are equal or not. The values can be optionally converted to str before comparison.
    """
    eq_type = 'equal'
    if isinstance(expected, str):
        eq_type = 'string_equal'
        actual = re.sub("0x[0-9a-fA-F]", "0xF", str(actual))
    elif isinstance(actual, np.ndarray) or isinstance(expected, np.ndarray):
        eq_type = 'numpy_equal'
        eq = np.all(np.isclose(actual, expected))

        if not eq:
            print("Expected:", expected)
            print("Actual   :", actual)

        assert eq, "Expected {} to {} {}".format(expected, eq_type, actual)
        return

    if actual != expected:
        print("Expected:", expected)
        print("Actual   :", actual)

    assert actual == expected, "Expected {} to {} {}".format(expected, eq_type, actual)
