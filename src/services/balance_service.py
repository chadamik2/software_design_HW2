from dataclasses import replace
from typing import Optional

from src.persistence.repositories.bank_account_repository_proxy import BankAccountRepositoryProxy
from src.persistence.repositories.operation_repository_proxy import OperationRepositoryProxy
from src.domain.entities import OperationType


class BalanceService:
    def __init__(self, ops: OperationRepositoryProxy, accounts: BankAccountRepositoryProxy):
        self.ops = ops
        self.accounts = accounts

    def recalculate_all(self) -> None:
        computed = {}
        for acc in self.accounts.list_all():
            computed[acc.id] = 0.0

        for op in self.ops.list_all():
            delta = op.amount if op.type == OperationType.INCOME else -op.amount
            computed[op.bank_account_id] = computed.get(op.bank_account_id, 0) + delta

        for acc in self.accounts.list_all():
            comp = computed.get(acc.id, 0)
            self.accounts.update(replace(acc, balance=comp))

    def recalculate_one(self, acc_id: str, new_balance: Optional[float]) -> float:
        acc = self.accounts.get(acc_id)

        if new_balance is None:
            new_balance = 0.0

            for op in self.ops.list_all():
                if op.bank_account_id == acc.id:
                    new_balance += op.amount if op.type == OperationType.INCOME else -op.amount

        self.accounts.update(replace(acc, balance=new_balance))
        return new_balance
