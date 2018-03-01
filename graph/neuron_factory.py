from graph.neuron import Neuron, random


class NeuronFactory:

    def create_neuron(self, neuron_id, brain, layer=None) -> Neuron:
        return Neuron(neuron_id, brain, layer)
