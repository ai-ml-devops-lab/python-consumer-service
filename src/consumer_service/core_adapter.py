from __future__ import annotations

from collections.abc import Sequence

try:
    import portfolio_core as native_core  # type: ignore
except Exception:  # pragma: no cover - depends on optional native package
    native_core = None


def moving_average(values: Sequence[float], window: int) -> list[float]:
    if native_core is not None:
        return list(native_core.moving_average(list(values), window))
    if window <= 0:
        raise ValueError("window must be greater than zero")
    if len(values) < window:
        return []
    return [sum(values[index : index + window]) / window for index in range(len(values) - window + 1)]


def implementation() -> str:
    return "native" if native_core is not None else "python-fallback"
