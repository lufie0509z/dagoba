class Dagoba:
    def __init__(self, nodes = None, edges = None):
        self._nodes = []
        self._edges = []
        self._nodes_by_id = {}
        for node in (nodes or []):
            self.add_node(node)
        for edge in (edges or []):
            self.add_edge(edge)
            

    def add_node(self, node):
        pk = node.get('_id', None)
        print(pk)
        if pk in self._nodes_by_id:
            raise ValueError(f'node with _id = {pk} already exists.')
        node = node.copy()
        self._nodes.append(node)
        self._nodes_by_id[pk] = node
    
    def add_edge(self, edge):
        in_id = edge.get('_in', None)
        out_id = edge.get("_out", None)
        if (in_id not in self._nodes_by_id or out_id not in self._nodes_by_id):
            raise ValueError(f'Invalid edge: edge({in_id}, {out_id}) not exists.')
        self._edges.append(edge.copy())
    
    def edges(self):
        return (x.copy() for x in self._edges)
    
    def nodes(self):
        return (x.copy() for x in self._nodes)
