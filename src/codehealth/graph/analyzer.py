from typing import Dict, List, Set, Tuple, Any
from .tarjan import TarjanSCC

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
            
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.reverse_adj[v]:
            self.reverse_adj[v].append(u)

    def get_fan_in(self, node: str) -> int:
        return len(self.reverse_adj.get(node, []))

    def find_scc(self) -> List[List[str]]:
        tarjan = TarjanSCC(self.adj, self.nodes)
        return tarjan.find_sccs()

def extract_module_parts(path: str) -> Set[str]:
    path = path.replace("\\", "/")
    if path.endswith(".py"):
        path = path[:-3]
    if path.endswith("/__init__"):
        path = path[:-9]
    parts = path.split("/")
    possibilities = set()
    for i in range(len(parts)):
        possibilities.add(".".join(parts[i:]))
    return possibilities

def build_project_graph(files: Dict[str, Any]) -> Tuple[Dict[str, int], Set[str]]:
    graph = DependencyGraph()
    path_modules = _map_file_modules(files, graph)
    _build_graph_edges(graph, files, path_modules)
    
    fan_in_map = _calculate_fan_in(graph, files)
    in_cycles = _find_cyclic_nodes(graph)
    
    return fan_in_map, in_cycles

def _map_file_modules(files: Dict[str, Any], graph: DependencyGraph) -> Dict[str, Set[str]]:
    path_modules = {}
    for path in files.keys():
        graph.nodes.add(path)
        path_modules[path] = extract_module_parts(path)
    return path_modules

def _build_graph_edges(graph: DependencyGraph, files: Dict[str, Any], path_modules: Dict[str, Set[str]]):
    for path, metrics in files.items():
        for imp in metrics.imports:
            for target_path, modules in path_modules.items():
                if target_path == path:
                    continue
                if imp in modules:
                    graph.add_edge(path, target_path)

def _calculate_fan_in(graph: DependencyGraph, files: Dict[str, Any]) -> Dict[str, int]:
    return {path: graph.get_fan_in(path) for path in files.keys()}

def _find_cyclic_nodes(graph: DependencyGraph) -> Set[str]:
    in_cycles = set()
    for scc in graph.find_scc():
        if len(scc) > 1:
            for node in scc:
                in_cycles.add(node)
    return in_cycles
