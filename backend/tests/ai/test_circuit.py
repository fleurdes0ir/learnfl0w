from app.ai.langflow.circuit import CircuitBreaker, CircuitState


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def make(threshold: int = 3, reset: float = 60.0) -> tuple[CircuitBreaker, FakeClock]:
    clock = FakeClock()
    return CircuitBreaker(failure_threshold=threshold, reset_seconds=reset, clock=clock), clock


def test_starts_closed_and_allows_calls() -> None:
    breaker, _ = make()
    assert breaker.state is CircuitState.CLOSED
    assert breaker.allow()


def test_opens_after_consecutive_failures() -> None:
    breaker, _ = make(threshold=3)
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.state is CircuitState.CLOSED
    breaker.record_failure()
    assert breaker.state is CircuitState.OPEN
    assert not breaker.allow()


def test_success_resets_failure_count() -> None:
    breaker, _ = make(threshold=3)
    breaker.record_failure()
    breaker.record_failure()
    breaker.record_success()
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.state is CircuitState.CLOSED


def test_half_open_after_reset_window_then_closes_on_success() -> None:
    breaker, clock = make(threshold=1, reset=60)
    breaker.record_failure()
    assert breaker.state is CircuitState.OPEN
    clock.now = 59.9
    assert breaker.state is CircuitState.OPEN
    clock.now = 60.0
    assert breaker.state is CircuitState.HALF_OPEN
    assert breaker.allow()
    breaker.record_success()
    assert breaker.state is CircuitState.CLOSED


def test_failed_trial_reopens_for_another_window() -> None:
    breaker, clock = make(threshold=1, reset=60)
    breaker.record_failure()
    clock.now = 61.0
    assert breaker.state is CircuitState.HALF_OPEN
    breaker.record_failure()
    assert breaker.state is CircuitState.OPEN
    clock.now = 100.0
    assert breaker.state is CircuitState.OPEN
    clock.now = 121.0
    assert breaker.state is CircuitState.HALF_OPEN
