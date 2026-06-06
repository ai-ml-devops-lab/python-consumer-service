from __future__ import annotations

from consumer_service import core_adapter


def test_moving_average_fallback():
    # ensure fallback implementation works for a simple case
    core_adapter.native_core = None
    result = core_adapter.moving_average([1, 2, 3, 4], 2)
    assert result == [1.5, 2.5, 3.5]


def test_moving_average_window_too_large():
    core_adapter.native_core = None
    result = core_adapter.moving_average([1, 2], 3)
    assert result == []


def test_implementation_string():
    # when native_core is None
    core_adapter.native_core = None
    assert core_adapter.implementation() == "python-fallback"

    # simulate native implementation presence
    class Dummy:
        def moving_average(self, values, window):
            return [42]

    core_adapter.native_core = Dummy()
    assert core_adapter.implementation() == "native"
