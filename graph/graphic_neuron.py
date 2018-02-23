from graphics import Point, Circle, color_rgb, Text

from graph.brain import Brain
from graph.graphic_brain import GraphicBrain
from graph.neuron import Neuron


class GraphicNeuron(Neuron):

    def __init__(self, inner_id, brain: GraphicBrain, location: Point):
        super(GraphicNeuron, self).__init__(inner_id, brain)
        self.location = location
        self.prev_firing = False

    def update(self):
        super(GraphicNeuron, self).update()
        if self.prev_firing != self.firing:
            self.draw()
        self.prev_firing = self.firing

    def draw(self):
        circle1 = Circle(center=self.location, radius=10)
        if self.firing:
            circle1.setFill('red')
        else:
            circle1.setFill(color_rgb(220, 220, 220))
        circle1.draw(self.brain.win)

        message = Text(self.location, self.inner_id)
        message.setTextColor('red')
        # message.setStyle('italic')
        message.setSize(10)
        message.draw(self.brain.win)
