from typing import Dict, List, Any

from src.domain.factory import DomainFactory
from src.services.balance_service import BalanceService
from src.services.bank_account_facade import BankAccountFacade
from src.services.category_facade import CategoryFacade
from src.services.operation_facade import OperationFacade


class DataImporter:
    def __init__(self, accounts: BankAccountFacade, cats: CategoryFacade,
                 ops: OperationFacade,
                 balance: BalanceService, factory: DomainFactory):
        self.accounts = accounts
        self.cats = cats
        self.ops = ops
        self.balance = balance
        self.factory = factory

    def import_data(self, path: str) -> None:
        text = self._read_text(path)
        payload = self._parse(text)
        self._persist(payload)
        self.balance.recalculate_all()

    def _read_text(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        raise NotImplementedError()

    def _persist(self, payload: Dict[str, List[Dict[str, Any]]]) -> None:
        for a in payload.get("bank_accounts", []):
            existing = self.accounts.get(a.get("id"))
            if existing is None:
                self.accounts.create(a["name"], float(a.get("balance", 0.0)), id=a.get("id"))

        for c in payload.get("categories", []):
            existing = self.cats.get(c.get("id"))
            if existing is None:
                self.cats.create(type=c.get("type"), name=c["name"], id=c.get("id"))

        for o in payload.get("operations", []):
            existing = self.ops.get(o.get("id"))
            if existing is None:
                self.ops.create(id=o.get("id"), type=o.get("type"),
                                bank_account_id=o["bank_account_id"],
                                amount=float(o["amount"]), date_value=o["date"],
                                description=o.get("description"), category_id=o["category_id"])
