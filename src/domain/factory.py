import uuid
from typing import Optional, Union
from datetime import datetime, date

from ..domain.entities import BankAccount, Category, CategoryType, OperationType, Operation
from ..domain.exceptions import ValidationError


class DomainFactory:
    @staticmethod
    def _gen_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def _parse_date(value: Union[str, date, datetime]) -> date:
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            return date.fromisoformat(value)
        raise ValidationError("Invalid date")

    def create_bank_account(self, name: str, balance: float = 0.0, id: Optional[str] = None) -> BankAccount:
        name = (name or "").strip()
        if not name:
            raise ValidationError("Name cannot be empty")
        if balance < 0:
            raise ValidationError("Balance cannot be negative")
        return BankAccount(id=id or self._gen_id(), name=name, balance=balance)

    def create_category(self, type: CategoryType, name: str, id: Optional[str] = None) -> Category:
        name = (name or "").strip()
        if not name:
            raise ValidationError("Name cannot be empty")
        return Category(id=id or self._gen_id(), type=type, name=name)

    def create_operation(self, type: OperationType, bank_account_id: str, amount: float,
                         date_value: Union[str, date, datetime], description: Optional[str], category_id: str,
                         id: Optional[str] = None) -> Operation:
        if amount < 0:
            raise ValidationError("Amount cannot be negative")
        dt = self._parse_date(date_value)
        description = (description or "").strip() or None
        return Operation(
            id=id or self._gen_id(),
            type=type,
            bank_account_id=bank_account_id,
            amount=amount,
            date=dt,
            description=description,
            category_id=category_id,
        )
