

class Node:

    def __init__(self, id, pattern):
        self.node_id = id
        self.pattern = pattern

    def _repr(self):
        return '[id: {}, pattern: {}]'.format(self.node_id, self.pattern)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()