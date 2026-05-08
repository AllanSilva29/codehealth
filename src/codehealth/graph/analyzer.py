from typing import Dict, List, Set, Tuple, Any
import os

class DependencyGraph:
    def __init__(self):
        self.adj: Dict[str, List[str]] = {}
        self.reverse_adj: Dict[str, List[str]] = {}
        self.nodes: Set[str] = set()

    def add_edge(self, u: str, v: str):
        self.nodes.add(u)
        self.nodes.add(v)
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.reverse_adj:
            self.reverse_adj[v] = []
            
        # Evitar arestas duplicadas
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.reverse_adj[v]:
            self.reverse_adj[v].append(u)

    def get_fan_in(self, node: str) -> int:
        return len(self.reverse_adj.get(node, []))

    def find_scc(self) -> List[List[str]]:
        """
        Tarjan's algorithm for Strongly Connected Components.
        Returns a list of SCCs. A cycle exists if an SCC has > 1 node.
        """
        index = 0
        indices: Dict[str, int] = {}
        lowlink: Dict[str, int] = {}
        on_stack: Dict[str, bool] = {}
        stack: List[str] = []
        sccs: List[List[str]] = []

        def strongconnect(v: str):
            nonlocal index
            indices[v] = index
            lowlink[v] = index
            index += 1
            stack.append(v)
            on_stack[v] = True

            for w in self.adj.get(v, []):
                if w not in indices:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif on_stack.get(w, False):
                    lowlink[v] = min(lowlink[v], indices[w])

            if lowlink[v] == indices[v]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == v:
                        break
                sccs.append(scc)

        for node in self.nodes:
            if node not in indices:
                strongconnect(node)

        return sccs

def extract_module_parts(path: str) -> Set[str]:
    """Extrai possíveis nomes de módulo de um caminho de arquivo."""
    path = path.replace("\\", "/")
    if path.endswith(".py"):
        path = path[:-3]
    if path.endswith("/__init__"):
        path = path[:-9]
    parts = path.split("/")
    # Se path for src/codehealth/models, pode ser codehealth.models, codehealth, models
    possibilities = set()
    for i in range(len(parts)):
        possibilities.add(".".join(parts[i:]))
    return possibilities

def build_project_graph(files: Dict[str, Any]) -> Tuple[Dict[str, int], Set[str]]:
    """
    Constrói o grafo de dependências entre os arquivos do projeto.
    Retorna o (fan_in por arquivo, arquivos que estão em ciclos).
    """
    graph = DependencyGraph()
    path_modules = {}
    
    # Mapeamento prévio
    for path in files.keys():
        graph.nodes.add(path)
        path_modules[path] = extract_module_parts(path)
        
    for path, metrics in files.items():
        for imp in metrics.imports:
            # Tentar achar a qual arquivo este import se refere
            for target_path, modules in path_modules.items():
                if target_path == path:
                    continue
                # Se o import for algo como 'codehealth.models' e bater com as possibilidades
                if imp in modules:
                    graph.add_edge(path, target_path)

    # Calcular fan_in
    fan_in_map = {}
    for path in files.keys():
        fan_in_map[path] = graph.get_fan_in(path)
        
    # Encontrar ciclos
    in_cycles = set()
    sccs = graph.find_scc()
    for scc in sccs:
        if len(scc) > 1:
            for node in scc:
                in_cycles.add(node)
                
    return fan_in_map, in_cycles
