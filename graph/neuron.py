import math

from graph.brain import *
from graph.upgrade_rule import UpgradeRule


class Neuron:

    def __init__(self, inner_id, presentation, brain, layer=None):
        self.brain = brain
        self.inner_id = inner_id
        self.firing = False
        self.was_firing = False
        self.potential = 0
        self.presentation = presentation
        self.threshold = brain.default_threshold
        self.layer = layer
        self.learning_counter = 0
        self.incoming_actions = []
        self.incoming_patterns = {}


    def incoming_connections_count(self):
        return sum([1 for connection in self.brain.connections if connection.target == self])


    def fire(self):
        self.firing = True
        outgoing_connections = [c for c in self.brain.connections if c.source == self]
        for connection in outgoing_connections:
            connection.pulsing = True


    def update(self):
        if self.brain.upgrade_rule == UpgradeRule.STOCHASTIC:
            self.update_stochastic()
        else:
            self.update_deterministic()
        self.incoming_actions.clear()


    def update_deterministic(self):
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
        if self.brain.upgrade_rule == UpgradeRule.HEBBIAN:
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


    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def update_stochastic(self):

        if not self.firing:
            outgoing_connections = [c for c in self.brain.connections if c.source == self]
            for connection in outgoing_connections:
                connection.pulsing = False

        if not self.incoming_actions:
            return

        self.learning_counter += 1

        gradient = 0.1
        incoming_action_pattern = '-'.join(self.incoming_actions)
        if incoming_action_pattern in self.incoming_patterns:
            likelihood = self.incoming_patterns[incoming_action_pattern]
        else:
            likelihood = self.brain.default_activation_likelihood
            self.incoming_patterns[incoming_action_pattern] = likelihood

        rnd_val = random.randint(1, 100)
        fire = rnd_val <= likelihood * 100
        density = self.layer.get_density(incoming_action_pattern)
        if density < self.layer.get_max_density():
            penalty = -gradient * 0.5
            stimulation = gradient * 4
        else:
            penalty = -gradient * 4
            stimulation = gradient * 0.5
        if fire:
            self._update_incoming_pattern(incoming_action_pattern, stimulation)
            self.fire()
        else:
            self._update_incoming_pattern(incoming_action_pattern, penalty)

        for pattern in self.incoming_patterns:
            if pattern != incoming_action_pattern:
                self._update_incoming_pattern(pattern, penalty)


    def _update_incoming_pattern(self, pattern, gradient):
        if self.incoming_patterns[pattern] > 0.9:
            self.incoming_patterns[pattern] += gradient * 0.1
        if self.incoming_patterns[pattern] > 0.8:
            self.incoming_patterns[pattern] += gradient * 0.2
        else:
            self.incoming_patterns[pattern] += gradient

        if self.incoming_patterns[pattern] < self.brain.default_activation_likelihood:
            if self.learning_counter > 30:
                self.incoming_patterns[pattern] = 0
            else:
                self.incoming_patterns[pattern] = self.brain.default_activation_likelihood
        if self.incoming_patterns[pattern] > 1.0:
            self.incoming_patterns[pattern] = 1.0


    def _repr(self):
        return '[id: {}, potential: {}, firing: {}]'.format(self.inner_id, self.potential, self.firing)

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._repr()
