def copy_dict(src: dict, *excludes) -> dict:
    return {k: v for k, v in src.items() if k not in excludes}
    
class Dagoba:
    def __init__(self, nodes = None, edges = None):
        self._nodes = []
        self._edges = []
        self._nodes_by_id = {}
        self._next_id = 1
        self._node_visits = 0
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
        node['_out'] = []
        node['_in'] = []
        self._nodes.append(node)
        self._nodes_by_id[pk] = node
        return pk
    
    def add_edge(self, edge):
        in_id = edge.get('_from', None)
        out_id = edge.get("_to", None)
        # if (in_id not in self._nodes_by_id or out_id not in self._nodes_by_id):
        #     raise ValueError(f'Invalid edge: edge({in_id}, {out_id}) not exists.')
        try:
            from_node = self.node(in_id)
            to_node = self.node(out_id)
            forward = copy_dict(edge, '_backward')
            self._edges.append(forward)
            from_node['_out'].append(forward)
            to_node['_in'].append(forward)
            if '_backward' in edge.keys():
                backward = copy_dict(edge, '_backward')
                backward['_type'] = edge['_backward']
                backward['_from'] = edge['_to']
                backward['_to'] = edge['_from']
                self._edges.append(backward)
                to_node['_out'].append(backward)
                from_node['_in'].append(backward)
        except KeyError:
            raise ValueError(f'Invalid edge: edge({in_id}, {out_id}) not exists.')
        # self._edges.append(edge.copy())

    # def copy_dict(src : dict, *excludes) -> dict:
    #     return {k : v for k, v in src.items() if k not in excludes}
            
    def edges(self):
        return (x.copy() for x in self._edges)
    
    def nodes(self):
        return (x.copy() for x in self._nodes)
    
    def node(self, pk : int, visit = False):
        if visit:
            self._node_visits += 1
        return self._nodes_by_id[pk]

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
        return self.node(edge['_to'], visit = True) 
    
    def from_node(self, edge):
        return self.node(edge['_from'], visit = True)

    def outcome(self, pk : int, type_ = None):
        node = self.node(pk, visit=True)
        return (self.to_node(x) for x in node['_out']
                if Dagoba.is_edge(x, '_from', pk, type_))

    
    def income(self, pk : int, type_ = None):
        node = self.node(pk, visit = True)
        return (self.from_node(x) for x in node['_in']
                if Dagoba.is_edge(x, '_to', pk, type_))
    
    def query(self, eager = True):
        return EagerQuery(self) if eager else LazyQuery(self)

    def reset_visits(self):
        self._node_visits = 0

    def get_visits(self) -> int:
        return self._node_visits
        
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
        
    def take(self, count: int):
        self._result = self._result[:count]
        return self


class LazyQuery:
    def __init__(self, db):
        self._db = db
        self._pipeline = []
    
    def node(self, pk: int):
        def func(arg):
            try:
                return [self._db.node(pk)]
            except KeyError:
                return []
        self._pipeline.append(func)
        return self

    def outcome(self, type_=None):
        def func(arg):
            for node in arg:
                pk = node['_id']
                for target_node in self._db.outcome(pk, type_):
                    yield target_node
        self._pipeline.append(func)
        return self

    def income(self, type_=None):
        def func(arg):
            for node in arg:
                pk = node['_id']
                for target_node in self._db.income(pk, type_):
                    yield target_node
        self._pipeline.append(func)
        return self

    def unique(self):
        def func(arg):
            dic = {Dagoba.pk(x): x for x in arg}
            for pk in dic.keys():
                yield dic[pk]
        self._pipeline.append(func)
        return self

    def run(self):
        input_, output_ = None, None
        for step in self._pipeline:
            output_ = step(input_)
            input_ = output_
        return list(output_)

    def take(self, count: int):
        def func(arg):
            result = []
            for i in range(count):
                result.append(arg[i])
            return result
        self._pipeline.append(func)
        return self

    def take(self, count: int):
        def func(arg):
            return [next(arg) for i in range(count)]
        self._pipeline.append(func)
        return self