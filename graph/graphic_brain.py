import random

import sys
from time import sleep

from graphics import GraphWin, Point, Circle, Line, Text, color_rgb, Rectangle
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
                 weight_upgrade=0.2,
                 falloff_rate=0.1,
                 weight_upper_limit=1.0,
                 upgrade_rule='synaptic',
                 rand_seed=42):
        super(GraphicBrain, self).__init__(
            neuron_factory=neuron_factory,
            max_connections_per_neuron=max_connections_per_neuron,
            average_connections_per_neuron=average_connections_per_neuron,
            default_weight=default_weight,
            default_threshold=default_threshold,
            weight_upgrade=weight_upgrade,
            falloff_rate=falloff_rate,
            rand_seed=rand_seed,
            weight_upper_limit=weight_upper_limit,
            upgrade_rule=upgrade_rule
        )
        self.win = graph_win
        self.min_margin = 40
        self.min_distance_between_neurons = 50
        self.max_distance_between_neurons = 200
        self.initially_firing = []

    def on_allocate(self):
        neuron0 = self.neurons[0]
        neuron0.location = Point(self.win.width / 2, self.win.height / 2)
        allocation_queue = [neuron0]
        self.allocate_adjacent_neurons(neuron0, allocation_queue)

    def allocate_adjacent_neurons(self, source_neuron, allocation_queue):
        post_synaptic_neurons = self.get_post_synaptic_neurons(source_neuron)
        post_synaptic_neurons = [n for n in post_synaptic_neurons if n not in allocation_queue]
        for neuron in post_synaptic_neurons:
            if neuron.location:
                continue
            neuron.location = self._find_location_for_neuron_near(source_neuron)
            allocation_queue.append(neuron)

        pred_synaptic_neurons = self.get_pred_synaptic_neurons(source_neuron)
        pred_synaptic_neurons = [n for n in pred_synaptic_neurons if n not in allocation_queue]
        for neuron in pred_synaptic_neurons:
            if neuron.location:
                continue
            neuron.location = self._find_location_for_neuron_near(source_neuron)
            allocation_queue.append(neuron)

        for neuron in post_synaptic_neurons:
            self.allocate_adjacent_neurons(neuron, allocation_queue)

        for neuron in pred_synaptic_neurons:
            self.allocate_adjacent_neurons(neuron, allocation_queue)

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

    def handle_double_click(self, p1, p2: Point):
        neuron1, distance = self._get_nearest_neuron_distance(p1.x, p1.y)
        neuron2, distance = self._get_nearest_neuron_distance(p2.x, p2.y)
        neuron1.fire()
        neuron2.fire()
        self.initially_firing = [neuron1, neuron2]
        self.run()

    def handle_neurons(self):
        self.run()

    def append_neuron_by_coord(self, p: Point):
        neuron, distance = self._get_nearest_neuron_distance(p.x, p.y)
        if distance <= 10:
            neuron.fire()
            neuron.draw()
            self.initially_firing.append(neuron)
            return True
        return False


    def append_neuron(self, neuron):
        self.initially_firing.append(neuron)


    def clear_initial_neurons(self):
        self.initially_firing.clear()

    def update_status_message(self, text):
        center_x = self.win.getWidth() / 2
        center_y = 20
        back_color = color_rgb(240, 240, 240)
        msg_width = 300
        msg_height = 20
        rect = Rectangle(
            Point(center_x - msg_width, center_y - msg_height),
            Point(center_x + msg_width, center_y + msg_height))
        rect.setFill(back_color)
        rect.setOutline(back_color)
        rect.setWidth(1)  # width of boundary line
        rect.draw(self.win)

        message = Text(Point(center_x, center_y), text)
        message.setTextColor('red')
        message.setStyle('bold')
        message.setSize(20)
        message.draw(self.win)

    def run(self):
        tick = 0
        self.update_status_message('running..')

        for neuron in self.neurons:
            neuron.reset()
            neuron.draw()

        max_ticks = 10
        while tick <= max_ticks:
            tick += 1
            sleep(1)

            one_fired = False
            for neuron in self.neurons:
                if tick <= 2 and neuron in self.initially_firing:
                    neuron.fire()
                neuron.update()
                if neuron.firing and not neuron in self.initially_firing:
                    one_fired = True

            for conn in self.connections:
                conn.update()

            for neuron in self.neurons:
                if neuron.was_fired > 0:
                    neuron.was_fired -= 1
                if neuron.was_firing:
                    neuron.was_firing = False
                if neuron.firing:
                    neuron.firing = False
                    neuron.was_firing = True

            for neuron in self.neurons:
                neuron.draw()

            if not one_fired:
                if tick >= max_ticks:
                    break
                tick = max_ticks

        for neuron in self.initially_firing:
            neuron.firing = False
            neuron.was_fired = 0
            neuron.draw()

        self.update_status_message('idle')
