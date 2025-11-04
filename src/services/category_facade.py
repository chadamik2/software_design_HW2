from dataclasses import replace
from typing import List, Optional

from src.domain.exceptions import NotFoundError
from src.persistence.repositories.category_repository_proxy import CategoryRepositoryProxy
from src.domain.entities import Category, CategoryType
from src.domain.factory import DomainFactory


class CategoryFacade:
    def __init__(self, repo: CategoryRepositoryProxy, factory: DomainFactory):
        self.repo = repo
        self.factory = factory

    def create(self, type_: CategoryType, name: str, id: Optional[str] = None) -> Category:
        cat = self.factory.create_category(type_=type_, name=name, id_=id)
        self.repo.add(cat)
        return cat

    def rename(self, cat_id: str, new_name: str) -> Category:
        cat = self.repo.get(cat_id)
        if not cat:
            raise NotFoundError("The category does not exist")
        new = replace(cat, name=new_name.strip())
        self.repo.update(new)
        return new

    def retag(self, category_id: str, new_type: CategoryType) -> Category:
        cat = self.repo.get(category_id)
        if not cat:
            raise NotFoundError("The category does not exist")
        new = replace(cat, type=new_type)
        self.repo.update(new)
        return new

    def delete(self, cat_id: str) -> None:
        self.repo.delete(cat_id)

    def list(self) -> List[Category]:
        return self.repo.list_all()

    def get(self, cat_id: str) -> Optional[Category]:
        return self.repo.get(cat_id)
