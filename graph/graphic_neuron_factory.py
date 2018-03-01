from graph.brain import Brain
from graph.graphic_neuron import GraphicNeuron
from graph.neuron import Neuron
from graph.neuron_factory import NeuronFactory


class GraphicNeuronFactory(NeuronFactory):

    def create_neuron(self, neuron_id, presentation, brain: Brain, layer) -> Neuron:
        return GraphicNeuron(neuron_id, presentation, brain, layer=layer, location=None)