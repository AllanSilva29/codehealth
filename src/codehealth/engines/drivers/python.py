import os
from typing import List, Dict, Set, Any
from ..base import BaseEngine
from ...models import FileMetrics, FunctionMetrics
from ...collectors.source_loader import list_files, is_generated_code, is_migration_code, is_test_code
from ...analyzers.complexity import analyze_complexity, get_cyclomatic_sum
from ...analyzers.dependencies import analyze_dependencies, get_fan_out
from ...analyzers.classifier import classify_architectural_roles, get_role_name

class PythonEngine(BaseEngine):
    def list_files(self, repo_path: str) -> List[str]:
        return list_files(repo_path, extension=".py")

    def analyze_source(self, rel_path: str, source: str) -> Dict[str, Any]:
        functions = analyze_complexity(source)
        imports = analyze_dependencies(source)
        return {
            "functions": functions,
            "imports": imports,
            "cyclomatic_sum": get_cyclomatic_sum(functions),
            "fan_out": get_fan_out(imports)
        }

    def classify_roles(self, files: Dict[str, FileMetrics]):
        classify_architectural_roles(files)

    def get_role_name(self, metrics: FileMetrics) -> str:
        return get_role_name(metrics)

    def is_test_code(self, rel_path: str) -> bool:
        return is_test_code(rel_path)

    def is_migration_code(self, rel_path: str, source: str) -> bool:
        return is_migration_code(rel_path, source)

    def is_generated_code(self, source: str) -> bool:
        return is_generated_code(source)
