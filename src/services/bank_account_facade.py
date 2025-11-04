from dataclasses import replace
from typing import Optional, List

from src.domain.entities import BankAccount
from src.domain.exceptions import NotFoundError, ValidationError
from src.domain.factory import DomainFactory
from src.persistence.repositories.bank_account_repository_proxy import BankAccountRepositoryProxy


class BankAccountFacade:
    def __init__(self, repo: BankAccountRepositoryProxy, factory: DomainFactory):
        self.repo = repo
        self.factory = factory

    def create(self, name: str, balance: float = 0.0) -> BankAccount:
        acc = self.factory.create_bank_account(name, balance)
        self.repo.add(acc)
        return acc

    def rename(self, acc_id: str, new_name: str) -> BankAccount:
        acc = self.repo.get(acc_id)
        if not acc:
            raise NotFoundError("The bank account does not exist")
        new = replace(acc, name=new_name.strip())
        self.repo.update(new)
        return new

    def set_balance(self, account_id, new_balance: float) -> BankAccount:
        if new_balance < 0:
            raise ValidationError("The new balance cannot be negative")
        acc = self.repo.get(account_id)
        if not acc:
            raise NotFoundError("The bank account does not exist")
        new = replace(acc, balance=new_balance)
        self.repo.update(new)
        return new

    def delete(self, account_id: str) -> None:
        self.repo.delete(account_id)

    def get(self, account_id: str) -> Optional[BankAccount]:
        return self.repo.get(account_id)

    def list(self) -> List[BankAccount]:
        return self.repo.list_all()
