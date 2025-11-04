from src.commands.base_command import Command
from src.commands.input_processing import ask, ask_float, ask_opt
from src.domain.entities import CategoryType, OperationType
from src.services.bank_account_facade import BankAccountFacade
from src.services.category_facade import CategoryFacade
from src.services.operation_facade import OperationFacade


class CreateAccountCommand(Command):
    def __init__(self, facade: BankAccountFacade):
        self.facade = facade

    @property
    def name(self) -> str:
        return "create_account"

    def execute(self):
        name = ask("Название счета: ")
        bal = ask_float("Начальный баланс: ")
        acc = self.facade.create(name, bal)
        print(f"Coздан счёт: {acc.id} | {acc.name} | {acc.balance}")


class CreateCategoryCommand(Command):
    def __init__(self, facade: CategoryFacade):
        self.facade = facade

    @property
    def name(self) -> str:
        return "create_category"

    def execute(self):
        t = ask("Тип (income/expense): ").lower()
        ctype = CategoryType(t)
        name = ask("Название категории: ")
        c = self.facade.create(ctype, name)
        print(f"Создана категория: {c.id} | {c.type.value} | {c.name}")


class CreateOperationCommand(Command):
    def __init__(self, facade: OperationFacade):
        self.facade = facade

    @property
    def name(self) -> str:
        return "create_operation"

    def execute(self):
        t = OperationType(ask("Тип операции (income/expense): ").lower())
        acc_id = ask("ID счета: ")
        amt = ask_float("Сумма (>0): ")
        dt = ask("Дата (YYYY-MM-DD): ")
        descr = ask_opt("Описание (опционально): ")
        cat_id = ask("ID категории: ")
        op = self.facade.create(t, acc_id, amt, dt, descr,
                                cat_id)
        print(
            f"Создана операция: {op.id} | {op.type.value} | {op.amount:.2f} | {op.date.isoformat()} | acc={op.bank_account_id} | cat={op.category_id}")
