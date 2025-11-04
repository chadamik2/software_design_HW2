from typing import Optional, List
from datetime import datetime, date

from src.domain.entities import Operation, OperationType
from ..sqlite_db import SQLiteDB


class OperationDAO:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def insert(self, op: Operation) -> None:
        self.db.conn.execute(
            "INSERT INTO operations(id, type, bank_account_id, amount, date, description, category_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (op.id, op.type.value, op.bank_account_id, op.amount, op.date.isoformat(), op.description, op.category_id))
        self.db.conn.commit()

    def update(self, op: Operation) -> None:
        self.db.conn.execute(
            "UPDATE operations SET type = ?, bank_account_id = ?, amount = ?, date = ?, description = ?, category_id = ? WHERE id = ?",
            (op.type.value, op.bank_account_id, op.amount, op.date.isoformat(), op.description, op.category_id, op.id))
        self.db.conn.commit()

    def delete(self, id: str) -> None:
        self.db.conn.execute("DELETE FROM operations WHERE id = ?", id)
        self.db.conn.commit()

    def get(self, id: str) -> Optional[Operation]:
        cur = self.db.conn.execute("SELECT * FROM operations WHERE id = ?", id)
        r = cur.fetchone()
        if r is None:
            return None
        return Operation(id=r["id"], type=OperationType(r["type"]), bank_account_id=r["bank_account_id"],
                         amount=r["amount"],
                         date=date.fromisoformat(r["date"]), description=r["description"], category_id=r["category_id"])

    def list_all(self) -> List[Operation]:
        cur = self.db.conn.execute("SELECT * FROM operations")
        return [Operation(id=r["id"], type=OperationType(r["type"]), bank_account_id=r["bank_account_id"],
                          amount=r["amount"],
                          date=date.fromisoformat(r["date"]), description=r["description"],
                          category_id=r["category_id"]) for r in cur.fetchall()]
