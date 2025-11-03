from typing import Protocol, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import date


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class OperationType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass(frozen=True)
class BankAccount:
    id: str
    name: str
    balance: float = 0.0

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_bank_account(self)


@dataclass(frozen=True)
class Category:
    id: str
    type: CategoryType
    name: str

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_category(self)


@dataclass(frozen=True)
class Operation:
    id: str
    type: OperationType
    bank_account_id: str
    amount: float
    date: date
    description: Optional[str]
    category_id: str

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_operation(self)


class Visitor(Protocol):
    def visit_bank_account(self, account: BankAccount) -> Any: ...

    def visit_category(self, category: Category) -> Any: ...

    def visit_operation(self, operation: Operation) -> Any: ...
