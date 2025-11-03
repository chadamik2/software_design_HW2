from typing import Optional, List, Dict

from src.domain.entities import BankAccount
from src.persistence.dao.bank_account_dao import BankAccountDAO
from ..repositories.abstract_repository import Repository


class BankAccountRepositoryProxy(Repository[BankAccount]):
    def __init__(self, dao: BankAccountDAO):
        self.dao = dao
        self._cache: Dict[str, BankAccount] = {a.id: a for a in self.dao.list_all()}

    def add(self, obj: BankAccount):
        self.dao.insert(obj)
        self._cache[obj.id] = obj

    def update(self, obj: BankAccount):
        self.dao.update(obj)
        self._cache[obj.id] = obj

    def delete(self, id: str):
        self.dao.delete(id)
        self._cache.pop(id, None)

    def get(self, id: str) -> Optional[BankAccount]:
        obj = self._cache.get(id)
        return obj

    def list_all(self) -> List[BankAccount]:
        return list(self._cache.values())
