# from graph.brain import Brain


class Neuron:

    def __init__(self, inner_id, brain):
        self.brain = brain
        self.inner_id = inner_id
        self.firing = False
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
            self.firing = False
        else:
            for connection in outgoing_connections:
                connection.pulsing = False
            if self.potential >= self.threshold:
                self.firing = True
            if self.potential > self.brain.falloff_rate:
                self.potential -= self.brain.falloff_rate


    def __repr__(self):
        return str(self.inner_id) + ('firing' if self.firing else '')

    def __str__(self):
        return str(self.inner_id)
