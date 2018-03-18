from onto.node import Node


class Connection:

    def __init__(self, source: Node, target: Node, container):
        self.source = source
        self.target = target
        self.weight = 1
        self.container = container
        self.pulsing = False
        self.potential = 0


    def update(self):
        if self.pulsing:
            self.target.potential += self.weight * self.potential
        self.pulsing = False
        self.potential = 0