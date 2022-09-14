class Dagoba:
    def __init__(self, nodes = None, edges = None):
        self._nodes = []
        self._edges = []
        self._nodes_by_id = {}
        self._next_id = 1
        for node in (nodes or []):
            self.add_node(node)
        for edge in (edges or []):
            self.add_edge(edge)         

    def add_node(self, node):
        node = node.copy()
        pk = node.get('_id', None)
        if pk in self._nodes_by_id:
            raise ValueError(f'node with _id = {pk} already exists.')
        if not pk:
            pk = self._next_id
            self._next_id += 1
            node['_id'] = pk
        self._nodes.append(node)
        self._nodes_by_id[pk] = node
        return pk
    
    def add_edge(self, edge):
        in_id = edge.get('_from', None)
        out_id = edge.get("_to", None)
        if (in_id not in self._nodes_by_id or out_id not in self._nodes_by_id):
            raise ValueError(f'Invalid edge: edge({in_id}, {out_id}) not exists.')
        self._edges.append(edge.copy())
    
    def edges(self):
        return (x.copy() for x in self._edges)
    
    def nodes(self):
        return (x.copy() for x in self._nodes)
    
    def node(self, pk : int):
        return self._nodes_by_id[pk]

    # "get primary_key from node"
    # def pk(self, node):
    #     return node['_id']
    
#     # def is_edge(edge, side, pk : int, type_ = None):
#     #     if edge[side] != pk or edge['_type'] != type_:
#     #         return False
#     #     return True

    @classmethod
    def pk(cls, node):
        """Get primary key of node"""
        return node['_id']
        
    @classmethod
    def is_edge(cls, edge, side, pk: int, type_=None):
        if edge[side] != pk:
            return False
        if type_ and edge.get('_type') != type_:
            return False
        return True

    def to_node(self, edge):
        return self.node(edge['_to']) 
    
    def from_node(self, edge):
        return self.node(edge['_from'])

    def outcome(self, pk : int, type_ = None):
        result = []
        for edge in self.edges():
            if Dagoba.is_edge(edge, '_from', pk, type_):
                result.append(self.node(edge.get('_to')))
        return result
    
    def income(self, pk : int, type_ = None):
        result = []
        for x in self.edges():
            if Dagoba.is_edge(x, '_to', pk, type_):
                result.append(self.node(x['_from']))
        return result
    
    def query(self, eager = True):
        return EagerQuery(self) if eager else LazyQuery(self)

class EagerQuery:
    def __init__(self, db):
        self._db = db
        self._result = None
    
    def node(self, pk : int):
        try:
            self._result = [self._db.node(pk)]
        except KeyError:
            self._result = []
        return self
    
    def run(self):
        return self._result

    def outcome(self, type_ = None):
        result = []
        for node in self._result:
            pk = node['_id']
            # pk = Dagoba.pk(node)
            result.extend(self._db.outcome(pk, type_))
        self._result = result
        return self

    def income(self, type_ = None):
        result = []
        for node in self._result:
            pk = self._db.pk(node)
            result.extend(self._db.income(pk, type_))
        self._result = result
        return self

    def unique(self):
        d = {}
        for node in self._result:
            pk = Dagoba.pk(node)
            d.setdefault(pk, node)
        self._result = list(d.values())
        return self


class LazyQuery:
    def __init__(self, db):
        self._db = db


