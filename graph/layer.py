import random


class Layer:

    def __init__(self, brain, index):
        self.brain = brain
        self.neurons = []
        self.index = index

    def get_density(self, ref_pattern):
        mass = 0.0
        counter = 0
        for neuron in self.neurons:
            if ref_pattern in neuron.incoming_patterns:
                likelihood = neuron.incoming_patterns[ref_pattern]
                if likelihood >= 0.9:
                    mass += likelihood
            # for pattern in neuron.incoming_patterns:
            #     likelihood = neuron.incoming_patterns[pattern]
            #     if likelihood >= 0.9: #self.brain.default_activation_likelihood:
            #         mass += likelihood
            #         counter += 1
        return mass / len(self.neurons)


    def reverberate(self):
        for neuron in self.neurons:
            neuron.learning_counter = 0
            for pattern in neuron.incoming_patterns:
                if neuron.incoming_patterns[pattern] <= self.brain.default_activation_likelihood:
                    neuron.incoming_patterns[pattern] = self.brain.default_activation_likelihood


    def get_max_density(self):
        return 0.5

