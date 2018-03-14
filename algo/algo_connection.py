from algo.algo_node import AlgoNode


class AlgoConnection:

    def __init__(self, source: AlgoNode, target: AlgoNode):
        self.source = source
        self.target = target


    def update(self):
        pass