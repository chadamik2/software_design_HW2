from src.commands.input_processing import ask, ask_float
from src.services.balance_service import BalanceService
from src.commands.base_command import Command


class RecalcOneBalanceCommand(Command):
    def __init__(self, balance_service: BalanceService, auto_fix: bool = True):
        self.auto_fix = auto_fix
        self.balance_service = balance_service

    @property
    def name(self) -> str:
        return "recalculate_one_balance"

    def execute(self):
        acc_id = ask("ID аккаунта: ")
        new_balance = 0.0
        if not self.auto_fix:
            new_balance: float = ask_float("Новый баланс: ")
        res = self.balance_service.recalculate_one(acc_id, new_balance=new_balance)
        print(f"Новый баланс: {res}")


class RecalcAllBalanceCommand(Command):
    def __init__(self, balance_service: BalanceService):
        self.balance_service = balance_service

    @property
    def name(self) -> str:
        return "recalculate_all_balance"

    def execute(self):
        self.balance_service.recalculate_all()
        print("Баланс успешно пересчитан")
