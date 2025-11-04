import json

try:
    import yaml
except Exception:
    yaml = None

from src.io.importers.data_importer import DataImporter


class JsonImporter(DataImporter):
    def _parse(self, text: str):
        obj = json.loads(text)
        return {
            "bank_accounts": list(obj.get("bank_accounts", [])),
            "categories": list(obj.get("categories", [])),
            "operations": list(obj.get("operations", [])),
        }


class YamlImporter(DataImporter):
    def _parse(self, text: str):
        if yaml is None:
            raise RuntimeError("YAML is not installed")
        obj = yaml.safe_load(text) or {}
        return {
            "bank_accounts": list(obj.get("bank_accounts", [])),
            "categories": list(obj.get("categories", [])),
            "operations": list(obj.get("operations", [])),
        }


def get_importer(fmt: str, *args, **kwargs) -> DataImporter:
    fmt = fmt.lower()
    if fmt == "json":
        return JsonImporter(*args, **kwargs)
    if fmt == "yaml" or fmt == "yml":
        return YamlImporter(*args, **kwargs)
    raise ValueError("Неизвестный формат импорта")
