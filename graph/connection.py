from graph.neuron import Neuron


class Connection:

    def __init__(self, brain, source, target: Neuron):
        self.source = source
        self.target = target
        self.pulsing = False
        self.weight = brain.default_weight
        self.brain = brain


    def update(self):
        if self.pulsing:
            self.target.potential += self.weight
            # self.pulsing = False

    def __repr__(self):
        return '{} - {}'.format(self.source.inner_id, self.target.inner_id)

    def __str__(self):
        return '{} - {}'.format(self.source.inner_id, self.target.inner_id)