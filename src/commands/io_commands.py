from src.commands.base_command import Command
from src.commands.input_processing import ask

from src.domain.factory import DomainFactory
from src.services.balance_service import BalanceService
from src.io.importers.concrete_importers import get_importer
from src.io.exporters.exporters import get_exporter
from src.services.bank_account_facade import BankAccountFacade
from src.services.category_facade import CategoryFacade
from src.services.operation_facade import OperationFacade


class ImportCommand(Command):
    def __init__(self, accounts: BankAccountFacade, cats: CategoryFacade,
                 ops: OperationFacade,
                 balance: BalanceService, factory: DomainFactory):
        self.accounts = accounts
        self.cats = cats
        self.ops = ops
        self.balance = balance
        self.factory = factory

    @property
    def name(self) -> str:
        return "import_data"

    def execute(self):
        fmt = ask("Формат (json/yaml): ").lower()
        path = ask("Путь к файлу: ")
        importer = get_importer(fmt, self.accounts, self.cats, self.ops, self.balance, self.factory)
        importer.import_data(path)
        print("Импорт выполнен")


class ExportCommand(Command):
    def __init__(self, accounts: BankAccountFacade, cats: CategoryFacade,
                 ops: OperationFacade):
        self.accounts = accounts
        self.cats = cats
        self.ops = ops

    @property
    def name(self) -> str:
        return "export_data"

    def execute(self):
        fmt = ask("Формат (json/yaml): ").lower()
        path = ask("Путь к файлу: ")
        exporter = get_exporter(fmt)
        exporter.export(path, self.accounts.list(), self.cats.list(), self.ops.list())
        print(f"Экспорт выполнен")
