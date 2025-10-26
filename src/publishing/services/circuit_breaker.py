import time
from typing import Callable, Any


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_time_sec: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failures = 0
        self.opened_at = 0.0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.is_open():
            raise RuntimeError("Circuit is open; skipping call")
        try:
            result = func(*args, **kwargs)
            self.reset()
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.opened_at = time.time()
            raise

    def is_open(self) -> bool:
        if self.opened_at == 0.0:
            return False
        if time.time() - self.opened_at >= self.recovery_time_sec:
            # half-open state; allow a trial call
            self.reset()
            return False
        return True

    def reset(self) -> None:
        self.failures = 0
        self.opened_at = 0.0
