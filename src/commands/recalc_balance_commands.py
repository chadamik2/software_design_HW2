from typing import Optional

from src.services.balance_service import BalanceService
from src.commands.base_command import Command


class RecalcOneBalanceCommand(Command):
    def __init__(self, acc_id: str, balance_service: BalanceService, new_balance: Optional[float] = None):
        self.acc_id = acc_id
        self.balance_service = balance_service
        self.new_balance = new_balance

    @property
    def name(self) -> str:
        return "recalculate_one_balance"

    def execute(self):
        res = self.balance_service.recalculate_one(self.acc_id, new_balance=self.new_balance)
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
