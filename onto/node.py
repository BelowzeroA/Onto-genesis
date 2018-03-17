

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
        incoming_connections = self.container.get_incoming_connections(self)
        for conn in incoming_connections:
            if conn.pulsing:
                conn.upgrade_weight()


    def update(self):
        if self.potential > self.threshold:
            self.firing = True
            self.potential -= 1

        if self.firing:
            connections = self.container.get_outgoing_connections(self)
            if connections:
                max_weight = max(connections, key=lambda c: c.weight).weight
                for connection in connections:
                    if connection.weight == max_weight:
                        connection.pulsing = True

        if self.potential > 2:
            self.container.brain.working_memory.write(self)


    def _repr(self):
        return '[id: {}, pattern: {}]'.format(self.node_id, self.pattern)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()