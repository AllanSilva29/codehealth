from typing import Dict, List, Set

class TarjanSCC:
    """
    Implementa o algoritmo de Tarjan para encontrar Componentes Fortemente Conexos (SCCs).
    Utilizado para detecção de ciclos em grafos de dependência.
    """
    def __init__(self, adj: Dict[str, List[str]], nodes: Set[str]):
        self.adj = adj
        self.nodes = nodes
        self.index = 0
        self.indices: Dict[str, int] = {}
        self.lowlink: Dict[str, int] = {}
        self.on_stack: Dict[str, bool] = {}
        self.stack: List[str] = []
        self.sccs: List[List[str]] = []

    def find_sccs(self) -> List[List[str]]:
        for node in self.nodes:
            if node not in self.indices:
                self._strongconnect(node)
        return self.sccs

    def _strongconnect(self, v: str):
        self.indices[v] = self.index
        self.lowlink[v] = self.index
        self.index += 1
        self.stack.append(v)
        self.on_stack[v] = True

        for w in self.adj.get(v, []):
            if w not in self.indices:
                self._strongconnect(w)
                self.lowlink[v] = min(self.lowlink[v], self.lowlink[w])
            elif self.on_stack.get(w, False):
                self.lowlink[v] = min(self.lowlink[v], self.indices[w])

        if self.lowlink[v] == self.indices[v]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            self.sccs.append(scc)
