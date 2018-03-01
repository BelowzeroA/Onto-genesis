from graph.neuron import Neuron


class Connection:

    def __init__(self, brain, source, target: Neuron):
        self.source = source
        self.target = target
        self.pulsing = False
        self.weight = brain.default_weight
        self.brain = brain
        self.inhibitory = False


    def update(self):
        if self.pulsing:
            sign = -1 if self.inhibitory else 1
            self.target.potential += sign * self.weight
            if self.target.potential < 0:
                self.target.potential = 0
            self.target.incoming_actions.append(self.source.inner_id)

            # self.pulsing = False

    def _repr(self):
        return '[{}-{} weight: {}]'.format(self.source.inner_id, self.target.inner_id, self.weight)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()