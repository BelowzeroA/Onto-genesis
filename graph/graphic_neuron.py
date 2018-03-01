from graphics import Point, Circle, color_rgb, Text

from graph.brain import Brain
from graph.graphic_brain import GraphicBrain
from graph.neuron import Neuron


class GraphicNeuron(Neuron):

    def __init__(self, inner_id, presentation, brain: GraphicBrain, location: Point, layer=None):
        super(GraphicNeuron, self).__init__(inner_id, presentation, brain, layer)
        self.location = location
        self.prev_firing = False
        self.was_fired = 0


    def update(self):
        super(GraphicNeuron, self).update()
        if self.firing:
            self.was_fired += 3
        if self.prev_firing != self.firing:
            self.draw(from_update=True)
        self.prev_firing = self.firing


    def reset(self):
        self.was_fired = 0
        self.firing = False
        self.potential = 0


    def draw(self, from_update=False):
        radius = 10
        circle1 = Circle(center=self.location, radius=radius)
        if self.firing:
            circle1.setFill('red')
        else:
            if self.was_fired > 0:
                circle1.setFill('yellow')
            else:
                circle1.setFill(color_rgb(240, 240, 240))
        # if self.prev_firing and from_update:
        #     circle1.setFill('yellow')
        circle1.draw(self.brain.win)

        message = Text(self.location, self.presentation)
        message.setTextColor('red')
        # message.setStyle('italic')
        message.setSize(10)
        message.draw(self.brain.win)
