from uuid import UUID
from datetime import date
from typing import Optional

from ..entities import (Operation, OperationType,
                        BankAccount, Category, new_id, CategoryType)

class OperationFactory:
    def create(self, *, type_: OperationType,
               bank_account_id: UUID, amount:float, op_date: date,
            description: Optional[str], category_id: UUID) -> Operation:
        if amount < 0:
            raise ValueError("Money cannot be negative")
        if type_ not in OperationType.__members__:
            raise ValueError("Operation type must be one of {}".format(OperationType.__members__))
        return Operation(id=new_id(),
                         type=type_,
                         bank_account_id=bank_account_id,
                         amount=amount,
                         description=description,
                         category_id=category_id,
                        date=op_date,)

class CategoryFactory:
    def create(self, *, type_: CategoryType, name: str) -> Category:
        if type_ not in CategoryType.__members__:
            raise ValueError("Category type must be one of {}".format(CategoryType.__members__))
        return Category(id=new_id(), type=type_, name=name)

class BankAccountFactory:
    def create(self, *, name: str, balance: float = 0.0) -> BankAccount:
        return BankAccount(id=new_id(), name=name, balance=balance)