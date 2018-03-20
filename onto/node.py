import jsonpickle


class Node:

    def __init__(self, id, pattern, container, abstract=False):
        self.node_id = id
        self.pattern = pattern
        self.firing = False
        self.initial = False
        self.threshold = 2
        self.potential = 0
        self.abstract = abstract
        self.container = container


    def fire(self):
        self.firing = True
        if self.potential == 0:
            self.potential = 1
        incoming_connections = self.container.get_incoming_connections(self)
        for conn in incoming_connections:
            if conn.pulsing:
                conn.upgrade_weight()


    def update(self):
        if self.potential > self.threshold:
            self.firing = True
            # self.potential = 0

        # leak
        if self.potential > 0 and not self.firing and not self.initial:
            self.potential -= 1

        potential_spent = False
        if self.firing:
            connections = self.container.get_outgoing_connections(self)
            if connections:
                max_weight = max(connections, key=lambda c: c.weight).weight
                for connection in connections:
                    if connection.weight == max_weight:
                        connection.pulsing = True
                        connection.potential = self.potential
                        potential_spent = True

        if self.potential > 2 and self.firing and not self.initial:
            self.container.brain.working_memory.write(self)
            self.potential = 0

        if potential_spent and not self.initial:
            self.potential = 0


    def _repr(self):
        return '[id: {} "{}"]'.format(self.node_id, self.pattern)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()


    def serialize(self):
        _dict = {
            'id': self.node_id,
            'patterns': [ self.pattern ],
            'abstract': self.abstract
        }
        return _dict
