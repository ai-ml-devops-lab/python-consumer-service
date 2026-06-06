from __future__ import annotations

from collections.abc import Callable, Sequence

NativeMovingAverage = Callable[[Sequence[float], int], list[float]]
native_moving_average: NativeMovingAverage | None

try:
    from portfolio_core import moving_average as native_moving_average
except Exception:  # pragma: no cover - depends on optional native package
    native_moving_average = None


def moving_average(values: Sequence[float], window: int) -> list[float]:
    if native_moving_average is not None:
        return native_moving_average(values, window)
    if window <= 0:
        raise ValueError("window must be greater than zero")
    if len(values) < window:
        return []
    return [
        sum(values[index : index + window]) / window
        for index in range(len(values) - window + 1)
    ]


def implementation() -> str:
    return "native" if native_moving_average is not None else "python-fallback"
