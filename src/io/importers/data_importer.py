from typing import Dict, List, Any

from src.domain.factory import DomainFactory
from src.persistence.repositories.bank_account_repository_proxy import BankAccountRepositoryProxy
from src.persistence.repositories.category_repository_proxy import CategoryRepositoryProxy
from src.persistence.repositories.operation_repository_proxy import OperationRepositoryProxy
from src.services.balance_service import BalanceService


class DataImporter:
    def __init__(self, accounts: BankAccountRepositoryProxy, cats: CategoryRepositoryProxy,
                 ops: OperationRepositoryProxy,
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
            try:
                acc = self.factory.create_bank_account(a["name"], float(a.get("balance", 0.0)), id=a.get("id"))
                existing = self.accounts.get(a.get("id"))
                if existing is None:
                    self.accounts.add(acc)
            except Exception:
                continue

        for c in payload.get("categories", []):
            try:
                cat = self.factory.create_category(type=c.get("type"), name=c["name"], id=c.get("id"))
                existing = self.cats.get(c.get("id"))
                if existing is None:
                    self.cats.add(cat)
            except Exception:
                continue

        for o in payload.get("operations", []):
            try:
                existing = self.ops.get(o.get("id"))
                if existing is None:
                    self.factory.create_operation(id=o.get("id"), type=o.get("type"),
                                                  bank_account_id=o["bank_account_id"],
                                                  amount=float(o["amount"]), date_value=o["date"],
                                                  description=o.get("description"), category_id=o["category_id"])
            except Exception:
                continue
