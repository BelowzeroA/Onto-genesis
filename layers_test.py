from asyncio import sleep

from graph.graphic_brain import GraphicBrain
from graph.graphic_neuron_factory import GraphicNeuronFactory
from graph.graphics_test import user32, GraphWin
from graph.upgrade_rule import UpgradeRule

def refresh(win):
    win.autoflush = False
    for item in win.items[:]:
        item.undraw()
    win.update()
    win.autoflush = True


def train_pattern(brain, win, middle_layer, output_layer, pattern):

    middle_layer.reverberate()
    output_layer.reverberate()

    for i in range(30):
        brain.update_status_message('memorizing {} iteration {}'.format(pattern, i + 1))
        brain.clear_initial_neurons()
        brain.initially_firing.append(brain.neurons[pattern])
        brain.run(update_status=False)
        sleep(1)
        win.update()

    win.getMouse()
    refresh(win)


def main():

    factory = GraphicNeuronFactory()

    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    win = GraphWin('It\'s kinda layered brain', screen_width * 0.8, screen_height * 0.8)

    brain = GraphicBrain(graph_win=win,
                         neuron_factory=factory,
                         max_connections_per_neuron=6,
                         average_connections_per_neuron=3.0,
                         default_weight=1.0,
                         default_threshold=0.7,
                         weight_upgrade=0.3,
                         upgrade_rule=UpgradeRule.STOCHASTIC,
                         default_activation_likelihood=0.2,
                         rand_seed=16)
    middle_layer_size = 10
    output_layer_size = 8
    input_layer = brain.create_layer(10)
    middle_layer = brain.create_layer(middle_layer_size)
    output_layer = brain.create_layer(output_layer_size, min_pattern_length=output_layer_size / 2)

    brain.connect_layers_all_to_all(source_layer=input_layer, target_layer=middle_layer)
    brain.connect_layers_all_to_all(source_layer=middle_layer, target_layer=output_layer)

    brain.allocate_layers()
    brain.draw()

    train_pattern(brain, win, middle_layer, output_layer, 2)
    train_pattern(brain, win, middle_layer, output_layer, 6)
    train_pattern(brain, win, middle_layer, output_layer, 8)
    train_pattern(brain, win, middle_layer, output_layer, 0)

    for i in range(20):
        brain.update_status_message('recovering {} iteration {}'.format(8, i + 1))
        brain.clear_initial_neurons()
        brain.initially_firing.append(brain.neurons[8])
        brain.run(update_status=False)
        sleep(1)

    win.getMouse()
    win.close()


if __name__ == '__main__':
    main()