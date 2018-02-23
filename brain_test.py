from graph.brain import Brain
from graph.graphic_brain import GraphicBrain
from graph.graphic_neuron_factory import GraphicNeuronFactory
from graph.graphics_test import user32, GraphWin


def main():

    factory = GraphicNeuronFactory()

    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    win = GraphWin('Draw a Triangle', screen_width * 0.8, screen_height * 0.8)

    brain = GraphicBrain(graph_win=win,
                         neuron_factory=factory,
                         max_connections_per_neuron=4,
                         average_connections_per_neuron=2.5,
                         default_weight=0.3,
                         default_threshold=0.4)
    brain.allocate_all(50)
    brain.draw()

    p = win.getMouse()
    brain.handle_click(p)

    win.getMouse()
    win.close()


if __name__ == '__main__':
    main()