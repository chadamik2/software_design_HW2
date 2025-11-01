from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Optional


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class OperationType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


@dataclass(frozen=True)
class BankAccount:
    id: UUID
    name: str
    balance: float = 0.0


@dataclass(frozen=True)
class Category:
    id: UUID
    type: CategoryType
    name: str


@dataclass(frozen=True)
class Operation:
    id: UUID
    type: OperationType
    bank_account_id: UUID
    amount: float
    date: date
    description: Optional[str]
    category_id: UUID


def new_id():
    return uuid4()
