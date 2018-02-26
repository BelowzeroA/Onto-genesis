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
                         max_connections_per_neuron=3,
                         average_connections_per_neuron=3.5,
                         default_weight=0.2,
                         default_threshold=0.7,
                         weight_upgrade=0.3,
                         rand_seed=1)
    brain.allocate_all(20)
    brain.draw()

    while True:
        brain.clear_initial_neurons()
        counter = 0
        while True:
            p1 = win.getMouse()
            added = brain.append_neuron(p1)
            if not added:
                break
            counter += 1
        if counter == 0:
            break
        # p2 = win.getMouse()
        # brain.handle_click(p)
        brain.handle_neurons()

    # win.getMouse()
    win.close()


if __name__ == '__main__':
    main()