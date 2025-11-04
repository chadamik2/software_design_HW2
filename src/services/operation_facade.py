from dataclasses import replace
from typing import List

from src.domain.entities import *
from src.domain.exceptions import NotFoundError, ValidationError
from src.domain.factory import DomainFactory
from src.persistence.repositories.bank_account_repository_proxy import BankAccountRepositoryProxy
from src.persistence.repositories.category_repository_proxy import CategoryRepositoryProxy
from src.persistence.repositories.operation_repository_proxy import OperationRepositoryProxy


class OperationFacade:
    def __init__(self,
                 ops: OperationRepositoryProxy,
                 accounts: BankAccountRepositoryProxy,
                 categories: CategoryRepositoryProxy,
                 factory: DomainFactory) -> None:
        self.ops = ops
        self.accounts = accounts
        self.categories = categories
        self.factory = factory

    def _apply_account_effect(self, account_id: str, type: OperationType, amount: float) -> None:
        acc = self.accounts.get(account_id)
        if acc is None:
            raise NotFoundError("The banl account does not exist")
        delta = amount if type == OperationType.INCOME else -amount
        new = replace(acc, balance=acc.balance + delta)
        self.accounts.update(new)

    def _reverse_account_effect(self, account_id: str, type: OperationType, amount: float) -> None:
        self._apply_account_effect(account_id,
                                   OperationType.EXPENSE if type == OperationType.INCOME else OperationType.INCOME,
                                   amount)

    def _check_category_and_account(self, bank_account_id: str, category_id: str, type: OperationType) -> None:
        acc = self.accounts.get(bank_account_id)
        if not acc:
            raise NotFoundError("The bank account does not exist")
        cat = self.categories.get(category_id)
        if not cat:
            raise NotFoundError("The category does not exist")
        if (type == OperationType.INCOME and cat.type != CategoryType.INCOME) or (
                type == OperationType.EXPENSE and cat.type != CategoryType.EXPENSE):
            raise ValidationError("The type of operation does not match the type of category")

    def create(self, type: OperationType, bank_account_id: str, amount: float, date_value, description: Optional[str],
               category_id: str, id: Optional[str] = None) -> Operation:
        self._check_category_and_account(bank_account_id, category_id, type)
        op = self.factory.create_operation(type=type, amount=amount, bank_account_id=bank_account_id,
                                           date_value=date_value, description=description,
                                           category_id=category_id, id=id)
        self.ops.add(op)
        self._apply_account_effect(account_id=bank_account_id, type=type, amount=amount)
        return op

    def update(self, operation_id: str, *, new_type=None, new_bank_account_id=None, new_amount=None, new_date=None,
               new_description=None, new_category_id=None) -> Operation:
        old = self.ops.get(operation_id)
        if not old:
            raise NotFoundError("The operation does not exist")

        type_v = new_type or old.type
        account_id_v = new_bank_account_id or old.bank_account_id
        amount_v = new_amount or old.amount
        date_v = new_date or old.date
        descr_v = new_description or old.description
        category_id_v = new_category_id or old.category_id

        if amount_v < 0:
            raise ValidationError("The amount cannot be negative")

        self._check_category_and_account(bank_account_id=account_id_v, category_id=category_id_v, type=type_v)

        self._reverse_account_effect(account_id=old.bank_account_id, type=old.type, amount=old.amount)
        new = replace(old, type=type_v, bank_account_id=account_id_v, amount=amount_v, date=date_v, description=descr_v,
                      category_id=category_id_v)
        self.ops.update(new)
        self._apply_account_effect(account_id=account_id_v, type=type_v, amount=amount_v)
        return new

    def delete(self, operation_id: str) -> None:
        op = self.ops.get(operation_id)
        if not op:
            raise NotFoundError("The operation does not exist")
        self._reverse_account_effect(account_id=op.bank_account_id, type=op.type, amount=op.amount)
        self.ops.delete(operation_id)

    def list(self) -> List[Operation]:
        return self.ops.list_all()

    def get(self, operation_id: str) -> Operation:
        return self.ops.get(operation_id)
