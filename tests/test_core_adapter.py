from __future__ import annotations

from collections.abc import Sequence

import pytest

from consumer_service import core_adapter


def test_moving_average_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    # ensure fallback implementation works for a simple case
    monkeypatch.setattr(core_adapter, "native_moving_average", None)
    result = core_adapter.moving_average([1, 2, 3, 4], 2)
    assert result == [1.5, 2.5, 3.5]


def test_moving_average_window_too_large(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(core_adapter, "native_moving_average", None)
    result = core_adapter.moving_average([1, 2], 3)
    assert result == []


def test_implementation_string(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(core_adapter, "native_moving_average", None)
    assert core_adapter.implementation() == "python-fallback"

    def dummy_moving_average(values: Sequence[float], window: int) -> list[float]:
        return [42.0]

    monkeypatch.setattr(core_adapter, "native_moving_average", dummy_moving_average)
    assert core_adapter.implementation() == "native"
