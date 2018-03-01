from graphics import Line, Point
from math import sqrt

from graph.connection import Connection
from graph.neuron import Neuron


class GraphicConnection(Connection):

    def __init__(self, brain, source, target: Neuron):
        super(GraphicConnection, self).__init__(brain, source, target)
        self.prev_pulsing = False


    def update(self):
        super(GraphicConnection, self).update()
        if self.prev_pulsing != self.pulsing:
            self.draw()
        self.prev_pulsing = self.pulsing


    def draw(self):
        return
        if self.pulsing:
            color = 'red'
        else:
            color = 'black'

        target = self.target
        source = self.source
        line = Line(source.location, target.location)
        line.setWidth(1)
        line.setFill(color)
        line.setOutline(color)
        line.draw(self.brain.win)

        dx = target.location.x - source.location.x
        dy = target.location.y - source.location.y
        k = dy / dx if dx != 0 else dy
        k = abs(k)
        dd = 20
        sign_dx = -1 if dx < 0 else 1
        sign_dy = -1 if dy < 0 else 1
        dx = -sign_dx * dd / sqrt(k ** 2 + 1)
        dy = -sign_dy * k * dd / sqrt(k ** 2 + 1)
        # sleep(1)

        dp = Point(target.location.x + dx, target.location.y + dy)
        line = Line(dp, target.location)
        line.setWidth(3)
        line.setFill(color)
        line.draw(self.brain.win)
