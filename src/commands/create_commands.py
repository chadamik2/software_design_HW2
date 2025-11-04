from src.commands.base_command import Command
from src.domain.entities import CategoryType, Operation, OperationType
from src.services.bank_account_facade import BankAccountFacade
from src.services.category_facade import CategoryFacade
from src.services.operation_facade import OperationFacade


class CreateAccountCommand(Command):
    def __init__(self, facade: BankAccountFacade, name: str, balance: float = 0.0):
        self.facade = facade
        self._name = name
        self._balance = balance

    @property
    def name(self) -> str:
        return "create_account"

    def execute(self):
        acc = self.facade.create(self._name, self._balance)
        print(f"Coздан счёт: {acc.id} | {acc.name} | {acc.balance}")


class CreateCategoryCommand(Command):
    def __init__(self, facade: CategoryFacade, type: CategoryType, name: str):
        self.facade = facade
        self._type = type
        self._name = name

    @property
    def name(self) -> str:
        return "create_category"

    def execute(self):
        c = self.facade.create(self._type, self._name)
        print(f"Создана категория: {c.id} | {c.type.value} | {c.name}")


class CreateOperationCommand(Command):
    def __init__(self, facade: OperationFacade, type: OperationType, bank_account_id: str, amount: float,
                 date_value: str, description: str, category_id: str):
        self.facade = facade
        self._type = type
        self._bank_account_id = bank_account_id
        self._amount = amount
        self._date_value = date_value
        self._description = description
        self._category_id = category_id

    @property
    def name(self) -> str:
        return "create_operation"

    def execute(self):
        op = self.facade.create(self._t, self._bank_account_id, self._amount, self._date_value, self._description,
                                self._category_id)
        print(
            f"Создана операция: {op.id} | {op.type.value} | {op.amount:.2f} | {op.date.isoformat()} | acc={op.bank_account_id} | cat={op.category_id}")
