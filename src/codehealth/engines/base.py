from abc import ABC, abstractmethod
from typing import List, Dict, Set, Any
from ..models import FileMetrics

class BaseEngine(ABC):
    @abstractmethod
    def list_files(self, repo_path: str) -> List[str]:
        """Lista arquivos relevantes para este tipo de projeto."""
        pass

    @abstractmethod
    def analyze_source(self, rel_path: str, source: str) -> Dict[str, Any]:
        """
        Executa análises estáticas (complexidade, dependências) 
        específicas para a linguagem.
        """
        pass

    @abstractmethod
    def classify_roles(self, files: Dict[str, FileMetrics]):
        """Classifica os papéis arquiteturais dos arquivos."""
        pass

    @abstractmethod
    def get_role_name(self, metrics: FileMetrics) -> str:
        """Retorna o nome amigável do papel arquitetural."""
        pass

    @abstractmethod
    def is_test_code(self, rel_path: str) -> bool:
        pass

    @abstractmethod
    def is_migration_code(self, rel_path: str, source: str) -> bool:
        pass

    @abstractmethod
    def is_generated_code(self, source: str) -> bool:
        pass
