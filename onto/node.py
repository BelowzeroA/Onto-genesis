
class Node:

    initial_potential_period = 2

    def __init__(self, id, pattern, container, abstract=False):
        self.node_id = id
        self.pattern = pattern
        self.firing = False
        self.initial = False
        self.threshold = 2
        self.potential = 0
        self.abstract = abstract
        self.container = container
        self.last_firing_tick = 0


    def fire(self):
        self.last_firing_tick = self.container.brain.current_tick
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
            self.last_firing_tick = self.container.brain.current_tick

        ticks_since_last_firing = self.container.brain.current_tick - self.last_firing_tick
        keep_firing = self.initial and ticks_since_last_firing <= Node.initial_potential_period

        # leak
        if self.potential > 0 and not self.firing and not keep_firing:
            self.potential -= 1
            if self.potential < 0:
                self.potential = 0

        potential_spent = False
        if self.firing:
            current_tick = self.container.brain.current_tick
            connections = self.container.get_outgoing_connections(self)
            if connections:
                max_weight = max(connections, key=lambda c: c.weight).weight
                for connection in connections:
                    if connection.weight == max_weight:
                        counter_connection = self.container.get_connection_between_nodes(
                            source=connection.target, target=connection.source)
                        if counter_connection and counter_connection.last_pulsing_tick > current_tick - 10:
                            continue
                        connection.pulsing = True
                        connection.potential = self.potential
                        potential_spent = True

        if self.potential > 2 and self.firing and not self.initial:
            self.container.brain.working_memory.write(self)
            self.potential = 0

        if potential_spent and not keep_firing:
            self.potential = 0
            self.firing = False


    def _repr(self):
        return '[id:{} "{}"]'.format(self.node_id, self.pattern)

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
