import random

from graph.brain import Brain
from graph.graphic_brain import GraphicBrain
from graph.graphic_neuron_factory import GraphicNeuronFactory
from graph.graphics_test import user32, GraphWin


def main():

    factory = GraphicNeuronFactory()

    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    win = GraphWin('It\'s kinda brain', screen_width * 0.8, screen_height * 0.8)

    brain = GraphicBrain(graph_win=win,
                         neuron_factory=factory,
                         max_connections_per_neuron=6,
                         average_connections_per_neuron=3.0,
                         default_weight=0.2,
                         default_threshold=0.7,
                         weight_upgrade=0.3,
                         upgrade_rule='hebbian',
                         rand_seed=1)
    brain.allocate_all(100)
    brain.draw()

    pattern_n = 0
    repetitions_count = 4
    while True:
        indices = []
        while pattern_n < 10:
            pattern_n += 1
            indices.clear()
            for i in range(20):
                idx = random.randint(0, len(brain.neurons) - 1)
                indices.append(idx)

            for i in range(repetitions_count):
                brain.update_status_message('pattern {} repetition {}'.format(pattern_n, i))
                p1 = win.getMouse()
                brain.clear_initial_neurons()
                for idx in indices:
                    brain.append_neuron(brain.neurons[idx])
                brain.handle_neurons()


        # brain.clear_initial_neurons()
        # counter = 0
        # while True:
        #     p1 = win.getMouse()
        #     added = brain.append_neuron_by_coord(p1)
        #     if not added:
        #         break
        #     counter += 1
        # if counter == 0:
        #     break
        # brain.handle_neurons()

    # win.getMouse()
    win.close()


if __name__ == '__main__':
    main()