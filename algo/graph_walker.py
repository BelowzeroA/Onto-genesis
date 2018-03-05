from algo.cb_take_1_common import cbTake1Common
from algo.cb_take_2_common import cbTake2Common


class GraphWalker:

    def __init__(self, container):
        self.container = container


    def resolve(self, input):
        input_nodes = [node for node in self.container.nodes if node.pattern in input]
        alg = cbTake1Common(self.container)
        result = alg.run(input_nodes)
        return result