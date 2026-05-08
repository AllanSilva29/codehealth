from radon.complexity import cc_visit
from typing import List
from ..models import FunctionMetrics

def analyze_complexity(source: str) -> List[FunctionMetrics]:
    """
    Analisa a complexidade ciclomática de cada função/método no arquivo.
    """
    try:
        blocks = cc_visit(source)
        return [
            FunctionMetrics(
                name=block.name,
                lineno=block.lineno,
                complexity=block.complexity
            )
            for block in blocks
        ]
    except Exception:
        # Em caso de erro de parsing (ex: sintaxe inválida)
        return []

def get_cyclomatic_sum(functions: List[FunctionMetrics]) -> int:
    """
    Retorna a soma da complexidade de todas as funções do arquivo.
    """
    return sum(f.complexity for f in functions)
