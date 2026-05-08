import json
from dataclasses import asdict
from typing import Any
from ..models import RepositoryReport

class SetEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

def emit_json(report: RepositoryReport, output_path: str):
    """
    Exporta o relatório consolidado para um arquivo JSON.
    """
    data = asdict(report)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, cls=SetEncoder, ensure_ascii=False)
