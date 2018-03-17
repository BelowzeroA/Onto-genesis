from algo.algo_node import AlgoNode


class AlgoConnection:

    def __init__(self, source: AlgoNode, target: AlgoNode):
        self.source = source
        self.target = target
        self.pulsing = False
        self.weight = 1


    def update(self):
        if self.pulsing:
            self.target.potential += self.weight
            self.pulsing = False