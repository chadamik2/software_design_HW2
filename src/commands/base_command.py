from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any

from .stats import StatsRegistry


class Command(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def execute(self) -> Any: ...


class TimedCommandDecorator(Command):
    def __init__(self, inner: Command, stats: StatsRegistry):
        self._inner = inner
        self._stats = stats

    @property
    def name(self) -> str:
        return self._inner.name

    def execute(self) -> Any:
        start = perf_counter()
        try:
            self._inner.execute()
        finally:
            duration = perf_counter() - start
            self._stats.add(self._inner.name, duration)
