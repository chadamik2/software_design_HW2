from src.cli.di import Container
from src.commands.analytics_commands import NetDiffCommand, GroupByCategoryCommand, NetDiffForAccountCommand
from src.commands.create_commands import CreateAccountCommand, CreateCategoryCommand, CreateOperationCommand
from src.commands.io_commands import ExportCommand, ImportCommand
from src.commands.list_commands import ListAccountsCommand, ListCategoriesCommand, ListOperationsCommand
from src.commands.recalc_balance_commands import RecalcAllBalanceCommand, RecalcOneBalanceCommand
from src.commands.show_stats_commands import ShowStatsCommand
from src.commands.stats import StatsRegistry
from src.domain.exceptions import DomainError
from src.domain.factory import DomainFactory
from src.persistence.dao.bank_account_dao import BankAccountDAO
from src.persistence.dao.category_dao import CategoryDAO
from src.persistence.dao.operation_dao import OperationDAO
from src.persistence.repositories.bank_account_repository_proxy import BankAccountRepositoryProxy
from src.persistence.repositories.category_repository_proxy import CategoryRepositoryProxy
from src.persistence.repositories.operation_repository_proxy import OperationRepositoryProxy
from src.persistence.sqlite_db import SQLiteDB
from src.services.analytics_facade import AnalyticsFacade
from src.services.balance_service import BalanceService
from src.services.bank_account_facade import BankAccountFacade
from src.services.category_facade import CategoryFacade
from src.services.operation_facade import OperationFacade
from src.commands.base_command import TimedCommandDecorator


def build_container(db_path: str = "finance.db") -> Container:
    c = Container()
    db = SQLiteDB(db_path)
    c.register_singleton("db", db)
    acc_dao = BankAccountDAO(db)
    cat_dao = CategoryDAO(db)
    op_dao = OperationDAO(db)
    acc_repo = BankAccountRepositoryProxy(acc_dao)
    cat_repo = CategoryRepositoryProxy(cat_dao)
    op_repo = OperationRepositoryProxy(op_dao)
    factory = DomainFactory()
    acc_facade = BankAccountFacade(acc_repo, factory)
    cat_facade = CategoryFacade(cat_repo, factory)
    op_facade = OperationFacade(op_repo, acc_repo, cat_repo, factory)
    analytics = AnalyticsFacade(op_repo, cat_repo)
    balance = BalanceService(op_repo, acc_repo)
    stats = StatsRegistry()
    c.register_singleton("factory", factory)
    c.register_singleton("acc_facade", acc_facade)
    c.register_singleton("cat_facade", cat_facade)
    c.register_singleton("op_facade", op_facade)
    c.register_singleton("analytics", analytics)
    c.register_singleton("balance", balance)
    c.register_singleton("stats", stats)
    return c


def run_cli_main() -> None:
    c = build_container()
    factory: DomainFactory = c.resolve("factory")
    accounts: BankAccountFacade = c.resolve("acc_facade")
    cats: CategoryFacade = c.resolve("cat_facade")
    ops: OperationFacade = c.resolve("op_facade")
    analytics: AnalyticsFacade = c.resolve("analytics")
    balance: BalanceService = c.resolve("balance")
    stats: StatsRegistry = c.resolve("stats")

    menu = """
[1] Создать счет
[2] Список счетов
[3] Создать категорию
[4] Список категорий
[5] Создать операцию
[6] Список операций
[7] Аналитика: разница за период
[8] Аналитика: разница за период для аккаунта
[9] Аналитика: по категориям за период
[10] Экспорт данных (json/yaml)
[11] Импорт данных (json/yaml)
[12] Пересчитать балансы (автоматически)
[13] Пересчитать баланс аккаунта вручную
[14] Пересчитать баланс аккаунта автоматически
[15] Показать статистику сценариев
[0] Выход
> """

    while True:
        try:
            print("\n=== ВШЭ БАНК ===")
            choice = input(menu).strip()
            if choice == "0":
                print("До свидания")
                return
            elif choice == "1":
                cmd = TimedCommandDecorator(CreateAccountCommand(accounts), stats)
                cmd.execute()
            elif choice == "2":
                cmd = TimedCommandDecorator(ListAccountsCommand(accounts), stats)
                cmd.execute()
            elif choice == "3":
                cmd = TimedCommandDecorator(CreateCategoryCommand(cats), stats)
                cmd.execute()
            elif choice == "4":
                cmd = TimedCommandDecorator(ListCategoriesCommand(cats), stats)
                cmd.execute()
            elif choice == "5":
                cmd = TimedCommandDecorator(CreateOperationCommand(ops), stats)
                cmd.execute()
            elif choice == "6":
                cmd = TimedCommandDecorator(ListOperationsCommand(ops), stats)
                cmd.execute()
            elif choice == "7":
                cmd = TimedCommandDecorator(NetDiffCommand(analytics), stats)
                cmd.execute()
            elif choice == "8":
                cmd = TimedCommandDecorator(
                    NetDiffForAccountCommand(accounts, analytics), stats)
                cmd.execute()
            elif choice == "9":
                cmd = TimedCommandDecorator(GroupByCategoryCommand(analytics), stats)
                cmd.execute()
            elif choice == "10":
                cmd = TimedCommandDecorator(ExportCommand(accounts, cats, ops), stats)
                cmd.execute()
            elif choice == "11":
                cmd = TimedCommandDecorator(ImportCommand(accounts, cats, ops, balance, factory), stats)
                cmd.execute()
            elif choice == "12":
                cmd = TimedCommandDecorator(RecalcAllBalanceCommand(balance), stats)
                cmd.execute()
            elif choice == "13":
                cdm = TimedCommandDecorator(RecalcOneBalanceCommand(balance, auto_fix=False), stats)
                cdm.execute()
            elif choice == "14":
                cdm = TimedCommandDecorator(RecalcOneBalanceCommand(balance), stats)
                cdm.execute()
            elif choice == "15":
                cmd = ShowStatsCommand(stats)
                cmd.execute()
            else:
                print("Неизвестная команда")
        except DomainError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
        _pause()


def _pause(text="\nНажмите Enter для продолжения..."):
    input(text)
