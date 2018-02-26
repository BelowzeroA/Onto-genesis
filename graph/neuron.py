from graph.brain import *


class Neuron:

    def __init__(self, inner_id, brain):
        self.brain = brain
        self.inner_id = inner_id
        self.firing = False
        self.was_firing = False
        self.potential = 0
        self.threshold = brain.default_threshold


    def incoming_connections_count(self):
        return sum([1 for connection in self.brain.connections if connection.target == self])


    def fire(self):
        self.firing = True


    def update(self):
        outgoing_connections = [c for c in self.brain.connections if c.source == self]
        if self.firing:
            for connection in outgoing_connections:
                connection.pulsing = True
            self.potential = 0
        else:
            for connection in outgoing_connections:
                connection.pulsing = False
            if self.potential >= self.threshold:
                self.firing = True
            if self.potential > self.brain.falloff_rate:
                self.potential -= self.brain.falloff_rate

        incoming_pulsing_connections = [c for c in self.brain.connections if c.target == self and c.pulsing]
        if self.brain.upgrade_rule == 'hebbian':
            if self.firing:
                incoming_connections = [c for c in self.brain.connections
                                        if c.target == self and (c.source.firing or c.source.was_firing)]
                for connection in incoming_connections:
                    connection.weight += self.brain.weight_upgrade
                    if connection.weight > self.brain.weight_upper_limit:
                        connection.weight = self.brain.weight_upper_limit
        else:
            if len(incoming_pulsing_connections) >= 2:
                for connection in incoming_pulsing_connections:
                    connection.weight += self.brain.weight_upgrade
                    if connection.weight > self.brain.weight_upper_limit:
                        connection.weight = self.brain.weight_upper_limit


    def _repr(self):
        return '[id: {}, potential: {}, firing: {}]'.format(self.inner_id, self.potential, self.firing)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()
