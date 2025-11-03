from abc import ABC
from typing import List, Dict, Optional

from src.persistence.repositories.abstract_repository import Repository
from src.domain.entities import Operation
from ..dao.operation_dao import OperationDAO


class OperationRepositoryProxy(Repository):
    def __init__(self, dao: OperationDAO):
        self.dao = dao
        self._cache: Dict[str, Operation] = {op.id: op for op in self.dao.list_all()}

    def add(self, obj: Operation) -> None:
        self.dao.insert(obj)
        self._cache[obj.id] = obj

    def update(self, obj: Operation) -> None:
        self.dao.update(obj)
        self._cache[obj.id] = obj

    def delete(self, id: str) -> None:
        self.dao.delete(id)
        self._cache.pop(id, None)

    def get(self, id: str) -> Optional[Operation]:
        return self._cache.get(id, None)

    def list_all(self) -> List[Operation]:
        return list(self._cache.values())

    def list_by_account(self, account_id: str) -> List[Operation]:
        return [o for o in self._cache.values() if o.bank_account_id == account_id]
