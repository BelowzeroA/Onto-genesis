import random

import sys
from time import sleep

from graphics import GraphWin, Point, Circle, Line, Text, color_rgb
from math import sqrt

from graph.brain import Brain
from graph.calc import get_distance_between_coords
from graph.graphic_connection import GraphicConnection
from graph.neuron_factory import NeuronFactory

sys.setrecursionlimit(1500)

class GraphicBrain(Brain):

    def __init__(self,
                 graph_win: GraphWin,
                 neuron_factory: NeuronFactory,
                 max_connections_per_neuron=4,
                 average_connections_per_neuron=2.5,
                 default_weight=0.2,
                 default_threshold=0.5,
                 falloff_rate=0.1):
        super(GraphicBrain, self).__init__(
            neuron_factory=neuron_factory,
            max_connections_per_neuron=max_connections_per_neuron,
            average_connections_per_neuron=average_connections_per_neuron,
            default_weight=default_weight,
            default_threshold=default_threshold,
            falloff_rate=falloff_rate
        )
        self.win = graph_win
        self.min_margin = 40
        self.min_distance_between_neurons = 50
        self.max_distance_between_neurons = 200


    def on_allocate(self):
        neuron0 = self.neurons[0]
        neuron0.location = Point(self.win.width / 2, self.win.height / 2)
        neurons_to_allocate = list(self.neurons)
        neurons_to_allocate.remove(neuron0)
        alloction_queue = []
        alloction_queue.append(neuron0)
        self.allocate_adjacent_neurons(neuron0, alloction_queue)


    def allocate_adjacent_neurons(self, source_neuron, alloction_queue):
        # if not neurons_to_allocate:
        #     return
        post_synaptic_neurons = self.get_post_synaptic_neurons(source_neuron)
        post_synaptic_neurons = [n for n in post_synaptic_neurons if n not in alloction_queue]
        for neuron in post_synaptic_neurons:
            if neuron.location:
                continue
            neuron.location = self._find_location_for_neuron_near(source_neuron)
            alloction_queue.append(neuron)

        pred_synaptic_neurons = self.get_pred_synaptic_neurons(source_neuron)
        pred_synaptic_neurons = [n for n in pred_synaptic_neurons if n not in alloction_queue]
        for neuron in pred_synaptic_neurons:
            if neuron.location:
                continue
            neuron.location = self._find_location_for_neuron_near(source_neuron)
            alloction_queue.append(neuron)

        for neuron in post_synaptic_neurons:
            self.allocate_adjacent_neurons(neuron, alloction_queue)

        for neuron in pred_synaptic_neurons:
            self.allocate_adjacent_neurons(neuron, alloction_queue)


    def _find_location_for_neuron(self):
        iter = 0
        while True:
            iter += 1
            x = random.randint(self.min_margin, self.win.width - self.min_margin)
            y = random.randint(self.min_margin, self.win.height - self.min_margin)
            _, dist = self._get_nearest_neuron_distance(x, y)
            if not dist or dist > self.min_distance_between_neurons:
                return Point(x, y)
            if iter > 1000:
                raise BaseException('Unable to allocate neuron')


    def _find_location_for_neuron_near(self, neuron):
        iter = 0
        while True:
            iter += 1
            x = random.randint(self.min_margin, self.win.width - self.min_margin)
            y = random.randint(self.min_margin, self.win.height - self.min_margin)
            dist_to_source = get_distance_between_coords(x, y, neuron.location.x, neuron.location.y)
            if dist_to_source < self.min_distance_between_neurons or dist_to_source > self.max_distance_between_neurons:
                continue
            _, dist = self._get_nearest_neuron_distance(x, y)
            if not dist or self.min_distance_between_neurons <= dist:
                return Point(x, y)
            if iter > 10000:
                raise BaseException('Unable to allocate neuron')


    def _get_nearest_neuron_distance(self, x, y):
        min_distance = 1000000.0
        found = False
        closest_neuron = None
        for neuron in self.neurons:
            if neuron.location:
                found = True
                dist = get_distance_between_coords(x, y, neuron.location.x, neuron.location.y)
                if dist < min_distance:
                    min_distance = dist
                    closest_neuron = neuron
        if found:
            return closest_neuron, min_distance
        else:
            return closest_neuron, None


    def create_connection(self, source, target):
        return GraphicConnection(self, source=source, target=target)


    def draw(self):
        for conn in self.connections:
            # sleep(1)
            conn.draw()

        for neuron in self.neurons:
            neuron.draw()


    def handle_click(self, p: Point):
        neuron, distance = self._get_nearest_neuron_distance(p.x, p.y)
        if distance > 10:
            return
        neuron.fire()
        self.run()


    def run(self):
        tick = 0
        while tick < 10:
            tick += 1
            sleep(1)
            for neuron in self.neurons:
                neuron.update()

            for conn in self.connections:
                conn.update()
