import sqlite3


class SQLiteDB:
    def __init__(self, path: str):
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._ensure_schema()

    @property
    def conn(self) -> sqlite3.Connection:
        return self._conn

    def _ensure_schema(self) -> None:
        cur = self._conn.cursor()

        self._create_table_bank_accounts(cur)
        self._create_table_categories(cur)
        self._create_table_operations(cur)

        self._conn.commit()

    def _create_table_bank_accounts(self, cur) -> None:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS bank_accounts (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        balance REAL NOT NULL
                    )
                """)

    def _create_table_operations(self, cur) -> None:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                bank_account_id TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                category_id TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id) ON DELETE CASCADE
            )
        """)

    def _create_table_categories(self, cur) -> None:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                name TEXT NOT NULL
            )
        """)


