from graph.neuron import Neuron


class NeuronFactory:

    def create_neuron(self, neuron_id, brain) -> Neuron:
        return Neuron(neuron_id, brain)
