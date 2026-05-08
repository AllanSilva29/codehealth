import ast
from typing import Set

def analyze_dependencies(source: str) -> Set[str]:
    """
    Extrai os módulos importados em um arquivo Python.
    """
    imports = set()
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
    except Exception:
        pass
        
    return imports

def get_fan_out(imports: Set[str]) -> int:
    """
    Retorna o número de dependências únicas (fan-out).
    """
    return len(imports)
