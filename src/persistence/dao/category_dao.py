from typing import Optional, List

from src.domain.entities import Category, CategoryType
from ..sqlite_db import SQLiteDB


class CategoryDAO:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def insert(self, category: Category) -> None:
        self.db.conn.execute("INSERT INTO categories(id, type, name) VALUES (?, ?, ?)",
                             (category.id, category.type.value, category.name))
        self.db.conn.commit()

    def update(self, category: Category) -> None:
        self.db.conn.execute("UPDATE categories SET type = ?, name = ? WHERE id = ?",
                             (category.type.value, category.name, category.id))
        self.db.conn.commit()

    def delete(self, id: str) -> None:
        self.db.conn.execute("DELETE FROM categories WHERE id = ?", id)
        self.db.conn.commit()

    def get(self, id: str) -> Optional[Category]:
        cur = self.db.conn.execute("SELECT * FROM categories WHERE id = ?", id)
        r = cur.fetchone()
        if r is None:
            return None
        return Category(id=r["id"], type=CategoryType(r["type"]), name=r["name"])

    def list_all(self) -> List[Category]:
        cur = self.db.conn.execute("SELECT * FROM bank_accounts")
        return [Category(id=r["id"], type=CategoryType(r["type"]), name=r["name"]) for r in cur.fetchall()]
