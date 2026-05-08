from collections import Counter
from pydriller import Repository
from typing import Dict, Set, Tuple

def collect_git_metrics(repo_path: str) -> Tuple[Dict[str, int], Dict[str, Set[str]], Dict[str, Dict[str, float]]]:
    """
    Coleta o churn, contribuidores por arquivo, e a matriz de co-changes.
    """
    churn: Counter[str] = Counter()
    contributors: Dict[str, Set[str]] = {}
    co_changes_raw: Dict[str, Counter[str]] = {}
    
    for commit in Repository(repo_path).traverse_commits():
        valid_files = []
        for mf in commit.modified_files:
            path = mf.new_path or mf.old_path
            if path:
                valid_files.append(path)
        
        # Ignora commits massivos (ex: formatação global)
        if len(valid_files) > 100:
            continue
            
        author = commit.author.name
        
        for path in valid_files:
            churn[path] += 1
            if path not in contributors:
                contributors[path] = set()
            contributors[path].add(author)
            
            if path not in co_changes_raw:
                co_changes_raw[path] = Counter()
            
            for other_path in valid_files:
                if path != other_path:
                    co_changes_raw[path][other_path] += 1
                    
    co_changes_perc: Dict[str, Dict[str, float]] = {}
    for path, co_counter in co_changes_raw.items():
        co_changes_perc[path] = {}
        total_churn = churn[path]
        for other, count in co_counter.items():
            if count >= 3:
                percentage = count / total_churn
                if percentage >= 0.5:
                    co_changes_perc[path][other] = round(percentage, 2)
                
    return dict(churn), contributors, co_changes_perc

def get_total_commits(repo_path: str) -> int:
    """
    Retorna o número total de commits no repositório.
    """
    return len(list(Repository(repo_path).traverse_commits()))
