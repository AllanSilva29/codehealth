from dataclasses import dataclass, field
from typing import Dict, List, Set

@dataclass
class FunctionMetrics:
    name: str
    lineno: int
    complexity: int

@dataclass
class FileMetrics:
    path: str
    churn: int = 0
    loc: int = 0
    fan_out: int = 0
    cyclomatic_sum: int = 0
    functions: List[FunctionMetrics] = field(default_factory=list)
    imports: Set[str] = field(default_factory=set)
    cycles: int = 0
    is_generated: bool = False
    severity: str = "Low"  # Low, Medium, High, Critical
    cochange_score: float = 0.0
    cohesion_score: float = 0.0
    hotspot_score: float = 0.0
    notes: List[str] = field(default_factory=list)

@dataclass
class RepositoryReport:
    files: Dict[str, FileMetrics] = field(default_factory=dict)
    total_commits: int = 0
    avg_complexity: float = 0.0
