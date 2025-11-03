from typing import Dict, List, Optional

from src.domain.entities import Category
from src.persistence.dao.category_dao import CategoryDAO
from src.persistence.repositories.abstract_repository import Repository


class CategoryRepositoryProxy(Repository[Category]):
    def __init__(self, dao: CategoryDAO):
        self.dao = dao
        self._cache: Dict[str, Category] = {c.id: c for c in self.dao.list_all()}

    def add(self, category: Category) -> None:
        self.dao.insert(category)
        self._cache[category.id] = category

    def update(self, category: Category) -> None:
        self.dao.update(category)
        self._cache[category.id] = category

    def delete(self, id: str) -> None:
        self.dao.delete(id)
        self._cache.pop(id, None)

    def get(self, id: str) -> Optional[Category]:
        return self._cache.get(id, None)

    def list_all(self) -> List[Category]:
        return list(self._cache.values())
