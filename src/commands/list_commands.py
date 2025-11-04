from src.commands.command import Command
from src.services.bank_account_facade import BankAccountFacade
from src.services.category_facade import CategoryFacade
from src.services.operation_facade import OperationFacade


class ListAccountsCommand(Command):
    def __init__(self, facade: BankAccountFacade):
        self.facade = facade

    @property
    def name(self) -> str:
        return "list_accounts"

    def execute(self):
        for acc in self.facade.list():
            print(f"{acc.id} | {acc.name} | {acc.balance}")


class ListCategoriesCommand(Command):
    def __init__(self, facade: CategoryFacade):
        self.facade = facade

    @property
    def name(self) -> str:
        return "list_categories"

    def execute(self):
        for c in self.facade.list():
            print(f"{c.id} | {c.type.value} | {c.name}")


class ListOperationsCommand(Command):
    def __init__(self, facade: OperationFacade):
        self.facade = facade

    @property
    def name(self):
        return "list_operations"

    def execute(self):
        for o in self.facade.list():
            print(
                f"{o.id} | {o.type.value} | {o.amount} | {o.date.isoformat()} | acc={o.bank_account_id} | cat={o.category_id} | {o.description or ''}")
