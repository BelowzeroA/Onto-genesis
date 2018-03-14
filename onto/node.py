

class Node:

    def __init__(self, id, pattern, container):
        self.node_id = id
        self.pattern = pattern
        self.firing = False
        self.threshold = 1.1
        self.potential = 0
        self.container = container


    def fire(self):
        self.firing = True


    def update(self):
        if self.potential > self.threshold:
            self.firing = True
            self.potential -= 1

        if self.firing:
            connections = self.container.get_outgoing_connections(self)
            for connection in connections:
                connection.pulsing = True


    def _repr(self):
        return '[id: {}, pattern: {}]'.format(self.node_id, self.pattern)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()