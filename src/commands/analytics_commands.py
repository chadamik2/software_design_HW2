from typing import Optional
from datetime import date

from src.commands.base_command import Command
from src.services.analytics_facade import AnalyticsFacade
from src.services.bank_account_facade import BankAccountFacade


class NetDiffCommand(Command):
    def __init__(self, analytics: AnalyticsFacade, start: Optional[str], end: Optional[str]):
        self.analytics = analytics
        self.start = date.fromisoformat(start) if start else None
        self.end = date.fromisoformat(end) if end else None

    @property
    def name(self) -> str:
        return "analytics_net_diff"

    def execute(self):
        val = self.analytics.net_difference(self.start, self.end)
        a = self.start.isoformat() if self.start else "-"
        b = self.end.isoformat() if self.end else "-"
        print(f"Разница (доходы - расходы) за [{a}..{b}]: {val:.2f}")


class GroupByCategoryCommand(Command):
    def __init__(self, analytics: AnalyticsFacade, start: Optional[str], end: Optional[str]):
        self.analytics = analytics
        self.start = date.fromisoformat(start) if start else None
        self.end = date.fromisoformat(end) if end else None

    @property
    def name(self) -> str:
        return "analytics_group_by_category"

    def execute(self):
        data = self.analytics.group_by_category(self.start, self.end)
        a = self.start.isoformat() if self.start else "-"
        b = self.end.isoformat() if self.end else "-"
        print(f"Группировка по категориям за [{a}..{b}]:")
        for k, v in data.items():
            print(f"  {k}: {v:.2f}")


class NetDiffForAccountCommand(Command):
    def __init__(self, accounts: BankAccountFacade, analytics: AnalyticsFacade, acc_id: str, start: Optional[str],
                 end: Optional[str]):
        self.accounts = accounts
        self.analytics = analytics
        self.acc_id = acc_id
        self.start = date.fromisoformat(start) if start else None
        self.end = date.fromisoformat(end) if end else None

    @property
    def name(self) -> str:
        return "analytics_net_diff_for_account"

    def execute(self):
        val = self.analytics.net_difference_for_account(self.accounts.get(self.acc_id), self.start, self.end)
        a = self.start.isoformat() if self.start else "-"
        b = self.end.isoformat() if self.end else "-"
        print(f"Разница (доходы - расходы) за [{a}..{b}]: {val:.2f}")
