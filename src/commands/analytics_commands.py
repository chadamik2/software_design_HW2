from typing import Optional
from datetime import date

from src.commands.base_command import Command
from src.commands.input_processing import ask_opt, ask
from src.services.analytics_facade import AnalyticsFacade
from src.services.bank_account_facade import BankAccountFacade


class NetDiffCommand(Command):
    def __init__(self, analytics: AnalyticsFacade):
        self.analytics = analytics

    @property
    def name(self) -> str:
        return "analytics_net_diff"

    def execute(self):
        start = date.fromisoformat(ask_opt("Начало периода (YYYY-MM-DD): "))
        end = date.fromisoformat(ask_opt("Конец периода (YYYY-MM-DD): "))
        val = self.analytics.net_difference(start, end)
        a = start.isoformat() if start else "-"
        b = end.isoformat() if end else "-"
        print(f"Разница (доходы - расходы) за [{a}..{b}]: {val:.2f}")


class GroupByCategoryCommand(Command):
    def __init__(self, analytics: AnalyticsFacade):
        self.analytics = analytics

    @property
    def name(self) -> str:
        return "analytics_group_by_category"

    def execute(self):
        start = date.fromisoformat(ask_opt("Начало периода (YYYY-MM-DD): "))
        end = date.fromisoformat(ask_opt("Конец периода (YYYY-MM-DD): "))
        data = self.analytics.group_by_category(start, end)
        a = start.isoformat() if start else "-"
        b = end.isoformat() if end else "-"
        print(f"Группировка по категориям за [{a}..{b}]:")
        for k, v in data.items():
            print(f"  {k}: {v:.2f}")


class NetDiffForAccountCommand(Command):
    def __init__(self, accounts: BankAccountFacade, analytics: AnalyticsFacade):
        self.accounts = accounts
        self.analytics = analytics

    @property
    def name(self) -> str:
        return "analytics_net_diff_for_account"

    def execute(self):
        acc_id = ask("ID аккаунта: ")
        start = date.fromisoformat(ask_opt("Начало периода (YYYY-MM-DD): "))
        end = date.fromisoformat(ask_opt("Конец периода (YYYY-MM-DD): "))
        val = self.analytics.net_difference_for_account(self.accounts.get(acc_id), start, end)
        a = start.isoformat() if start else "-"
        b = end.isoformat() if end else "-"
        print(f"Разница (доходы - расходы) за [{a}..{b}]: {val:.2f}")
