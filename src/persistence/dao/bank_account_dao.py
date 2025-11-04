from typing import Optional, List

from src.domain.entities import BankAccount
from ..sqlite_db import SQLiteDB


class BankAccountDAO:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def insert(self, account: BankAccount) -> None:
        self.db.conn.execute("INSERT INTO bank_accounts(id, name, balance) VALUES (?, ?, ?)",
                             (account.id, account.name, account.balance))
        self.db.conn.commit()

    def update(self, account: BankAccount) -> None:
        self.db.conn.execute("UPDATE bank_accounts SET name = ?, balance = ? WHERE id = ?",
                             (account.name, account.balance, account.id))
        self.db.conn.commit()

    def delete(self, id_: str) -> None:
        self.db.conn.execute("DELETE FROM bank_accounts WHERE id = ?", id_)
        self.db.conn.commit()

    def get(self, id_: str) -> Optional[BankAccount]:
        cur = self.db.conn.execute("SELECT * FROM bank_accounts WHERE id = ?", id_)
        r = cur.fetchone()
        if r is None:
            return None
        return BankAccount(id=r["id"], name=r["name"], balance=r["balance"])

    def list_all(self) -> List[BankAccount]:
        cur = self.db.conn.execute("SELECT * FROM bank_accounts")
        return [BankAccount(id=r["id"], name=r["name"], balance=r["balance"]) for r in cur.fetchall()]
