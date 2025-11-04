from typing import Optional, Dict
from datetime import date

from src.persistence.repositories.category_repository_proxy import CategoryRepositoryProxy
from src.persistence.repositories.operation_repository_proxy import OperationRepositoryProxy
from src.domain.entities import Operation, OperationType, BankAccount


class AnalyticsFacade:
    def __init__(self, ops: OperationRepositoryProxy, cats: CategoryRepositoryProxy):
        self.ops = ops
        self.cats = cats

    def _in_period(self, op: Operation, start: Optional[date], end: Optional[date]) -> bool:
        if start and op.date < start:
            return False
        if end and op.date > end:
            return False
        return True

    def net_difference(self, start: Optional[date], end: Optional[date]) -> float:
        total = 0.0
        for op in self.ops.list_all():
            if not self._in_period(op, start, end):
                continue
            if op.type == OperationType.INCOME:
                total += op.amount
            else:
                total -= op.amount
        return total

    def group_by_category(self, start: Optional[date], end: Optional[date]) -> Dict[str, float]:
        res: Dict[str, float] = {}
        categories = {c.id: c for c in self.cats.list_all()}
        for op in self.ops.list_all():
            if not self._in_period(op, start, end):
                continue
            name = categories.get(op.category_id).name if op.category_id in categories else None
            if name:
                sign = 1.0 if op.type == OperationType.INCOME else -1.0
                res[name] = res.get(name, 0.0) + sign * op.amount
        return res

    def net_difference_for_account(self, acc: BankAccount, start: Optional[date], end: Optional[date]) -> float:
        total = 0.0
        for op in self.ops.list_all():
            if not op.bank_account_id != acc.id or self._in_period(op, start, end):
                continue
            if op.type == OperationType.INCOME:
                total += op.amount
            else:
                total -= op.amount
        return total
