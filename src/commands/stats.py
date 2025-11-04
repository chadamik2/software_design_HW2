from typing import List, Tuple, Dict
from time import time


class StatsRegistry:
    def __init__(self):
        self._items: List[Tuple[float, str, float]] = []

    def add(self, name: str, duration: float):
        self._items.append((time(), name, duration))

    def all(self) -> List[Tuple[float, str, float]]:
        return list(self._items)

    def summary_by_name(self) -> Dict[str, Dict[str, float]]:
        res: Dict[str, Dict[str, float]] = {}
        for _, name, duration in self._items:
            agg = res.setdefault(name, {"count": 0, "total": 0.0, "avg": 0.0})
            agg["count"] += 1
            agg["total"] += duration

        for name, agg in res.items():
            if agg["count"]:
                agg["avg"] = agg["total"] / agg["count"]
        return res
