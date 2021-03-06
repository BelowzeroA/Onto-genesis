import random


class Layer:

    def __init__(self, brain, index, min_pattern_length):
        self.brain = brain
        self.neurons = []
        self.index = index
        self.min_pattern_length = min_pattern_length

    def get_density(self, ref_pattern):
        mass = 0.0
        counter = 0
        for neuron in self.neurons:
            if ref_pattern in neuron.incoming_patterns:
                likelihood = neuron.incoming_patterns[ref_pattern]
                if likelihood >= 0.9:
                    mass += likelihood
        return mass / len(self.neurons)


    def reverberate(self):
        for neuron in self.neurons:
            neuron.learning_counter = 0
            for pattern in neuron.incoming_patterns:
                if neuron.incoming_patterns[pattern] <= self.brain.default_activation_likelihood:
                    neuron.incoming_patterns[pattern] = self.brain.default_activation_likelihood


    def get_max_density(self):
        return 0.5

    #
    # def stable_pattern_length(self):
    #     return len(self.neurons) * self.get_max_density()

