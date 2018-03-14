from algo.algo_node_types import AlgoNodeType


class AlgoNode:

    def __init__(self, id: str, brain):
        self.node_id = id
        # self.type = type
        self.brain = brain


    def update(self):
        pass