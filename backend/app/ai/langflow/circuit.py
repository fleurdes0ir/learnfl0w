"""Minimal circuit breaker. Standard library only, so it is trivial to unit test."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    """Opens after `failure_threshold` consecutive failures; retries after `reset_seconds`."""

    failure_threshold: int = 3
    reset_seconds: float = 60.0
    clock: Callable[[], float] = time.monotonic
    _failures: int = field(default=0, init=False)
    _opened_at: float | None = field(default=None, init=False)

    @property
    def state(self) -> CircuitState:
        if self._opened_at is None:
            return CircuitState.CLOSED
        if self.clock() - self._opened_at >= self.reset_seconds:
            return CircuitState.HALF_OPEN
        return CircuitState.OPEN

    def allow(self) -> bool:
        """True when a call may be attempted (closed, or half-open trial)."""
        return self.state is not CircuitState.OPEN

    def record_success(self) -> None:
        self._failures = 0
        self._opened_at = None

    def record_failure(self) -> None:
        if self.state is CircuitState.HALF_OPEN:
            self._opened_at = self.clock()  # trial failed: reopen for another window
            return
        self._failures += 1
        if self._failures >= self.failure_threshold:
            self._opened_at = self.clock()
