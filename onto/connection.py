from onto.node import Node


class Connection:

    def __init__(self, source: Node, target: Node, container):
        self.source = source
        self.target = target
        self.weight = 1
        self.sign = 1
        self.container = container
        self.pulsing = False
        self.potential = 0
        self.last_pulsing_tick = -999
        self.secondary = False


    def update(self):
        if self.pulsing:
            self.last_pulsing_tick = self.container.brain.current_tick
            weight_coefficient = 0.5 if self.secondary else 1
            potentiation = self.weight * weight_coefficient
            self.target.potential += potentiation # self.potential
            self.target.contributors.append('{}: {}'.format(self.source.node_id, potentiation))
        self.pulsing = False
        self.potential = 0


    def _repr(self):
        return '[{}-{}]'.format(self.source.node_id, self.target.node_id)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()


    def serialize(self):
        _dict = {
            'source': self.source.node_id,
            'target': self.target.node_id
        }
        return _dict
