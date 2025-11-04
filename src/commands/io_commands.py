from src.commands.base_command import Command

from src.domain.factory import DomainFactory
from src.persistence.repositories.bank_account_repository_proxy import BankAccountRepositoryProxy
from src.persistence.repositories.category_repository_proxy import CategoryRepositoryProxy
from src.persistence.repositories.operation_repository_proxy import OperationRepositoryProxy
from src.services.balance_service import BalanceService
from src.io.importers.concrete_importers import get_importer
from src.io.exporters.exporters import get_exporter


class ImportCommand(Command):
    def __init__(self, importer_fmt: str, accounts: BankAccountRepositoryProxy, cats: CategoryRepositoryProxy,
                 ops: OperationRepositoryProxy,
                 balance: BalanceService, factory: DomainFactory, path: str):
        self.importer_fmt = importer_fmt
        self.accounts = accounts
        self.cats = cats
        self.ops = ops
        self.balance = balance
        self.factory = factory
        self.path = path

    @property
    def name(self) -> str:
        return "import_data"

    def execute(self):
        importer = get_importer(self.importer_fmt, self.accounts, self.cats, self.ops, self.balance, self.factory)
        importer.import_data(self.path)
        print("Импорт выполнен")


class ExportCommand(Command):
    def __init__(self, exporter_fmt: str, accounts: BankAccountRepositoryProxy, cats: CategoryRepositoryProxy,
                 ops: OperationRepositoryProxy, path: str):
        self.fmt = exporter_fmt
        self.accounts = accounts
        self.cats = cats
        self.ops = ops
        self.path = path

    @property
    def name(self) -> str:
        return "export_data"

    def execute(self):
        exporter = get_exporter(self.fmt)
        exporter.export(self.path, self.accounts.list_all(), self.cats.list_all(), self.ops.list_all())
        print(f"Экспорт выполнен")
