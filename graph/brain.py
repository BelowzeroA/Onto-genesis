from abc import abstractmethod

from typing import List
import random

from graph.connection import Connection
from graph.layer import Layer
from graph.neuron import Neuron
from graph.neuron_factory import NeuronFactory
from graph.upgrade_rule import UpgradeRule

class Brain:

    def __init__(self,
                 neuron_factory: NeuronFactory,
                 max_connections_per_neuron=4,
                 average_connections_per_neuron=2.5,
                 default_weight=0.2,
                 default_threshold=0.5,
                 falloff_rate=0.1,
                 weight_upgrade=0.2,
                 weight_upper_limit=1.0,
                 upgrade_rule=UpgradeRule.SYNAPTIC,
                 default_activation_likelihood=0.1,
                 rand_seed=43):
        self.neurons: List[Neuron] = []
        self.connections: List[Connection] = []
        self.neuron_factory = neuron_factory
        self.max_connections_per_neuron = max_connections_per_neuron
        self.average_connections_per_neuron = average_connections_per_neuron
        self.default_weight = default_weight
        self.default_threshold = default_threshold
        self.falloff_rate = falloff_rate
        self.weight_upgrade = weight_upgrade
        self.rand_seed = rand_seed
        self.upgrade_rule = upgrade_rule
        self.weight_upper_limit = weight_upper_limit
        self.default_activation_likelihood = default_activation_likelihood
        self.layers = []
        random.seed(self.rand_seed)


    @abstractmethod
    def on_allocate(self):
        pass


    def allocate_all(self, neuron_number):
        for i in range(neuron_number):
            neuron = self.neuron_factory.create_neuron(i, i, self)
            self.neurons.append(neuron)
        self.build_connections()
        self.on_allocate()


    def create_layer(self, neuron_number):
        layer_number = len(self.layers)
        layer = Layer(self, layer_number)
        for i in range(neuron_number):
            neuron_id = 'l{}_{}'.format(layer_number, i)
            neuron = self.neuron_factory.create_neuron(neuron_id, i, self, layer)
            layer.neurons.append(neuron)
            self.neurons.append(neuron)
        self.layers.append(layer)
        return layer


    def connect_layers_all_to_all(self, source_layer, target_layer):
        for src_neuron in source_layer.neurons:
            for target_neuron in  target_layer.neurons:
                connection = self.create_connection(source=src_neuron, target=target_neuron)
                r = random.randint(0, 9)
                connection.inhibitory = r == 10
                self.connections.append(connection)


    def store_neuron_patterns(self):
        for neuron in self.neurons:
            neuron.store_patterns()


    def _get_random_neuron_index(self, except_idx):
        while True:
            idx = random.randint(0, len(self.neurons) - 1)
            if idx != except_idx:
                return idx


    def get_post_synaptic_neurons(self, neuron):
        return [conn.target for conn in self.connections if conn.source == neuron]


    def get_pred_synaptic_neurons(self, neuron):
        return [conn.source for conn in self.connections if conn.target == neuron]


    def get_connection(self, source, target):
        connections = [conn for conn in self.connections if conn.source == source and conn.target == target]
        if connections:
            return connections[0]
        else:
            return None


    def create_connection(self, source, target):
        return Connection(self, source=source, target=target)


    def build_connections(self):
        self.connections.clear()
        iter = 0
        while True:
            for i, neuron in enumerate(self.neurons):
                if neuron.incoming_connections_count() < self.max_connections_per_neuron:
                    target_idx = self._get_random_neuron_index(except_idx=i)
                    target = self.neurons[target_idx]
                    if self.get_connection(source=neuron, target=target)\
                        or self.get_connection(source=target, target=neuron):
                        continue
                    connection = self.create_connection(source=neuron, target=target)
                    r = random.randint(0, 9)
                    connection.inhibitory = r == 0
                    self.connections.append(connection)
                if len(self.connections) / len(self.neurons) > self.average_connections_per_neuron:
                    break
            if len(self.connections) / len(self.neurons) > self.average_connections_per_neuron:
                break
            iter += 1
            if iter > 1000:
                break
