import json
from typing import Any, Dict, List
from abc import ABC, abstractmethod

try:
    import yaml
except Exception:
    yaml = None

from src.domain.entities import BankAccount, Category, Operation


class DataExportVisitor:
    def visit_bank_account(self, acc: BankAccount) -> Dict[str, Any]:
        return {"id": acc.id, "name": acc.name, "balance": acc.balance}

    def visit_category(self, cat: Category) -> Dict[str, Any]:
        return {"id": cat.id, "type": cat.type.value, "name": cat.name}

    def visit_operation(self, op: Operation) -> Dict[str, Any]:
        return {
            "id": op.id,
            "type": op.type.value,
            "bank_account_id": op.bank_account_id,
            "amount": op.amount,
            "date": op.date.isoformat(),
            "description": op.description,
            "category_id": op.category_id,
        }


class Exporter(ABC):
    @abstractmethod
    def export(self, path: str, accounts: List[BankAccount], cats: List[Category], ops: List[Operation]) -> None: ...


class JsonExporter(Exporter):
    def export(self, path: str, accounts: List[BankAccount], cats: List[Category], ops: List[Operation]) -> None:
        v = DataExportVisitor()
        payload = {
            "bank_accounts": [a.accept(v) for a in accounts],
            "categories": [c.accept(v) for c in cats],
            "operations": [op.accept(v) for op in ops],
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)


class YamlExporter(Exporter):
    def export(self, path: str, accounts: List[BankAccount], cats: List[Category], ops: List[Operation]) -> None:
        if yaml is None:
            raise RuntimeError("PyYAML is not installed")
        v = DataExportVisitor()
        payload = {
            "bank_accounts": [a.accept(v) for a in accounts],
            "categories": [c.accept(v) for c in cats],
            "operations": [op.accept(v) for op in ops],
        }

        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(payload, f, allow_unicode=True, sort_keys=False)


def get_exporter(fmt: str) -> Exporter:
    fmt = fmt.lower()
    if fmt == "json":
        return JsonExporter()
    if fmt == "yaml" or fmt == "yml":
        return YamlExporter()
    raise ValueError("Неизвестный формат экспорта")
