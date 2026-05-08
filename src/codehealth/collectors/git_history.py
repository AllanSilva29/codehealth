from collections import Counter
from pydriller import Repository
from typing import Dict

def collect_file_churn(repo_path: str) -> Dict[str, int]:
    """
    Coleta o churn (número de modificações) por arquivo.
    """
    counter: Counter[str] = Counter()
    
    # Traverse commits para contar modificações
    for commit in Repository(repo_path).traverse_commits():
        for mf in commit.modified_files:
            # Consideramos apenas o caminho novo (ou atual) do arquivo
            path = mf.new_path or mf.old_path
            if path:
                counter[path] += 1
                
    return dict(counter)

def get_total_commits(repo_path: str) -> int:
    """
    Retorna o número total de commits no repositório.
    """
    return len(list(Repository(repo_path).traverse_commits()))
